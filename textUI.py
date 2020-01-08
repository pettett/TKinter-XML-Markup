import tkml
# simple test ui featuring every element.
# when every element is changed a message will be written to console
markup = '''
<tkml>
<head>
    <title>Example</title>
</head>
<body minWidth="100" minHeight="200">
    <grid>
        <columnconfig column="0" weight="4"></columnconfig>
        <columnconfig column="1" weight="4"></columnconfig>
        <columnconfig column="2" weight="1"></columnconfig>
        <p gridx="0" gridy="0">Button</p>
        <button callback="ButtonOnePressed" gridx="1" gridy="0">Press Me!</button>
        
        <p gridx="0" gridy="1">String Field</p>
        <field varname="InputValue" callback="InputValueChanged" gridx="1" gridy="1"></field>
        <p gridx="2" gridy="1" varname="InputValue">Value</p>

        <p gridy="2">Radio Buttons</p>
        <radiobutton group="radio1" gridy="2" gridx="1" value="0">Radio Option 1</radiobutton>
        <radiobutton group="radio1" gridy="3" gridx="1" value="1">Radio Option 2</radiobutton>
        <p gridy="2" gridx="2" varname="radio1">Value</p>

        <p gridy="4">Dropdown</p>
        <dropdown varname="Dropdown" gridy="4" gridx="1">Option 1;Option 2;Option 3</dropdown>
        <p gridy="4" gridx="2" varname="Dropdown">Option 1</p>

        <p gridy="5">Spin Box</p>
        <spinbox varname="SpinboxValue" gridy="5" gridx="1">option 1;option 2;option 3;option 4</spinbox>
        <p gridy="5" gridx="2" varname="SpinboxValue">spinbox</p>

        <p gridy="6">Slider</p>
        <slider orient="HORIZONTAL" gridy="6" gridx="1" varname="slider" min="0" max="1" resolution="0.01"></slider>
        <p gridy="6" gridx="2" varname="slider">0</p>
    </grid>
</body>
</tkml>
'''


with tkml.Window(markup) as window:
    @window.callback
    def ButtonOnePressed():
        print("Button one pressed")
    window.callbacks = {'buttonOnePressed': ButtonOnePressed}
