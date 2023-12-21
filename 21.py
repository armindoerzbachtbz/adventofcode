from functools import reduce

COUNT=0
gardenmap = []
linen = 0
with open("21.txt", "r") as f:
    for line in f:
        gardenmap.append(line.strip())
        if "S" in line:
            sx = line.find("S")
            sy = linen
        linen += 1
witdh = len(gardenmap[0])
height = len(gardenmap)
gardensreached = [[sx, sy]]

def printgarden(map,reached):
    nmap=[]
    for l in map:
        line=[]
        for r in l:
            line.append(r)
        nmap.append(line)

    for c in reached:
        if c[0] < height and c[0] >= 0 and c[1] < witdh and c[1] >= 0:
            nmap[c[0]][c[1]] = 'O'
    for line in nmap:
        print(reduce(lambda a,b:a+b,line))


for i in range(COUNT):
    newgardensreached = {}
    for g in gardensreached:
        for c in [[g[0], g[1] + 1], [g[0], g[1] - 1], [g[0] - 1, g[1]], [g[0] + 1, g[1]]]:
            if c[0] < height and c[0] >= 0 and c[1] < witdh and c[1] >= 0:
                if gardenmap[c[0]][c[1]] in 'S.':
                    newgardensreached[f"{c[0]},{c[1]}"]=[c[0],c[1]]
    gardensreached=newgardensreached.values()

    #print(gardensreached)
    print(len(gardensreached))
COUNT=500
lastlast=0
last=1
gardensreached=[[sx,sy]]
changeofchange=[]
numberofgardens=[]
for i in range(COUNT):
    newgardensreached = {}
    for g in gardensreached:
        for c in [[g[0], g[1] + 1], [g[0], g[1] - 1], [g[0] - 1, g[1]], [g[0] + 1, g[1]]]:
                if gardenmap[c[0]%height][c[1]%witdh] in 'S.':
                    newgardensreached[f"{c[0]},{c[1]}"]=[c[0],c[1]]
    gardensreached=newgardensreached.values()

    #print(gardensreached)
    #printgarden(gardenmap,gardensreached)
    #print(f"{i},{len(gardensreached)},{len(gardensreached)-last}",lastlast-last)
    changeofchange.append((len(gardensreached)-last)-(last-lastlast))
    numberofgardens.append(len(gardensreached))
    lastlast=last
    last=len(gardensreached)


def searchrecurringpattern(samples, maxlength=20, minrepeat=3):
    for patternlength in range(1, maxlength + 1):
        pattern = samples[-1:-patternlength - 1:-1]
        i = 0
        found = True
        for repeat in range(minrepeat):
            for p in pattern:
                if samples[-i - 1] != p:
                    found = False
                    break
                i += 1
            if not found:
                break
        if found:
            return pattern
    return []

print(numberofgardens)
print(searchrecurringpattern(changeofchange,maxlength=100,minrepeat=3))