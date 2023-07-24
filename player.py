import math
import pygame
import numpy as np

class PLayer:
    '''
    class representing player

    Args:
        game (Game): game

    Attributes:
        score (int): score achieved by player
        height (int): height above surface
        velocity (int): vertical speed
        rect (pygame.Rect): rectangle around player used for detecting collisions
        game (game): game
        brain (list): list of numpy arrays containing neural network weights
        images (tuple): images used for animating run
        currimg (int): variable controling player animation
        dimage (int): variable controling player animation
    '''

    def __init__(self, game):
        self.score = 0
        self.height = 0
        self.velocity = 0
        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))
        self.game = game
        self.brain = []
        self.images = (pygame.image.load('static/dinorl.png'), pygame.image.load(
            'static/dinoll.png'), pygame.image.load('static/dino.png'),
                       pygame.image.load('static/dinodll.png'), pygame.image.load(
            'static/dinodrl.png'), pygame.image.load('static/dinod.png'))
        self.currimg = 0
        self.dimage = 0
        self.fitness_score = 0


    def control(self):
        '''
        controling player movement by human
        w - jumping
        s - dodgeing
        '''
        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))
        self.dimage = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.velocity == 0:
            self.velocity = 0.7
        if keys[pygame.K_s]:
            self.rect = pygame.Rect((30, 385 - self.height), (30, 15))
            self.dimage = 3

        self.height += self.velocity

        if self.height > 0:
            self.velocity -= 0.0025
        else:
            self.height = 0
            self.velocity = 0


    def draw(self):
        ''' drawing player '''
        if self.height > 0:
            image = self.images[2+self.dimage]
        else:
            image = self.images[self.currimg+self.dimage]
            self.currimg = abs(self.currimg-1)

        self.game.screen.blit(image, (30, 375 - self.height))


    def get_move(self):
        input = np.array(self.game.get_game_state_vector())
        output = self.brain.predict(np.atleast_2d(input))

        if output[0] > 0.5 and self.velocity == 0:
            self.velocity = 0.7
        elif output[0] < 0.5:
            self.rect = pygame.Rect((30, 385 - self.height), (30, 15))
            self.dimage = 3
        else:
            self.fitness_score += 10
            pass

        self.height += self.velocity

        if self.height > 0:
            self.velocity -= 0.003
        else:
            self.height = 0
            self.velocity = 0
