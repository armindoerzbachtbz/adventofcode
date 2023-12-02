s=0
maxcubes={'red':12,'green':13,'blue':14}
with open("second_1.txt", "r") as f:
    line = 'start'
    while line:
        line = f.readline()
        # extract games and prefix
        try:
            prefix,games=line.strip().split(":")
            gamenumber=int(prefix.split()[1])
            games=games.split(';')
            for game in games:
                cubes=game.strip().split(',')
                for cube in cubes:
                    number,color=cube.split()
                    if int(number)>maxcubes[color]:
                        gamenumber=0
                        break
            s+=gamenumber
        except Exception as ex:
            break

    print(s)


s=0

with open("second_2.txt", "r") as f:
    line = 'start'
    while line:
        line = f.readline()
        # extract games and prefix
        try:
            prefix,games=line.strip().split(":")
            gamenumber=int(prefix.split()[1])
            games=games.split(';')

            mincubes = {'red': 0, 'green': 0, 'blue': 0}
            for game in games:
                cubes=game.strip().split(',')
                for cube in cubes:
                    number,color=cube.split()
                    if int(number)>mincubes[color]:
                        mincubes[color]=int(number)
            power=1
            for p in mincubes.values():
                power*=p
            s+=power
        except Exception as ex:
            break

    print(s)
