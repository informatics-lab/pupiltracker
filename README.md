# Pupil Tracker

This proof of concept demonstrates how we could use pupil tracking to investigate how people ingest information from atmospheric science visualisations.

There are two servers, one for serving HTML and the other providing an API for saving data. You can start them like this

`python simple-htts-server.py`
`python data-server.py`

in the root directory.

The web app code is located in `src`. Most javascript files are dependencies and standard webgazer template apart form `data_logging.js` which sets up the data logging capability. There are also some edits to `main.js`

Analysis code is in the `analysis` directory. `generate.py` takes the local NetCDF file and generates a borderless image plot. `analyse.py` takes pupil data and creates a plot of dwell time as a function of binned data value.

Todo:
* investigate accuracy
* adapt the data saving to send a proper json and not hide stuff in the parameters
* use cartopy to do the lookup of data taking the image projection into account.