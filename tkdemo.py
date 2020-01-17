from tkml import *

with Window(filename="xml/tkdemo.xml") as window:

    @window.callback
    def OnButtonPress():
        print("button pressed")

    @window.callback
    def OnSave():
        print("Saved!")
