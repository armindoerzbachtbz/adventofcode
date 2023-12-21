

class module:
    highcount = 0
    lowcount = 0
    sendqueue=[]
    def __init__(self, name):
        self.name = name
        self.output = []

    def send(self, pulse):

        #print(f"highcount: {module.highcount} lowcount:{module.lowcount}")
        for out in self.output:
            if pulse:
                module.highcount += 1
            else:
                module.lowcount += 1
            #print(f"{self.name} -{'high' if pulse else 'low'}- -> {out.name}")
            out.input(pulse, self)
        #while self.sendqueue:
        #    sendf,args=self.sendqueue.pop(0)
        #    sendf(args)
        for out in self.output:
            out.sendit()

    def addoutput(self, output):
        self.output.append(output)

    def addinput(self,input):
        pass

    def __repr__(self):
        return f"{self.name}:{type(self)}\n"
class notype(module):
    def __init__(self,name):
        super().__init__(name)
        self.state=True
    def send(self,pulse):
        pass
    def sendit(self):
        pass
    def input(self, pulse, input):
        self.state=pulse

class flipflop(module):
    def __init__(self, name):
        super().__init__(name)
        self.state = False
        self.sendflag = False
    def input(self, pulse, input):
        if not pulse:
            self.state = not self.state
            self.sendflag = True
        else:
            self.sendflag=False
    def sendit(self):
        module.sendqueue.append([self.send,self.state]) if self.sendflag else None



class conjunction(module):
    def __init__(self, name):
        super().__init__(name)
        self.state = False
        self.inputs = {}

    def addinput(self, input):
        self.inputs[input] = False

    def input(self, pulse, input):
        if input not in self.inputs:
            raise Exception(f"Input {input.name} not defined")
        self.inputs[input] = pulse
    def sendit(self):
        pulse = False
        for input1, state in self.inputs.items():
            if not state:
                pulse = True
                break
        module.sendqueue.append([self.send, pulse])


class broadcast(module):

    def input(self, pulse, input):
        self.pulse=pulse
    def sendit(self):
        module.sendqueue.append([self.send, pulse])



def createmodule(line, createmodule=True):
    modulename = ""
    obj = None
    if line.startswith("broadcaster"):
        modulename, obj = "broadcaster", broadcast("broadcaster") if createmodule else None
    if line[0] == "%":
        modulename, obj = line.split(" ")[0][1:], flipflop(line.split(" ")[0][1:]) if createmodule else None
    if line[0] == "&":
        modulename, obj = line.split(" ")[0][1:], conjunction(line.split(" ")[0][1:]) if createmodule else None
    return modulename, obj


modules = {}

with open("twentieth.txt", "r") as f:
    for line in f:
        newmodule = None
        modulename, obj = createmodule(line)
        if obj:
            modules[modulename] = obj
        else:
            raise Exception(f"module type {line[0]} not found")
with open("twentieth.txt", "r") as f:
    for line in f:
        outputs = [x.strip() for x in line.strip().split("->")[-1].split(",")]

        modulename, _ = createmodule(line, False)
        for output in outputs:
            if output in modules:
                modules[modulename].addoutput(modules[output])
                modules[output].addinput(modules[modulename])
            else:
                modules[output]=notype(output)
                modules[modulename].addoutput(modules[output])

for i in range(1000):
    module.lowcount+=1
    modules["broadcaster"].send(False)
    while module.sendqueue:
        f,a = module.sendqueue.pop(0)
        f(a)

print(f"highcount: {module.highcount} lowcount:{module.lowcount}")
print(f"result: {module.highcount*module.lowcount}")

modules = {}
with open("twentieth.txt", "r") as f:
    for line in f:
        newmodule = None
        modulename, obj = createmodule(line)
        if obj:
            modules[modulename] = obj
        else:
            raise Exception(f"module type {line[0]} not found")
with open("twentieth.txt", "r") as f:
    for line in f:
        outputs = [x.strip() for x in line.strip().split("->")[-1].split(",")]

        modulename, _ = createmodule(line, False)
        for output in outputs:
            if output in modules:
                modules[modulename].addoutput(modules[output])
                modules[output].addinput(modules[modulename])
            else:
                modules[output]=notype(output)
                modules[modulename].addoutput(modules[output])

count=0
module.lowcount=0
module.highcount=0
module.sendqueue=[]
qnmodule=modules['qn']
secondlevel=[x for x,y in qnmodule.inputs.items()]
thirdlevel=[]
for i in secondlevel:
    thirdlevel+=[x for x,y in i.inputs.items()]

fourthlevel = []
for i in thirdlevel:
    fourthlevel += [x for x, y in i.inputs.items()]
print(secondlevel)
print(thirdlevel)
print(fourthlevel)
fourthlevelcount={}
for x in fourthlevel:
    fourthlevelcount[x]=[0,0]



rxmodule=modules['rx']
broadcastmodule=modules["broadcaster"]
for i in range(1000):
    module.lowcount+=1
    modules["broadcaster"].send(False)
    while module.sendqueue:
        f,a = module.sendqueue.pop(0)
        f(a)

print(f"highcount: {module.highcount} lowcount:{module.lowcount}")
print(f"result: {module.highcount*module.lowcount}")

while rxmodule.state:
    broadcastmodule.send(False)

    while module.sendqueue:
        f, a = module.sendqueue.pop(0)
        f(a)
        if not rxmodule.state:
            break

    for m,c in fourthlevelcount.items():
        if m.state:
            c[0]+=1
        else:
            c[1]+=1
        print(f"{m}:{c}") if not count%100000 else None

    count+=1
    print(f"count:{count}") if not count%100000 else None

print(count)