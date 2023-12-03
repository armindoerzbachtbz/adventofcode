class value:
    def __init__(self,start,end,value):
        self.start=start
        self.end=end
        self.value=value
    def getvalue(self,symbols):
        for symbol in symbols:
            if self.start-1<=symbol and self.end+1>=symbol:
                return self.value
        return 0
    def isnextto(self,symbol):
        return self.start-1<=symbol and self.end+1>=symbol

s=0
sg=0
values=[[],[],[]]
symbols=[[],[],[]]
gears=[[],[],[]]
with open("third_1.txt", "r") as f:
    line = '....'
    lastline=''
    while line:
        values[0]=values[1]
        values[1]=values[2]
        values[2]=[]
        symbols[0] = symbols[1]
        symbols[1] = symbols[2]
        symbols[2] = []
        gears[0] = gears[1]
        gears[1] = gears[2]
        gears[2] = []

        lastlastline=lastline
        lastline=line
        line=f.readline().strip()
        currentvalue = 0
        currentstart = 0
        currentend = 0
        for i in range(len(line)):
            if line[i]=='.':
                if currentvalue!=0:
                    values[2].append(value(currentstart,currentend,currentvalue))
                    currentvalue=0
                continue
            if line[i] not in '1234567890':
                if line[i]=='*':
                    gears[2].append(i)
                symbols[2].append(i)
                if currentvalue!=0:
                    values[2].append(value(currentstart, currentend, currentvalue))
                    currentvalue = 0
                continue
            if currentvalue==0:
                currentstart=i
                currentend=i
                currentvalue=int(line[i])
            else:
                currentvalue=currentvalue*10+int(line[i])
                currentend=i
        if currentvalue!=0:
            values[2].append(value(currentstart,currentend,currentvalue))
        for val in values[1]:
            s+=val.getvalue(symbols[1]+symbols[2]+symbols[0])
        for gear in gears[1]:
            vals = []
            for val in values[1]+values[2]+values[0]:
                if val.isnextto(gear):
                    vals.append(val)
            if len(vals)==2:
                if vals[0].value*vals[1].value>1000000:
                    print(vals[0].value*vals[1].value)
                sg+=vals[0].value*vals[1].value
            if len(vals)>2:
                print(lastlastline)
                print(lastline)
                print(line)

print(s)
print(sg)