#include <cstdio>
#include <cstdlib>
#include <string>
#include <iostream>
#include <regex>

int main(){

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

    // filters out all device names
    std::regex e("Product Name: (.*)");
    std::sregex_iterator iter(resultString.begin(), resultString.end(), e);
    std::sregex_iterator end;
    std::cout << "Devices found: " << iter->size() << std::endl;
    int deviceCounter = 1;
    // lists devices
    while(iter != end){
        std::cout << "Device " << deviceCounter << ": " << (*iter)[1] << std::endl;
        ++iter;
        ++deviceCounter;
    }
}


