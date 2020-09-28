import sys
from tkml.tkml import *
import threading
import time
import builtins


def runincustomconsole(fun):
    saved = sys.stdout
    with Window(filename="xml/console_demo.xml") as w:
        class writer:
            def __init__(self, ogConsole):
                self.ogConsole = ogConsole

            def write(self, text):
                if (text != "\n"):  # Print statement automatically adds a line break
                    w.elements["console"].insert(END, text)
                    w.elements["console"].yview(END)

        sys.stdout = writer(sys.stdout)

        def fake_input(prompt):
            global inp, hasInput
            print(prompt)
            hasInput = False
            inp = ""

            @w.callback
            def OnInput():
                global inp, hasInput
                hasInput = True
                inp = w.inp

            while not hasInput:
                time.sleep(0.1)
            return inp

        builtins.input = fake_input

        threading.Thread(target=fun).start()

    sys.stdout = saved


@runincustomconsole
def AsyncTester():

    while True:
        print("iteration {}".format(input("Continue?")))

        time.sleep(1)
