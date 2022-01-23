#include <iostream>
#include "RtAudio.h"

#include <cstdlib>
#include <cstring>


int main(){

    RtAudio audio;

    // Determine the number of devices available
    unsigned int devices = audio.getDeviceCount();
    std::cout << "Devices found: " << devices << std::endl << std::endl;
    // Scan through devices for various capabilities
    RtAudio::DeviceInfo info;
    for ( unsigned int i=0; i<devices; i++ ) {
        info = audio.getDeviceInfo( i );
        if ( info.probed == true ) {
          // Print, for example, the maximum number of output channels for each device
          std::cout << "device " << i;
          std::cout << ": name: " << info.name << ", ";
          std::cout << "out ch: " << info.outputChannels << ", ";
          std::cout << "in ch: " << info.inputChannels << "\n";
        }
    }

    // RtAudio::DeviceInfo info;
    // info = audio.getDeviceInfo( 7 );

    // std::cout << info.name << std::endl;

    return 0;
}
