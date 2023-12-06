import sys

sys.setrecursionlimit(3000)


class Map:
    def __init__(self, buffer, mapname):
        self.mapname = mapname
        self.mappings = []
        for line in buffer:
            startdest, startsrc, count = line.split()
            self.mappings.append([int(startdest), int(startsrc), int(count)])

    def getMappedID(self, id):
        for startdest, startsrc, count in self.mappings:
            if id >= startsrc and id < startsrc + count:
                return startdest + id - startsrc
        return id

    def getMappedRanges(self, inranges):
        outranges = []
        for inrange in inranges:
            for startdest, startsrc, count in self.mappings:
                if inrange[0] >= startsrc and inrange[0] < startsrc + count and inrange[1] >= startsrc and inrange[
                    1] < startsrc + count:
                    outranges.append([startdest + inrange[0] - startsrc, startdest + inrange[1] - startsrc])
                    inrange=[]
                    break
                if (inrange[0] < startsrc) and inrange[1] >= startsrc and inrange[
                    1] < startsrc + count:
                    outranges.append([startdest,startdest + inrange[1] - startsrc])
                    inrange=[inrange[0],startsrc-1]
                if inrange[0] >= startsrc and inrange[0] < startsrc + count and inrange[1]>=startsrc+count:
                    outranges.append([startdest + inrange[0] - startsrc,startdest+count-1])
                    inrange=[startsrc+count,inrange[1]]
            if inrange:
                outranges.append(inrange)
        return outranges

s = 0
nlines = 0
maps = []
mapname = ''
lc = 0
with open("fifth.txt", "r") as f:
    inbuffer = False
    for line in f:
        lc += 1
        if line.startswith('seeds:'):
            seeds = line.split(':')[1].strip().split()
        if inbuffer:
            if line[0] in '0123456789':
                buffer.append(line.strip())
            else:
                maps.append(Map(buffer, mapname))
                inbuffer = False
        if 'map' in line:
            mapname = line
            buffer = []
            inbuffer = True
    if inbuffer:
        maps.append(Map(buffer, mapname))
locations = []
for seed in seeds:
    id = int(seed)
    for map in maps:
        id = map.getMappedID(id)
    locations.append(id)
print(min(locations))

i = 0
ranges=[]
while i < len(seeds):
    print(i, seeds[i], seeds[i + 1])
    ranges.append([int(seeds[i]), int(seeds[i + 1]) + int(seeds[i])])
    i += 2
for map in maps:
    ranges=map.getMappedRanges(ranges)
minloc=9999999999999999
for r in ranges:
    if minloc>r[0]:
        minloc=r[0]
print(minloc)
