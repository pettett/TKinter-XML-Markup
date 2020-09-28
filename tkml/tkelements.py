from tkinter import *


class ScrollRegion(Frame):
    def OnMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.OnMouseWheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def __init__(self, root, **tags):
        super().__init__(root, **tags)
        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)

        self.frame.bind("<Configure>", self.OnFrameConfigure)
        self.myscrollbar = Scrollbar(
            self, orient="vertical", command=self.canvas.yview)
        self.canvas.pack(side="left", fill='both', expand=1)
        self.myscrollbar.pack(side="right", fill="y")

        self.canvasFrame = self.canvas.create_window(
            (0, 0), window=self.frame, anchor='nw')

        self.canvas.bind('<Leave>', self._unbound_to_mousewheel)
        self.canvas.bind('<Configure>', self.FrameWidth)
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        self.canvas.bind('<Enter>', self._bound_to_mousewheel)

    def FrameWidth(self, event):
        self.canvas.itemconfig(self.canvasFrame, width=event.width)

    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class AutoGrid(Frame):

    def AddChildToGrid(self, child):
        self.allFrameWidgets.append(child)

    def __init__(self, root, **tags):
        super().__init__(root, relief=GROOVE, width=50, height=100, bd=1)

        self.allFrameWidgets = []

        self.prevColumns = 0
        self.minColumnWidth = 200
        self.maxColumns = 15

        self.bind('<Configure>', self.FrameWidth)

    def FrameWidth(self, event):
        self.UpdateItemGrid(event.width)

    def UpdateItemGrid(self, width):
        avalibleColumns = max(
            min(width//self.minColumnWidth, self.maxColumns, len(self.allFrameWidgets)), 1)
        if avalibleColumns != self.prevColumns:
            # Re-calculate the weights of the columns
            for i in range(self.maxColumns):
                if i < avalibleColumns:
                    self.columnconfigure(i, weight=1)
                else:
                    self.columnconfigure(i, weight=0)
            # re - distrobute the positions of the child widgets
            for index, item in enumerate(self.allFrameWidgets):
                gridY = index//avalibleColumns
                gridX = index % avalibleColumns
                item.grid_configure(row=gridY, column=gridX)
            self.prevColumns = avalibleColumns


class FloatField(Entry):
    def __init__(self, master, **kwd):
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')  # register custom validation command to have access to all variables
        self.floatVar = kwd.pop("floatvariable", None)
        super().__init__(master, validate="key", validatecommand=vcmd, **kwd)

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            # int casts allow spaces at start or end of string, do not allow this
            if value_if_allowed == prior_value + " " or value_if_allowed == " " + prior_value:
                return False
            try:
                float(value_if_allowed)
                # from this point float is good, update float var
                if self.floatVar != None:
                    self.floatVar.set(float(value_if_allowed))
                return True
            except ValueError:
                return False
        else:
            return False


class IntField(Entry):
    def __init__(self, master, **kwd):
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')  # register custom validation command to have access to all variables
        self.intVar = kwd.pop("intvariable", None)
        super().__init__(master, validate="key", validatecommand=vcmd, **kwd)

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            # int casts allow spaces at start or end of string, do not allow this
            # Find the character that was added to test if it is valid
            if " " in value_if_allowed:
                return False
            if "." in value_if_allowed:
                return False
            try:
                int(value_if_allowed)
                # from this point value is good, update intvar
                if self.intVar != None:
                    self.intVar.set(int(value_if_allowed))
                return True
            except ValueError:
                return False
        else:
            return False


if __name__ == "__main__":
    import tkml
    import tkviewport

    class CustomFrame(Frame):

        def ElementPressed(self):
            pass

        def __init__(self, window, root, **tags):
            name = tags.pop('label', 'New Item')
            callback = tags.pop('command', '')
            changetopage = tags.pop('changetopage', '')
            index = int(tags.pop('index', 0))
            clearCol = tuple([int(x)
                              for x in tags.pop('bg', '1,1,1').split(',')])
            speed = float(tags.pop('speed', 1))

            if callback == '' and changetopage == '':
                self.callback = self.ElementPressed
            elif changetopage != '':
                self.callback = lambda: window.ChangeToPage(changetopage)
            elif callback != '':

                self.callback = lambda: window.OnCallback(
                    callback, index)

            super().__init__(root, height=1, bd=3, relief=GROOVE)
            label = Label(self, text=name)
            images = 2

            #imageName = "image{0}.gif".format(index % images)
            '''
            photo = PhotoImage(file=imageName)
            image = Label(self, image=photo, height=100)
            image.photo = photo
            image.pack()'''
            viewport = tkviewport.CubePreview(
                self, height=300, width=200, speed=speed, clearCol=clearCol)
            label.grid()
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            viewport.grid(row=1, sticky='nsew')

            button = Button(self, text='Go', command=self.callback)
            button.grid(row=2, sticky="ew")

            self.grid(stick="ew", pady=5, padx=5)

    def ElementPressed(index, event):
        print('element {} pressed'.format(index))
        if index == 1:
            # george frame
            georgeWindow.root.tkraise()
        else:
            harryWindow.root.tkraise()

    def Back():
        autoGrid.tkraise()

    harryMarkup = '''
    <vertical>
    <p fontsize=20>Harry</p>
    <p>Yeet</p>
    <button callback="back" label="Back"/>
    </vertical>
    '''
    georgeMarkup = '''
    <vertical>
    <p fontsize=20>George</p>
    <p>Eh.</p>
    <button callback="back" label="Back"/>
    </vertical>
    '''

    # Class tag will make custom class be used. all tags after this will be sent to the targeted class
    FirstLayerMarkup = '''
    <body>
    <vertical>
    <p>The is page 1!</p>
    <autogrid>
    <CustomFrame changetopage="Items" label="Items" index="0" speed="1" bg="1,1,0"/>
    <CustomFrame command='test' label="Blocks" index="1" speed="-1" bg="1,0,1"/>
    <CustomFrame command='test' label="Blocks" index="1" speed="-2" bg="0,0,1"/>
    <CustomFrame command='test' label="Blocks" index="1" speed="2" bg="0,1,0"/>
    </autogrid>
    </vertical>
    </body>
    '''

    def Test(x):
        print(x)

    '''<autogrid>
    <custom changetopage="Items" class="selectionPreview" name="Items"/>
    <custom changetopage="Blocks" class="selectionPreview" name="Blocks"/>
    </autogrid>'''

    # TODO - allow page change on press

    itemsGridMarkup = '''
    <body>
    <vertical>
    <p>The is page 2!</p>
    <button changetopage="root" label="Back"/>
    </vertical>
    </body>
    '''

    blocksGridMarkup = '''
    <body>
    <vertical>
    <p>The is page 3</p>
    <button changetopage="root" label="Back"/>
    </vertical>
    </body>
    '''

    pages = {
        'Items': itemsGridMarkup,
        'Blocks': blocksGridMarkup
    }

    window = tkml.Window(FirstLayerMarkup,pages= pages,generate=False)

    window.custom(CustomFrame)

    window.GenerateWindow()
    
    window.callbacks['test'] = Test
    window.mainloop()

    root = Tk()
    sizex = 800
    sizey = 600
    posx = 100
    posy = 100
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

    harryWindow = tkml.Window(harryMarkup, Frame(root))
    georgeWindow = tkml.Window(georgeMarkup, Frame(root))

    harryWindow.callbacks['back'] = Back
    georgeWindow.callbacks['back'] = Back

    autoGrid = AutoGrid(root, onElementPressed=ElementPressed)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    harryWindow.root.grid(column=0, row=0, sticky='nsew')
    georgeWindow.root.grid(column=0, row=0, sticky='nsew')
    autoGrid.grid(column=0, row=0, sticky='nsew')

    root.mainloop()
