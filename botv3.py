from game.logic.base import BaseLogic
import time
from game.models import Board, GameObject, Position
from typing import Optional
from ..util import get_direction


# This bot use the nearest distance to avoid zero division error in botv2

class Botv3(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.target_type = 'DiamondGameObject'
    
    def next_move(self, board_bot: GameObject, board: Board):
        # Inisialization of important variable
        current_position = board_bot.position
        diamond = board.diamonds
        base = board_bot.properties.base

        # Select Game Object to Target
        # Move to base if inventory full
        if board_bot.properties.diamonds == board_bot.properties.inventory_size:
            self.goal_position = base
        else:  
            # Exclude red diamond if inventory remaining size is 1
            if board_bot.properties.diamonds == (board_bot.properties.inventory_size - 1):
                self.goal_position = self.select_target(diamond, board, current_position, 1)
            else:
                self.goal_position = self.select_target(diamond, board, current_position, 2)
        
        # We are aiming for a specific position, calculate delta
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        # Bug handler
        if delta_x != delta_y: 
            return delta_x, delta_y
        else:
            print(board_bot.properties.name)
            time.sleep(0.1)
            return 0,1
        

    def select_target(self, diamond, board: Board, current_position, max_allow_point):
        # variable inisialization
        target_position = current_position
        min_distance = 100

        # find highest weight diamond
        for i in diamond:
            distance_to_candidate = self.calculate_distance(i.position, current_position, i.properties.points)
            if  distance_to_candidate < min_distance and i.properties.points <= max_allow_point:
                min_distance = distance_to_candidate
                target_position = i.position
                self.target_type = 'DiamondGameObject'
        
        # if reset button has more weight then go to the button instead
        Reset_Button = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"];
        for i in Reset_Button:
            if self.calculate_distance(i.position, current_position, 1) < min_distance:
                target_position = i.position
                self.target_type = 'DiamondButtonGameObject'
        
        # Consider using teleporter to go to the goal
        Teleporter = [d for d in board.game_objects if d.type == "TeleportGameObject"];
        nearest_teleporter = Teleporter[0]
        farthest_teleporter = Teleporter[1]
        if self.calculate_distance(current_position, Teleporter[1].position, 1) < self.calculate_distance(current_position, Teleporter[0].position,1):
            nearest_teleporter = Teleporter[1]
            farthest_teleporter = Teleporter[0]
        if self.calculate_distance(current_position, nearest_teleporter.position,1) + self.calculate_distance(target_position,farthest_teleporter.position,1) < min_distance:
            target_position = nearest_teleporter.position

        return target_position

    def calculate_distance(self, a : Position, b : Position, weight : int) -> float:
        return  (abs(a.x - b.x) + abs(a.y - b.y)) / weight