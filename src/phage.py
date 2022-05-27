"""
Includes three classes, namely Phage, ChloralPhage and SlayerPhage.
The last two are inherited from the first one.
The main difference between ChloralPhage and SlayerPhage:
    ChloralPhage consumes energy from the sun, while
    SlayerPhage gets it by killing ChloralPhage.
---------------------------------------------
#    Developed by Mr. DamnChuk 27.05.2022   #
#           All rights reserved.            #
#         For educational use only.         #
---------------------------------------------
"""
from src.brain import Brain

MAX_ENERGY = 100


class Phage:
    """
    Main Phage class.
    """

    def __init__(self, genome):
        self.energy = MAX_ENERGY
        self._pos = (None, None)
        self._genome = genome
        self._brain = Brain(genome)

    @property
    def genome(self):
        return self._genome

    @genome.setter
    def genome(self, new_genome: list):
        self._brain = Brain(new_genome)


    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, tup: tuple):
        self._pos = tup

    def get_next_move(self, dx=None, dy=None):
        """
        Returns the State that represents next move of the phage.
        Must be handled outside the module.
        """
        return self._brain.get_final_state([self.energy, self._pos[0], self._pos[1], dx, dy])


class ChloroPhage(Phage):
    """
    ChloroPhage class.
    Contains also get_next_move() function.
    """

    def __init__(self, genome):
        super().__init__(genome)

    def get_next_move(self, dx=None, dy=None):
        return super().get_next_move(dx, dy)


class HunterPhage(Phage):
    """
    HunterPhage class.
    Contains also get_next_move() function.
    """
    def __init__(self, genome):
        super().__init__(genome)

    def get_next_move(self, dx=None, dy=None):
        return super().get_next_move(-dx, -dy)
