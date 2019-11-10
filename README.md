# TKML


## Head Elements
#### head 
menu bar and title 
#### title 
sets title of window (default)
#### menu 
starts menu bar
#### cascade 
start menu in menu bar
#### command 
label:TEXT - add command to menu [Default - label]
#### separator 
add seperator to menu
#### radiobutton 
value:BOOL
#### checkbutton 
value:BOOL
#### dropdown
value:INT


## Actual TK classes

#### body minWidth:FLOAT [0] minHeight:FLOAT [0]- places widgets

#### p 
font:STRING fontsize:FLOAT [10]  image:STRING (file name for image) - displays text(default) or image but not both
    image can be of type gif only - idk why
#### input 
placeHolder:STRING [""], placeHolderColor:STRING [grey],varname:STRING - entry object that can store input in varname
#### radiobutton
#### checkbutton
#### button

##list elements - default: list of choices seperated by ";"
#### dropdown 
click to reveil choices 
#### listbox 
box with list of choices 
#### spinbox 
entry with arrows for choices - kinda bad

##layout elements

#### grid
rows:INT [1] columns:INT [1] creates grid object - objects inside gain tags gridx:INT [0],gridy:INT [0],gridspanx:INT [1],gridspany:INT [1]
#### notebook 
- maximum 10 tabs
#### horizontal
#### vertical
