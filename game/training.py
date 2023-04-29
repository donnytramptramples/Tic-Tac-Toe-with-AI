import game
import pygame
import sys
from player import PLayer
import numpy as np
import random

pygame.init()
screen = pygame.display.set_mode((895, 600))

num_of_generations = 40
population_size = 20
num_crossover_brains = 4
brains = []

def create_brain(input_size, hidden_size, out_size):
    layer1 = np.array([[random.uniform(-1, 1) for i in range(input_size + 1)] for j in range(hidden_size)])
    layer2 = np.array([[random.uniform(-1, 1) for i in range(hidden_size + 1)] for j in range(hidden_size)])
    out_layer = np.array([[random.uniform(-1, 1) for i in range(hidden_size + 1)] for j in range(out_size)])
    return [layer1, layer2, out_layer]

def mutate(brain):
    new = []
    for layer in brain:
        new_layer = np.copy(layer)
        for i in range(new_layer.shape[0]):
            for j in range(new_layer.shape[1]):
                if random.uniform(0, 1) < 0.1:
                    new_layer[i][j] += random.uniform(-1, 1)*0.1
        new.append(new_layer)
    return new

def create_new_pop(brains):
    new_pop = []
    for brain in brains:
        new_pop.append(brain)
    for brain in brains:
        new_pop.append(mutate(brain))
    for i in range(population_size - len(new_pop)):
        new_pop.append(create_brain(3, 15, 2))
    return new_pop



for i in range(num_of_generations):

    _game = game.Game(screen, population_size)
    if i == 0:
        for j in range(population_size):
            brains.append(create_brain(3, 15, 2))
    else:
        brains = create_new_pop(brains)
        print(len(brains))

    for player in _game.players:
        player.brain = brains.pop()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (0, 400), (900, 400))
        score_text = pygame.font.Font('freesansbold.ttf', 30).render(f'generation {i}', False, (20, 20, 20))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (800, 100)
        screen.blit(score_text, score_text_rect)

        for player in _game.players:
            player.get_ai_move()
            player.draw()
            for object in _game.world_objects:
                if object.rect.colliderect(player.rect) and player in _game.players:
                    _game.players.remove(player)

        if len(_game.players) == num_crossover_brains:
            for player in _game.players:
                brains.append(player.brain)
            run = False
        if len(_game.players) == 0:
            run = False

        _game.generate_world()
        pygame.display.update()
