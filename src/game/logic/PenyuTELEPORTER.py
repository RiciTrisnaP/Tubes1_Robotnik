from typing import List, Optional
from ..util import get_direction

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position, Properties

class PenyuTELEPORT(BaseLogic):
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
        def isTargetValid(diamonds, teleporters):   
            # Mengembalikan true jika terdapat diamond pada posisi self.goal_position
            return (any(isEqualPosition(diamond.position, self.goal_position) for diamond in diamonds) or \
                    any(isEqualPosition(teleporter.position, self.goal_position) for teleporter in teleporters))
        def isTeleporter(board_bot: GameObject, teleporters: List[GameObject]) -> bool:
            # Mengembalikan true jika terdapat teleporter pada posisi bot
            return (any(isEqualPosition(teleporter.position, board_bot.position) for teleporter in teleporters))
        def Jarak(Pos1: Position, Pos2: Position) -> int:
            # Mengembalikan jumlah gerakan yang diperlukan untuk bergerak dari Pos1 ke Pos2
            return (abs(Pos1.y - Pos2.y) + abs(Pos1.x - Pos2.x))
        def JarakTeleporter(board_bot: GameObject, teleporters: List[GameObject], diamond: GameObject):
            nearest_teleporter = teleporters[0]
            farthest_teleporter = teleporters[1]

            current_position = board_bot.position
            if Jarak(current_position, teleporters[1].position) < Jarak(current_position, teleporters[0].position):
                nearest_teleporter = teleporters[1]
                farthest_teleporter = teleporters[0]
            return nearest_teleporter, Jarak(current_position, nearest_teleporter.position) + Jarak(diamond.position, farthest_teleporter.position)
        
        # FUNGSI SELEKSI
        def seleksi(diamonds: List[GameObject], board_bot: GameObject, board: Board) -> (Optional[GameObject], Optional[GameObject]):
            # Mengembalikan diamond atau none jika tidak terdapat diamond yang memenuhi fungsi kelayakan

            # FUNGSI KELAYAKAN
            def layak(kandidatSolusi: (Optional[GameObject], Optional[GameObject]), board_bot: GameObject) -> bool:
                # Mengembalikan true jika diamond yang dipilih layak
                if kandidatSolusi[0]:
                    if isEqualPosition(board_bot.position, kandidatSolusi[0].position):
                        return False
                if kandidatSolusi[1]:
                    if (kandidatSolusi[1].properties.points == 2 and board_bot.properties.diamonds >= 4):
                        return False
                    # return (board_bot.properties.diamonds + kandidatSolusi.properties.points <= 5)    
                return True

            def rumus(n: GameObject, isTeleporter: bool, teleporters):
                if (isTeleporter):
                    nearest_teleporter, dist = JarakTeleporter(board_bot, teleporters, n)
                    return (nearest_teleporter, (dist / n.properties.points))
                return ((Jarak(current_position, n.position) / n.properties.points))
            
            teleporters = [t for t in board.game_objects if t.type == "TeleportGameObject"]

            poin = [rumus(n, False, teleporters) for n in diamonds]
            poin_teleporter = [rumus(n, True, teleporters) for n in diamonds]
            
            print(poin)
            print(diamonds)
            min_nt = min(poin)
            index_min = poin.index(min_nt)

            # cari min + index min dari poin_teleporter
            index_min_tel, index = 0, 0
            min_teleporter = poin_teleporter[0][1]
            for i in poin_teleporter:
                if i[1] < min_teleporter:
                    min_teleporter = i[1]
                    index_min_tel = index
                index += 1
            
            isTeleporter = False
            if (min_teleporter < min_nt): 
                index_min = index_min_tel
                isTeleporter = True

            kandidatSolusi = poin_teleporter[index_min][0] if isTeleporter else None, diamonds[index_min]

            while not layak(kandidatSolusi, board_bot):
                if len(diamonds) - 1 == 0:
                    # Tidak ada diamond yang layak, balik ke base
                    kandidatSolusi = None
                    break
                del diamonds[index_min]
                kandidatSolusi = seleksi(diamonds, board_bot, board) 

            return (kandidatSolusi)
        
        # FUNGSI OBYEKTIF
        def resetTarget(current_position: Position, stats: Properties, teleporters: List[GameObject]) -> bool:
            # Mengembalikan TRUE jika:
            # - Sudah sampai tujuan
            # - Diamond yang dituju sudah tidak ada (diambil bot lain / tombol merah ditekan)
            # - Poin berubah
            # - Kena teleporter
            return (self.goal_position and isEqualPosition(self.goal_position, current_position)) or \
                    (not isEqualPosition(self.goal_position, stats.base) and not isTargetValid(diamonds, teleporters)) or \
                    (self.poin_lama != stats.diamonds) or (isTeleporter(board_bot, teleporters))
        
        # FUNGSI SOLUSI
        def fungsiSolusi(stats: Properties) -> bool:
            return (stats.diamonds == 5)

        # ------------------------------------------------------------------------------------------------------- #

        stats = board_bot.properties
        current_position = board_bot.position
        diamonds = board.diamonds
        teleporters = [t for t in board.game_objects if t.type == "TeleportGameObject"]

        if resetTarget(current_position, stats, teleporters):
            self.goal_position = None

        if fungsiSolusi(stats):
            # Kalo inventory penuh balik ke base
            self.goal_position = stats.base
        elif stats.diamonds != 5 and self.goal_position == None:    
            solusi = seleksi(diamonds, board_bot, board)
            self.poin_lama = board_bot.properties.diamonds

            if not solusi[1]:
                self.goal_position = stats.base
            else:
                self.goal_position = solusi[0].position if solusi[0] else solusi[1].position
        
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        if (delta_x == delta_y):
            self.goal_position = None
            delta_x, delta_y = self.next_move(board_bot, board)

        return delta_x, delta_y
    
# Himpunan Kandidat : diamonds
# Himpunan Solusi   : self.goal_position (?)
# Fungsi solusi     : solusi()
# Fungsi seleksi    : seleksi()
# Fungsi kelayakan  : layak()
# Fungsi objektif   : resetTarget()
