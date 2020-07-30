# Pupil Tracker

This proof of concept demonstrates how we could use pupil tracking to investigate how people ingest information from atmospheric science visualisations.

## Installation/Setup
You will need conda

1. `git clone git@github.com:niallrobinson/pupiltracker.git`
1. `cd pupiltracker`
1. `conda env create -f environment.yml`
1. `conda activate pupiltracking`
1. `python simple-https-server.py`
1. in a new terminal `conda activate pupiltracking` and then `python data-server.py`
1. in a browser go to http://localhost:4443/main.html

## Use
1. wait until the app has locked on to your face
1. start the app by clicking
1. you can calibrate the system by looking at the mouse pointer and clicking
    * the best way to do this is to press "Hide/Display tracking", otherwise its very hard not to look at the dot
    * then move the mouse, look at the mouse, and click. It's surprisingly hard to look where you think you're looking
    * make sure you do this all over the screen
1. press "Hide/Display tracking" again to check it's doing something sensible
1. press "Hide/Display tracking" again to get the controls out the way
1. press "Measure accuracy", this will pop up a box which asks you to stare at a dot in the centre of the screen for 5s. If you feel like you accidentally looked at something else you can do it again.
1. press "Start recording" and inspect the image!
1. when you're done, press the "Stop recording" button.

## Analysis
To view a heatmap of your session
1. `cd ./analysis`
1. python analysis.py

## Top tips
* Make sure your face/eyes are well illuminated
* Bigger screen will increase the accuracy. You can use an external monitor as long as your webcam has a good view of your face.
# Try to keep your head still and inside the box

---

There are two servers, one for serving HTML and the other providing an API for saving data. You can start them like this

`python simple-htts-server.py`
`python data-server.py`

in the root directory.

The web app code is located in `src`. Most javascript files are dependencies and standard webgazer template apart form `data_logging.js` which sets up the data logging capability. There are also some edits to `main.js`

Analysis code is in the `analysis` directory. `generate.py` takes the local NetCDF file and generates a borderless image plot. `analyse.py` takes pupil data and creates a plot of dwell time as a function of binned data value.

Todo:
* investigate accuracy [DONE?]
* adapt the data saving to send a proper json and not hide stuff in the parameters [DONE]
* use cartopy to do the lookup of data taking the image projection into account.
* calibrate on mouseclick [DONE]
* heatmap creator [DONE]