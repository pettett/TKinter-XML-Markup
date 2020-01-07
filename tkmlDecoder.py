from tkinter import *
from tkml import *

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


def ReadTags(tagsString):  # return name, dictionary of tags:tags value
    tagsList = tagsString.split(' ')
    # seperate out tags

    tagsDict = {}  # Each tag is stored in a pair TAGNAME=VALUE
    tagsDict['name'] = tagsList[0]
    for i in range(1, len(tagsList)):
        attribute = tagsList[i].split('=')
        try:
            if attribute[1] in consts:
                attribute[1] = consts[attribute[1]]
            elif attribute[1].find('"') != -1 or attribute[1].find("'") != -1:  # string value
                attribute[1] = attribute[1][1:-1]
            elif attribute[1][-1] == 'f':  # float value
                attribute[1] = float(attribute[1][0:-1])
            elif attribute[1].lower() == "false" or attribute[1].lower() == "true":  # boolean
                attribute[1] = attribute[1].lower() == "true"
            else:  # int value
                attribute[1] = int(attribute[1])

            tagsDict[attribute[0]] = attribute[1]
        except:
            raise Exception("incorrect tags in {0}".format(tagsString))
    return tagsDict


class Element:
    def __init__(self, tagName, default):
        self.tags = ReadTags(tagName)
        self.name = self.tags.pop('name', 'ERROR')
        self.default = default
        self.children = []


def Decode(tkml):

    # remove comments and decode the xml
    ended = False
    while ended == False:
        commentStart = tkml.find('<!--')
        commentEnd = tkml.find('-->')
        if commentStart == -1:
            # no more comments in markup
            ended = True
        else:
            tkml = tkml[:commentStart] + tkml[commentEnd+3:]
            # remove comment from tkml
    return DecodeTKML(tkml)[0]


def DecodeTKML(tkml):

    tagsStartIndex = tkml.find("<")
    tagsEndIndex = tkml.find('>')

    # check for empty element tag
    if tkml[tagsEndIndex-1] == '/':
        # element is empty, simply return
        root = Element(tkml[tagsStartIndex+1:tagsEndIndex-1], '')
        remainingText = tkml[tagsEndIndex+1:]
        nextBrocket = remainingText.find('<')
        ended = False
        if remainingText[nextBrocket + 1] == "/":
            ended = True
        return root, remainingText, ended
        # Root object should be the only one with <tkml></tkml>

    remainingText = tkml[tagsEndIndex+1:]
    endBrocket = remainingText.find('<')
    root = Element(tkml[tagsStartIndex+1:tagsEndIndex], '')

    if remainingText[endBrocket+1] == "/":  # Found an end piece
        root.default = remainingText[:endBrocket]
        remainingText = remainingText[endBrocket:]
        endEndBrocket = remainingText.find(">")
        remainingText = remainingText[endEndBrocket+1:]
        # if the brocket after this is an end piece </
        nextBrocket = remainingText.find('<')
        ended = False
        if remainingText[nextBrocket + 1] == "/":
            ended = True
        return root, remainingText, ended

    else:
        ended = False
        while ended == False:
            child, remainingText, ended = DecodeTKML(remainingText)
            root.children.append(child)

        # should return ended as true if the next element after this is an end piece

        ended = True
        endTag = "</{0}>".format(root.name)
        # remove end tag from object from remaining text
        remainingText = remainingText[remainingText.find(
            endTag) + len(endTag):]

        # there is another element after this one still, not ended
        nextTag = remainingText.find('<')
        if (nextTag != -1):  # there might be more
            if remainingText[nextTag+1] != '/':  # this is a new element, continue
                ended = False

        return root, remainingText, ended


if __name__ == "__main__":
    testLayout = '''
    <parent>
    <!-- This Comment will be removed-->
        <element tag="cheese" number=1f orient=VERTICAL>Hello chunky</element>
        <element>Next Element</element>
        <parent>
            <element label="Next-Element"/>
            <element/>
            <parent>
                <element stringone="string">Next Element</element>
                <element stringtwo='yeet'>Next Element</element>
                <element>Next Element</element>
                <element><element>Next Element</element>
                <element>Next Element</element>
                <element>Next Element</element>
                <element>Next Element</element></element>
                <element>Next Element</element>
                <element><element>Next Element</><element>Next Element</><element>Next Element</></>
            </>
    </>
        <element>Next Element</>
        <element>Next Element</>
        <element>Next Element</>
        <element>Next Element</>
    <element>Next Element</>
        <element>Next Element</>
        <element>Next Element</>
    </parent>
    '''
    # debug method to guage what is a child of other objects

    def PrintLayout(root, indents):
        print("{0}-{1} : {2}".format("    "*indents, root.name,
                                     '<br/>'.join(['%s - %s' % (key, value) for (key, value) in root.tags.items()])))
        for child in root.children:
            PrintLayout(child, indents+1)

    root = Decode(testLayout)
    PrintLayout(root, 0)
