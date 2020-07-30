import iris
import json
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as pyplot


def clean_tracking_data(tracking_data, upper_dwell_lim=2000, tolerance=0.2):
    deltas = tracking_data["t"].shift(-1) - tracking_data["t"]
    mean_delta = deltas[deltas < upper_dwell_lim].mean()

    clean_tracking_data = tracking_data[(deltas < upper_dwell_lim) & (deltas > (1.0-tolerance)*mean_delta) & (deltas < (1.0+tolerance)*mean_delta)]
    return clean_tracking_data


def load_webapp_data(webapp_data_path):
    with open(webapp_data_path, "r") as f:
        data = json.load(f)
    viewport = data["viewport"]

    pupil_data = convert_to_frac_coords(clean_tracking_data(pd.DataFrame(data["tracking"])),
                                                                (0, viewport["w"]), (0, viewport["h"]))
    accuracy_data = convert_to_frac_coords(clean_tracking_data(pd.DataFrame(data["accuracy"])),
                                                                (0, viewport["w"]), (0, viewport["h"]))

    return (pupil_data, accuracy_data)


def NaN_out_of_range(tracking_data, x_range, y_range):
    tracking_data["x"][(tracking_data["x"] < x_range[0]) | (tracking_data["x"] > x_range[1])] = np.NaN # i.e. not looking at img
    tracking_data["y"][(tracking_data["y"] < y_range[0]) | (tracking_data["y"] > y_range[1])] = np.NaN # i.e. not looking at img
    return tracking_data
    

def convert_to_coords(tracking_data, orig_xrange, orig_yrange, new_xrange, new_yrange):
    frac_tracking_data = convert_to_frac_coords(tracking_data, orig_xrange, orig_yrange)
    new_tracking_data = frac_tracking_data.copy()
    new_tracking_data["x"] = new_xrange[0] + frac_tracking_data["x"] * (new_xrange[1]-new_xrange[0])
    new_tracking_data["y"] = new_yrange[0] + frac_tracking_data["y"] * (new_yrange[1]-new_yrange[0])

    return new_tracking_data


def convert_to_frac_coords(tracking_data, orig_xrange, orig_yrange):
    """
    Converts from absolut position (in terms of the viewport)
    to the fraction

    * tracking data DataFrame of x, y, t
    * <>_range tuple (xmin, xmax)

    """

    frac_tracking_data = tracking_data.copy()
    frac_tracking_data["x"] = tracking_data["x"]/(orig_xrange[1]-orig_xrange[0])
    frac_tracking_data["y"] = tracking_data["y"]/(orig_yrange[1]-orig_yrange[0])

    return frac_tracking_data


def analyse_accuracy_tracking(accuracy_data, stare_pt):
    """
    calculates reduced statistics of data from an accuracy session

    accuracy_data: DatFrame of x, y,t
    stare_pt: (x, y) of the point that the user was told to stare at
    """
    var = (accuracy_data["x"].var(), accuracy_data["y"].var())
    bias = (accuracy_data["x"].mean()-stare_pt[0], accuracy_data["y"].mean()-stare_pt[1])

    return var, bias


def calc_heatmap(frac_pupil_data, shape, accuracy_var=None, heat_range=5):
    """
    * frac_pupil_data: DataFrame of x, y, t
    * shape: (w, h) shape of heatmap array to create
    * accuracy_var: (x_var, y_var) error from the fractional accuracy calibration data.
        Default no variance
    * heat_range: (int) number of sigmas to propogate heat in each direction 

    """

    if not accuracy_var:
        splat = np.array([[1.0]])
    else:
        frac_var_x, frac_var_y = accuracy_var
        frac_var_x *= 1000
        frac_var_y *= 1
        x_size = int(frac_var_x*heat_range*2*shape[0])
        y_size = int(frac_var_y*heat_range*2*shape[1])
        splat_x = sp.stats.norm.pdf(range(x_size),
                                    0.5*x_size,
                                    frac_var_x*shape[0])
        splat_y = sp.stats.norm.pdf(range(y_size),
                                    0.5*y_size,
                                    frac_var_y*shape[0])

        splat = splat_x[:, None] * splat_y[None, :]

    def add_splat(heatmap, splat, target):
        clamp_to_range = lambda v, vmin, vmax: min(max(vmin, v), vmax)

        target_x_heatmap = target[0]*heatmap.shape[0]
        target_y_heatmap = target[1]*heatmap.shape[1]

        splat_x_halfsize = splat.shape[0]/2.0
        splat_y_halfsize = splat.shape[1]/2.0

        hm_xslice = slice(clamp_to_range(int(round(target_x_heatmap-splat_x_halfsize)), 0, heatmap.shape[0]),
                          clamp_to_range(int(round(target_x_heatmap+splat_x_halfsize)), 0, heatmap.shape[0]))
        hm_yslice = slice(clamp_to_range(int(round(target_y_heatmap-splat_y_halfsize)), 0, heatmap.shape[1]),
                          clamp_to_range(int(round(target_y_heatmap+splat_y_halfsize)), 0, heatmap.shape[1]))
        sp_xslice = slice(clamp_to_range(int(round(splat_x_halfsize-target_x_heatmap)), 0, splat.shape[0]),
                          clamp_to_range(int(round(target_x_heatmap+splat_x_halfsize)), 0, splat.shape[0]))
        sp_yslice = slice(clamp_to_range(int(round(splat_y_halfsize-target_y_heatmap)), 0, splat.shape[1]),
                          clamp_to_range(int(round(target_y_heatmap+splat_y_halfsize)), 0, splat.shape[1]))

        heatmap[hm_xslice, hm_yslice] += splat[sp_xslice, sp_yslice]

    heatmap = np.zeros(shape)
    for row in frac_pupil_data.itertuples(name=None):
        add_splat(heatmap, splat, (row[1], row[2]))

    return heatmap


# def dwell_histogram(webapp_data_path, image_data_path, upper_dwell_lim=1000, nbins=10):
#     pupil_data, accuracy_data = load_webapp_data(webapp_data_path)

#     image_data = iris.load_cube(image_data_path).data

#     dataw, datah = image_data.shape

#     pupil_data["xidxs"] = pupil_data["x"]/viewport_data["w"]*dataw
#     pupil_data["yidxs"] = pupil_data["y"]/viewport_data["h"]*datah
#     pupil_data["xidxs"][(pupil_data["xidxs"] < 0) | (pupil_data["xidxs"] > viewport_data["w"])] = np.NaN # i.e. not looking at img
#     pupil_data["yidxs"][(pupil_data["yidxs"] < 0) | (pupil_data["yidxs"] > viewport_data["h"])] = np.NaN # i.e. not looking at img

#     halfdeltas = (pupil_data["t"] - pupil_data["t"].shift(1)) / 2
#     dwell = halfdeltas + halfdeltas.shift(-1)
#     dwell[dwell > upper_dwell_lim] = np.NaN
#     pupil_data["dwell"] = dwell

#     pupil_data = pupil_data.dropna()

#     i_s = pupil_data["xidxs"].astype("int").to_list()
#     j_s = pupil_data["yidxs"].astype("int").to_list()

#     values = image_data[i_s, j_s]
#     pupil_data["values"] = values

#     delta = (image_data.max() - image_data.min()) / nbins
#     bounds = [image_data.min() + i*delta for i in range(nbins)]
#     binned_dwell = []
#     for a,b in zip(bounds[:-1], bounds[1:]):
#         this_sum = pupil_data["dwell"][(pupil_data["values"] > a) & (pupil_data["values"] < b)].sum()
#         binned_dwell.append(this_sum)

#     plt.hist(binned_dwell, bins=bounds, edgecolor="k")
#     plt.xticks(bounds)
#     plt.show()

#     return binned_dwell, bounds


# res = dwell_histogram("pupil_data.json", "global_daily_pmsl_mean_20200509.nc", "viewport.json")
# print(res)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import iris.plot as iplt

    pupil_data, accuracy_data = load_webapp_data("./pupil_data.json")
    image_data = iris.load_cube("./global_daily_pmsl_mean_20200509.nc")

    var, bias = analyse_accuracy_tracking(accuracy_data, (0.5, 0.5))
    print(var)
    plt.scatter(accuracy_data['x'], accuracy_data['y'])
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.title("Calibration measurement")

    # var = (var[0]*100, var[1]*100)
    hm = calc_heatmap(pupil_data, image_data.shape, var)
    heatmap = image_data.copy(data=hm)

    plt.figure()
    plt.subplot(1,2,1)
    plt.title("Field")
    iplt.pcolormesh(image_data)
    plt.gca().coastlines()
    plt.subplot(1,2,2)
    plt.title("Heat Map")
    iplt.pcolormesh(heatmap)
    plt.gca().coastlines()
    plt.show()