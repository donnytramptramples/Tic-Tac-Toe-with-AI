from game.game import Game
from pygad import torchga
import pygad.torchga
from model import Model
from genetic_algorithm import GeneticAlgorithm


# CONFIG
class Config():
    NUM_SOLUTIONS = 50
    NUM_GENERATIONS = 200
    NUM_PARENTS_MATING = 5


config = Config()

game = Game()

model = Model()
torch_ga = pygad.torchga.TorchGA(model=model, num_solutions=config.NUM_SOLUTIONS)
initial_population = torch_ga.population_weights

ga = GeneticAlgorithm(initial_population, config.NUM_GENERATIONS, game=game)
ga.run()
