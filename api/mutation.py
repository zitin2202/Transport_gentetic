import importlib
import random

import numpy

from other import randomWithException, searchValueInMassiveWithMinHoriz, \
    searchValueInMassiveWithMinVerticl, Print, searchRandWithMinHoriz, searchRandWithMinVerticl
import Data
from setting import toolbox

A = []
B = []
costs_table = []

def rebalanceAorB(rebalance_coord, individual, index_a, index_b, unbalance, another_index=None):

    if rebalance_coord == "A":
        if another_index is None: another_index = searchRandWithMinHoriz(individual,index_a,-unbalance, lambda: randomWithException(0,len(B) - 1, index_b))
        coord_y = index_a
        coord_x = another_index
    else:
        if another_index is None: another_index = searchRandWithMinVerticl(individual,index_b,-unbalance, lambda: randomWithException(0,len(A) - 1, index_a))
        coord_y = another_index
        coord_x = index_b


    new_count_another = individual[coord_y][coord_x] + unbalance

    diff = individual[coord_y][coord_x] - new_count_another
    unbalance += diff
    individual[coord_y][coord_x] = new_count_another

    return individual, another_index, diff


def rebalance(individual, index_a, index_b, unbalance):
    new_b_unbalance_coord = None
    new_a_unbalance_coord = None


    individual, new_b_unbalance_coord, new_unbalance = rebalanceAorB("A", individual, index_a, index_b, unbalance)

    if searchValueInMassiveWithMinVerticl(individual, new_b_unbalance_coord, -new_unbalance, index_a):
        individual, new_a_unbalance_coord, new_unbalance = rebalanceAorB("B", individual, index_a, new_b_unbalance_coord,
                                                                                  new_unbalance)
    else:
        return False

    if individual[new_a_unbalance_coord][index_b] + new_unbalance <0:
        return False
    individual, new_a_unbalance_coord, new_unbalance = rebalanceAorB("A", individual, new_a_unbalance_coord, None, new_unbalance, index_b)

    return individual



def changeValue(individual, index_a, index_b, value):

    new_individual = toolbox.individualCopy(generator=lambda: [[j for j in i] for i in individual])
    last_count = individual[index_a][index_b]
    new_individual[index_a][index_b] = value
    diff_count = last_count - value

    if searchValueInMassiveWithMinHoriz(new_individual,index_a,-diff_count, index_b) and searchValueInMassiveWithMinVerticl(new_individual,index_b,-diff_count,index_a):
        new_individual = rebalance(new_individual, index_a, index_b, diff_count)
    else:
        return False

    return new_individual



def mutCastom(Data,individual):
    global A,B,costs_table
    A,B,costs_table = Data.A,Data.B,Data.costs_table

    while True:
        index_a = random.randint(0, len(A)-1)
        index_b = random.randint(0, len(B)-1)
        last_count = individual[index_a][index_b]



        new_count = randomWithException(0,min(A[index_a],B[index_b]),last_count)

        new_individual = changeValue(individual,index_a,index_b,new_count)
        if new_individual is False:
            continue

        individual = new_individual

        return individual,


def cxUniformCastom(Data,ind1, ind2):
    count = 0
    global A,B,costs_table
    A,B,costs_table = Data.A,Data.B,Data.costs_table

    while True:
        index_a = random.randint(0, len(A)-1)
        index_b = random.randint(0, len(B)-1)

        new_ind1 = changeValue(ind1,index_a,index_b,ind2[index_a][index_b])
        new_ind2 = changeValue(ind2,index_a,index_b,ind1[index_a][index_b])
        if (new_ind1 is False or new_ind2 is False):
            continue
        else:
            break

    ind1, ind2 = new_ind1, new_ind2


    return ind1, ind2
