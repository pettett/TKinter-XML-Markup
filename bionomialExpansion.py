from tkml import *
import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


superscripts = {
    "0":"\u2070",
    "1":"\u00B9",
    "2":"²",
    "3":"\u00B3",
    "4":"⁴",
    "5":"⁵",
    "6":"⁶",
    "7":"⁷",
    "8":"⁸",
    "9":"⁹",
    ".":"\u00B7"
    }


def superize(num:str) -> str:
    return "".join([superscripts[c] for c in "{:g}".format(num)])


with open("xml/bionomialExpansion.xml") as f:
    w = Window(f.read())


@w.callback
def OnButtonPressed():
    #binomial expansion
    
    c1 = w.coeffeciant1.get()
    c2 = w.coeffeciant2.get()
    e1 = w.exponent1.get()
    e2 = w.exponent2.get()
    p = w.power.get()

    asending = bool(w.asendingPowers.get())

    values = []
    out = ""
    for r in range(p+1):
        mult = ncr(p,r)
        power1 = r * e1
        power2 = (p-r) * e2
        
        values.append((mult*c1**r * c2**(p-r)  ,power1+power2))

    for i,(c,e) in enumerate(sorted(values,key=lambda x: x[1], reverse=not asending)):
        if not (c == 1 and e != 0):
            out += "{:g}".format(c)

        if e == 1:
            out += "x"
        elif e != 0:
            out += "x{}".format(superize(e))

        if i != len(values)-1:
            out += " + "

    w.Output.set(out)

w.mainloop()


