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


# CONFIG
class Config():
    NUM_SOLUTIONS = 20
    NUM_GENERATIONS = 20
    NUM_PARENTS_MATING = 5

config = Config()

game = game.Game()

model = Model()
torch_ga = pygad.torchga.TorchGA(model=model, num_solutions=10)
initial_population = torch_ga.population_weights

def fitness_function(ga_instance ,solution, solution_index):
    model_weights_dict = torchga.model_weights_as_dict(model=model, weights_vector=solution)
    player = PLayer(game, model_weights_dict)
    score = 0
    while True:
        # player.get_move()
        player.draw()
        for object in game.obstacles:
            if object.rect.colliderect(player.rect):
                return score
        score += 1
        pygame.display.update()

def update_world():
    while True:
        game.screen.fill((255, 255, 255))
        game.generate_world()
        pygame.display.update()
        print(len(game.players))


def callback_generation(ga_instance):
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))

ga_instance = pygad.GA(
    num_generations=config.NUM_GENERATIONS,
    num_parents_mating=config.NUM_PARENTS_MATING,
    initial_population=initial_population,
    fitness_func=fitness_function,
    on_generation=callback_generation
)

def ga_run():
    p1 = Process(target=ga_instance.run())
    p1.start()
    p2 = Process(target=update_world())
    p2.start()
    p1.join()
    p2.join()

ga_run()
