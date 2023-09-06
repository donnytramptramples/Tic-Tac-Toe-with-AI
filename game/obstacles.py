import pygame
import random
import os


class Obstacle:
    '''
    class representing obstacle
    :arg screen : pygame display window
    :arg pos (int): obstacle position
    '''
    def __init__(self, screen, pos):
        self.screen = screen
        self.position = pos

class Bird(Obstacle):
    '''
    class representing Bird
    :arg height (int): obstacle height above surface
    :arg rect (pygame.Rect): rectangle around obstacle, used for detecting collisions
    :arg images (tuple) : images used for animating bird
    :arg currimg : variable used for controling bird animation
    '''
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.height = random.randint(20, 40)
        self.rect = pygame.Rect((self.position - 2, 402 - self.height), (20, 20))
        self.images = (pygame.image.load(os.path.join(os.getcwd(), '/game/static/bird1.png')), pygame.image.load(os.path.join(os.getcwd(), '/game/static/bird2.png')))
        self.currimg = 0


    def draw(self):
        ''' drawing obstacle '''
        self.screen.blit(self.images[self.currimg], (self.position - 4, 400 - self.height))
        self.currimg = abs(self.currimg - 1)

    def move(self, value):
        ''' moveing obstacle by value '''
        self.position -= value + 0.1
        self.rect = pygame.Rect((self.position - 2, 402 - self.height), (15, 15))


class Cactus(Obstacle):
    '''
    class representing Cactus
    :arg height (int): obstacle height above surface
    :arg rect (pygame.Rect): rectangle around obstacle, used for detecting collisions
    :arg image : cactus image
    '''
    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        self.rect = pygame.Rect((self.position+3, 378), (10, 20))
        self.image = pygame.image.load(f'{os.getcwd()}\game\static\cactus.png')
        self.height = 0

    def draw(self):
        ''' drawing obstacle '''
        self.screen.blit(self.image, (self.position, 377))

    def move(self, value):
        ''' moveing obstacle by value '''
        self.position -= value
        self.rect = pygame.Rect((self.position+3, 378), (10, 25))