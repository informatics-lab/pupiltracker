window.onload = function(){
    alert("This webpage is a proof of concept and not for public consumption. It emplies no level of quality, accuary, ability or anything else.")
    //start the webgazer tracker
    webgazer.setRegression('ridge') /* currently must set regression and tracker */
        //.setTracker('clmtrackr')
        .setGazeListener(function(data, clock) {
          //   console.log(data); /* data is an object containing an x and y key which are the x and y prediction coordinates (no bounds limiting) */
          //   console.log(clock); /* elapsed time in milliseconds since webgazer.begin() was called */
        })
        .begin()
        .showPredictionPoints(true); /* shows a square every 100 milliseconds where current prediction is */


    var setup_control_toggle = function(){
        var controls_visible = true; 
        var toggle_controls = function(){
            controls_visible = !controls_visible;
            var display = controls_visible ? "block" : "none";
            console.log(display)
            console.log(controls_visible)
            webgazer.showFaceOverlay(controls_visible);
            webgazer.showFaceFeedbackBox(controls_visible);
            webgazer.showPredictionPoints(controls_visible);
            webgazer.showVideo(controls_visible);
            document.getElementById("webgazerVideoFeed").style.display = display; //weirdly there are two of these?!
            document.getElementById("webgazerFaceFeedbackBox").style.display = display; //weirdly there are two of these?!
            document.getElementById("webgazerDot").style.display = display; //weirdly there are two of these?!
        };

        document.getElementById("toggle").onclick = toggle_controls;
    };

    function checkIfReady() {
        if (webgazer.isReady()) {
            setup_control_toggle();
            setup_data_gathering();
        } else {
            setTimeout(checkIfReady, 100);
        }
    }
    setTimeout(checkIfReady,100);
};

// Kalman Filter defaults to on. Can be toggled by user.
window.applyKalmanFilter = true;

// Set to true if you want to save the data even if you reload the page.
window.saveDataAcrossSessions = false;

window.onbeforeunload = function() {
    webgazer.end();
}

/**
 * Restart the calibration process by clearing the local storage and reseting the calibration point
 */
function Restart(){
    document.getElementById("Accuracy").innerHTML = "<a>Not yet Calibrated</a>";
    ClearCalibration();
    PopUpInstruction();
}
