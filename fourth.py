s=1
nlines=0
with open("fourth.txt", "r") as f:
    line = '....'

    while line.strip():
        line=f.readline()
        if not line:
            break
        nlines+=1
        winingnumbers,mynumbers=line.strip().split(":")[1].split("|")
        winingnumbers=[int(i) for i in winingnumbers.strip().split()]
        mynumbers=[int(i) for i in mynumbers.strip().split()]
        print(mynumbers,winingnumbers)
        count=1
        for num in mynumbers:
            if num in winingnumbers:
                count<<=1
        print(count>>1)
        s+=count>>1

print(s)

s=0
cards=[1 for i in range(nlines)]
index=0
with open("fourth.txt", "r") as f:
    line = '....'
    while line.strip():
        line=f.readline()
        if not line:
            break
        winingnumbers,mynumbers=line.strip().split(":")[1].split("|")
        winingnumbers=[int(i) for i in winingnumbers.strip().split()]
        mynumbers=[int(i) for i in mynumbers.strip().split()]
        count=0
        for num in mynumbers:
            if num in winingnumbers:
                count+=1
        for iii in range(index + 1, index + 1 + count):
            if iii<len(cards):
                cards[iii]+=cards[index]
            else:
                print(iii)
        index+=1
print(sum(cards))