import tkml
# simple test ui featuring every element.
# when every element is changed a message will be written to console


window = tkml.Window(filename="xml/textUI.xml")


@window.callback
def ButtonOnePressed():
    print("Button one pressed")


window.mainloop()
