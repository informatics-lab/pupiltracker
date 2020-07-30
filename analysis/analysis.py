from analysis_tools import *
import numpy as np


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import iris.plot as iplt

    pupil_data, accuracy_data = load_webapp_data("./pupil_data.json")
    image_data = iris.load_cube("./global_daily_pmsl_mean_20200509.nc") 

    std, bias = analyse_accuracy_tracking(accuracy_data, (0.5, 0.5))
    plt.scatter(accuracy_data['x'], accuracy_data['y'])
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.title("Calibration measurement")

    hm = calc_heatmap(pupil_data, (image_data.shape[1], image_data.shape[0]), std)
    hm = np.moveaxis(hm, 1, 0)
    shift = int(hm.shape[1]/2.0)
    hm = np.roll(hm, shift, axis=1)
    hm = hm[::-1, :]
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