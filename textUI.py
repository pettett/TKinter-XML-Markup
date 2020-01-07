import tkml
# simple test ui featuring every element.
# when every element is changed a message will be written to console
markup = '''
<tkml>
<head>
    <title>Example</title>
</head>
<body minWidth=100 minHeight=200>
    <grid>
        <columnconfig column=0 weight=4></columnconfig>
        <columnconfig column=1 weight=4></columnconfig>
        <columnconfig column=2 weight=1></columnconfig>
        <p gridx=0 gridy=0>Button</p>
        <button callback="buttonOnePressed" gridx=1 gridy=0>Press Me!</button>
        
        <p gridx=0 gridy=1>String Field</p>
        <field varname="InputValue" callback="InputValueChanged" gridx=1 gridy=1></field>
        <p gridx=2 gridy=1 varname="inputValueText">Value</p>

        <p gridy=2>Radio Buttons</p>
        <radiobutton group="radio1" gridy=2 gridx=1 value=0>Radio Option 1</radiobutton>
        <radiobutton group="radio1" gridy=3 gridx=1 value=1>Radio Option 2</radiobutton>
        <p gridy=2 gridx=2 varname="radio-value">Value</p>

        <p gridy=4>Dropdown</p>
        <dropdown callback="OnDropdownChanged" varname="Dropdown" gridy=4 gridx=1>Option 1;Option 2;Option 3</dropdown>
        <p gridy=4 gridx=2 varname="DropdownValue">Option 1</p>

        <p gridy=5>Spin Box</p>
        <spinbox callback="OnSpinboxChange" varname="SpinboxValue" gridy=5 gridx=1>option 1;option 2;option 3;option 4</spinbox>
        <p gridy=5 gridx=2 varname="SpinboxValueOut">spinbox</p>

        <p gridy=6>Slider</p>
        <slider orient=HORIZONTAL gridy=6 gridx=1 varname="slider" callback="OnSliderChanged" min=0 max=1 resolution=0.01f></slider>
        <p gridy=6 gridx=2 varname="SliderValueOutput">0</p>
    </grid>
</body>
</tkml>
'''


def ButtonOnePressed():
    print("Button one pressed")


def InputValueChanged():
    print("Input value changed to {0}".format(
        window.values['InputValue'].get()))
    window.values['inputValueText'].set(window.values['InputValue'].get())


def RadioButtonsChanged():
    print(window.values['radio1'].get())
    window.values['radio-value'].set(window.values['radio1'].get())


def DropdownChanged():
    window.values['DropdownValue'].set(window.values['Dropdown'].get())


def SpinboxChanged():
    window.values['SpinboxValueOut'].set(
        window.values['SpinboxValue'].get())


def SliderChanged():
    window.values['SliderValueOutput'].set(window.values['slider'].get())


window = tkml.Window(markup)
window.callbacks = {'buttonOnePressed': ButtonOnePressed, 'InputValueChanged': InputValueChanged, 'OnDropdownChanged': DropdownChanged,
                    'radio1': RadioButtonsChanged, 'OnSpinboxChange': SpinboxChanged, 'OnSliderChanged': SliderChanged}
window.mainloop()
