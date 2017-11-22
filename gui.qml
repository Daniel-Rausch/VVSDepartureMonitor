import QtQuick 2.2
//import QVVSConnection 1.0

Rectangle {
    color: "black"
    width: 500
    height: 500

    Rectangle {
	color: "darkblue"
	anchors.top: parent.top
	anchors.left: parent.left
	anchors.right: parent.right
	anchors.bottom: parent.bottom
	
	Text {
	    id: text_remaining
	    color: "white"
	    text: "Next bus in: " + con.nextConnection.line
	    anchors.fill: parent
	}
    }
	
	/*
    Column {
	anchors.top: text_remaining.bottom
	anchors.left: parent.left
	anchors.right: parent.right
	anchors.bottom: parent.bottom

	Repeater {
	    model: countdowns.items
	    
	    Text {
		color: "yellow"
		//anchors.top: text_remaining.bottom
		text: generateText();
		//fontSizeMode: Text.Fit
		font.pixelSize: 100
		//width: parent.width
		//height: parent.height/2
		height: 120

		function generateText() {
		    return index + ". " + modelData.name + ": " + modelData.remaining + "s";
		}
		
	    }
	}
    }*/
}
