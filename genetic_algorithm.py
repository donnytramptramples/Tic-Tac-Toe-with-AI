import torch


class GeneticAlgorithm():

    def __init__(self, fitness, init_pop):
        self.fitness = fitness
        self.population = init_pop

    def run(self):
        for solution in self.population:
            print(type(solution))
            fitness = self.fitness(solution)
            print(fitness)
