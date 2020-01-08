from tkml import *
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

    <cascade label="RadioButtons"><radiobutton value="True">Option1</radiobutton><radiobutton>Option2</radiobutton><radiobutton>Option3</radiobutton></cascade>
    <cascade label="CheckButtons"><checkbutton value="True">Option1</checkbutton><checkbutton>Option2</checkbutton><checkbutton>Option3</checkbutton></cascade>
    <command>Exit</command>
    </menu>
</head>
<body minWidth="400" minHeight="100">
    <grid relief="sunken">
        <grid.columnconfig column="0" weight="1"></grid.columnconfig>
        <grid.columnconfig column="1">
             <columnconfig.minsize>100</columnconfig.minsize>
             <columnconfig.weight>1</columnconfig.weight>
        </grid.columnconfig>

        <p varname="text">Enter your data:</p>

        <field varname="username">
            <grid.gridx>1</grid.gridx>
        </field>

        <button callback="OnButtonPress" gridy="1" gridspanx="2" label="Enter"/>

        <checkbutton gridy="2">Check Button</checkbutton>
        <slider gridy="2" gridx="1" min="0" max="100" orient="horizontal"></slider>


        <radiobutton gridy="3" value="1">Radio Option 1</radiobutton>
        <radiobutton gridy="3" value="0" gridx="1">Radio Option 2</radiobutton>


        <dropdown gridy="4">Option 1;Option 2;Option 3</dropdown>
        <spinbox gridy="4" gridx="1">1;2;4;8;16</spinbox>

        <colorfield gridy="5"/>

    </grid>

</body>
</tkml>
'''

with Window(layout) as window:

    @window.callback
    def OnButtonPress():
        print("button pressed")
