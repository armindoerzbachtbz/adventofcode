sequence=[]
with open("fifteenth.txt", "r") as f:
    for line in f:
        sequence=line.strip().split(",")

#sequence='rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.strip().split(",")

#print(sequence)
def calchash(param):
    hash=0
    for c in param:
        hash+=ord(c)
        hash*=17
        hash%=256
    return hash

s=0
for i in sequence:
    s+=calchash(i)


print(f"Hash:{s}")

lensboxes=[{} for i in range(256)]

for i in sequence:
    if '=' in i:
        lens=i.split('=')
        hash=calchash(lens[0])
        lensboxes[hash][lens[0]]=int(lens[1])
    elif '-' in i:
        lens=i.split('-')
        hash=calchash(lens[0])
        if lens[0] in lensboxes[hash]:
            lensboxes[hash].pop(lens[0])
    else:
        raise Exception(f'Command not found in sequence {i}')

s=0
i=1
for box in lensboxes:
    e=1
    for focallength in box.values():
        s+=i*e*focallength
        e+=1
    i+=1

print(f'Focussing power:{s}')