import tkml


with open("demoxml/notebook.xml") as f:
    window = tkml.Window(f.read())

@window.callback
def OnFloatChange(*args):
    print("float changed to {}".format(window.floatvalue.get()))
@window.callback
def OnIntChange(*args):
    print("int changed to {}".format(window.intvalue.get()))
window.mainloop()
