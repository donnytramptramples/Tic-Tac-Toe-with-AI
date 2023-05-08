from game import Game
import pygame
import sys
import numpy as np
import random
import pickle
import operator

pygame.init()
screen = pygame.display.set_mode((895, 600))

num_of_generations = 500
population_size = 50
num_crossover_brains = 4
brains = []

def create_brain(input_size=5, hidden_size=3, out_size=1):
    '''
    creates neural network
    :param input_size: input vector size - default 5, same as size of vector returned by
                                                        get_game_state_vector function from game.py
    :param hidden_size: hidden layers size
    :param out_size: output size - default 2, 1 for jumping and 1 for dodge
    :return: neural network weights
    '''
    layer1 = np.array([[random.uniform(-1, 1) for i in range(input_size + 1)] for j in range(hidden_size)])
    layer2 = np.array([[random.uniform(-1, 1) for i in range(hidden_size + 1)] for j in range(hidden_size)])
    out_layer = np.array([[random.uniform(-1, 1) for i in range(hidden_size + 1)] for j in range(out_size)])
    return [layer1, layer2, out_layer]

def mutate(brain):
    '''
    mutates brain by adding small random values to network weights
    :param brain: list of nn layers
    :return: mutated brain
    '''
    new = []
    for layer in brain:
        new_layer = np.copy(layer)
        for i in range(new_layer.shape[0]):
            for j in range(new_layer.shape[1]):
                if random.uniform(0, 1) < 0.03:
                    new_layer[i][j] += random.uniform(-1, 1)
        new.append(new_layer)
    return new

def create_new_pop(brains):
    '''
    creates new population based on brains param (best brains from previous generation)
    :param brains: parent brains for population
    :return: brains population of size population_size
    '''
    new_pop = []
    for brain in brains:
        new_pop.append(brain)
    for i in range(population_size-len(brains)-2):
        new_pop.append(mutate(brains[random.randint(0, 1)]))
    for i in range(2):
        new_pop.append(create_brain(5, 3, 1))
    return new_pop


max_score = 0
for i in range(num_of_generations):

    _game = Game(screen, population_size)
    if i == 0:
        for j in range(population_size):
            brains.append(create_brain(5, 3, 1))
    else:
        brains = create_new_pop(brains)

    for player in _game.players:
        player.brain = brains.pop()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (0, 400), (900, 400))

        generation_text = pygame.font.Font('freesansbold.ttf', 30).render(f'generation {i}', False, (20, 20, 20))
        generation_text_rect = generation_text.get_rect()
        generation_text_rect.center = (700, 100)
        screen.blit(generation_text, generation_text_rect)

        score_text = pygame.font.Font('freesansbold.ttf', 30).render(f'max score {max_score}', False, (20, 20, 20))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (700, 150)
        screen.blit(score_text, score_text_rect)

        for player in _game.players:
            player.get_ai_move()
            player.draw()
            for object in _game.obstacles:
                if object.rect.colliderect(player.rect) and player in _game.players:
                    _game.players.remove(player)

        if len(_game.players) <= 4:
            _game.players.sort(key=operator.attrgetter('fitness_score'), reverse=True)
            best = _game.players[0]
            brains.append(_game.players[0].brain)
            brains.append(_game.players[1].brain)
            # for player in _game.players[:num_crossover_brains]:
            #     brains.append(player.brain)
            if best.score > max_score:
                max_score = best.score
            run = False

        _game.generate_world()
        pygame.display.update()

with open('trained_nn.pkl', 'wb') as file:
    pickle.dump(brains[0], file)