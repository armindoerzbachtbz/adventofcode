import re
with open("first.txt", "r") as f:
    line = 'start'
    s = 0
    while line:
        line = f.readline()
        i = 0
        while i < len(line) and line[i] not in '0123456789':
            i += 1
        if i < len(line):
            first = int(line[i])
        else:
            first = 0
        i = len(line) - 1
        while i >= 0 and line[i] not in '0123456789':
            i -= 1
        if i >= 0:
            last = int(line[i])
        else:
            last = 0
        s += last + first * 10

    print(s)

matcher = {'one': 1, 'two': 2, 'three': 3, 'four': 4,
           'five':5 ,'six':6,'seven':7,'eight':8, 'nine':9}
for i in range(1,10):
    matcher[str(i)]=i

s=0
with open("first_2.txt", "r") as f:
    line = 'start'
    while line:
        line = f.readline()
        firstindex=len(line)
        lastindex=0
        firstval=0
        lastval=0
        for key,value in matcher.items():
            for match in re.finditer(key,line):
                if lastindex<=match.start():
                    lastindex=match.start()
                    lastval=value
                if firstindex>=match.start():
                    firstindex=match.start()
                    firstval=value
        if firstindex==lastindex:
            print(line,firstval,lastval)
        s+=firstval*10+lastval

print(s)
