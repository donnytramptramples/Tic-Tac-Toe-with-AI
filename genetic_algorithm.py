import torch
import multiprocessing


class GeneticAlgorithm:

    def __init__(self, fitness, init_pop, num_generations):
        self.fitness = fitness
        self.population = init_pop
        self.num_generations = num_generations

    def run(self):
        for generation in range(self.num_generations):
            print(f'Generation: {generation + 1}')

            proc = []
            for solution in self.population:
                p = multiprocessing.Process(target=self.fitness, args=(solution,))
                p.start()
                proc.append(p)
            for p in proc:
                p.join()
