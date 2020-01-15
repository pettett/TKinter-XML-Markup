import tkml
# simple test ui featuring every element.
# when every element is changed a message will be written to console


with tkml.Window(filename="xml/textUI.xml") as window:
    @window.callback
    def ButtonOnePressed():
        print("Button one pressed")
