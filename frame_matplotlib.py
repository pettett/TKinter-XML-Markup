import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

import tkml


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
        <vertical>
            <p>This graph is embedded inside tkinter!</p>
            <matgraph ref="sinGraph" width="400" height="400" sticky="news" weight="1"/>
        </vertical>
    </tkml>
    """

    window = tkml.Window(layout)

    graph = window.elements["sinGraph"]

    t = np.arange(0, 5, .01)
    graph.fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    window.mainloop()

"""
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    MatplotlibFrame(root, bd=2, relief=tkinter.SUNKEN).pack(
        expand=1, fill="both")

    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)

    tkinter.mainloop()
    # If you put root.destroy() here, it will cause an error if the window is
<<<<<<< HEAD
    # closed with the window manager.
=======
    # closed with the window manager."""
