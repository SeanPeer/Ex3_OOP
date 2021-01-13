import matplotlib.pyplot as plt
import json
import numpy


def bar_plot(data, files, json_datam, colors=None, total_width=0.8, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: List
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data[0])

    # The width of a single bar
    bar_width = total_width / n_bars

    for i, file in enumerate(files):
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # List containing handles for the drawn bars, used for the legend
        bars = []
        labels = []
        ticks = []

        fig, ax = plt.subplots(figsize=(10,10))
        fig.canvas.set_window_title('Test')

        for x, k in enumerate(data[i]):
            labels.append(x)
            ticks.append(x+x_offset)
            bar = ax.bar(x + x_offset, k, width=bar_width * single_width, color=colors[x % len(colors)])
            bars.append(bar[0])

        if legend:
            ax.legend(bars, json_datam.keys())

        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)
        plt.title("Comparing graph: " + file.split(".json")[0].split("/")[2])
        plt.xlabel("Method")
        plt.ylabel("Runtime (m/s) ")

        plt.show(block=False)
        plt.pause(1)
        plt.savefig(file.split(".json")[0].split("/")[2]+".png")
        plt.close()


def read_reasults():

    G_10_80_0 = '../data/G_10_80_0.json'
    G_100_800_0 = '../data/G_100_800_0.json'
    G_1000_8000_0 = '../data/G_1000_8000_0.json'
    G_10000_80000_0 = '../data/G_10000_80000_0.json'
    G_20000_160000_0 = '../data/G_20000_160000_0.json'
    G_30000_240000_0 = '../data/G_30000_240000_0.json'

    G_10_80_1 = '../data/G_10_80_1.json'
    G_100_800_1 = '../data/G_100_800_1.json'
    G_1000_8000_1 = '../data/G_1000_8000_1.json'
    G_10000_80000_1 = '../data/G_10000_80000_1.json'
    G_20000_160000_1 = '../data/G_20000_160000_1.json'
    G_30000_240000_1 = '../data/G_30000_240000_1.json'

    G_10_80_2 = '../data/G_10_80_2.json'
    G_100_800_2 = '../data/G_100_800_2.json'
    G_1000_8000_2 = '../data/G_1000_8000_2.json'
    G_10000_80000_2 = '../data/G_10000_80000_2.json'
    G_20000_160000_2 = '../data/G_20000_160000_2.json'
    G_30000_240000_2 = '../data/G_30000_240000_2.json'

    files = [G_10_80_0, G_100_800_0, G_1000_8000_0, G_10000_80000_0, G_20000_160000_0, G_30000_240000_0,
             G_10_80_1, G_100_800_1, G_1000_8000_1, G_10000_80000_1, G_20000_160000_1, G_30000_240000_1,
             G_10_80_2, G_100_800_2, G_1000_8000_2, G_10000_80000_2, G_20000_160000_2, G_30000_240000_2]

    with open("./results.txt", 'r') as f:
        data = json.load(f)

    bars = {"python_load": data["Algo_load"],
            "python_shortest_p": data["Algo_sp"],
            "python_scc": data['Algo_scc'],
            "nx_load": data['networkx_load'],
            "nx_sp": data['networkx_sp'],
            "nx_scc": data['networkx_scc'],
            "java_load": data['Java_load'],
            "java_sp": data["Java_sp"],
            "java_scc": data["Java_scc"]}

    index = 0
    list_ = []

    while index is not len(bars["python_load"]):
        l = []

        for list in bars.values():
            # print(list)
            l.append(list[index])

        list_.append(l)

        index += 1

    bar_plot(list_, files, bars, total_width=.8, single_width=.9)


if __name__ == '__main__':
    read_reasults()