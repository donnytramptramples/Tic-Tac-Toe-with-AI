import player
from obstacles import Bird, Cactus
import random
from operator import attrgetter

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

    def __init__(self, screen, num_players):
        self.screen = screen
        self.obstacles = [Cactus(self.screen, random.randint(900 + 200*i, 1500 + 200*i)) for i in range(5)]
        self.players = [player.PLayer(self) for i in range(num_players)]
        self.game_speed = 0.2

    def generate_world(self):
        '''
        randomly creates new obstacles
        '''
        if len(self.obstacles) < 5:
            for i in range(5):
                self.obstacles.append(Cactus(self.screen, random.randint(900 + 200*i, 1100 + 200*i)))
            if not random.randint(0, 5):
                self.obstacles.append(Bird(self.screen, random.randint(1000, 1200)))

        for object in self.obstacles:
            if object.position < -100:
                self.obstacles.remove(object)
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
        list[3] - distance to 2nd nearest obstacle
        list[4] - height of 2nd nearest obstacle
        '''
        nearest_obstacle = sorted([world_object for world_object in self.obstacles if world_object.position > 30], key=attrgetter('position'))
        return [self.game_speed, nearest_obstacle[0].position, nearest_obstacle[0].height, nearest_obstacle[1].position, nearest_obstacle[1].height]


