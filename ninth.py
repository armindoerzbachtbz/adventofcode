import functools


def differentiate(sequence):
    last=sequence[0]
    newseq=[]
    for x in sequence[1:]:
        newseq.append(x-last)
        last=x
    return newseq

def checkzero(sequence):
    for i in sequence:
        if i!=0:
            return False
    return True
def getprevandnextnumber(sequence):
    if checkzero(sequence):
        return [0,0]
    else:
        nextseq = differentiate(sequence)
        prevandnextnumbers=getprevandnextnumber(nextseq)
        nextnumber=sequence[-1]+prevandnextnumbers[1]
        prevnumber=sequence[0]-prevandnextnumbers[0]
        return [prevnumber,nextnumber]
d=0
s=0
with open("ninth.txt") as f:
    for line in f:
        sequence=[int(x) for x in line.strip().split()]
        nextnumbers=getprevandnextnumber(sequence)
        s+=nextnumbers[1]
        d+=nextnumbers[0]

print(s,d)
