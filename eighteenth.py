class Vector(list):

    def __add__(self, other):
        if len(other) != len(self):
            raise Exception("Not the same dimensions")
        return Vector([self[i] + other[i] for i in range(len(other))])
    def __mul__(self,scalar):
        return Vector([i*scalar for i in self])


last = Vector([0, 0])
area = 0
length=0
part1=False
advancevektors = {'L': Vector([-1, 0]), 'R': Vector([1, 0]), 'D': Vector([0, 1]), 'U': Vector([0, -1])}
advancevektorspart2 = {'2': Vector([-1, 0]), '0': Vector([1, 0]), '1': Vector([0, 1]), '3': Vector([0, -1])}
with open("eighteenth.txt", "r") as f:
    for line in f:
        dir, count, color = line.strip().split()
        if part1:
            next=last+advancevektors[dir]*int(count)
        else:
            vector=advancevektorspart2[color[-2]]
            count=int(color[2:-2],16)
            next=last+vector*count
        area+=(next[1]+last[1])/2*(next[0]-last[0])
        last=next
        length+=int(count)

print(f"Pathlength={length}")
print(f"Enclosed Area={abs(area)}")
print(f"Total Area={abs(area)+length/2+1}")
