var positions = [];

webgazer.setGazeListener(function(data, elapsedTime) {
    if (data == null) {
        return;
    }
    var xprediction = data.x; //these x coordinates are relative to the viewport
    var yprediction = data.y; //these y coordinates are relative to the viewport
    console.log(elapsedTime); //elapsed time is based on time since begin was called
    position.append(data);
}).begin();

var dump_pupil_data = function(pupil_data){
    xmlhttp = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/save-data";
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-type", "application/json");
    xmlhttp.onreadystatechange = function () { //Call a function when the state changes.
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            alert(xmlhttp.responseText);
        }
    }
    var data = JSON.stringify(pupil_data);
    xmlhttp.send({data: data})
};