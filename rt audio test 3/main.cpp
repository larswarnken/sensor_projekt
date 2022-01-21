#include "RtAudio.h"
#include <iostream>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <unistd.h> // sleep
#include <fstream> // writing to file

using namespace std;

ofstream myfile;

// emptying output file
void empty_file() {
    myfile.open ("data.txt");
    myfile << "";
    myfile.close();
}


int record( void *outputBuffer, void *inputBuffer, unsigned int nBufferFrames,
         double streamTime, RtAudioStreamStatus status, void *userData ) { 


    std::cout << streamTime << std::endl;

    // accesses input buffer
    float *buffer = (float *)inputBuffer;

    // writes data to txt file
    myfile.open ("data.txt", ios_base::app); // append mode
    static unsigned int i;
    for (i=0;i<nBufferFrames;i++) {
        // std::cout << buffer[i] << ", ";
        if(streamTime != 0){
            myfile << buffer[i] << "\n";
        }
    }
    myfile.close();

    return 0;
}


int main() {

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
    unsigned int record_device = 9;

    if (record_device > devices) {
        std::cout << "\nDevice not found!\n";
        exit (0);
    }

    info = audio.getDeviceInfo(record_device);
    std::cout << "\nrecord with: " << info.name << "\n" << std::endl;


    // set input parameters
    RtAudio::StreamParameters parameters;
    parameters.deviceId = record_device;
    parameters.nChannels = 1;
    parameters.firstChannel = 0;
    unsigned int sampleRate = 1000;
    unsigned int bufferFrames = 256; // 256 sample frames


    empty_file();

    // open and start input stream
    adc.openStream( NULL, &parameters, RTAUDIO_FLOAT32,
        sampleRate, &bufferFrames, &record );
    adc.startStream();
  
  
    // char input;
    // std::cout << "\nRecording ... press <enter> to quit.\n";
    // std::cin.get( input );

    // record for x milliseconds
    Sleep(2000);

    // stops the input stream
    adc.stopStream();
    if ( adc.isStreamOpen() ) adc.closeStream();

    // seperator for python output
    std::cout << std::string(60, '-') << std::endl;

    // executes python plotter
    system("main.py");

    return 0;
}
