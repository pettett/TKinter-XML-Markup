from tkml import *

with Window(filename="xml/tkdemo.xml") as window:

    @window.callback
    def OnButtonPress():
        print("button pressed, Option menu: {}, Radio Buttons: {}".format(window.optionBox,
                                                                          window.radioGroup1))

    @window.callback
    def OnSave():
        print("Saved!")
