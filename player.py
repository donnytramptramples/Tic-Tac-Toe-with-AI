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


    def get_ai_move(self):
        '''
        controling player movement using neural network
        brain gets input vector from get_game_state_vector function and computes output vector
        whose first position controls jumping and second dodgeing
        '''
        layer1 = self.brain[0]
        layer2 = self.brain[1]
        out_layer = self.brain[2]

        input = self.game.get_game_state_vector()
        input = list(np.array(input).flatten()) + [1]

        result1 = np.array([math.tan(np.dot(input, layer1[i])) for i in range(layer1.shape[0])] + [1])
        result2 = np.array([math.tan(np.dot(result1, layer2[i])) for i in range(layer2.shape[0])] + [1])
        output = np.array([math.tan(np.dot(result2, out_layer[i])) for i in range(out_layer.shape[0])])

        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))
        self.dimage = 0

        if output[0] > 0 and self.velocity == 0:
            self.velocity = 0.7
            self.score -= 2
        if output[1] > 0:
            self.rect = pygame.Rect((30, 385 - self.height), (30, 15))
            self.dimage = 3
            self.score += 2

        self.height += self.velocity

        if self.height > 0:
            self.velocity -= 0.003
        else:
            self.height = 0
            self.velocity = 0
