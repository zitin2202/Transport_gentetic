import random


def randomWithException(min,max,eception):
    while True:
        random_int = random.randint(min, max)
        if random_int != eception: break

    return random_int

def searchRandWithMinHoriz(mass,y, min, func_random):
    while True:
        index = func_random()
        if mass[y][index]>=min:
            return index

def searchRandWithMinVerticl(mass,x,min, func_random):
    while True:
        index = func_random()
        if mass[index][x]>=min:
            return index


def searchValueInMassiveWithMinHoriz(mass,y,min,exception):
    for i in range(len(mass[0])):
            if mass[y][i] >= min and i!=exception:
                return True
    return False

def searchValueInMassiveWithMinVerticl(mass,x,min,exception):
    for i in range(len(mass)):
        if mass[i][x] >= min and i!=exception:
            return True
    return False

def Print(individual):
    for i in individual:
        for j in i:
            print(j, end=" ")
            if j<9:print(end=" ")
            if j < 99: print(end=" ")
        print("\n")