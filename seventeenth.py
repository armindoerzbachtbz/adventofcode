import heapq


class heatmap:
    def __init__(self, file):
        self.hm = []
        with open(file, "r") as f:
            for line in f:
                self.hm.append([[int(x), False] for x in line.strip()])

    def width(self):
        return len(self.hm[0])

    def height(self):
        return len(self.hm)

    def heat(self, x, y):
        return self.hm[y][x][0]

    def passed(self, x, y):
        return self.hm[y][x][1]

    def markpassed(self, x, y):
        self.hm[y][x][1] = True

    def next(self, x, y, dir, movesinsamedir, heat):
        return x, y, dir, movesinsamedir, heat


hmap = heatmap("seventeenth.txt")
candidates = []

x, y = [0, 0]
heat = 0
movesinsamedir = 0
dir = -1
while x != hmap.width() - 1 or y != hmap.height() - 1:

    candnext = [[x, y - 1], [x + 1, y], [x, y + 1], [x - 1, y]]
    nextdirs = [dir%4, (dir + 1) % 4, (dir - 1) % 4]
    if movesinsamedir == 3:
        nextdirs.pop(0)

    for nextdir in nextdirs:
        xn = candnext[nextdir][0]
        yn = candnext[nextdir][1]
        if xn < hmap.width() and xn >= 0 and yn < hmap.height() and yn >= 0 and not hmap.passed(xn, yn):
            hmap.markpassed(xn, yn)
            if nextdir == dir:
                heapq.heappush(candidates,
                               [heat + hmap.heat(xn, yn), xn, yn, nextdir, movesinsamedir + 1])
            else:
                heapq.heappush(candidates,
                               [heat + hmap.heat(xn, yn), xn, yn, nextdir, 1])

    heat, x, y, dir, movesinsamedir = heapq.heappop(candidates)
    print(heat, x, y)

print(heat)
