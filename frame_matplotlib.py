import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

import tkml.tkml


class MatplotlibFrame(tkinter.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.fig = Figure(figsize=(5, 4), dpi=100)

        # A tk.DrawingArea.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)

    def on_key_press(self, event):
        key_press_handler(event, self.canvas, self.toolbar)


tkml.TKMLElement("matgraph", MatplotlibFrame, hasFont=False)


if __name__ == "__main__":

    layout = """
    <tkml>
        <horizontal>
            <matgraph ref="sinGraph" width="400" height="400" sticky="news" weight="1"/>
            <vertical>
                <p>Number of points</p>
                <intfield varname="pointCount">20</intfield>
                <button callback="RandomizePoints" keybind="*Return*">Randomize!</button>
                <p>Random Mode:</p>
                <dropdown varname="randomMode">Random;Binomial</dropdown>
            </vertical>
        </horizontal>
    </tkml>
    """

    with tkml.Window(layout) as window:
        @window.callback
        def RandomizePoints():
            if window.randomMode == "Random":
                # generate a load of random points
                x = np.random.uniform(
                    low=0, high=10, size=window.pointCount)
                y = np.random.uniform(
                    low=0, high=10, size=window.pointCount)
            elif window.randomMode == "Binomial":
                n = 2000
                bi = np.random.binomial(n=n, p=0.2, size=window.pointCount)
                x = np.arange(300, 500, 1)
                y = [sum(bi == v)/n for v in x]

            plt.clear()

            plt.scatter(x, y, color="r")

            graph.canvas.draw()

        graph = window.elements["sinGraph"]

        plt = graph.fig.add_subplot(111)

        x = np.random.uniform(
            low=0, high=10, size=window.pointCount)
        y = np.random.uniform(
            low=0, high=10, size=window.pointCount)
        sct = plt.scatter(x, y, color="r")
