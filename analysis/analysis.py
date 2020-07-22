import iris
import numpy as np
import pandas as pd



def histogram(pupil_data_path, image_data_path, imgw=1280, imgh=640, upper_dwell_lim=1000, nbins=10):
    pupil_data = pd.read_json(pupil_data_path)
    image_data = iris.load_cube(image_data_path).data

    dataw, datah = image_data.shape

    pupil_data["xidxs"] = pupil_data["x"]/imgw*dataw
    pupil_data["yidxs"] = pupil_data["y"]/imgh*datah
    pupil_data["xidxs"][(pupil_data["xidxs"] < 0) | (pupil_data["xidxs"] > imgw)] = np.NaN # i.e. not looking at img
    pupil_data["yidxs"][(pupil_data["yidxs"] < 0) | (pupil_data["yidxs"] > imgh)] = np.NaN # i.e. not looking at img

    halfdeltas = (pupil_data["t"] - pupil_data["t"].shift(1)) / 2
    dwell = halfdeltas + halfdeltas.shift(-1)
    dwell[dwell > upper_dwell_lim] = np.NaN
    pupil_data["dwell"] = dwell

    pupil_data = pupil_data.dropna()

    i_s = pupil_data["xidxs"].astype("int").to_list()
    j_s = pupil_data["yidxs"].astype("int").to_list()

    values = image_data[i_s, j_s]
    pupil_data["values"] = values

    delta = (image_data.max() - image_data.min()) / nbins
    bounds = [image_data.min() + i*delta for i in range(nbins)]
    binned_dwell = []
    for a,b in zip(bounds[:-1], bounds[1:]):
        this_sum = pupil_data["dwell"][(pupil_data["values"] > a) & (pupil_data["values"] < b)].sum()
        binned_dwell.append(this_sum)

    return binned_dwell, bounds
