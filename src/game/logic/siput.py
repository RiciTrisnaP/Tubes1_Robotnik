from typing import List, Optional
from ..util import get_direction

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position

class Siput(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
    
    def next_move(self, board_bot: GameObject, board: Board):
        stats = board_bot.properties
        current_position = board_bot.position
        diamonds = board.diamonds

        # FUNGSI PEMBANTU
        def isEqualPosition(Pos1, Pos2):
            if not(Pos1 and Pos2):
                return False
            return (Pos1.x == Pos2.x and Pos1.y == Pos2.y)
        def isDiamondValid(diamonds):   
            return (any(isEqualPosition(diamond.position, self.goal_position) for diamond in diamonds))
        def Jarak(Pos1, Pos2):
            return (abs(Pos1.y - Pos2.y) + abs(Pos1.x - Pos2.x))
        
        # FUNGSI SELEKSI
        def seleksi(diamonds: List[GameObject], board_bot: GameObject) -> Optional[GameObject]:
            # FUNGSI KELAYAKAN
            def layak(kandidatSolusi: Optional[GameObject], board_bot: GameObject) -> bool:
                if kandidatSolusi:
                    return (board_bot.properties.diamonds + kandidatSolusi.properties.points <= 5)
                return True

            def rumus(n: GameObject, board_bot: GameObject) -> float:
                return (n.properties.points / (Jarak(current_position, n.position)))
                # return (n.properties.points / (Jarak(current_position, n.position) + Jarak(board_bot.properties.base, n.position)))

            poin = [rumus(n, board_bot) for n in diamonds]
            index_max = poin.index(max(poin))

            kandidatSolusi = diamonds[index_max]

            while not layak(kandidatSolusi, board_bot):
                if len(diamonds) - 1 == 0:
                    # Tidak ada diamond yang layak, balik ke base
                    kandidatSolusi = None
                del diamonds[index_max]
                kandidatSolusi = seleksi(diamonds, board_bot) 
            
            return kandidatSolusi
            
        if (self.goal_position and isEqualPosition(self.goal_position, current_position)) or \
            not(isEqualPosition(self.goal_position, stats.base) or isDiamondValid(diamonds)):
            # Reset goal jika:
            # - Sudah sampai tujuan
            # - Diamond yang dituju sudah tidak ada (diambil bot lain / tombol merah ditekan)
            self.goal_position = None

        if stats.diamonds == 5:
            # Kalo inventory penuh balik ke base
            self.goal_position = stats.base
        elif stats.diamonds != 5 and self.goal_position == None:    
            solusi = seleksi(diamonds, board_bot)
            if solusi:
                self.goal_position = solusi.position
            else:
                self.goal_position = stats.base

        # Jalan
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y
    
# Himpunan Kandidat : diamonds
# Himpunan Solusi   : -
# Fungsi solusi     : -
# Fungsi seleksi    : seleksi()
# Fungsi kelayakan  : layak()
# Fungsi objektif   : -
