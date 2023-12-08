import functools


def ggt(numbers):
    for i in range(0, len(numbers) - 1):
        while numbers[1]:
            numbers[0], numbers[1] = numbers[1], numbers[0] % numbers[1]
        numbers[1] = numbers[i + 1]

    return numbers[0]


def kgve(numbers):
    return functools.reduce(lambda a, b: a * b // ggt([a, b]), numbers)
    # Weniger "pythonisch" und ohne functools:
    '''for i in range(0, len(numbers)-1):
        numbers[0] *= numbers[1] // ggt([numbers[0], numbers[1]])
        numbers[1] = numbers[i+1]

    return 	numbers[0] * numbers[1] // ggt([numbers[0], numbers[1]])'''

map={}
with open("eighth.txt","r") as f:
    for line in f:
        if line.strip() and '=' not in line.strip():
            instructions=line.strip()
        if '=' in line.strip():
            src, instruction=line.strip().split('=')
            left,right=instruction.strip().split(',')
            map[src.strip()]={'L': left.strip()[1:],'R': right.strip()[:-1]}

current='AAA'
i=0
count=0
while current != 'ZZZ':
    current=map[current][instructions[i]]
    i+=1
    count+=1
    if i>=len(instructions):
        i=0

print(count)

currents=[]
zs=[]
for key in map.keys():
    if key[2]=='A':
        currents.append(key)

count=0
i=0

print(zs)
print(currents)


countnextz=[]
countfirstz=[]
for current in currents:
    count=0
    while current[2] != 'Z':
        current = map[current][instructions[i]]
        i+=1
        count+=1
        if i>=len(instructions):
            i=0
    countfirstz.append(count)
    zs.append(current)


print(countfirstz)
print(zs)
nextzs=[]
for z in zs:
    count = 1
    z = map[z][instructions[i]]
    zstart = z
    i+=1
    while z[2] != 'Z':
        z = map[z][instructions[i]]
        i += 1
        count += 1
        if i >= len(instructions):
            i = 0
    countnextz.append(count)

counttable=list(zip(countfirstz, countnextz))
steps,nextz1=counttable.pop()
while counttable:
    firstz,nextz2=counttable.pop()
    print(steps, nextz2, nextz1, counttable)
    # Wait for the next time when both have reched z
    while (steps-firstz)%nextz2:
        steps+=nextz1

    nextz1=kgve([nextz1,nextz2])
    print(steps,nextz2,nextz1,counttable)

print(steps)
