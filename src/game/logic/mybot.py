from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class MyBot(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        diamond = board.diamonds
        def jarak(a,b) :
            return abs(a.x-b.x) + abs(a.y-b.y)
        
        # Analyze new state
        current_position = board_bot.position
        if props.diamonds >= 4:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            jarakDiamond = [] 
            for d in diamond :
                jarakDiamond.append(jarak(d.position,current_position))
            jarak_terdekat = min(jarakDiamond)
            idx = jarakDiamond.index(jarak_terdekat)
            self.goal_position = diamond[idx].position
            
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
