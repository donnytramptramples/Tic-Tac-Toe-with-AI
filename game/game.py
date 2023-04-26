import time

import pygame
import sys
from player import PLayer
from world_objects import Bird, Cactus
import random

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.world_objects = []
        self.player = PLayer(screen)
        self.game_speed = 0.2
        self.score = 0

    def game_loop(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill((255, 255, 255))
            pygame.draw.line(self.screen, (0, 0, 0), (0, 400), (900, 400))
            score_text = pygame.font.Font('freesansbold.ttf', 30).render(f'{self.score}', False, (20, 20, 20))
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (800, 100)
            self.screen.blit(score_text, score_text_rect)

            self.player.control()
            self.player.draw()
            self.generate_world()

            for object in self.world_objects:
                if object.rect.colliderect(self.player.rect):
                        run = False

            pygame.display.update()



    def generate_world(self):

        if len(self.world_objects) < 5:
            for i in range(5):
                self.world_objects.append(Cactus(self.screen, random.randint(900 + 200*i, 1500 + 200*i)))
            if not random.randint(0, 5):
                self.world_objects.append(Bird(self.screen, random.randint(20, 40), random.randint(1000, 1200)))

        for object in self.world_objects:
            if object.position < -100:
                self.world_objects.remove(object)
                self.score += 10
                if self.score % 100 == 0:
                    self.game_speed += 0.05
            object.move(self.game_speed)
            object.draw()
