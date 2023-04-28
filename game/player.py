import pygame


class PLayer:

    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.height = 0
        self.velocity = 0
        self.super_jump = 0
        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))

        self.images = (pygame.image.load('static/dinorl.png'), pygame.image.load('static/dinoll.png'), pygame.image.load('static/dino.png'),
                       pygame.image.load('static/dinodll.png'), pygame.image.load('static/dinodrl.png'), pygame.image.load('static/dinod.png'))
        self.currimg = 0
        self.dimage = 0


    def control(self):
        self.rect = pygame.Rect((33, 375 - self.height), (20, 25))
        self.dimage = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.velocity == 0:
            self.velocity = 0.7
        if keys[pygame.K_SPACE] and self.velocity == 0 and self.super_jump == 0:
            self.velocity = 1.3
            self.super_jump = 50000
        if keys[pygame.K_s]:
            self.rect = pygame.Rect((30, 385 - self.height), (30, 15))
            self.dimage = 3

        self.height += self.velocity

        if self.super_jump > 0:
            self.super_jump -= 1

        if self.height > 0:
            self.velocity -= 0.003
        else:
            self.height = 0
            self.velocity = 0


    def draw(self):

        if self.height > 0:
            image = self.images[2+self.dimage]
        else:
            image = self.images[self.currimg+self.dimage]
            self.currimg = abs(self.currimg-1)

        self.screen.blit(image, (30, 375 - self.height))