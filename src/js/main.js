window.onload = function() {

    //start the webgazer tracker
    webgazer.setRegression('ridge') /* currently must set regression and tracker */
        //.setTracker('clmtrackr')
        .setGazeListener(function(data, clock) {
          //   console.log(data); /* data is an object containing an x and y key which are the x and y prediction coordinates (no bounds limiting) */
          //   console.log(clock); /* elapsed time in milliseconds since webgazer.begin() was called */
        })
        .begin()
        .showPredictionPoints(true); /* shows a square every 100 milliseconds where current prediction is */


    //Set up the webgazer video feedback.
    var setup_canvas = function() {

        //Set up the main canvas. The main canvas is used to calibrate the webgazer.
        var canvas = document.getElementById("plotting_canvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        canvas.style.position = 'fixed';

        var img = new Image();   // Create new img element
        img.addEventListener('load', function() {
            canvas.getContext("2d").drawImage(img, 0, 0, canvas.width, canvas.height); // what about aspect ratio
        }, false);
        img.src = "./src/res/data.png"; // Set source path
    };

    var setup_control_toggle = function(){
        var toggle_controls = function(){
            var state = document.getElementById("webgazerGazeDot").style.display == "block"
            webgazer.showFaceOverlay(!state);
            webgazer.showFaceFeedbackBox(!state);
            webgazer.showPredictionPoints(!state);
            webgazer.showVideo(!state);
            document.getElementById("webgazerVideoFeed").style.display = "none" //weirdly there are two of these?!
        };

        document.getElementById("toggle").onclick = toggle_controls;
    };

    function checkIfReady() {
        if (webgazer.isReady()) {
            setup_canvas();
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
