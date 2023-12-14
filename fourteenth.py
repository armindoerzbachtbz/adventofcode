import functools
from os import PathLike


class Dish:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    moveunitvector = {NORTH: [0, -1], EAST: [1, 0], SOUTH: [0, 1], WEST: [-1, 0]}
    SOLIDROCK = '#'
    ROLLINGROCK = 'O'
    FREE = '.'

    def isrock(self, nextcoord):
        return (nextcoord[0] < 0 or nextcoord[0] >= len(self.dish[0])
                or nextcoord[1] < 0 or nextcoord[1] >= len(self.dish)
                or self.dish[nextcoord[1]][nextcoord[0]] in [Dish.ROLLINGROCK, Dish.SOLIDROCK])

    def __init__(self, file: PathLike):
        self.dish = []
        with open(file) as f:
            for line in f:
                self.dish.append(list(line.strip()))

    def nextcoord(self, coordinates: [int, int], direction=NORTH):
        return [coordinates[i] + self.moveunitvector[direction][i] for i in range(2)]

    def moveit(self, pos1, pos2):
        rock = self.dish[pos1[1]][pos1[0]]
        self.dish[pos1[1]][pos1[0]] = self.dish[pos2[1]][pos2[0]]
        self.dish[pos2[1]][pos2[0]] = rock

    def moverock(self, coordinates: [int, int], direction=NORTH):
        nextcoord = self.nextcoord(coordinates, direction)
        lastcoord = coordinates
        while not self.isrock(nextcoord):
            lastcoord = nextcoord
            nextcoord = self.nextcoord(nextcoord, direction)
        self.moveit(coordinates, lastcoord)

    def moveallrocks(self, rocktype, direction=NORTH):
        for rockcoord in self.getrocks(rocktype, direction):
            self.moverock(rockcoord, direction)

    def calcload(self, rocktype, direction=NORTH):
        load = 0
        for rock in self.getrocks(rocktype, direction):

            if self.moveunitvector[direction][0]:
                additionalload = rock[0] * self.moveunitvector[direction][0] + len(self.dish[0])
                if additionalload > len(self.dish[0]):
                    additionalload -= len(self.dish[0])
            else:
                additionalload = rock[1] * self.moveunitvector[direction][1] + len(self.dish)
                if additionalload > len(self.dish):
                    additionalload -= len(self.dish)
            load += additionalload
        return load

    def getrocks(self, rocktype, direction=NORTH):
        rocks = []
        if direction == Dish.SOUTH:
            yrange = range(len(self.dish) - 1, -1, -1)
            xrange = range(len(self.dish[0]))
        if direction == Dish.NORTH or direction == Dish.WEST:
            yrange = range(len(self.dish))
            xrange = range(len(self.dish[0]))
        if direction == Dish.EAST:
            yrange = range(len(self.dish))
            xrange = range(len(self.dish[0]) - 1, -1, -1)
        for y in yrange:
            for x in xrange:
                if self.dish[y][x] == rocktype:
                    yield [x, y]

    def print(self):
        print("-" * 100)
        for line in self.dish:
            print(functools.reduce(lambda a, b: a + b, line))
        print("-" * 100)


dish = Dish("fourteenth.txt")
dish.print()
dish.moveallrocks(Dish.ROLLINGROCK, Dish.NORTH)
dish.print()
print(dish.calcload(Dish.ROLLINGROCK, Dish.NORTH))


# part 2


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


cycles = 1000000000
numberofiterations = 200
dish = Dish("fourteenth.txt")
results = []
for i in range(0, numberofiterations):
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.NORTH)
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.WEST)
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.SOUTH)
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.EAST)
    results.append(dish.calcload(Dish.ROLLINGROCK, Dish.NORTH))

pattern = searchrecurringpattern(results)
if not pattern:
    print("increase the number of itereations")

print(pattern)
remainingiterations = (cycles - numberofiterations) % len(pattern)
for i in range(0, remainingiterations):
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.NORTH)
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.WEST)
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.SOUTH)
    dish.moveallrocks(Dish.ROLLINGROCK, Dish.EAST)

print(dish.calcload(Dish.ROLLINGROCK, Dish.NORTH))
