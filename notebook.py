import tkml.tkml


with tkml.Window(filename="xml/notebook.xml") as window:
    @window.callback
    def OnFloatChange(*args):
        print("float changed to {}".format(window.floatvalue))

    @window.callback
    def OnIntChange(*args):
        print("int changed to {}".format(window.intvalue))
