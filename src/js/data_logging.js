
var setup_data_gathering = function(){
    var pupil_data = [];
    
    webgazer.setGazeListener(function(data, elapsedTime) {
        Promise.all([data, elapsedTime]).then(function(valArray) {
            var data = valArray[0];
            var elapsedTime = valArray[1];
            var x = data.x; //these x coordinates are relative to the viewport
            var y = data.y; //these y coordinates are relative to the viewport
            pupil_data.push({x: x, y: y, t: elapsedTime});
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
        var viewport_data = JSON.stringify({w: c.width, h: c.height})
        xmlhttp.setRequestHeader("viewport", viewport_data);
        var json_data = JSON.stringify(pupil_data);
        xmlhttp.send(json_data)
    };

    document.getElementById("save").onclick = dump_pupil_data;
};