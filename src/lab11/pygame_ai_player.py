import random
import time
from lab11.turn_combat import CombatPlayer
""" Create PyGameAIPlayer class here"""


class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        #Randomly move
        num = random.randint(0, 9)
        time.sleep(5)
        return num + 48


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        while True:
            self.weapon = random.randint(0, 2)
            time.sleep(2)
            return self.weapon
