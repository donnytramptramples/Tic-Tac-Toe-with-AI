import player
from obstacles import Bird, Cactus
import random
from operator import attrgetter
import pygame
import sys
import time


class Game:
    '''
    class representing game
    Args:
        screen : pygame display window
        num_players (int) : number of players, used for nn training
    Attributes:
        screen : pygame display window
        obstacles (list): obstacles which player must avoid to survive
        players (list): list of players
        game_speed (int): speed of obstacles moveing towards player
    '''

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((895, 600))
        self.obstacles = [Cactus(self.screen, 900), Cactus(self.screen, 1400)]
        self.players = []
        self.game_speed = 0.3

    def game_loop(self):

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill((255, 255, 255))
            pygame.draw.line(self.screen, (0, 0, 0), (0, 400), (900, 400))
            score_text = pygame.font.Font('freesansbold.ttf', 30).render(f'{self.players[0].score}', False,
                                                                         (20, 20, 20))
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (800, 100)
            self.screen.blit(score_text, score_text_rect)

            for player in self.players:
                player.control()
                player.draw()
            for object in self.obstacles:
                if object.rect.colliderect(self.players[0].rect):
                    run = False
            self.generate_world()
            pygame.display.update()

        game_over_text = pygame.font.Font('freesansbold.ttf', 30).render('GAME OVER', False, (200, 20, 20))
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = (450, 100)
        self.screen.blit(game_over_text, game_over_text_rect)

        score_text = pygame.font.Font('freesansbold.ttf', 30).render(f'your score: {self.players[0].score}', False,
                                                                         (200, 20, 20))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (450, 150)
        self.screen.blit(score_text, score_text_rect)

        press_space_text = pygame.font.Font('freesansbold.ttf', 30).render('press space to play again', False,
                                                                               (200, 20, 20))
        press_space_text_rect = game_over_text.get_rect()
        press_space_text_rect.center = (350, 200)
        self.screen.blit(press_space_text, press_space_text_rect)

        pygame.display.update()

        # while True:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             sys.exit()
        #     keys = pygame.key.get_pressed()
        #     if keys[pygame.K_SPACE]:
        #         time.sleep(0.5)
        #         break

        return score


    def generate_world(self):
        '''
        randomly creates new obstacles
        '''
        if len(self.obstacles) < 3:
            for i in range(5):
                self.obstacles.append(Cactus(self.screen, random.randint(900 + 1000 * i, 1500 + 1000*i)))
            if not random.randint(0, 5):
                self.obstacles.append(Bird(self.screen, random.randint(1000, 1200)))

        for object in self.obstacles:
            if object.position < -100:
                self.obstacles.remove(object)
                for player in self.players:
                    player.score += 10
                    player.fitness_score += 10
                if len(self.players) > 0:
                    if self.players[0].score % 100 == 0:
                        self.game_speed += 0.05
            object.move(self.game_speed)
            object.draw()

    def get_game_state_vector(self):
        '''
        return list representing current game state vector
        where:
        list[0] - game speed
        list[1] - distance to nearest obstacle
        list[2] - height of nearest obstacle
        list[3] - distance to 2nd nearest obstacle
        list[4] - height of 2nd nearest obstacle
        '''
        nearest_obstacle = sorted([world_object for world_object in self.obstacles if world_object.position > 30], key=attrgetter('position'))
        return [self.game_speed, nearest_obstacle[0].position, nearest_obstacle[0].height, nearest_obstacle[1].position, nearest_obstacle[1].height]


