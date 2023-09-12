import random
import matplotlib.pyplot as plt
import torch
from game.player import Player
from pygad import torchga
from model import Model
from torch.nn.utils import parameters_to_vector
import pygame
import sys
import os


class GeneticAlgorithm:

    def __init__(self, init_pop, num_generations, game=None):
        self.population = init_pop
        self.num_solutions = len(init_pop)
        self.num_generations = num_generations
        self.game = game
        self.num_parents_mating = 5
        self.keep_parents = False
        self.scores = []
        self.mutation_rate = 0.3


    def run(self):
        '''
        Main loop
        creates new population and selects best instances for next one, self.num_generation times
        '''
        for generation in range(self.num_generations):
            print(f'Generation: {generation + 1}')
            self.get_generation_scores()
            self.create_new_pop()
            self.game.obstacles.pop(0)
        self.scores_curve()

        torch.save(self.game.players[0].brain.state_dict(), f'{os.getcwd()}\models')

    def get_generation_scores(self):
        '''
        Runs game for newly created generation, stopped when there is self.num_parents_mating players left
        '''
        self.game.players = [Player(self.game, torchga.model_weights_as_dict(model=Model(), weights_vector=weights)) for weights in self.population]
        self.game.game_speed = 2.5
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            for player in self.game.players:
                player.get_move()
                for obstacle in self.game.obstacles:
                    if obstacle.rect.colliderect(player.rect):
                        self.game.players.remove(player)

            if len(self.game.players) <= self.num_parents_mating:
                score = max((player.score for player in self.game.players))
                self.scores.append(score)
                return

            self.game.generate_world()

    def create_new_pop(self):
        '''
        creates new population based on best players from previous one,
        '''
        parents_params = [parameters_to_vector(player.brain.parameters()).tolist() for player in self.game.players]
        new_population = parents_params if self.keep_parents else []
        while len(new_population) < self.num_solutions:
            new_population.append(self.crossover(parents_params[0], parents_params[1]))


    def crossover(self, parent1, parent2):
        '''
        creates new player based on two parents
        '''
        crossover_point = random.randint(1, len(parent1) - 1)
        child = self.mutate(parent1[:crossover_point] + parent2[crossover_point:])
        return torch.tensor(child)


    def mutate(self, weights):
        '''
        introduces minor modifications to the model's weights vector
        '''
        for parameter in weights:
            if random.random() < self.mutation_rate:
                parameter += random.uniform(-0.1, 0.1)
        return weights

    def scores_curve(self):
        '''
        ploting score chart per generation
        '''
        plt.plot(range(1, len(self.scores) + 1), self.scores)
        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title('Max scores of each generation')
        plt.grid(True)
        plt.show()
