import QtQuick 2.2
//import QVVSConnectionData 1.0

Rectangle {
    id: outer_frame
    color: "black"
    //width: 720
    //height: 480
    width: 640
    height: 480

    property double scale: computeScale()

    function computeScale(){
        var xScale = width / 640;
        var yScale = height / (240 * con.length);
        return xScale < yScale ? xScale : yScale;
    }


    FontLoader{
        id: myFont; source: "fonts/NotoSans-Regular.ttf"
    }
    FontLoader{
        source: "fonts/NotoSans-Bold.ttf"
    }
    FontLoader{
        source: "fonts/NotoSans-Italic.ttf"
    }
    FontLoader{
        source: "fonts/NotoSans-BoldItalic.ttf"
    }



    Column {
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        Repeater {
            id: repeater
            model: con

            Rectangle{
                id: repeater_element
                anchors.left: parent.left
                anchors.right: parent.right
                height: outer_frame.height/con.length

                Rectangle{
                    id: background
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    color: computeBGColor()

                    function computeBGColor() {
                        //Check for errors
                        if (modelData.nextConnection.errorInternet || modelData.nextConnection.errorNotFound){
                            return "purple"
                        }
                        
                        var minRemaining = modelData.nextConnection.minutesToDeparture
                        if(minRemaining > 15){
                            return "darkblue"
                        }else if(minRemaining >6){
                            return "forestgreen"
                        }else if(minRemaining >= 4){
                            return "goldenrod"
                        }
                        return "darkred";
                    }
                    
                    Text {
                        id: text_line_name
                        anchors.top: parent.top
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        width: 175 * outer_frame.scale
                        font.family: myFont.name
                        font.pixelSize: 78 * outer_frame.scale
                        
                        color: "white"
                        font.bold: true
                        text: modelData.nextConnection.line + ":"
                    }
                    
                    Text {
                        id: text_time_remaining
                        anchors.left: text_line_name.right
                        anchors.top: text_line_name.top
                        font.pixelSize: text_line_name.font.pixelSize
                        font.family: text_line_name.font.family
                        
                        color: "white"
                        text: computeText();

                        function computeText() {
                            //Check for errors. Note that the updater ensures that only one at a time can occur.
                            if (modelData.nextConnection.errorInternet){
                                return "<i>Internet<br>Error!</i>";
                            }
                            else if(modelData.nextConnection.errorNotFound){
                                return "<i>Not found!</i>";
                            }
                            
                            return modelData.nextConnection.minutesToDeparture + " min left";
                        }
                    }
                    
                    Text {
                        id: text_departure_time
                        anchors.left: text_line_name.left
                        anchors.leftMargin: text_line_name.width * 0.3
                        anchors.top: text_line_name.bottom
                        font.pixelSize: text_line_name.font.pixelSize * 0.58
                        font.family: text_line_name.font.family
                        
                        color: "white"
                        text: computeText();

                        function computeText() {
                            //Check for errors. Note that the updater ensures that only one at a time can occur.
                            if (modelData.nextConnection.errorInternet || modelData.nextConnection.errorNotFound){
                                return "";
                            }
                            
                            return "Departs at " + modelData.nextConnection.departureTime;
                        }
                    }
                    
                    Text {
                        id: text_delay
                        anchors.left: text_departure_time.left
                        anchors.top: text_departure_time.bottom
                        font.pixelSize: text_departure_time.font.pixelSize
                        font.family: text_line_name.font.family
                        
                        color: "white"
                        text: computeText();
                        function computeText() {
                            //Check for errors. Note that the updater ensures that only one at a time can occur.
                            if (modelData.nextConnection.errorInternet || modelData.nextConnection.errorNotFound){
                                return ""
                            }
                            
                            return "Delay of " + modelData.nextConnection.delay + " min";
                        }
                    }

                    Canvas {
                        id: progress_indicator
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom

                        width: Math.max(1, 100 * outer_frame.scale)
                        height: width

                        property int nextUpdateUnix: modelData.nextUpdate
                        property int updateDelayInSec: modelData.updateDelay
                        
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.reset();

                            var centreX = width / 2;
                            var centreY = height / 2;

                            
                            //var arcPercentage = modelData.updateProgress * -1 + 1;

                            
                            var currentTime = Date.now()/1000;  //convert from milliseconds to seconds
                            var updateProgress = (nextUpdate - currentTime)/updateDelayInSec
                            if(updateProgress < 0){
                                updateProgress = 0;
                            }else if (updateProgress > 1){
                                updateProgress = 1;
                            }
                            var arcPercentage = updateProgress * -1 + 1;
                            

                            
                            ctx.beginPath();
                            ctx.fillStyle = "white";
                            ctx.moveTo(centreX, centreY);
                            ctx.arc(centreX, centreY, width / 4, Math.PI*(-0.5), Math.PI*(-0.5) - arcPercentage * Math.PI * 2, true);
                            ctx.fill();
                        }
                        
                        Timer {
                            interval: 1000; running: true; repeat: true
                            onTriggered: progress_indicator.requestPaint()
                        }
                    }
                }
                
                Rectangle{
                    id: separator_line
                    anchors.left: parent.left
                    anchors.right: parent.right
                    //anchors.bottom: parent.bottom
                    y: parent.height - height/2
                    height: Math.max(1, 8 * (outer_frame.scale)) //Math.max(1,Math.min(10, 10 * (outer_frame.height/240/repeater.count)));
                    color: computeColor()

                    function computeColor(){
                        //Do not show the last separator
                        if (repeater.count - 1 == index){
                            return "transparent";
                        }
                        return "white";
                    }
                }
            }
        }
    }
}
