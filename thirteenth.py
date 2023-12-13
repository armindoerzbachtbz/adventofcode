def findhmirror(pattern,repair=False):
    #print("-"*40)
    #for line in pattern:
    #    print(line)
    #print("-" * 40)
    lastln = 0
    currln = 1
    while currln<len(pattern):
        countsmudge = 0
        while currln<len(pattern):
            if pattern[lastln] == pattern[currln]:
                break
            if repair:
                for e in range(len(pattern[lastln])):
                    if pattern[lastln][e] != pattern[currln][e]:
                        countsmudge += 1
                if countsmudge == 1:
                    break
                else:
                    countsmudge=0
            currln+=1
            lastln+=1
        if not currln<len(pattern):
            break
        ismirror = True
        for i in range(1,min(len(pattern) - currln, lastln + 1)):
            if pattern[lastln - i] != pattern[currln + i]:
                if repair:
                    for e in range(len(pattern[lastln-i])):
                        if pattern[lastln-i][e]!=pattern[currln+i][e]:
                            countsmudge+=1
                    if countsmudge>1:
                        ismirror=False
                        break
                else:
                    ismirror = False
                    break
        if ismirror:
            if repair and countsmudge==1:
                return lastln+1
            if not repair:
                return lastln+1
        lastln+=1
        currln+=1
    return 0

def findvmirror(pattern,repair=False):
    newpattern=[]
    for row in pattern:
        linenumber=0
        for chr in row:
            if linenumber<len(newpattern):
                newpattern[linenumber]+=chr
            else:
                newpattern.append(chr)
            linenumber+=1
    return findhmirror(newpattern,repair)


s_withoutsmudge = 0
s_withsmudge = 0
with open("thirteenth.txt", "r") as f:
    pattern = []
    for line in f:
        if line.strip():
            pattern.append(line.strip())
        else:
            line1 = findhmirror(pattern)
            s_withoutsmudge+= line1 * 100
            line2 = findvmirror(pattern)
            s_withoutsmudge += line2
            print(line1, line2, s_withoutsmudge)
            line1 = findhmirror(pattern,True)
            s_withsmudge += line1 * 100
            line2 = findvmirror(pattern,True)
            s_withsmudge += line2
            print(line1, line2, s_withsmudge)
            pattern=[]

print(s_withoutsmudge)
print(s_withsmudge)

