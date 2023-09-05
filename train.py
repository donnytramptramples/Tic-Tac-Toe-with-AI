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
    NUM_SOLUTIONS = 5
    NUM_GENERATIONS = 20
    NUM_PARENTS_MATING = 5

config = Config()

game = game.Game()

model = Model()
torch_ga = pygad.torchga.TorchGA(model=model, num_solutions=config.NUM_SOLUTIONS)
initial_population = torch_ga.population_weights

def fitness_function(ga_instance, solution, solution_index):
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


def callback_generation(ga_instance):
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))


ga_instance = pygad.GA(
    num_generations=config.NUM_GENERATIONS,
    num_parents_mating=config.NUM_PARENTS_MATING,
    initial_population=initial_population,
    fitness_func=fitness_function,
    on_generation=callback_generation,
    delay_after_gen=0.05
)
ga_instance.run()


