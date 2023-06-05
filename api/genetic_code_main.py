import array
import importlib
import time
from math import ceil

import numpy
import numpy as np
from deap import base, algorithms
from deap import creator
from deap import tools
import algelitism
import random

import Data
from mutation import cxUniformCastom, mutCastom
from other import Print
from setting import POPULATION_SIZE, toolbox, P_CROSSOVER, P_MUTATION, MAX_GENERATION, createdIndividual

def detectionFitness(Data,individual):
    cost = 0
    A,B = Data.giveWithoutExcess()
    distance_between_destinations = Data.distance_between_destinations
    for i in range(len(A)):
        if distance_between_destinations is None:
            for j in range(len(B)):
                count = ceil(float(individual[i][j])/float(Data.capacity))
                cost+= Data.costs_table[i][j] * count
        else:
            way = makeWay(individual[i][:len(B)], Data.costs_table[i], distance_between_destinations,Data.capacity)
            if individual.ways is None:
                individual.ways = []
            individual.ways.append(way) #individual объект класса наследуемый от list, но также имеет свои поля.
            for j in range(len(way)):
                if len(way[j]) > 0: # если элементов в массиве нету, значит мы не начинаем цепочку через эту точку. Она находиться в другой цепочке.
                        quantity = 0
                        sum_distance_in_chain = 0
                        for chain_index in range(len(way[j])):
                            destination_index = way[j][chain_index]
                            quantity+=individual[i][destination_index]
                            if chain_index==0: # первая точка в цепочке идет от поставщика
                                sum_distance_in_chain+=Data.costs_table[i][j]
                            else:
                                sum_distance_in_chain+=distance_between_destinations[way[j][chain_index-1]][destination_index]

                        count = ceil(float(quantity) / float(Data.capacity))
                        cost += sum_distance_in_chain * count  #если доставка идет только до одной точки без цепочки, то в sum_distance_in_chain будет храниться значение только до неё




    return cost,



def nearestPoints(distribution_points, distance_between_destinations):
    nearest_points_indexes = [[] for i in range(len(distribution_points))]

    for i in range(len(distribution_points)):
        if distribution_points[i] !=0:
            nearest_points_indexes[i] = [index for index, value in sorted(enumerate(distance_between_destinations[i]), key=lambda x: x[1])][1:]  # соритруем от ближних к дальним точкам.

    return nearest_points_indexes

def makeWay(distribution_points, distances, distance_between_destinations,capacity):
    ways = [[] for i in distribution_points] #двойной массив, где каждый элемент хранит последовательность прохождения по точкам, начиная с индекса текущего элемента
    points_remains = len(list(filter(lambda x: x != 0, distribution_points))) #сколько точек осталось пройти
    nearest_points_indexes = nearestPoints(distribution_points,distance_between_destinations) #двойной массив, с отсортированным точкам для каждой точкой, от ближних к дальним
    pass_points = []#точки, через которые мы уже прошли


    while points_remains>0:
        nearest = None
        nearest_index = None
        for i in range(len(distribution_points)):
            if distribution_points[i]>0 and (nearest is None or distances[i]<nearest) and i not in pass_points:
                nearest = distances[i]
                nearest_index = i

        ways[nearest_index].append(nearest_index)
        points_remains-=1
        pass_points.append(nearest_index)
        point_index = nearest_index
        quantity = distribution_points[point_index]
        while points_remains>0 and quantity<capacity: #ищет всё точки, через которые можно пройти за раз, начиная с текущей, с учетом вместимости транспортного средства
            point_found = False
            for near in nearest_points_indexes[point_index]:#смысл цикла в том, чтобы найти одну ближайшую точку относительно текущей, которая будет ближе к текущей, чем к поставщику
                if near in pass_points: #проверяем, является ли текущая точка уже пройденой
                    continue
                if distribution_points[near] == 0:
                    continue
                if quantity+distribution_points[near]>capacity: #если к количеству товара прибавить, необходимый для данной точки и получиться больше вместимости транспортного средства, то такая точка не станет частью данной цепочки поставки
                    continue
                elif distance_between_destinations[point_index][near] < distances[near]: #проверяю расстояние от поставщика до точки, которые находиться близко с текущей точкой, чтобы сравнить, ближе ли она к прошлой точке назначения или к поставщику
                    point_index = near
                    ways[nearest_index].append(point_index)
                    points_remains -= 1
                    pass_points.append(point_index)
                    quantity+=distribution_points[point_index]
                    point_found = True #из всех точек была найдена подходящая по условиям. Значит теперь можно искать продолжать искать ближайшую уже для новой точки.
                    break
            if not point_found:
                break

    return ways






def Start(data):

    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax, ways=None)

    toolbox.register("randIndividual", createdIndividual, data.A, data.B)
    toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randIndividual)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    toolbox.register("individualCopy", tools.initIterate, creator.Individual)



    population = toolbox.populationCreator(n=POPULATION_SIZE)


    toolbox.register("evaluate", detectionFitness, data)
    toolbox.register("select", tools.selTournament, tournsize=int(POPULATION_SIZE / 23))
    toolbox.register("mate", cxUniformCastom, data)
    toolbox.register("mutate", mutCastom, data)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)


    hof = tools.HallOfFame(5)
    copy = [toolbox.individualCopy(generator=lambda :[[j for j in i] for i in n]) for n in population]
    copy, logbook = algelitism.eaSimpleElitism(copy,toolbox,
                                              cxpb=P_CROSSOVER,
                                              mutpb=P_MUTATION,
                                              ngen=MAX_GENERATION,
                                              stats=stats,
                                              halloffame=hof,
                                              verbose=True,
                                                 )

    maxFitnessValues, meanFitnessValues = logbook.select("min","avg")



    return hof[0]


if __name__ == "__main__":
    Start(Data.Data([1, 20],[1, 1, 1, 1, 1, 1],
                    [
                        [245.86, 2386.55, 14791.71,  11584.7, 1929.11, 1523079.13],
                        [481.54, 2106.8,  14772.3, 10983.09, 1327.51, 1522350.75],

                    ],20,

                    [
                        [0,   2401.75, 15067.24, 11278.04, 1622.45, 1522772.38],

                        [2169.99, 0 ,  13650.49, 9861.29, 835.02, 1518731.38],

                        [15163.42, 13297.31, 0,   4351.81, 13884.92, 1505332.88],

                        [11792.69, 9926.58, 3330.41, 0,   10514.19, 1507816.5],

                        [1551.34, 779.29, 13444.79, 9655.59, 0,   1518525.63],

                        [1526956.13, 1525694.5, 1512921.13, 1520163, 1525677.63, 0]
,
                    ]
                    ))