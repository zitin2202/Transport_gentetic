import random

import numpy as np
from deap import creator, base,tools

import Data

A = []
B = []
costs_table = []
def randDistribution(needed, A_local, distribution = None):
    if distribution is None: distribution = [0 for i in range(len(A))]
    queue = np.random.choice(len(A_local), size=len(A_local), replace=False)
    for i in range(len(A_local)):
        count = random.randint(0, A_local[queue[i]])
        if count>needed:
            count = needed

        needed-=count
        A_local[queue[i]] -= count
        distribution[queue[i]]+=count
        if needed==0:break

    if needed == 0:
        return distribution, A_local
    else:
        return randDistribution(needed,A_local,distribution)


def createdIndividual(loc_A,loc_B):
    global A,B
    A,B = loc_A,loc_B
    routes = [[None for i in range(len(B))] for i in range(len(A))]
    np.random.rand()
    A_local = [i for i in A]
    for i in range(len(B)):
        distribution, A_local = randDistribution(B[i],A_local)
        for j in range(len(A)):
            routes[j][i] = distribution[j]

    return routes

POPULATION_SIZE = 300
P_CROSSOVER = 0.3
P_MUTATION = 1
MAX_GENERATION = 100

toolbox = base.Toolbox()

