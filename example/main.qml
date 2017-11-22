import QtQuick 2.2

Rectangle {
    color: "black"
    width: 500
    height: 500

    Text {
	id: text_remaining
	color: "white"
	anchors.top: parent.top
	anchors.left: parent.left
	text: "Time remaining: " + countdown.remaining
    }
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
    }
}
