#include "mainwindow.h"
#include "ui_mainwindow.h"


#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <iostream>
#include <regex>

std::vector<std::string> giveInputDevices(){
    // executes waveenum.exe and saves result in a string
    std::string resultString;
    FILE *fp = _popen("cd .. && waveenum.exe" , "r");
    if(fp == nullptr){
        perror("unable to open file");
        exit(1);
    }

    char chunk[128];

    while(fgets(chunk, sizeof(chunk), fp) != nullptr){
        resultString.append(chunk);
    }

    // deletes output devices from string
    resultString = regex_replace(resultString, std::regex("waveOut[\\S\\s]*"), "");

    // input devices with additional information if needed
    // std::cout << resultString << std::endl;

    // results as vector
    std::vector<std::string> resultVector;

    // filters out all device names
    std::regex e("Product Name: (.*)");
    std::sregex_iterator iter(resultString.begin(), resultString.end(), e);
    std::sregex_iterator end;
    std::cout << "Devices found: " << iter->size() << std::endl;
    int deviceCounter = 1;
    // lists devices
    while(iter != end){
        resultVector.emplace_back(std::string((*iter)[1]));
//        std::cout << "Device " << deviceCounter << ": " << (*iter)[1] << std::endl;
        ++iter;
        ++deviceCounter;
    }
    return resultVector;
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    std::vector<std::string> inputDevices = giveInputDevices();

    for(std::size_t i = 0; i < inputDevices.size(); ++i) {
        ui->comboBox->addItem(QString::fromUtf8(inputDevices[i].c_str()));
    }



}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_clicked()
{
//    giveInputDevices();
}



void MainWindow::on_comboBox_activated(int index)
{
    std::cout << index << std::endl;
}

