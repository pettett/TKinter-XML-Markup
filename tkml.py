from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

from tkelements import *
import tkmlDecoder as decode
import colorpick
import pygame_frame


class Label(Label):
    def __init__(self, master=None, **options):
        font = options.pop("font", "TkDefaultFont")
        fontSize = options.pop("fontsize", 9)
        options["font"] = (font, fontSize)
        super().__init__(master, **options)


'''#help
<head> - menu bar and title
<title> - sets title of window (default)
<menu> - starts menu bar
<cascade> - start menu in menu bar
<command> label:TEXT - add command to menu [Default - label]
<separator> - add seperator to menu
<radiobutton> value:BOOL
<checkbutton> value:BOOL
<dropdown> value:INT


// Actual TK classes

<body> minWidth:FLOAT [0] minHeight:FLOAT [0]- places widgets

<p> font:STRING fontsize:FLOAT [10]  image:STRING (file name for image) - displays text(default) or image but not both
    image can be of type gif only - idk why
<input> placeHolder:STRING [""], placeHolderColor:STRING [grey],varname:STRING - entry object that can store input in varname
<radiobutton>
<checkbutton>
<button>

<colorpick> - color picker

//list elements - default: list of choices seperated by ";"
<dropdown> click to reveil choices
<listbox> box with list of choices
<spinbox> entry with arrows for choices - kinda bad

//layout elements

<grid> rows:INT [1] columns:INT [1] creates grid object - objects inside gain tags gridx:INT [0],gridy:INT [0],gridspanx:INT [1],gridspany:INT [1]
<notebook> - maximum 10 tabs
<horizontal>
<vertical>
'''

layout = '''
<tkml>
<head>
    <title>Markup Compiler</title>
    <menu>
    <cascade label="File">

        <command>Open</command>
        <command command="onSave">Save</command>
        <separator/>
        <!--Queen Menu is here - this is a comment-->
        <cascade label="Queen">
            <command>Mummma</command>
            <separator/>
            <command command="onSave">*Guitar solo*</command>
            <cascade label="*Brum-brum*">
                <command>i just killed a maaan</command>
                <cascade label="*dum-dum*">
                    <command>Put a</command>
                    <command>gun up</command>
                    <command>to his</command>
                    <command>head</command>
                    <cascade label="*guitar*">
                        <command>pulled</command>
                        <command>the trigger</command>
                        <command>now he's</command>
                        <command>dead</command>
                    </cascade>
                </cascade>
            </cascade>
        </cascade>
    </cascade>
    <cascade label="Edit">
        <command>Cut</command>
        <separator/>
        <command>Copy</command>
        <separator/>
        <command>Paste</command>
    </cascade>

    <cascade label="RadioButtons"><radiobutton value=True>Option1</radiobutton><radiobutton>Option2</radiobutton><radiobutton>Option3</radiobutton></cascade>
    <cascade label="CheckButtons"><checkbutton value=True>Option1</checkbutton><checkbutton>Option2</checkbutton><checkbutton>Option3</checkbutton></cascade>
    <command>Exit</command>
    </menu>
</head>
<body minWidth=400 minHeight=100>
    <grid relief="sunken">
        <columnconfig column=0 weight=1></columnconfig>
        <columnconfig column=1 weight=1></columnconfig>

        <p varname="text">Enter your data:</p>

        <field varname="username" gridx=1/>

        <button command="onButtonSubmit" gridy=1 gridspanx=2 label="Enter"/>

        <checkbutton gridy=2>Check Button</checkbutton>
        <slider gridy=2 gridx=1 min=0 max=100 orient=HORIZONTAL></slider>


        <radiobutton gridy=3 value=1>Radio Option 1</radiobutton>
        <radiobutton gridy=3 gridx=1 value=0 gridx=1>Radio Option 2</radiobutton>


        <dropdown gridy=4>Option 1;Option 2;Option 3</dropdown>
        <spinbox gridy=4 gridx=1>1;2;4;8;16</spinbox>

        <colorfield gridy=5/>

        <listbox gridx=2 gridspany=6>option 1;option 2;option 3</listbox>
    </grid>

</body>
</tkml>
'''

FLOAT = "FLOAT"
INT = "INT"
STRING = "STRING"

consts = {
    "HORIZONTAL": HORIZONTAL,
    "VERTICAL": VERTICAL,
    "SINGLE": SINGLE,
    "EXTENDED": EXTENDED,
    "MULTIPLE": MULTIPLE,
    "BROWSE": BROWSE,
    "FLOAT": FLOAT,
    "INT": INT,
    "STRING": STRING
}


class Window:
    # Functions used to create the window:
    def GenerateElement(self, element, root):

        style = element.tags.pop('style', '')
        if style != '':
            # get dict of all tags accosiated with the style and include it - if tag is in style and element tags the local tag will take priority
            styleTags = self.styles[style]
            for tag in styleTags.keys():
                if tag not in element.tags:
                    element.tags[tag] = styleTags[tag]

        callback = element.tags.pop('callback', '')
        hasCallback = callback != ''

        callbackArgs = element.tags.pop('arg', [])
        if callbackArgs != []:  # temporary conversion to list because args not passed as list
            callbackArgs = [callbackArgs]

        varname = element.tags.pop("varname", "")
        hasVariable = varname != ''
        image = element.tags.pop("image", '')

        if image != '':
            image = PhotoImage(file=image)

        ref = element.tags.pop("ref", '')

        hasRef = ref != ''

        output = None

        usesStringVar = ['p', 'dropdown', 'spinbox']
        if element.name in usesStringVar:
            if varname in self.values:
                element.tags['textvariable'] = self.values[varname]
            else:
                stringVar = StringVar()
                if hasCallback:
                    stringVar.trace(
                        'w', lambda *a: self.OnCallback(callback, *callbackArgs))
                if hasVariable:
                    self.values[varname] = stringVar
                element.tags['textvariable'] = stringVar
        if element.name in self.customs:
            output = self.customs[element.name](self, root,  **element.tags)

        elif element.name == "p":
            if type(element.tags['textvariable']) is StringVar:
                element.tags['textvariable'].set(element.default)
            if element.default != '':
                element.tags['text'] = element.default
            if image == '':
                output = Label(root, **element.tags)
            else:  # set up label with image object
                imageLabel = Label(root, image=image, **element.tags)
                imageLabel.image = image  # keep reference so GC does not destroy it
                output = imageLabel

        elif element.name == "progressbar":
            # controller must have access to value and like of bar
            # functions start,stop and step up to 100%
            bar = ttk.Progressbar()

            output = bar
        elif element.name == "text":
            scrolled = element.tags.pop('scrolled', False)
            if scrolled:
                text = scrolledtext.ScrolledText(root)
            else:
                text = Text(root)
            text.insert(END, element.default)
            output = text

        elif element.name == 'seperator':
            output = ttk.Separator(root, **element.tags)

        elif element.name == "field":

            # Get type of entry - defaults to string for convience
            valueType = element.tags.pop("type", STRING)
            vartagname = 'textvariable'
            if valueType == INT:
                vartagname = 'intvariable'
            elif valueType == FLOAT:
                vartagname = 'floatvariable'

            if varname in self.values:  # already variable defined, use that
                element.tags[vartagname] = self.values[varname]

            else:  # create a new variable
                if valueType == FLOAT:
                    # setup float variable
                    variable = DoubleVar()

                elif valueType == STRING:
                    # setup string varaible
                    variable = StringVar()

                elif valueType == INT:
                    # setup int variable
                    variable = IntVar()

                if hasCallback:
                    variable.trace(
                        'w', lambda *args: self.OnCallback(callback, *callbackArgs))
                if hasVariable:
                    self.values[varname] = variable
                element.tags[vartagname] = variable

            # return the correct type
            if valueType == FLOAT:
                output = FloatField(root, **element.tags)
            elif valueType == INT:
                output = IntField(root, **element.tags)
            elif valueType == STRING:
                output = Entry(root, **element.tags)

        # custom widgets
        elif element.name == "colorfield":
            output = colorpick.ColorField(root, **element.tags)
        elif element.name == "pygameframe":
            element.tags['flags'] = element.default.split(';')
            output = pygame_frame.PygameFrame(root, **element.tags)

        elif element.name == "button":
            if element.default != "":
                element.tags['text'] = element.default
            if 'label' in element.tags:
                element.tags['text'] = element.tags.pop('label', '')
            if hasCallback:  # lambda used to pass callback name so function can be applied
                element.tags["command"] = lambda: self.OnCallback(
                    callback, *callbackArgs)

            # change to page tag will change the selected page when the button is pressed
            changeToPage = element.tags.pop('changetopage', '')
            if changeToPage != '':
                element.tags['command'] = lambda x=changeToPage: self.ChangeToPage(
                    x)

            output = Button(root, **element.tags)

        elif element.name == "canvas":
            output = Canvas(root, **element.tags)

        elif element.name == "gradient":  # inherits from canvas with function to draw gradients onto
            output = colorpick.Gradient(root, **element.tags)
        elif element.name == "checkbutton":
            if element.default != "":
                element.tags['text'] = element.default
            output = Checkbutton(root, **element.tags)

        elif element.name == "radiobutton":
            if element.default != "":
                element.tags['text'] = element.default
            var = element.tags.pop("group", "defaultgroup")
            if var not in self.values:
                self.values[var] = IntVar()
                self.values[var].trace(
                    "w", lambda: self.OnCallback(callback, *callbackArgs))
            output = Radiobutton(
                root, variable=self.values[var], **element.tags)

        elif element.name == "dropdown":
            options = element.default.split(';')
            stringVar.set(options[0])
            output = OptionMenu(root, stringVar, *options)

        elif element.name == "slider":
            element.tags['from_'] = element.tags.pop('min', 0)
            element.tags['to'] = element.tags.pop("max", 1)
            if hasVariable:
                vartype = element.tags.pop('type', FLOAT)
                if vartype == FLOAT:
                    variable = DoubleVar()
                elif vartype == INT:
                    variable = IntVar()
                defaultValue = element.tags.pop('default', min)
                variable.set(defaultValue)
                if hasCallback:
                    variable.trace(
                        'w', lambda *a: self.OnCallback(callback, *callbackArgs))
                element.tags['variable'] = variable
                self.values[varname] = variable
            output = Scale(root, **element.tags)

        elif element.name == "spinbox":
            spins = element.default.split(';')
            output = Spinbox(root, values=spins, **element.tags)

        elif element.name == "listbox":
            options = element.default.split(';')
            # if user wants scrollbar link scrollbar object to list events

            box = Listbox(root, **element.tags)
            for option in options:
                box.insert(END, option)
            output = box

        elif element.name == 'autogrid':
            # autogrid simply needs childs attached to it to work
            output = AutoGrid(root, **element.tags)
            for child in element.children:
                output.AddChildToGrid(self.GenerateElement(child, output))
            output.UpdateItemGrid(50)

        elif element.name == 'grid':
            output = self.GenerateChildrenInGrid(element)
        elif element.name == "horizontal":
            output = self.GenerateHorizontalLayout(element, root=root)
        elif element.name == "vertical":
            output = self.GenerateVerticalLayout(element, root=root)
        elif element.name == "notebook":
            output = self.GenerateNotebook(element, root=root)
        if hasRef:
            self.elements[ref] = output
        return output

    def GenerateChildren(self, parent, root):
        for element in parent.children:

            if element.name == "title":
                self.title = self.root.title(element.default)
            elif element.name == "style":
                self.AddStyle(element)
            elif element.name == "body" or element.name == "head":
                widgets = self.GenerateChildren(element, root)
                if element.name == "body":
                    minWidth = element.tags.pop('minWidth', 0)
                    minHeight = element.tags.pop('minHeight', 0)
                    self.root.minsize(minWidth, minHeight)
                for widget in widgets:
                    yield widget
            elif element.name == "menu":
                self.GenerateMenuBar(element, root)
            else:
                widget = self.GenerateElement(element, root)
                widget.grid(sticky=N+S+W+E)
                yield widget

    def AddStyle(self, style):
        # style always needs a reference to be used by other elements
        ref = style.tags.pop('ref', '')
        if ref == '':
            raise Exception('Style has no reference')
        self.styles[ref] = style.tags

    def GenerateChildrenInGrid(self, grid):
        label = grid.tags.pop('label', '')
        defaultColumnWeight = grid.tags.pop('defaultcolumnweight', 0)
        defaultRowWeight = grid.tags.pop('defaultrowweight', 0)

        if label == '':
            gridFrame = Frame(self.root, **grid.tags)
        else:
            grid.tags['text'] = label
            gridFrame = LabelFrame(self.root, **grid.tags)

        columns = 1
        configuredColumns = []
        rows = 1
        configuredRows = []

        for element in grid.children:
            if element.name == 'rowconfig':
                row = element.tags.pop('row', 0)
                configuredRows.append(row)
                gridFrame.columnconfigure(row, element.tags)
            elif element.name == 'columnconfig':
                column = element.tags.pop("column", 0)
                configuredColumns.append(column)
                gridFrame.columnconfigure(column, element.tags)
            else:
                gridX = element.tags.pop("gridx", 0)
                gridY = element.tags.pop("gridy", 0)
                pady = element.tags.pop("pady", 0)
                padx = element.tags.pop("padx", 0)
                if gridX > columns:
                    columns = gridX  # If this row or column is the biggest
                if gridY > rows:  # update the value so all unconfiged
                    rows = gridY  # zones can be defaulted
                stick = element.tags.pop('sticky', 'wen')
                gridSpanX = element.tags.pop("gridspanx", 1)
                gridSpanY = element.tags.pop("gridspany", 1)

                generated = self.GenerateElement(element, gridFrame)
                generated.grid(row=gridY,
                               column=gridX,
                               rowspan=gridSpanY,
                               columnspan=gridSpanX,
                               sticky=stick, padx=padx, pady=pady)

        for row in range(rows+1):  # set defaults
            if row not in configuredRows:
                gridFrame.rowconfigure(row, weight=defaultRowWeight)
        for column in range(columns+1):
            if column not in configuredColumns:
                gridFrame.columnconfigure(column, weight=defaultColumnWeight)
        gridFrame.grid(sticky=W+E+N+S)
        return gridFrame

    def GenerateMenuBar(self, menubar, root):  # menubar - element
        menubarWidget = Menu(root, tearoff=0)

        for item in menubar.children:
            if item.name == "cascade":  # create submenus within the menu
                self.GenerateMenuBar(item, root=menubarWidget)
            elif item.name == "separator":
                menubarWidget.add_separator()
            elif item.name == "command":
                function = item.tags.pop('command', '')
                if function != '':
                    item.tags['command'] = lambda f=function: self.OnCallback(
                        f)

                menubarWidget.add(item.name, label=item.default, **item.tags)
            else:
                boolVar = BooleanVar()
                value = item.tags.pop("value", True)
                boolVar.set(value)

                menubarWidget.add(item.name, label=item.default)

        if root == self.root:
            self.root.config(menu=menubarWidget)
        else:
            root.add_cascade(
                label=menubar.tags['label'], menu=menubarWidget, underline=0)

    def GenerateNotebook(self, notebook, root):
        # Make each child of notebook object their own page
        # return the notebook object so it can be used elsewhere
        widget = ttk.Notebook(root)
        for index, child in enumerate(notebook.children):
            tabName = child.tags.pop("tabname", "Tab {0}".format(index+1))
            tabFrame = Frame(widget)
            tabFrame.rowconfigure(0, weight=1)
            tabFrame.columnconfigure(0, weight=1)
            element = self.GenerateElement(child, root=tabFrame)
            element.grid(sticky='NSEW')
            widget.add(tabFrame, text=tabName)
        return widget

    def GenerateVerticalLayout(self, vertical, root):

        scrolled = vertical.tags.pop("scrolled", False)

        frameWidget = Frame(root)

        frameWidget.columnconfigure(0, weight=1)
        for index, child in enumerate(vertical.children):
            self.AddChildToVerticalLayout(child, index, frameWidget)
        return frameWidget

    def AddChildToVerticalLayout(self, child, index, parent):
        stick = child.tags.pop("sticky", N+E+W+S)
        pady = child.tags.pop("pady", 0)
        padx = child.tags.pop("padx", 0)
        weight = child.tags.pop("weight", 0)
        parent.rowconfigure(index, weight=weight)
        childWidget = self.GenerateElement(child, parent)
        childWidget.grid(row=index, sticky=stick, pady=pady, padx=padx)

    def GenerateHorizontalLayout(self, horizontal, root=None):
        if root == None:
            root = self.root  # same as vertical but set coumn not row
        frameWidget = Frame(root)
        frameWidget.rowconfigure(0, weight=1)
        for index, child in enumerate(horizontal.children):
            stick = child.tags.pop("sticky", N+E+W+S)
            pady = child.tags.pop("pady", 0)
            padx = child.tags.pop("padx", 0)
            weight = child.tags.pop("weight", 1)
            frameWidget.columnconfigure(index, weight=weight)
            childWidget = self.GenerateElement(child, root=frameWidget)
            childWidget.grid(column=index, row=0,
                             sticky=stick, pady=pady, padx=padx)
        return frameWidget

    def OnCallback(self, name, *args):
        if name in self.callbacks:
            self.callbacks[name](*args)

    def __init__(self, tkml, root=None, pages={}, customClasses={}):
        """Create A TKML Window"""
        # compile tkml to elements
        pages['root'] = tkml

        self.customs = customClasses
        # Element('tkml', tkml).children[0]

        self.values = {}
        self.callbacks = {}
        self.elements = {}
        self.styles = {}

        if root == None:
            self.root = Tk()
        else:
            self.root = root

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        for item in pages.keys():
            markup = pages[item]
            rootElement = decode.Decode(markup)

            rootWidget = next(self.GenerateChildren(rootElement, self.root))

            rootWidget.grid(column=0, row=0)
            pages[item] = rootWidget

        self.pages = pages
        self.pages['root'].tkraise()

    def ChangeToPage(self, page):
        # functions avalible to start the window
        self.pages[page].tkraise()

    def mainloop(self):
        self.root.mainloop()

    def AppendElements(self, tkml, parent):
        """Adds an element to a vertical element group"""
        # TODO Allow this to work on all widget tpyes, not just vertical

        rootElement = decode.Decode(tkml)
        if rootElement.name == 'body':  # if only one element needs to be added the compiler dies :(
            # temporary fix to this by wrapping the object in the body tag before compiling
            rootElement = rootElement.children[0]
        childIndex = len(parent.children.values())

        self.AddChildToVerticalLayout(rootElement, childIndex, parent)


if __name__ == '__main__':
    window = Window(layout)
    window.mainloop()
