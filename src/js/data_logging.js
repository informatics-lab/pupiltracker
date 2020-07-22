
var setup_data_gathering = function(){
    var pupil_data = [];
    
    webgazer.setGazeListener(function(data, elapsedTime) {
        data.then(function(data, elapsedTime){
            test = data;
            var xprediction = data.x; //these x coordinates are relative to the viewport
            var yprediction = data.y; //these y coordinates are relative to the viewport
            // console.log(elapsedTime); //elapsed time is based on time since begin was called
            pupil_data.push({xprediction, yprediction, elapsedTime});
        },
            function(){return;}
        )

    }).begin();

    var dump_pupil_data = function(){
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

    document.getElementById("save").onclick = dump_pupil_data;
};