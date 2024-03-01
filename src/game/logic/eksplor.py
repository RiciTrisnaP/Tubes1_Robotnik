from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class Eksplor(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        diamond = board.diamonds        
        # Analyze new state
        current_position = board_bot.position
        if props.diamonds >= 4:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            jarak_terdekat = float('inf')  # Initialize with positive infinity
            for d in diamond:
                jarak_current = abs(d.position.x - current_position.x) + abs(d.position.y - current_position.y)
                if jarak_current < jarak_terdekat:
                    jarak_terdekat = jarak_current
                    self.goal_position = d.position
            
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
