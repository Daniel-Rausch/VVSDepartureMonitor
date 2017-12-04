# README #

### What is this repository for? ###

This project allows you to retrieve departure times of buses and trains in the VVS network (available in the area around Stuttgart, Germany) and display the next departure for specific lines on a raspberry pi. The project consists of two parts:

* The backend allows for finding the next departure of specific lines and specific stations. It is written in Python and uses the [meta-efa](https://github.com/opendata-stuttgart/metaEFA) project which provides the current VVS data as a json file. This backend can also be used as a standalone.
* The Frontent is written in QML via PyQT5 and provides a UI that displays the data obtained from the backend. The original purpose is to run it on a Raspberry Pi with a 3.5" display attached, but it should run on any system that supports PyQT5/QML.

### How do I get set up? ###

* Install Python v3.
* Install the python requests library. The easiest way is to use pip3, i.e., type the following in your terminal (potentially after installing pip3 first):
> pip3 install requests
* If you want to use the frontend, also install PyQT5 and QT. The easiest way to do so is also via pip3:
> pip3 install pyqt5
Note that this won't work for the raspberry pi. Instead, you need to manually install the required packages:
> TODO: package list