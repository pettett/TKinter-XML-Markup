from tkinter import *
import os

class FileField(Frame):
    def __init__(self,window,root,**args):
        self.selectFolder = bool( args.pop("selectfolder",False))
        self.window = window
        self.callback = args.pop("onselect",None)
        text = args.pop("text","Selet")
        self.dialogArgs = args
        super().__init__(root)
        self.button = Button(self,text=text,command=self.OnButtonPressed)
        self.button.pack(expand=1,fill="y")
        
    def OnButtonPressed(self):
        if self.selectFolder:
            self.filename = filedialog.askdirectory(**self.dialogArgs)
        else:
            self.filename = filedialog.askopenfilename(**self.dialogArgs)
        if self.callback != None:
            self.window.OnCallback(self.callback)


if __name__ == "__main__":
    root = Tk()

    file = FileField(root,OnFileSelected)
    file.pack()

    label = Label()
    label.pack()

    file.OnButtonPressed()

    root.mainloop()
    
