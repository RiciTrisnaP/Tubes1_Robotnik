from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from typing import Optional
from ..util import get_direction


class Rici(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        diamond = board.diamonds
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        elif props.diamonds == 4:
            self.goal_position = self.optimum_position(diamond, board, current_position, 1)
        else:
            self.goal_position = self.optimum_position(diamond, board, current_position, 2)
        
        # We are aiming for a specific position, calculate delta
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
            
        return delta_x, delta_y
    
    def optimum_position(self, diamond, board: Board, current_position, weight_max):
        min_distance = self.distance(diamond[0].position, current_position, diamond[0].properties.points)
        target_position = diamond[0].position
        for i in diamond:
            if self.distance(i.position, current_position, i.properties.points) < min_distance and i.properties.points <= weight_max:
                target_position = i.position
        return target_position

    def distance(self, a : Position, b : Position, weight : int):
        return (abs(a.x - b.x) + abs(a.y - b.y))/weight