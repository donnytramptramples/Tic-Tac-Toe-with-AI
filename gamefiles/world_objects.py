import pygame


class Bird:
    def __init__(self, screen, height, pos):
        self.screen = screen
        self.height = height
        self.position = pos
        self.rect = pygame.Rect((self.position - 2, 402 - self.height), (20, 20))
        self.images = (pygame.image.load('static/bird1.png'), pygame.image.load('static/bird2.png'))
        self.currimg = 0


    def draw(self):
        self.screen.blit(self.images[self.currimg], (self.position - 4, 400 - self.height))
        self.currimg = abs(self.currimg - 1)

    def move(self, value):
        self.position -= value + 0.1
        self.rect = pygame.Rect((self.position - 2, 402 - self.height), (15, 15))


class Cactus:
    def __init__(self, screen, pos):
        self.screen = screen
        self.position = pos
        self.rect = pygame.Rect((self.position+3, 378), (10, 20))
        self.image = pygame.image.load('static/cactus.png')
        self.height = 0

    def draw(self):
        self.screen.blit(self.image, (self.position, 377))

    def move(self, value):
        self.position -= value
        self.rect = pygame.Rect((self.position+3, 378), (10, 25))