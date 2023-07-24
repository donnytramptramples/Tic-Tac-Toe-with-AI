from keras.layers import Dense
from keras.models import Sequential
from sklearn.preprocessing import StandardScaler
import random
import numpy as np
from game import Game
import pygame
import sys



num_of_brains_in_pop = 10
num_of_generations = 30
population = []


def create_model():
    model = Sequential([
        Dense(5, activation='relu', input_shape=(5,)),
        Dense(7, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='mse', optimizer='adam')
    model.build()
    return model


def brain_crossover(brain1, brain2):
    weights1 = brain1.get_weights()
    weights2 = brain2.get_weights()

    new_weights = []

    for i in range(len(weights1)):
        new_weights.append(random.choice((weights1, weights2))[i])

    new_brain = create_model()
    new_brain.set_weights(new_weights)
    return new_brain

def brain_mutate(brain):
    weights = brain.get_weights()
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if (random.uniform(0, 1) > .85):
                change = random.uniform(-.5, .5)
                weights[i][j] += change
    new_brain = create_model()
    new_brain.set_weights(weights)
    return new_brain

def create_new_population(brain1, brain2):
    new_population = []
    main_brain = brain_crossover(brain1, brain2)
    for i in range(num_of_brains_in_pop):
        new_population.append(brain_mutate(main_brain))
    return new_population



pygame.init()
screen = pygame.display.set_mode((895, 600))
max_score = 0
for i in range(num_of_generations):

    _game = Game(screen, num_of_brains_in_pop)
    if i == 0:
        for j in range(num_of_brains_in_pop):
            population.append(create_model())
    else:
        population = create_new_population(population[0], population[1])

    for player in _game.players:
        player.brain = population.pop()

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
            player.get_move()
            player.draw()
            for object in _game.obstacles:
                if object.rect.colliderect(player.rect) and player in _game.players:
                    _game.players.remove(player)

        if len(_game.players) <= 2:
            population.append(_game.players[0].brain)
            population.append(_game.players[1].brain)
            if _game.players[0].score > max_score:
                max_score = _game.players[0].score
            run = False

        _game.generate_world()
        pygame.display.update()
