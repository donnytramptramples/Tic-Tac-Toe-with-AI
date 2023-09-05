import time
import pygame
import sys
import game
from player import PLayer
import pygad
from pygad import torchga
import torch
import pygad.torchga
from model import Model
from multiprocessing import Process
from genetic_algorithm import GeneticAlgorithm


# CONFIG
class Config():
    NUM_SOLUTIONS = 5
    NUM_GENERATIONS = 20
    NUM_PARENTS_MATING = 5

config = Config()

game = game.Game()

model = Model()
torch_ga = pygad.torchga.TorchGA(model=model, num_solutions=config.NUM_SOLUTIONS)
initial_population = torch_ga.population_weights

def fitness_function(solution):
    model_weights_dict = torchga.model_weights_as_dict(model=model, weights_vector=solution)
    player = PLayer(game, model_weights_dict)
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        game.screen.fill((255, 255, 255))
        pygame.draw.line(game.screen, (0, 0, 0), (0, 400), (900, 400))

        player.get_move()
        player.draw()

        for object in game.obstacles:
            if object.rect.colliderect(player.rect):
                return int(score)

        score += 0.01
        game.generate_world()
        pygame.display.update()


ga = GeneticAlgorithm(fitness_function, initial_population)
ga.run()
