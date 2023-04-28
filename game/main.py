import time
import pygame
import sys
import game

pygame.init()
screen = pygame.display.set_mode((895, 600))

while True:
    _game = game.Game(screen)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (0, 400), (900, 400))
        score_text = pygame.font.Font('freesansbold.ttf', 30).render(f'{_game.players[0].score}', False, (20, 20, 20))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (800, 100)
        screen.blit(score_text, score_text_rect)

        for player in _game.players:
            player.control()
            player.draw()
        for object in _game.world_objects:
            if object.rect.colliderect(_game.players[0].rect):
                run = False

        _game.generate_world()
        pygame.display.update()

    game_over_text = pygame.font.Font('freesansbold.ttf', 30).render('GAME OVER', False, (200, 20, 20))
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (450, 100)
    screen.blit(game_over_text, game_over_text_rect)

    score_text = pygame.font.Font('freesansbold.ttf', 30).render(f'your score: {_game.players[0].score}', False, (200, 20, 20))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (450, 150)
    screen.blit(score_text, score_text_rect)

    press_space_text = pygame.font.Font('freesansbold.ttf', 30).render('press space to play again', False, (200, 20, 20))
    press_space_text_rect = game_over_text.get_rect()
    press_space_text_rect.center = (350, 200)
    screen.blit(press_space_text, press_space_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            time.sleep(0.5)
            break
