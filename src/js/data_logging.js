
var setup_data_gathering = function(){
    var pupil_data = [];
    
    webgazer.setGazeListener(function(data, elapsedTime) {
        data.then(function(data, elapsedTime){
            var x = data.x; //these x coordinates are relative to the viewport
            var y = data.y; //these y coordinates are relative to the viewport
            // console.log(elapsedTime); //elapsed time is based on time since begin was called
            pupil_data.push([x, y, elapsedTime]);
        },
            function(){return;}
        )

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
        var data = JSON.stringify(pupil_data);
        xmlhttp.send(data)
    };

    document.getElementById("save").onclick = dump_pupil_data;
};