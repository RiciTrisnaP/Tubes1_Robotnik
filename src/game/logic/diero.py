from typing import List, Optional
from ..util import get_direction

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position

class Diero(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
    
    def next_move(self, board_bot: GameObject, board: Board):
        # FUNGSI PEMBANTU
        def isEqualPosition(Pos1, Pos2):
            if not Pos1 or not Pos2:
                return False
            return (Pos1.x == Pos2.x and Pos1.y == Pos2.y)
        def isDiamondValid(diamonds):
            for diamond in diamonds:
                if isEqualPosition(diamond.position, self.goal_position):
                    return True
            return False
        def Jarak(Pos1, Pos2):
            return (abs(Pos1.y - Pos2.y) + abs(Pos1.x - Pos2.x))
        
        stats = board_bot.properties
        current_position = board_bot.position
        diamonds = board.diamonds
        
        if (self.goal_position and isEqualPosition(self.goal_position, current_position)) or \
            not(isEqualPosition(self.goal_position, stats.base) or isDiamondValid(diamonds)):
            self.goal_position = None

        if stats.diamonds == 5:
            # Kalo penuh ke base
            self.goal_position = stats.base
        elif stats.diamonds != 5 and self.goal_position == None:    
            diamonds_position: List[Position] = [n.position for n in diamonds]
            
            if stats.diamonds < 4:  
                # Poin / Jarak terbesar
                poinPerJarak = [(n.properties.points / Jarak(current_position, n.position)) for n in diamonds]

                index_max = poinPerJarak.index(max(poinPerJarak))
                self.goal_position = diamonds_position[index_max]
            else:
                # Diamond biru terdekat
                relative_position: List[int] = [Jarak(current_position, n) for n in diamonds_position]
                rp_sort: List[int] = sorted(relative_position)
                
                for j in range(len(diamonds)):
                    idx = relative_position.index(rp_sort[j])
                    if diamonds[idx].properties.points == 1:
                        self.goal_position = diamonds_position[idx]
                        break
                else:
                    # Tidak ada diamond biru
                    self.goal_position = stats.base

        # Jalan
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        return delta_x, delta_y
        