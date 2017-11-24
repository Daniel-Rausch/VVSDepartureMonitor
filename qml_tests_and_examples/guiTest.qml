import QtQuick 2.5
import QtQuick.Controls 1.2
ApplicationWindow {
    width: 500; height: 500;
    objectName: "MainWindow";
    id: applicationwindow01;

    Rectangle {
        width: 250; height: 250;
        objectName: "Rectangle1";
        color: "red";
        id: rectangle01;
    }

    Rectangle {
        width: 250; height: 250;
        objectName: "Rectangle2";
        color: "green";
        id: rectangle02;
        anchors.left: rectangle01.right;
        anchors.top: rectangle01.bottom;
    }
}