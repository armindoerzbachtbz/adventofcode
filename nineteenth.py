parts = []
rulesets = {}
with open("nineteenth.txt", "r") as f:
    for line in f:
        if line.strip():
            if line.startswith("{"):
                lineparts = line.strip()[1:-1].split(",")
                #
                part = {}
                for val in lineparts:
                    part[val.split("=")[0]] = int(val.split("=")[1])
                parts.append(part)
            else:
                key, rules = line.strip()[:-1].split("{")
                rulessplitet = rules.split(",")
                rulesets[key] = {}
                rulesets[key]['default'] = rulessplitet[-1]
                rulesets[key]['rules'] = []
                for rule in rules.split(",")[:-1]:
                    varname = rule[0]
                    operator = rule[1]
                    value = rule[2:].split(":")[0]
                    action = rule[2:].split(":")[1]
                    rulesets[key]['rules'].append([varname, operator, value, action])

s = 0
for part in parts:
    rulename = 'in'
    while rulename not in ['A', 'R']:
        nextrulename = ""
        for rule in rulesets[rulename]['rules']:
            if rule[1] == '<':
                if part[rule[0]] < int(rule[2]):
                    nextrulename = rule[3]
                    break
            else:
                if part[rule[0]] > int(rule[2]):
                    nextrulename = rule[3]
                    break
        rulename = nextrulename if nextrulename else rulesets[rulename]['default']

    if rulename == 'A':
        s += sum(part.values())

print(f"Part1 sum of parts={s}")

posibleranges = {'x': [1, 4000], 'm':[1, 4000], 'a': [1, 4000], 's': [1, 4000]}

def calcposibilities(range):
    posibilities=1
    for subrange in range.values():
        posibilities*=subrange[1]-subrange[0]+1
    return posibilities
def range_to_rule(range, rulename):
    if rulename=='A':
        return calcposibilities(range)
    if rulename=='R':
        return 0
    s=0
    rules=rulesets[rulename]['rules']
    for rule in rules:
        if rule[1] == '>':
            if range[rule[0]][0]<int(rule[2]) and range[rule[0]][1]>=int(rule[2]):
                newrange = {x: [z for z in y] for x, y in range.items()}
                newrange[rule[0]][0]=int(rule[2])+1
                range[rule[0]][1] = int(rule[2])
                s+=range_to_rule(newrange, rule[3])
                rulematched=True
        if rule[1] == '<':
            if range[rule[0]][1]>int(rule[2]) and range[rule[0]][0]<=int(rule[2]):
                newrange={x:[z for z in y] for x,y in range.items()}
                newrange[rule[0]][1]=int(rule[2])-1
                range[rule[0]][0]=int(rule[2])
                s+=range_to_rule(newrange, rule[3])

    s+=range_to_rule(range, rulesets[rulename]['default'])
    return s

val=range_to_rule(posibleranges,'in')
print(f'Result of Part2={val}')