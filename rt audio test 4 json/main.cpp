#include "include/RtAudio.h"
#include "include/json.hpp"
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <unistd.h>
#include <fstream>

using namespace std;
using json = nlohmann::json;

// output file
ofstream outputFile;

// emptying output file
void empty_file() {
    outputFile.open ("data.txt");
    outputFile << "";
    outputFile.close();
}

// record function, saves data in txt file
int record( void *outputBuffer, void *inputBuffer, unsigned int nBufferFrames,
         double streamTime, RtAudioStreamStatus status, void *userData ) { 


    std::cout << streamTime << std::endl;

    // accesses input buffer
    float *buffer = (float *)inputBuffer;

    // writes data to txt file
    outputFile.open ("data.txt", ios_base::app); // append mode
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


int main() {

    // get settings from json file
    json settings_json;
    std::ifstream jfile("settings.json");
    jfile >> settings_json;
    int recordDeviceSetting = settings_json.at("recordDevice");
    int inputChannelsSetting = settings_json.at("inputChannels");
    int firstChannelSetting = settings_json.at("firstChannel");
    int sampleRateSetting = settings_json.at("sampleRate");
    int bufferFramesSetting = settings_json.at("bufferFrames");

    RtAudio audio;

    // Determine the number of devices available
    unsigned int devices = audio.getDeviceCount();


    // lists input devices with id and name
    RtAudio::DeviceInfo info;
    for ( unsigned int i=0; i<devices; i++ ) {
        info = audio.getDeviceInfo( i );
        if ( info.inputChannels > 0 ) {
          std::cout << "device = " << i;
          std::cout << ": name = " << info.name << "\n";
        }
    }
    RtAudio adc;
    if ( adc.getDeviceCount() < 1 ) {
        std::cout << "\nNo devices found!\n";
        exit( 0 );
    }


    // set device to record with 
    // check if device exists
    // print the devices name
    unsigned int recordDevice = settings_json.at("recordDevice");

    if (recordDevice > devices) {
        std::cout << "\nDevice not found!\n";
        exit (0);
    }

    info = audio.getDeviceInfo(recordDeviceSetting);
    std::cout << "\nrecord with: " << info.name << "\n" << std::endl;
    std::cout << "input channels: " << inputChannelsSetting << std::endl;
    std::cout << "first channel: " << firstChannelSetting << std::endl;
    std::cout << "sample rate: " << sampleRateSetting << std::endl;
    std::cout << "buffer frames: " << bufferFramesSetting << std::endl;
    std::cout << std::endl;


    // set input parameters
    RtAudio::StreamParameters parameters;
    parameters.deviceId = recordDeviceSetting;
    parameters.nChannels = inputChannelsSetting;
    parameters.firstChannel = firstChannelSetting;
    unsigned int sampleRate = sampleRateSetting;
    unsigned int bufferFrames = bufferFramesSetting; // 256 sample frames


    empty_file();

    Sleep(2000);

    // open and start input stream
    adc.openStream( NULL, &parameters, RTAUDIO_FLOAT32,
        sampleRate, &bufferFrames, &record );
    adc.startStream();
  
  
    // char input;
    // std::cout << "\nRecording ... press <enter> to quit.\n";
    // std::cin.get( input );

    // record for x milliseconds
    int recordTime = settings_json.at("recordTime");
    Sleep(recordTime);

    // stops the input stream
    adc.stopStream();
    if ( adc.isStreamOpen() ) adc.closeStream();

    // seperator for python output
    std::cout << std::string(60, '-') << std::endl;

    // executes python plotter
    system("main.py");

    return 0;
}
