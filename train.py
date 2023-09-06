import time
import pygame
import sys
import game
from player import Player
import pygad
from pygad import torchga
import torch
import pygad.torchga
from model import Model
import multiprocessing
from multiprocessing import Process
from genetic_algorithm import GeneticAlgorithm
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

# CONFIG
class Config():
    NUM_SOLUTIONS = 15
    NUM_GENERATIONS = 250
    NUM_PARENTS_MATING = 5


config = Config()

game = game.Game()

model = Model()
torch_ga = pygad.torchga.TorchGA(model=model, num_solutions=config.NUM_SOLUTIONS)
initial_population = torch_ga.population_weights

def fitness_function(ga_instance, solution, sol_idx):
    model_weights_dict = torchga.model_weights_as_dict(model=model, weights_vector=solution)
    player = (Player(game, model_weights_dict))
    score = 0

    while True:
        game.screen.fill((255, 255, 255))
        pygame.draw.line(game.screen, (0, 0, 0), (0, 400), (900, 400))

        player.get_move()
        player.draw()
        for obstacle in game.obstacles:
            if obstacle.rect.colliderect(player.rect):
                game.obstacles.remove(obstacle)
                return int(score)

        score += 0.01

        game.generate_world()
        pygame.display.update()

#
# def update_world():
#     print('world')
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#
#         game.screen.fill((255, 255, 255))
#         pygame.draw.line(game.screen, (0, 0, 0), (0, 400), (900, 400))
#
#         game.generate_world()
#         pygame.display.update()



def callback_generation(ga_instance):
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))



# ga_instance = pygad.GA(
#     num_generations=config.NUM_GENERATIONS,
#     num_parents_mating=config.NUM_PARENTS_MATING,
#     initial_population=initial_population,
#     fitness_func=fitness_function,
#     on_generation=callback_generation,
#
# )
# ga_instance.run()
ga = GeneticAlgorithm(fitness_function, initial_population, config.NUM_GENERATIONS, game=game)
ga.run()

# process1 = multiprocessing.Process(target=update_world)
# process2 = multiprocessing.Process(target=ga.run)
#
# process1.start()
# process2.start()
#
# process1.join()
# process2.join()