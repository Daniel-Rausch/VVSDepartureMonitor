import QtQuick 2.2
//import QVVSConnectionData 1.0

Rectangle {
    color: "black"
    //width: 720
    //height: 480
    width: 480
    height: 320



    Column {
	    anchors.top: parent.top
	    anchors.left: parent.left
	    anchors.right: parent.right
	    anchors.bottom: parent.bottom

	    Repeater {
	        model: con

            Rectangle{
	            anchors.left: parent.left
	            anchors.right: parent.right
                height: parent.parent.height/2
                color: "green"
                
            	Text {
                    id: text_line_name
		            color: "white"
		            //anchors.top: text_remaining.bottom
		            text: generateText();
		            //fontSizeMode: Text.Fit
		            font.pixelSize: 100
		            //width: parent.width
		            //height: parent.height/2
		            height: 120

		            function generateText() {
		                return index + ". " + modelData.nextConnection.line + ": " + modelData.nextConnection.minutesToDeparture + "s";
		            }
	            }
                Rectangle{
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: text_line_name.bottom
                    anchors.bottom: parent.bottom
                    color: "red"
                }
            }
	    }
    }


/*
    Rectangle {
	color: "darkblue"
	anchors.top: parent.top
	anchors.left: parent.left
	anchors.right: parent.right
	anchors.bottom: parent.bottom
	
	Text {
	    id: text_remaining
	    color: "white"
	    text: "Next bus in: " + con.nextConnection.line + " - " + con.nextConnection.minutesToDeparture
	    anchors.fill: parent
	}
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
    }*/
}
