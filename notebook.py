import tkml

markup='''
<tkml>
<head>
<title>Notebook Demo</title>
<menu><command>Yeet</command></menu>
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
        <p sticky="EWS" weight=1>Stick to the ground</p>
    </vertical>

    <text>This is page 2, featuring the grand 'text box', a wonderous moment for mankind</text>
    <text scrolled=True>This is page 3, and features scrolled text</text>
    <p>This is page 4 with a boring label</p>
    <p tabname="fone" image="image1.gif"></p>
    <p tabname="devlin" image="image2.gif">s</p>
    <p>This is page 7</p>
    <p>This is page 8</p>
    <p>This is page 9</p>
    <p>This is page 10</p>

</notebook>
</body>
</tkml>
'''

window = tkml.Window(markup)
window.mainloop()