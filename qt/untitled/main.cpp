#include "mainwindow.h"

#include <QApplication>

#include <iostream>

#include <cstdio>
#include <cstdlib>
#include <string>
#include <iostream>
#include <regex>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}



