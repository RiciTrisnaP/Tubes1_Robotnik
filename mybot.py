from game.logic.base import BaseLogic
import time
from game.models import Board, GameObject, Position
from typing import Optional
from ..util import get_direction, position_equals


class MyBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
    
    def next_move(self, board_bot: GameObject, board: Board):
        # for i in board.game_objects:
        #     if i.type == "TeleportGameObject":
        #         print(i.position)
        props = board_bot.properties
        current_position = board_bot.position
        diamond = board.diamonds
        base = board_bot.properties.base
        # Analyze new state
        if props.diamonds == 5 and current_position != base:
            # Move to base
            self.goal_position = base
        else:
            if props.diamonds == 4:
                self.goal_position = self.optimum_position(diamond, board, current_position, 1)
            else:
                self.goal_position = self.optimum_position(diamond, board, current_position, 2)
        
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        # for i in board.game_objects:
        #     print(i.type)

        if delta_x != delta_y:
            return delta_x, delta_y
        else:
            return 0,1
    
    def optimum_position(self, diamond, board: Board, current_position, weight_max):
        target_position = current_position
        min_distance = 100
        for i in diamond:
            if self.distance(i.position, current_position, i.properties.points) < min_distance and i.properties.points <= weight_max:
                min_distance = self.distance(i.position, current_position, i.properties.points)
                target_position = i.position
        return target_position

    def distance(self, a : Position, b : Position, weight : int) -> float:
        return  (abs(a.x - b.x) + abs(a.y - b.y)) / weight