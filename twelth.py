import datetime
import functools
import re


def checkmodifiedpattern(numbers, modifiedpattern):
    i = 0
    numberindex = 0
    while i < len(modifiedpattern):
        if modifiedpattern[i] == '#':
            if numberindex >= len(numbers):
                return False
            n = numbers[numberindex]
            start = i
            while i < len(modifiedpattern) and modifiedpattern[i] == '#':
                i += 1
            numberindex += 1
            if n != i - start:
                return False
        else:
            i += 1
    if numberindex < len(numbers):
        return False
    return True


def getwildcardpos(pattern):
    wildcardpos = []
    i = 0
    while i < len(pattern):
        if pattern[i] == '?':
            wildcardpos.append(i)
        i += 1
    return wildcardpos


def getpossibilities(numbers, pattern):
    wildcardpos = getwildcardpos(pattern)
    posibilities = 0
    for i in range(1 << len(wildcardpos)):
        modifiedpattern = list(pattern)
        count = len(wildcardpos)
        while count:
            count -= 1
            bitmask = 1 << count
            if bitmask & i:
                modifiedpattern[wildcardpos[count]] = '#'
            else:
                modifiedpattern[wildcardpos[count]] = '.'
        if checkmodifiedpattern(numbers, modifiedpattern):
            posibilities += 1
    return posibilities


def getpossibilitiesfast(numbers, pattern):
    posibilities = 0
    wildcardpos = getwildcardpos(pattern)
    numberofhashesinpattern = len(re.findall("#", pattern))
    numberofhashesneeded = sum(numbers)
    additionalhashes = numberofhashesneeded - numberofhashesinpattern
    # Modify ? only additionalhashes to #. The rest of ? should be .
    # generate all choices of additionalhashes positions of wildcardpos.
    # start with the 3 first positions
    positions = [x for x in range(additionalhashes)]
    # now move 1 positon to the right
    changed = True
    while changed:
        modifiedpattern = list(pattern)
        # Modify pattern now at these positions
        for pos in positions:
            modifiedpattern[wildcardpos[pos]] = '#'
        for pos in wildcardpos:
            if modifiedpattern[pos] == '?':
                modifiedpattern[pos] = '.'
        if checkmodifiedpattern(numbers, modifiedpattern):
            posibilities += 1
        # Now generate new posistions
        newpositions = [x for x in positions]
        changed = False
        for x in range(additionalhashes):
            if x == len(newpositions) - 1:
                if newpositions[x] < len(wildcardpos) - 1:
                    newpositions[x] += 1
                    for i in range(x):
                        newpositions[i] = i
                    changed = True
                break
            if newpositions[x] < newpositions[x + 1] - 1:
                newpositions[x] += 1
                for i in range(x):
                    newpositions[i] = i
                changed = True
                break
        positions = newpositions
    return posibilities
cache={}
def getpossibilitiesrecursion(numbers, pattern):
    # this algorithm just takes the pattern and gos from left to right to look for the first
    # possibility to match the first number of hashes and uses recursion to find the possibilities
    # for the remaining numbers and the remaining part of the pattern
    if (pattern+str(numbers) in cache):
        cache[pattern+str(numbers)][1]+=1
        return cache[pattern+str(numbers)][0]

    if not numbers:
        # We have no hash to match anymore
        if '#' not in pattern:
            # Return 1 if we have no # anymore in remaining pattern
            return 1
        else:
            # We still have # in pattern -> no match -> return 0
            return 0

    # We still have numbers of # to match
    number = numbers[0]
    countin = 0
    posibilities = 0
    i = 0
    while i < len(pattern):
        if pattern[i] == "?":
            # We have found ?
            if countin:
                # We are in the pattern
                if countin == number:
                    # We have already counted number times in pattern and we take the current ? as .
                    if i < len(pattern) - 1:
                        # Do match the Rest with recursion if we have pattern left
                        #print(functools.reduce(lambda a,b: a+b,modifiedpattern), number)
                        posibilities += getpossibilitiesrecursion(numbers[1:], pattern[i + 1:])
                    else:
                        if len(numbers)==1:
                            posibilities += 1
                    if pattern[i - number] == "#":
                        countin = 0
                        break
                else:
                    countin += 1
            else:
                countin+=1
        elif pattern[i] == "#":
            countin += 1
            if countin > number:
                if pattern[i - number] == '?':
                    countin=number
                else:
                    break
        elif pattern[i] == ".":
            if countin == number:
                if i < len(pattern) - 1:
                    #print(functools.reduce(lambda a, b: a + b, modifiedpattern), number)
                    posibilities += getpossibilitiesrecursion(numbers[1:], pattern[i + 1:])
                elif len(numbers)==1:
                    posibilities+=1
                if pattern[i-number]=="#":
                    countin = 0
                    break

            allwildcards=True
            for l in range(i-countin,i):
                if pattern[l]=="#":
                    allwildcards=False
                    break
            if not allwildcards:
                break

            countin = 0
        else:
            raise Exception("wrong character in pattern " + pattern[i])

        i += 1
    if countin == number and len(numbers) == 1 and len(pattern)==i:
        posibilities+=1

    if (len(pattern+str(numbers))<300 and len(numbers)<30):
        cache[pattern+str(numbers)]=[posibilities,0]
    return posibilities

def cleanupcache():
    print("Cachesize before cleanup:%d" % len(cache))
    keys=[]
    s=0
    p=0
    for key,item in cache.items():
        if item[1]<1:
            keys.append(key)
        s += item[1]
        p += item[0] * item[1]
        item[1]-=1

    for key in keys:
        cache.pop(key)
    print("Cache Hits:%d"%s)
    print("Sum of Possibilities cached:%d"%p)
    print("Cachesize after cleanup:%d" % len(cache))


posibilities = 0
with open("twelth.txt", "r") as f:
    for line in f:
        numbers = [int(x) for x in line.strip().split()[1].split(",")]
        pattern = line.strip().split()[0]
        posrec = getpossibilitiesrecursion(numbers, pattern)
        posfast = getpossibilitiesfast(numbers, pattern)
        posibilities += posrec
        if posrec != posfast:
            print(pattern, numbers, posrec, posfast)
print("Posibilities Task1:%d"%posibilities)
cleanupcache()
posibilities = 0
count=0
with open("twelth.txt", "r") as f:
    for line in f:
        numbers = [int(x) for x in line.strip().split()[1].split(",")]
        numbers *= 5
        pattern = line.strip().split()[0]
        newpattern = pattern
        newpattern += '?' + pattern
        newpattern += '?' + pattern
        newpattern += '?' + pattern
        newpattern += '?' + pattern
        starttime = datetime.datetime.now()
        posibilities_rec= getpossibilitiesrecursion(numbers, newpattern)
        posibilities += posibilities_rec
        count += 1
        print(starttime,(datetime.datetime.now()-starttime).total_seconds(),count,posibilities_rec, posibilities, newpattern, numbers)
        if not count % 10:
            cleanupcache()
print(posibilities)
