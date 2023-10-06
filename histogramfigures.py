from matplotlib.figure import Figure

def create_histogram_figure(histogram: dict, title: str, y_label: str) -> Figure:
    letters = histogram.keys()
    frequency = histogram.values()

    figure = Figure(figsize=(4, 4), dpi=100)
    axes = figure.add_subplot()
    axes.bar(list(letters), list(frequency))
    axes.set_title(title)
    axes.set_ylabel(y_label)

    return figure

def update_histogram_figure(figure: Figure, histogram: dict, title: str = None, ylabel: str = None):
    axes = figure.get_axes()[0]

    current_title = axes.title.get_text()
    current_ylabel = axes.yaxis.get_label().get_text()

    axes.clear()
    axes.bar(list(histogram.keys()), list(histogram.values()))

    axes.set_title(title if title else current_title)
    axes.set_ylabel(ylabel if ylabel else current_ylabel)