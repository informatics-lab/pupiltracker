var setup_data_gathering = function(){
    var record_tracking_data = true;
    var record_accuracy_data = false;

    var tracking_data = [];
    var accuracy_data = [];
    
    webgazer.setGazeListener(function(data, elapsedTime) {
        Promise.all([data, elapsedTime]).then(function(valArray) {
            var data = valArray[0];
            var elapsedTime = valArray[1];
            var x = data.x; //these x coordinates are relative to the viewport
            var y = data.y; //these y coordinates are relative to the viewport
            if(record_tracking_data){
                tracking_data.push({x: x, y: y, t: elapsedTime});
            }
            if(record_accuracy_data){
                accuracy_data.push({x: x, y: y, t: elapsedTime});
            }
        });

    }).begin();

    var dump_pupil_data = function(){
        xmlhttp = new XMLHttpRequest();
        var url = "http://localhost:5000/save-data";
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.setRequestHeader("Access-Control-Allow-Origin", "true");
        xmlhttp.onreadystatechange = function () { //Call a function when the state changes.
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                alert("Saved");
            }
        }
        var c = document.getElementById("plotting_canvas");

        data = {"tracking": tracking_data, "viewport": {w: c.width, h: c.height}, "accuracy": accuracy_data}
        var json_data = JSON.stringify(data);
        xmlhttp.send(json_data)
    };

    var measure_accuracy = function(){
        alert("Stare at the tip of Cornwall for the next five seconds")
        var canvas = document.getElementById("plotting_canvas");
        var ctx = canvas.getContext("2d")
        var w = canvas.width / 2;
        var h = canvas.height / 2;
        var orig_record_state = record_tracking_data;
        record_tracking_data = false;
        record_accuracy_data = true;

        async function wait(ms) {
          return new Promise(resolve => {
            setTimeout(resolve, ms);
          });
        }

        wait(5000).then(() => {
            record_accuracy_data = false;
            alert("Finished accuracy recording")
            record_tracking_data = orig_record_state;
            console.log(accuracy_data)
        });
    };

    document.getElementById("accuracy").onclick = measure_accuracy;
    document.getElementById("save").onclick = dump_pupil_data;
};