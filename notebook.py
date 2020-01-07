import tkml

markup = '''
<tkml>
<head>
<title>Notebook Demo</title>
<menu><command>Yeet</command></menu>
<style ref="title" fontsize=20 font="times" fg="grey"></style>
</head>
<body>
<notebook>
    <vertical defaultcolumnweight=0 defaultrowweight=0>
        <p>This is page 1</p> 
        <p>This new line is sponsered by verticle layout TM</p>
        <horizontal>
            <p>Horizontal?</p>
            <button>Yes</button>
        </horizontal>
        <checkbutton>Button</checkbutton>
        <checkbutton>Button</checkbutton>
        <button>Button</button>
        <p sticky="ES" weight=1>Stick to the ground</p>
    </vertical>

    <text>This is page 2, featuring the grand 'text box', a wonderous moment for mankind</text>
    <text scrolled=True>This is page 3, and features scrolled text</text>
    <vertical>
        <p style="title">This is page 4 with a cool styled title</p>
        <p>This is page 4 with a boring label</p>
    </vertical>
    <p tabname="fone" image="image1.gif"></p>
    <p tabname="devlin" image="image2.gif">s</p>
    <vertical>
        <field type=FLOAT callback="onfloatchange" varname="floatvalue"></field>
        <p varname="floatvalue"></p>
    </vertical>

    <vertical>
        <field type=INT callback="onintchange" varname="intvalue"></field>
        <p varname="intvalue"></p>
    </vertical>

    <p style="title">This is page 9, with the same style as 4</p>
    <p>This is page 10</p>

</notebook>
</body>
</tkml>
'''


window = tkml.Window(markup)
window.mainloop()
