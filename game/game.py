import player
from world_objects import Bird, Cactus
import random
from operator import attrgetter

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.world_objects = [Cactus(self.screen, random.randint(900 + 200*i, 1500 + 200*i)) for i in range(5)]
        self.players = [player.PLayer(screen)]
        self.game_speed = 0.2

    def generate_world(self):
        if len(self.world_objects) < 5:
            for i in range(5):
                self.world_objects.append(Cactus(self.screen, random.randint(900 + 200*i, 1500 + 200*i)))
            if not random.randint(0, 5):
                self.world_objects.append(Bird(self.screen, random.randint(20, 40), random.randint(1000, 1200)))

        for object in self.world_objects:
            if object.position < -100:
                self.world_objects.remove(object)
                for player in self.players:
                    player.score += 10
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
        '''
        nearest_obstacle = min([world_object for world_object in self.world_objects if world_object.position > 30], key=attrgetter('position'))
        return [self.game_speed, nearest_obstacle.position, nearest_obstacle.height]


