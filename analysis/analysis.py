import iris
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def dwell_histogram(pupil_data_path, image_data_path, viewport_data_path, upper_dwell_lim=1000, nbins=10):
    pupil_data = pd.read_json(pupil_data_path)
    image_data = iris.load_cube(image_data_path).data
    with open(viewport_data_path, "r") as f:
        viewport_data = json.loads(json.load(f))

    dataw, datah = image_data.shape

    pupil_data["xidxs"] = pupil_data["x"]/viewport_data["w"]*dataw
    pupil_data["yidxs"] = pupil_data["y"]/viewport_data["h"]*datah
    pupil_data["xidxs"][(pupil_data["xidxs"] < 0) | (pupil_data["xidxs"] > viewport_data["w"])] = np.NaN # i.e. not looking at img
    pupil_data["yidxs"][(pupil_data["yidxs"] < 0) | (pupil_data["yidxs"] > viewport_data["h"])] = np.NaN # i.e. not looking at img

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

    plt.hist(binned_dwell, bins=bounds, edgecolor="k")
    plt.xticks(bounds)
    plt.show()

    return binned_dwell, bounds


res = dwell_histogram("pupil_data.json", "global_daily_pmsl_mean_20200509.nc", "viewport.json")
print(res)
