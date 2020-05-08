# TKML
TKInter for python ui really is kinda bad, so I made this. Uses standard xml markup to map text to tkinter widgets, with support for adding custom widgets and using Textvar and other linked variables as normal python variables.
Custom attributes are labelled below, however all default tkinter args are supported within the attributes, dispite not being labeled below. For example `relief="sunken"` on a frame such as grid or vertical would act the same as a normal tkinter frame
#### Area organisers
* `<tkml></tkml>` Start and end of the xml file structure for the document
* `<head></head>` Area for xml related to the top tool bar
* `<body>` Main frame
  * `minWidth="400"` minimum window width
  * `minHeight="400"` minimum window height
#### Toolbar widgets
* `<cascade></cascade>` Toolbar cascade - items within the cascade should be placed as children
  * `label="file"` name of cascade
* `<seperator>` Toolbar seperator
* `<command>` Toolbar command 
  * `command="OnSave"` event function to call on pressed 
  * `keybind="*Control-s*"` tkinter binding to place on command
#### Frame layouts
* `<grid>` tkinter grid layout
  * `<grid.columnconfig>` tkinter column configuration
    * `column="0"` column index
    * `weight="1"` column weight
  * `gridy="0"` Children of the grid can use this attribute to change their grid column
  * `gridx="0"` Children of the grid can use this attribute to change their grid row
* `<vertical></vertical>` automatically creates a tkinter grid to place children in a vertical list
* `<horizontal></horizontal>` automatically creates a tkinter grid to place children in a vertical list
#### tkinter Widgets
* `<p>Hello!</p>` tkinter label
  * `varname="text"` Variable name of text in the label
* `<field>` tkinter entry
  * `varname="entry"` Variable name of text in the entry
* `<floatfield>` custom tkinter entry that only accepts floating point entries
* `<intfield>` custom tkinter entry that only accepts intager entries
* `<button>Enter</button>` tkinter button
* `<checkbutton>Check Button</checkbutton>`
* `<slider min="0" max="100" orient="horizontal">`
* `<radiobutton>Radio Option 1</radiobutton>`
  * `varname="radioGroup1"` Intager variable of selected button - buttons within a group should have the same varname
  * `value="1"` starting value
* `<dropdown>Option 1;Option 2;Option 3</dropdown>` tkinter Dropdown box - different elements should be seperated by ; ,as should other elements in widgets that input a list
* `<spinbox>1;2;4;8;16</spinbox>` tkinter spinbox
* `<notebook></notebook>` Each child of the notebook will act as a seperate frame, so children are recommended to be frame types such as grid or vertical
  * `tabname="New Tab!"` Children of the notebook can use this to change the title of their tab
* `<text>Default text</text>` tkinter Multiline text editor
* `<scrolledtext>Default text</scrolledtext>` tkinter Multiline text editor with auto scroll bar
#### Styles
* `<style/>` Style object to set re-occuring args of widgets
  * `ref="title"` Name of the style
    * `style="title"` Set the style of any element with this attribute (Not to be used within the style object)
  * `font.size="16"` Font size (Can also be used in any element with text)
  * `font.family="Arial"` Font family (Can also be used in any element with text)
  * `font.bold="false"` Font bold (Can also be used in any element with text)
  * `font.italic="True"` Font italic (Can also be used in any element with text)
  * `font.underline="True"` Font underline (Can also be used in any element with text)
  * `font.overstrike="False"` Font overstrike (Can also be used in any element with text)
  * `fg="SystemHighlight"` Any tkinter arg can be applied in a style object (Setting the foreground colour here as an example)
#### Custom Widgets
Example: `tkml.TKMLElement("pygameframe", PygameFrame, hasFont=False)` is used in pygame_frame.py to add the custom widget `"<pygameframe>"` using class PygameFrame.
Use this to add complex custom tk elements while still retaining the simplicity of tkml
