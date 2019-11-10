from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext


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
        <separator></separator>

    </cascade>
    <cascade label="Edit">
        <command>Cut</command>
        <separator></separator>
        <command>Copy</command>
        <separator></separator>
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

        <input varname="username" gridx=1></input>

        <button command="onButtonSubmit" gridy=1 gridspanx=2 text="Enter"></button>

        <checkbutton gridy=2>Check Button</checkbutton>
        <slider gridy=2 gridx=1 min=0 max=100 orient=HORIZONTAL></slider>


        <radiobutton gridy=3 value=1>Radio Option 1</radiobutton>
        <radiobutton gridy=3 gridx=1 value=0 gridx=1>Radio Option 2</radiobutton>


        <dropdown gridy=4>Option 1;Option 2;Option 3</dropdown>
        <spinbox gridy=4 gridx=1>1;2;4;8;16</spinbox>


        <listbox gridx=2 gridspany=5>option 1;option 2;option 3</listbox>
    </grid>

</body>
</tkml>
'''

currentElement = ""

consts = {
    "HORIZONTAL":HORIZONTAL,
    "VERTICAL":VERTICAL,
    "SINGLE":SINGLE,
    "EXTENDED":EXTENDED,
    "MULTIPLE":MULTIPLE,
    "BROWSE":BROWSE
}



def ReadTags(tagsString): #return name, dictionary of tags:tags value
    tagsList = tagsString.split(' ')
    # seperate out tags
    name = tagsList[0]
    tagsDict = {}  # Each tag is stored in a pair TAGNAME=VALUE
    
    for i in range(1, len(tagsList)):
        tag = tagsList[i].split('=')
        try:
            if tag[1] in consts:
                tag[1] = consts[tag[1]]
            elif (tag[1].find('"') != -1):  # string value
                tag[1] = tag[1][1:-1]
            elif tag[1][-1] == 'f':  # float value
                tag[1] = float(tag[1][0:-1])
            elif tag[1].lower() == "false" or tag[1].lower() == "true":  # boolean
                tag[1] = tag[1].lower() == "true"
            else:  # int value
                tag[1] = int(tag[1])

            tagsDict[tag[0]] = tag[1]
        except:
            raise Exception("incorrect tags in {0}".format(tagsString))
    return name, tagsDict

class Element:

    def CompileTKML(self, html):  # TODO Add support for nested objects - cascade within cascade
        elements = []
        ended = False
        workingString = html
        searchingForEnd = []
        while ended == False:
            startBrocket = workingString.find('<')
            endTagsBrocket = workingString.find('>')

            if startBrocket == -1:
                ended = True
            else:
                name, tagsDict =ReadTags( workingString[startBrocket+1:endTagsBrocket])

                #find next open brocket after end



                targetEndTag = "</{0}>".format(name)
                startTerminatorBrocket = workingString.find(targetEndTag)

                if startTerminatorBrocket == -1:
                    ended = True
                else:
                    defaultTag = workingString[endTagsBrocket +
                                               1:startTerminatorBrocket]

                    workingString = workingString[startTerminatorBrocket +
                                                  len(targetEndTag):]

                    elements.append(Element(name, defaultTag, **tagsDict))
        return elements

            


    def __init__(self, name, defaultTag, **kwargs):
        self.name = name
        self.default = defaultTag
        self.tags = kwargs
        self.children = []
        # compile chilren code
        canCompile = [
            'tkml', 'body', 'head', 'grid',"vertical",
            "horizontal",'notebook', "menu", "cascade"]
        for item in canCompile:
            if item in name:
                self.children = self.CompileTKML(defaultTag)





class Window:
    def GenerateElement(self, element, root=None):
        if root == None:
            root = self.root

        callback = element.tags.pop('callback','')
        hasCallback = callback != ''
        varname= element.tags.pop("varname", "")
        hasVariable = varname != ''
        image = element.tags.pop("image",'')
        if image != '':
            image = PhotoImage(file=image)

        usesStringVar = ['p','input','dropdown','spinbox']
        if element.name in usesStringVar:
            stringVar = StringVar()
            if hasCallback:
                stringVar.trace('w',lambda *args: self.OnCallback(callback,*args))
            if hasVariable:
                self.textVars[varname] = stringVar
            element.tags['textvariable'] = stringVar

        if element.name == "p":
            stringVar.set(element.default)
            if image == '':
                return Label(root, text=element.default, **element.tags)
            else:#set up label with image object
                imageLabel = Label(root,image=image, text=element.default, **element.tags)
                imageLabel.image = image #keep reference so GC does not destroy it
                return imageLabel

        elif element.name== "progressbar":
            #controller must have access to value and like of bar
            #functions start,stop and step up to 100%
            bar = ttk.Progressbar()
            
            return bar
        elif element.name == "text":
            scrolled = element.tags.pop('scrolled',False)
            if scrolled:
                text = scrolledtext.ScrolledText(root)
            else:
                text = Text(root)
            text.insert(END,element.default)
            return text
        elif element.name == "input":
            return Entry(root, **element.tags)

        elif element.name == "button":
            if element.default != "":
                element.tags['text'] = element.default
            if hasCallback:
                element.tags["command"] = lambda: self.OnCallback(callback)
            return Button(root, **element.tags)

        elif element.name=="checkbutton":
            if element.default != "":
                element.tags['text'] = element.default
            return Checkbutton(root,**element.tags)

        elif element.name=="radiobutton":
            if element.default != "":
                element.tags['text'] = element.default
            var = element.tags.pop("group","defaultgroup")
            if var not in self.intVars:
                self.intVars[var] = IntVar() 
                self.intVars[var].trace("w",lambda *args: self.OnCallback(var))
            return Radiobutton(root,variable=self.intVars[var],**element.tags)
        
        elif element.name == "dropdown":
            options = element.default.split(';')
            stringVar.set(options[0])
            return OptionMenu(root,stringVar,*options)

        elif element.name == "slider":
            element.tags['from_'] = element.tags.pop('min',0)
            element.tags['to'] = element.tags.pop("max",1)
            if hasVariable:
                doubleVar = DoubleVar()
                if hasCallback:
                    doubleVar.trace('w',lambda *args: self.OnCallback(callback))
                element.tags['variable'] = doubleVar
                self.textVars[varname] = doubleVar
            return Scale(root,**element.tags)
        
        elif element.name == "spinbox":
            spins = element.default.split(';')

            return Spinbox(root,values=spins,**element.tags)

        elif element.name == "listbox":
            options = element.default.split(';')
            #if user wants scrollbar link scrollbar object to list events

            box = Listbox(root,**element.tags)
            for option in options:
                box.insert(END,option)
            return box
        elif "grid" in element.name:
            return self.GenerateChildrenInGrid(element)
        elif element.name == "horizontal":
            return self.GenerateHorizontalLayout(element,root=root)
        elif element.name == "vertical":
            return self.GenerateVerticalLayout(element,root=root)
        elif element.name == "notebook":
            return self.GenerateNotebook(element,root=root)

    def GenerateChildren(self, parent):
        for element in parent.children:

            if element.name == "title":
                self.title = self.root.title(element.default)

            elif element.name == "body" or element.name == "head":
                self.GenerateChildren(element)
                if element.name == "body":
                    minWidth = element.tags.pop('minWidth', 0)
                    minHeight = element.tags.pop('minHeight', 0)
                    self.root.minsize(minWidth, minHeight)
            elif element.name == "menu":
                self.GenerateMenuBar(element)
            else:
                widget = self.GenerateElement(element)
                widget.grid(sticky=N+S+W+E)

    def GenerateChildrenInGrid(self, grid):
        label = grid.tags.pop('label','')
        defaultColumnWeight = grid.tags.pop('defaultcolumnweight',0)
        defaultRowWeight=grid.tags.pop('defaultrowweight',0)

        if label == '':
            gridFrame = Frame(self.root, **grid.tags)
        else:
            grid.tags['text'] = label
            gridFrame = LabelFrame(self.root,**grid.tags)

        columns=1
        configuredColumns = []
        rows=1
        configuredRows = []

        for element in grid.children:
            if element.name == 'rowconfig':
                row=element.tags.pop('row',0)
                configuredRows.append(row)
                gridFrame.columnconfigure(row,element.tags)
            elif element.name == 'columnconfig':
                column=element.tags.pop("column",0)
                configuredColumns.append(column)
                gridFrame.columnconfigure(column,element.tags)
            else:
                gridX = element.tags.pop("gridx", 0)
                gridY = element.tags.pop("gridy", 0)
                if gridX > columns:
                    columns = gridX #If this row or column is the biggest
                if gridY > rows: # update the value so all unconfiged
                    rows = gridY #zones can be defaulted
                stick = element.tags.pop('sticky','wen')
                gridSpanX = element.tags.pop("gridspanx", 1)
                gridSpanY = element.tags.pop("gridspany", 1)

                generated = self.GenerateElement(element, gridFrame)
                generated.grid(row=gridY,
                            column=gridX,
                            rowspan=gridSpanY,
                            columnspan=gridSpanX,
                            sticky=stick)
        
        for row in range(rows+1): # set defaults
            if row not in configuredRows:
                gridFrame.rowconfigure(row,weight=defaultRowWeight)
        for column in range(columns+1):
            if column not in configuredColumns:
                gridFrame.columnconfigure(column,weight=defaultColumnWeight)
        gridFrame.grid(sticky=W+E+N+S)
        return gridFrame

    def GenerateMenuBar(self, menubar, root=None):  # menubar - element
        if root == None:
            root = self.root

        menubarWidget = Menu(root, tearoff=0)

        for item in menubar.children:
            if item.name == "cascade":  # create submenus within the menu
                self.GenerateMenuBar(item, root=menubarWidget)
            elif item.name == "separator":
                menubarWidget.add_separator()
            elif item.name == "command":
                function = item.tags.pop('command','')
                if function != '': 
                    item.tags['command'] = lambda:self.OnCallback(function)
                menubarWidget.add(item.name, label=item.default,**item.tags)
            else:
                boolVar = BooleanVar()
                value = item.tags.pop("value",True)
                boolVar.set(value)
                
                menubarWidget.add(item.name, label=item.default)
                


        if root == self.root:
            self.root.config(menu=menubarWidget)
        else:
            root.add_cascade(
                label=menubar.tags['label'], menu=menubarWidget, underline=0)

    def GenerateNotebook(self,notebook,root=None):
        #Make each child of notebook object their own page
        #return the notebook object so it can be used elsewhere
        if root == None:
            root = self.root
        widget = ttk.Notebook(root)
        for index,child in enumerate(notebook.children) :
            tabName = child.tags.pop("tabname","Tab {0}".format(index+1))
            tabFrame = Frame(widget)
            tabFrame.rowconfigure(0,weight=1)
            tabFrame.columnconfigure(0,weight=1)
            element = self.GenerateElement(child,root=tabFrame)
            element.grid(sticky='NSEW')
            widget.add(tabFrame,text= tabName)
        return widget

    def GenerateVerticalLayout(self,vertical,root=None):
        if root==None:root=self.root
        frameWidget = Frame(root)
        
        frameWidget.columnconfigure(0,weight=1)
        for index, child in enumerate(vertical.children):
            stick = child.tags.pop("sticky",N+E+W+S)
            weight= child.tags.pop("weight",0)
            frameWidget.rowconfigure(index,weight=weight)
            childWidget = self.GenerateElement(child,root=frameWidget)
            childWidget.grid(row=index, sticky=stick)
        return frameWidget

    def GenerateHorizontalLayout(self,horizontal,root=None):
        if root==None:root=self.root # same as vertical but set coumn not row
        frameWidget = Frame(root)
        for index, child in enumerate(horizontal.children):
            frameWidget.columnconfigure(index,weight=1)
            childWidget = self.GenerateElement(child,root=frameWidget)
            childWidget.grid(column=index,row=0, sticky=N+E+S+W)
        return frameWidget
    def OnCallback(self,name,*args):
        if name in self.callbacks:
            self.callbacks[name]()

    def __init__(self, tkml):
        #compile tkml to elements
        root = Element('tkml', tkml).children[0]
        
        self.textVars = {}
        self.intVars = {}
        self.callbacks={}

        self.root = Tk()
        
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.GenerateChildren(root)

    def mainloop(self):
        self.root.mainloop()



if __name__ == '__main__':
    window = Window(layout)
    window.mainloop()
