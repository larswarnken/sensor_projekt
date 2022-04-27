#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "RtAudio.h"

#include <string>
#include <QProcess>
#include <QFile>
#include <QJsonDocument>
#include <QJsonParseError>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonArray>
#include <QDir>

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <unistd.h>
#include <fstream>
#include <filesystem>
#include <QFileDialog>
#include <QMessageBox>
#include <QFile>
#include <QTextStream>
#include <regex>

std::vector<std::vector<std::string>> inputDevices;

QString saveLocation = "Aufnahmen/data.txt";

// output file
std::ofstream outputFile;

// rt audio
RtAudio audio;
RtAudio adc;


// saves save location in json file
int updateJsonFile(int time) {
    QJsonObject root;
    root["outputPath"] = saveLocation;
    QByteArray ba = QJsonDocument(root).toJson();
        {
            QFile fout("test.json");
            fout.open(QIODevice::WriteOnly);
            fout.write(ba);
        }
    return 0;
}


// creates new output file so it doesn't overwrite existing files
void createNewFile() {
    //checks output folder
    if(std::filesystem::exists("Aufnahmen//data.txt") != 0){
        std::string path = "Aufnahmen/";
        std::regex rgx("Aufnahmen\\\\data_(\\d+).txt");
        int highestFileName = 0;
        // iterates through output folder and finds highest number
        for(const auto & entry : std::filesystem::directory_iterator(path)){
            std::string input = std::filesystem::relative(entry.path()).string();
            // checks for files with format "Aufnahmen/data_x.txt"
            if(std::regex_match(input, rgx) > 0) {
                // extracts number
                int output = std::stoi(std::regex_replace(input, rgx, std::string("$1")));
                if(output > highestFileName){
                    highestFileName = output;
                }
            }
        }
        // if there's only one file
        if(highestFileName == 0) {
            std::cout << "Aufnahmen/data_2.txt" << std::endl;
            saveLocation = "Aufnahmen/data_2.txt";
        } else {
            QString resultFileName = QString("Aufnahmen/data_%1.txt").arg(highestFileName+1);
            saveLocation = resultFileName;
        }
    }
    updateJsonFile(0);
}


// emptying output file
void empty_file() {
    outputFile.open(saveLocation.toStdString());
    outputFile << "";
    outputFile.close();
}




// returns input devices
std::vector<std::vector<std::string>> giveInputDevices() {
    std::vector<std::vector<std::string>> resultString;
    unsigned int devices = audio.getDeviceCount();

    RtAudio::DeviceInfo info;
    for (unsigned int i=0; i<devices; i++) {
        info = audio.getDeviceInfo(i);
        if (info.probed == true && info.inputChannels > 0) {
            std::vector<std::string> tempDevice;
            tempDevice.push_back(std::to_string(i));
            tempDevice.push_back(info.name);
            resultString.push_back(tempDevice);
        }
    }
    return resultString;
}


// record function, saves data in txt file
int record( void *outputBuffer, void *inputBuffer, unsigned int nBufferFrames,
         double streamTime, RtAudioStreamStatus status, void *userData ) {

    // accesses input buffer
    float *buffer = (float *)inputBuffer;

    // writes data to txt file
    outputFile.open (saveLocation.toStdString(), std::ios_base::app); // append mode
    static unsigned int i;
    for (i=0;i<nBufferFrames;i++) {
        // std::cout << buffer[i] << ", ";
        if(streamTime != 0){
            outputFile << buffer[i] << "\n";
        }
    }
    outputFile.close();
    return 0;
}

// main window function
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    createNewFile();

    // add input devices to dropdown
    inputDevices = giveInputDevices();
    for(std::size_t i = 0; i < inputDevices.size(); ++i) {
            ui->ComboBoxDevices->addItem(QString::fromUtf8(inputDevices[i][1].c_str()));
    }
    // default device is last in list (most likely plugged in)
    ui->ComboBoxDevices->setCurrentIndex(inputDevices.size());

    ui->labelSaveLocation->setText(saveLocation);
}


MainWindow::~MainWindow()
{
    delete ui;
}


// BUTTON: start the recording
void MainWindow::on_pushButtonStartRecord_clicked()
{
    int recordDeviceSetting = 0;
    int inputChannelsSetting;
    int firstChannelSetting;
    int sampleRateSetting;
    int bufferFramesSetting;
    int recordTimeSetting;

    // record device
    QString deviceName = ui->ComboBoxDevices->itemText(ui->ComboBoxDevices->currentIndex());
    for (unsigned int i=0; i<inputDevices.size(); i++) {
        if (QString::compare(QString::fromStdString(inputDevices[i][1]), deviceName, Qt::CaseSensitive) == 0) {
            recordDeviceSetting = std::stoi(inputDevices[i][0]);
        }
    }
    inputChannelsSetting = ui->comboBoxIputChannels->itemText(ui->comboBoxIputChannels->currentIndex()).toInt();
    firstChannelSetting = ui->comboBoxFirstChannel->itemText(ui->comboBoxFirstChannel->currentIndex()).toInt();
    sampleRateSetting = ui->lineEditFrameRate->displayText().toInt();
    bufferFramesSetting = ui->lineEditBufferFrames->displayText().toInt();
    recordTimeSetting = ui->lineEditRecordTime->displayText().toInt();

    // set input parameters
    RtAudio::StreamParameters parameters;
    parameters.deviceId = recordDeviceSetting;
    parameters.nChannels = inputChannelsSetting;
    parameters.firstChannel = firstChannelSetting;
    unsigned int sampleRate = sampleRateSetting;
    unsigned int bufferFrames = bufferFramesSetting;

    empty_file();


    // saves samplerate and recording time as first line
    outputFile.open (saveLocation.toStdString(), std::ios_base::app); // append mode
    outputFile << sampleRateSetting << ", " << recordTimeSetting << "\n";
    outputFile.close();



    // open and start input stream
    adc.openStream( NULL, &parameters, RTAUDIO_FLOAT32,
         sampleRate, &bufferFrames, &record );
    adc.startStream();

    hide();

    Sleep(recordTimeSetting);

    // stops the input stream
    adc.stopStream();
    if ( adc.isStreamOpen() ) adc.closeStream();

    updateJsonFile(recordTimeSetting);

    close();
}


// BUTTON: change saving directory
void MainWindow::on_ButtonSaveFile_clicked()
{
    QString newSaveLocation = QFileDialog::getSaveFileName(this, tr("save file"), "", tr("All Files (*)"));
    if(newSaveLocation != ""){
        saveLocation = newSaveLocation;
        ui->labelSaveLocation->setText(saveLocation);
        updateJsonFile(0);
    }
}

