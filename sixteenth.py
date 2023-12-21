from os import PathLike

class Dish:
    EMPTY = '.'
    SPLITVER = '|'
    SPLITHOR = '-'
    MIRRORWESTUP = '/'
    MIRRORWESTDOWN = '\\'
    EAST = 1
    NORTH = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, file: PathLike):
        self.dish = []
        self.energized = []
        with open(file) as f:
            for line in f:
                self.dish.append(list(line.strip()))
        self.resetenergized()
        self.maxwidth = len(self.dish[0])
        self.maxheight = len(self.dish)

    def printenergized(self):
        for line in self.energized:
            out=""
            for cell in line:
                out+="#" if cell else "."
            print(out)

    def countenergized(self):
        count=0
        for line in self.energized:
            for cell in line:
                if cell:
                    count+=1
        return count
    def nextcells(self, x, y, direction):
        if self.energized[y][x] & direction:
            # Stop if we have already traversed in the same direction
            return
        else:
            self.energized[y][x] += direction
        nextcells = []
        if direction == self.NORTH:
            if self.dish[y][x] in [self.MIRRORWESTUP, self.SPLITHOR]:
                nextcells.append([x + 1, y, self.WEST])
            if self.dish[y][x] in [self.MIRRORWESTDOWN, self.SPLITHOR]:
                nextcells.append([x - 1, y, self.EAST])
            if self.dish[y][x] in [self.EMPTY, self.SPLITVER]:
                nextcells.append([x, y - 1, direction])
        elif direction == self.SOUTH:
            if self.dish[y][x] in [self.MIRRORWESTDOWN, self.SPLITHOR]:
                nextcells.append([x + 1, y, self.WEST])
            if self.dish[y][x] in [self.MIRRORWESTUP, self.SPLITHOR]:
                nextcells.append([x - 1, y, self.EAST])
            if self.dish[y][x] in [self.EMPTY, self.SPLITVER]:
                nextcells.append([x, y + 1, direction])
        elif direction == self.EAST:
            if self.dish[y][x] in [self.MIRRORWESTDOWN, self.SPLITVER]:
                nextcells.append([x, y - 1, self.NORTH])
            if self.dish[y][x] in [self.MIRRORWESTUP, self.SPLITVER]:
                nextcells.append([x, y + 1, self.SOUTH])
            if self.dish[y][x] in [self.EMPTY, self.SPLITHOR]:
                nextcells.append([x - 1, y, direction])
        else: #WEST
            if self.dish[y][x] in [self.MIRRORWESTDOWN, self.SPLITVER]:
                nextcells.append([x, y + 1, self.SOUTH])
            if self.dish[y][x] in [self.MIRRORWESTUP, self.SPLITVER]:
                nextcells.append([x, y - 1, self.NORTH])
            if self.dish[y][x] in [self.EMPTY, self.SPLITHOR]:
                nextcells.append([x + 1, y, direction])

        # Check if nextcells are still on the dish
        nextcellsfiltered=[]
        for x,y,direction in nextcells:
            if x>=0 and x<self.maxwidth and y>=0 and y<self.maxheight:
                nextcellsfiltered.append([x,y,direction])
        return nextcellsfiltered


    def advancebeam(self, x, y, direction):
        nextcells = self.nextcells(x, y, direction)
        while nextcells:
            if len(nextcells) == 1:
                x, y, direction = nextcells[0]
            else:
                for x, y, direction in nextcells:
                    self.advancebeam(x, y, direction)
                return
            nextcells = self.nextcells(x, y, direction)

    def resetenergized(self):
        self.energized=[]
        for line in self.dish:
            self.energized.append([0 for x in line])



dish = Dish("sixteenth.txt")

# Part one: Beam from top left to the WEST
dish.advancebeam(0,0,Dish.WEST)
dish.printenergized()
print(dish.countenergized())

# Part 2: Check countenergized for Beams from all directions and positions.
maxlava=0
for x in range(dish.maxwidth):
    dish.resetenergized()
    dish.advancebeam(x,0,Dish.SOUTH)
    maxlava=max(dish.countenergized(),maxlava)
    dish.resetenergized()
    dish.advancebeam(x,dish.maxheight-1,Dish.NORTH)
    maxlava = max(dish.countenergized(), maxlava)
for y in range(dish.maxheight):
    dish.resetenergized()
    dish.advancebeam(0,y,Dish.WEST)
    maxlava = max(dish.countenergized(), maxlava)
    dish.resetenergized()
    dish.advancebeam(dish.maxwidth-1,y,Dish.EAST)
    maxlava = max(dish.countenergized(), maxlava)

print(maxlava)

