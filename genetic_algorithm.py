import torch
import multiprocessing
from player import Player
from pygad import torchga
from model import Model


class GeneticAlgorithm:

    def __init__(self, fitness, init_pop, num_generations, game=None):
        self.fitness = fitness
        self.population = init_pop
        self.num_generations = num_generations
        self.game = game
        self.num_parents_mating = 4
        self.keep_parents = True


    def run(self):
        for generation in range(self.num_generations):
            print(f'Generation: {generation + 1}')

            self.generation()

    def generation(self):
        self.game.players = [Player(self.game, torchga.model_weights_as_dict(model=Model(), weights_vector=weights)) for weights in self.population]

        score = 0

        while True:
            for player in self.game.players:
                player.get_move()
                player.draw()
                for obstacle in self.game.obstacles:
                    if obstacle.rect.colliderect(player.rect):
                        self.game.players.remove(player)
                        self.game.obstacles.remove(obstacle)

            if len(self.game.players) <= self.num_parents_mating:
                print(score)
                return

            score += 0.01

            self.game.generate_world()

    def create_new_pop(self):
        self.game.players[0].brain.