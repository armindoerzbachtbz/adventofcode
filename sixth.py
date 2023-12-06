import math

class Race:
    def __init__(self,record,time):
        self.record=record
        self.time=time

    def getpossibilities(self):
        ## Rechne minimum und maximum mit mitternachtsformel fuer quadradische gleichungen
        min=(self.time-math.sqrt(self.time**2-4*self.record))/2
        max=(self.time+math.sqrt(self.time**2-4*self.record))/2
        # Jetzt kommt das runden
        if(min!=int(min)):
            # Keine ganze zahl
            min=int(min+1)
        else:
            # Ganze Zahl
            min=int(min)+1
        if(max!=int(max)):
            max=int(max)
        else:
            max=int(max-1)
        return max-min+1
races=[]
with open("sixth.txt","r") as f:
    for line in f:
        if line.startswith("Time:"):
            times=line.strip().split(":")[1].split()
        if line.startswith("Distance:"):
            distances=line.strip().split(":")[1].split()
        i=0
    while i<len(times):
        races.append(Race(int(distances[i]),int(times[i])))
        i += 1
prod=1
for race in races:
    prod*=race.getpossibilities()


print(prod)

with open("sixth.txt","r") as f:
    for line in f:
        if line.startswith("Time:"):
            time=line.strip().split(":")[1].replace(" ","")
        if line.startswith("Distance:"):
            distance=line.strip().split(":")[1].replace(" ","")
    print(Race(int(distance),int(time)).getpossibilities())