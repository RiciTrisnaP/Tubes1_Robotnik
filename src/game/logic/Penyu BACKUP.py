from typing import List, Optional
from ..util import get_direction

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position, Properties

class Penyu(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.poin_lama: int = 0
    
    def next_move(self, board_bot: GameObject, board: Board):
        # FUNGSI PEMBANTU
        def isEqualPosition(Pos1, Pos2):
            # Mengembalikan true jika Pos1 sama dengan Pos2
            if not(Pos1 and Pos2):
                return False
            return (Pos1.x == Pos2.x and Pos1.y == Pos2.y)
        def isDiamondValid(diamonds):   
            # Mengembalikan true jika terdapat diamond pada posisi self.goal_position
            return (any(isEqualPosition(diamond.position, self.goal_position) for diamond in diamonds))
        def Jarak(Pos1: Position, Pos2: Position) -> int:
            # Mengembalikan jumlah gerakan yang diperlukan untuk bergerak dari Pos1 ke Pos2
            return (abs(Pos1.y - Pos2.y) + abs(Pos1.x - Pos2.x))
        def isTeleporter(board_bot: GameObject, teleporters: List[GameObject]) -> bool:
            # Mengembalikan true jika terdapat teleporter pada posisi bot
            return (any(isEqualPosition(teleporter.position, board_bot.position) for teleporter in teleporters))
        
        # FUNGSI SELEKSI
        def seleksi(diamonds: List[GameObject], board_bot: GameObject) -> Optional[GameObject]:
            # Mengembalikan diamond atau none jika tidak terdapat diamond yang memenuhi fungsi kelayakan

            # FUNGSI KELAYAKAN
            def layak(kandidatSolusi: Optional[GameObject], board_bot: GameObject) -> bool:
                # Mengembalikan true jika diamond yang dipilih layak
                if kandidatSolusi:
                    if (kandidatSolusi.properties.points == 2 and board_bot.properties.diamonds >= 4):
                        return False
                    # return (board_bot.properties.diamonds + kandidatSolusi.properties.points <= 5)
                return True

            def rumus(n: GameObject) -> float:
                return (n.properties.points / (Jarak(current_position, n.position)))

            poin = [rumus(n) for n in diamonds]
            index_max = poin.index(max(poin))

            kandidatSolusi = diamonds[index_max]

            while not layak(kandidatSolusi, board_bot):
                if len(diamonds) - 1 == 0:
                    # Tidak ada diamond yang layak, balik ke base
                    kandidatSolusi = None
                del diamonds[index_max]
                kandidatSolusi = seleksi(diamonds, board_bot) 
            return kandidatSolusi
        
        # FUNGSI OBYEKTIF
        def resetTarget(current_position: Position, stats: Properties) -> bool:
            # Mengembalikan TRUE jika:
            # - Sudah sampai tujuan
            # - Diamond yang dituju sudah tidak ada (diambil bot lain / tombol merah ditekan)
            # - Poin berubah
            # - Kena teleporter
            return (self.goal_position and isEqualPosition(self.goal_position, current_position)) or \
                    (not isEqualPosition(self.goal_position, stats.base) and not isDiamondValid(diamonds)) or \
                    (self.poin_lama != stats.diamonds) or (isTeleporter(board_bot, teleporters))
        
        # FUNGSI SOLUSI
        def fungsiSolusi(stats: Properties) -> bool:
            return (stats.diamonds == 5)

        # ------------------------------------------------------------------------------------------------------- #

        stats = board_bot.properties
        current_position = board_bot.position
        diamonds = board.diamonds
        teleporters = [t for t in board.game_objects if t.type == "TeleportGameObject"]

        if resetTarget(current_position, stats):
            self.goal_position = None

        if fungsiSolusi(stats):
            # Kalo inventory penuh balik ke base
            self.goal_position = stats.base
        elif stats.diamonds != 5 and self.goal_position == None:    
            solusi = seleksi(diamonds, board_bot)
            self.poin_lama = board_bot.properties.diamonds
            if solusi:
                self.goal_position = solusi.position
            else:
                self.goal_position = stats.base
        
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        return delta_x, delta_y
    
# Himpunan Kandidat : diamonds
# Himpunan Solusi   : self.goal_position (?)
# Fungsi solusi     : solusi()
# Fungsi seleksi    : seleksi()
# Fungsi kelayakan  : layak()
# Fungsi objektif   : resetTarget()
