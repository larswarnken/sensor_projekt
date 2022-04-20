#include <iostream>
#include "RtAudio.h"

#include <cstdlib>
#include <cstring>

#include <unistd.h> // sleep

#include <fstream> // writing to file

using namespace std;

ofstream myfile;

// emptying output file
void empty_file() {
    myfile.open ("example.txt");
    myfile << "";
    myfile.close();
}

int record( void *outputBuffer, void *inputBuffer, unsigned int nBufferFrames,
         double streamTime, RtAudioStreamStatus status, void *userData )
{ 
    // Do something with the data in the "inputBuffer" buffer.
    // std::cout << *(int *)inputBuffer << std::endl;

    // std::cout << streamTime << std::endl;

    
    // myfile.open ("example.txt", ios_base::app);
    // myfile << streamTime << "\n";
    // myfile.close();

    myfile.open ("example.txt", ios_base::app);

    float *buffer = (float *)inputBuffer;

    static unsigned int i;
    for (i=0;i<nBufferFrames;i++) {
        std::cout << buffer[i] << ", ";
        if(streamTime != 0){
            myfile << buffer[i] << "\n";
        }
    }
    myfile.close();
    std::cout << "\n\n";

    return 0;
}

int main() {

    RtAudio audio;

    // Determine the number of devices available
    unsigned int devices = audio.getDeviceCount();
    // Scan through devices for various capabilities
    RtAudio::DeviceInfo info;
    for ( unsigned int i=0; i<devices; i++ ) {
        info = audio.getDeviceInfo( i );
        if ( info.inputChannels == 2 ) {
          // Print, for example, the maximum number of output channels for each device
          std::cout << "device = " << i;
          std::cout << ": name = " << info.name << "\n";
        }
    }

    RtAudio adc;
    if ( adc.getDeviceCount() < 1 ) {
        std::cout << "\nNo audio devices found!\n";
        exit( 0 );
    }

    int record_device = 11;
    info = audio.getDeviceInfo(record_device);
    std::cout << std::endl <<"record with: " << info.name << std::endl;

    RtAudio::StreamParameters parameters;
    parameters.deviceId = record_device;
    parameters.nChannels = 1;
    parameters.firstChannel = 0;
    unsigned int sampleRate = 44100;
    unsigned int bufferFrames = 256; // 256 sample frames

    empty_file();
  
    adc.openStream( NULL, &parameters, RTAUDIO_FLOAT32,
        sampleRate, &bufferFrames, &record );
    adc.startStream();
  
  
  
    // char input;
    // std::cout << "\nRecording ... press <enter> to quit.\n";
    // std::cin.get( input );

    // record for x milliseconds
    Sleep(2000);

    // Stop the stream
    adc.stopStream();
    if ( adc.isStreamOpen() ) adc.closeStream();

    system("main.py");

    return 0;
}
