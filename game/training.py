import game
import pygame
import sys

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

        print(_game.get_game_state_vector())
        _game.generate_world()
        pygame.display.update()