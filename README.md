# README #

### What is this repository for? ###

This project allows you to retrieve departure times of buses and trains in the VVS network (available in the area around Stuttgart, Germany) and display the next departure for specific lines on a raspberry pi. The project consists of two parts:

* The backend allows for finding the next departure of specific lines and specific stations. It is written in Python and uses the [meta-efa](https://github.com/opendata-stuttgart/metaEFA) project which provides the current VVS data as a json file. This backend can also be used as a standalone.
* The Frontent is written in QML via PyQT5 and provides a UI that displays the data obtained from the backend. The original purpose is to run it on a Raspberry Pi with a 3.5" display attached, but it should run on any system that supports PyQT5/QML.

### How do I get set up? ###

* Install Python v3.
* Install the following libraries (if missing).
    * pyyaml
    * pyqt5 (not necessary when using only the backend as a library)
    * requests
    * notify2 (optional, for the notification feature on linux)

    The easiest way to install these libraries is via pip. Just enter, e.g., the following command into your terminal:

        pip3 install pyqt5

* On the raspberry pi, pip does not have the required pyqt5 libraries. So you have to install the following packages using apt-get:

    TODO: package list