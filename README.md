# Pupil Tracker

This proof of concept demonstrates how we could use pupil tracking to investigate how people ingest information from atmospheric science visualisations.

Top tips:
* Make sure your face/eyes are well illuminated
* If the pupil tracking is inaccurate, look at the mouse pointer and click to add a new calibration point. Be sure to do this all over the screen.
* Bigger screen will increase the accuracy

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