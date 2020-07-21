import iris
import iris.plot as iplt
import matplotlib.pyplot as plt


def generate_image(file_name):
    d = iris.load_cube(file_name)
    iplt.pcolormesh(d)
    plt.gca().coastlines()
    plt.gca().set_axis_off()
    plt.savefig("./data.png", bbox_inches="tight", dpi=500)

if __name__ == '__main__':
    pass