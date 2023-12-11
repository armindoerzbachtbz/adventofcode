emptyrows=[]
fullcols=[]
galaxies=[]
y=0
width=0
with open("eleventh.txt","r") as f:
    for line in f:
        if width<len(line.strip()):
            width=len(line.strip())
        if '#' not in line:
            emptyrows.append(y)

        x=0
        while x!=-1 and x<len(line):
            x=line.find("#",x)
            if x!=-1:
                galaxies.append([x,y])
                fullcols.append(x)
                x += 1
        y+=1

# Expand universe
expantionratio=1000000
for g in galaxies:
    y=g[1]
    x=g[0]
    for row in emptyrows:
        if g[1]>row:
            y+=expantionratio-1
    g[1]=y
    for r in range(width):
        if r not in fullcols:
            if g[0]>r:
                x+=expantionratio-1
    g[0]=x

s=0
print(len(galaxies))
for this in range(len(galaxies)):
    for other in range(this,len(galaxies)):
        s+=abs(galaxies[this][0]-galaxies[other][0])+abs(galaxies[this][1]-galaxies[other][1])


print(s)


