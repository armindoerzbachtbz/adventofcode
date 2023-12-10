class Pipegrid:
    def __init__(self):
        self.grid = []
        self.startx = -1
        self.starty = -2

    def setStart(self, startx, starty):
        self.startx = startx
        self.starty = starty

    def append(self, line):
        self.grid.append(line)

    def __tile__(self, x, y):
        return self.grid[y][x]

    def __area__(self, x, y):
        return

    def nextarea(self, x, y, lastx, lasty, reverse=False):

        t = self.__tile__(x, y)

        if x >= len(self.grid[y]) or y >= len(self.grid) or x < 0 or y < 0:
            return None
        area = (lasty + y) * (x - lastx) / 2    # Fleache unter Trapez -> summieren -> Flaeche innerhalb kurve.
                                                # Inspiriert von https://de.wikipedia.org/wiki/Polygon
        print(area,x,lastx,y,lasty)
        if t == '|':
            if lasty == y + 1 or reverse:
                return [x, y - 1], area
            else:
                return [x, y + 1], area
        if t == '-':
            if lastx == x + 1 or reverse:
                return [x - 1, y], area
            else:
                return [x + 1, y], area
        if t == 'L':
            if lastx == x + 1 or reverse:
                return [x, y - 1], area
            else:
                return [x + 1, y], area
        if t == 'J':
            if lasty == y - 1 or reverse:
                return [x - 1, y], area
            else:
                return [x, y - 1], area
        if t == '7':
            if lasty == y + 1 or reverse:
                return [x - 1, y], area
            else:
                return [x, y + 1], area
        if t == 'F':
            if lastx == x + 1 or reverse:
                return [x, y + 1], area
            else:
                return [x + 1, y], area
        if t == 'S':
            return [x,y],area
        return None

    def next(self, x, y, lastx, lasty, reverse=False):
        next, area = self.nextarea(x, y, lastx, lasty, reverse)
        return next


with open("tenth.txt", "r") as f:
    count = 0
    pipegrid = Pipegrid()
    for line in f:
        if 'S' in line:
            startx, starty = [line.index("S"), count]
            pipegrid.setStart(startx, starty)
        pipegrid.append(line)
        count += 1


def equal(a, b):
    return a[1] == b[1] and b[0] == a[0]


steps = 0
totarea = 0
x, y = [startx, starty]

candidates = [[x + 1, y],
              [x - 1, y],
              [x, y + 1],
              [x, y - 1]]
for next in candidates:
    reversenext, area = pipegrid.nextarea(next[0], next[1], x, y, True)
    if reversenext:
        if equal(reversenext, [x, y]):
            lastx, lasty = [startx, starty]
            x, y = next
            #totarea += area
            steps = 1
            break

while not equal([x, y], [startx, starty]):
    next, area = pipegrid.nextarea(x, y, lastx, lasty)
    if next:
        lastx, lasty = [x, y]
        x, y = next
        totarea += area
        steps += 1
    else:
        print("Brokenpipe at x=%d,y=%d" % (x, y))
        break

next,area=pipegrid.nextarea(x,y,lastx,lasty)
totarea+=area
print("Groesste distanz %-10.0f"%(steps / 2))
print("Flaeche innerhalb von track %-10.0f"%abs(totarea))
# Korrektur: Streckenlaenge*0.5 anziehen. Das war aber genau in jedem ecken 1/4 zuviel, darum +1
print("Anzahl Felder innerhalb des Tracks %-10.0f"%(abs(totarea)-steps/2+1))
