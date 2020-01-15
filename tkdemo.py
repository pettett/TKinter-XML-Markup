import tkml


with tkml.Window(filename="xml/tkdemo.xml") as window:
    @window.callback
    def OnButtonPress():
        print("button pressed")
        print(window.username)
        window.username = "apple"
