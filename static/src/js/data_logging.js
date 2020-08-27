var setup_data_gathering = function(){
    var record_tracking_data = false;
    var record_accuracy_data = false;

    var tracking_data = [];
    var accuracy_data = [];
    var imgurls = [];
    var imgurl = null;
    
    webgazer.setGazeListener(function(data, elapsedTime) {
        Promise.all([data, elapsedTime]).then(function(valArray) {
            var data = valArray[0];
            var elapsedTime = valArray[1];
            if (data == null) {return;}
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

    var update_image = function(){
        if (imgurls.length == 0){
            var xmlhttp = new XMLHttpRequest();
            var api_urls = "get-image-urls";
            xmlhttp.open("GET", api_urls);
            xmlhttp.setRequestHeader("subdomain", window.location.hostname.split(".")[0])
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    imgurls = JSON.parse(xmlhttp.responseText);
                    imgurl = imgurls.pop();
                    img.src = imgurl;
                }
            }
            xmlhttp.send()
        }else{
            imgurl = imgurls.pop();
            img.src = imgurl;
        }
    }

        //Set up the webgazer video feedback.
    var setup_canvas = function() {
        //Set up the main canvas. The main canvas is used to calibrate the webgazer.
        var canvas = document.getElementById("plotting_canvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        canvas.style.position = 'fixed';
        canvas.style.display = 'none'; //hidden by default

        
        img.addEventListener('load', function() {
            canvas.getContext("2d").drawImage(img, 0, 0, canvas.width, canvas.height); // what about aspect ratio
        }, false);
    };

    var canvas = document.getElementById("plotting_canvas");
    var img = new Image();   // Create new img element
    setup_canvas()
    update_image()

    var getUID = function() {
        var generateUID = function () { return '_' + Math.random().toString(36).substr(2, 9); };
        UIDcookie = document.cookie.split('; ').find(row => row.startsWith('UID'));
        if (UIDcookie == undefined){
            var UID = generateUID();
            document.cookie = "UID="+UID;    
        }else{
            var UID = UIDcookie.split('=')[1];
        }
        
        return UID
    };

    var dump_pupil_data = function(){
        xmlhttp = new XMLHttpRequest();
        var url = "save-data";
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("subdomain", window.location.hostname.split(".")[0])
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.setRequestHeader("Access-Control-Allow-Origin", "true");
        xmlhttp.onreadystatechange = function () { //Call a function when the state changes.
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                alert("Saved");
            }
        }
        var c = document.getElementById("plotting_canvas");
        var UID = getUID();

        data = {"tracking": tracking_data, "viewport": {w: c.width, h: c.height},
                "accuracy": accuracy_data, "UID": UID,
                "imageurl": imgurl};
        var json_data = JSON.stringify(data);
        xmlhttp.send(json_data)
    };

    var measure_accuracy = function(){
        accuracy_data = []
        document.getElementById("calibration_dot").style.display = "block";
        alert("Stare at the orange dot for the next five seconds")

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
            document.getElementById("calibration_dot").style.display = "none";
            record_tracking_data = orig_record_state;
            console.log(accuracy_data)
        });
    };

    document.getElementById("accuracy").onclick = measure_accuracy;

    document.getElementById("session").onclick = function (){
        record_tracking_data = !record_tracking_data
        if(record_tracking_data){
            tracking_data = [];
            document.getElementById("session").innerHTML = "Stop recording";
            document.getElementById("plotting_canvas").style.display = "block";
        }else{
            update_image()
            document.getElementById("session").innerHTML = "Start recording";
            document.getElementById("plotting_canvas").style.display = "none";
            dump_pupil_data()
        }
    };
};