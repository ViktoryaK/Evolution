"""
---------------------------------------------
#    Developed by Mr. DamnChuk 27.05.2022   #
#           All rights reserved.            #
#         For educational use only.         #
---------------------------------------------
Includes three classes, namely Phage, ChloralPhage and SlayerPhage.
The last two are inherited from the first one.
The main difference between ChloralPhage and SlayerPhage:
    ChloralPhage consumes energy from the sun, while
    SlayerPhage gets it by killing ChloralPhage.
"""
import random

from brain import Brain, create_random_genome

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
        self._genome = new_genome
        self._brain = Brain(new_genome)

    @property
    def position(self):
        return self._pos[1], self._pos[0]

    @position.setter
    def position(self, tup: tuple):
        self._pos = tup[1], tup[0]

    def get_next_move(self, dy=None, dx=None):
        """
        Returns the State that represents next move of the phage.
        Must be handled outside the module.
        """
        return self._brain.get_final_state([self.energy, self._pos[0], self._pos[1], dx, dy])


class ChloroPhage(Phage):
    """
    ChloroPhage class.
    Also contains get_next_move() function.
    """

    def __init__(self, genome):
        super().__init__(genome)

    def get_next_move(self, dy=None, dx=None):
        return super().get_next_move(dy, dx)

    def __repr__(self):
        return "green"


class HunterPhage(Phage):
    """
    HunterPhage class.
    Contains also get_next_move() function.
    """

    def __init__(self, genome):
        super().__init__(genome)

    def get_next_move(self, dy=None, dx=None):
        return super().get_next_move(None, None) if dx is None or dy is None \
            else super().get_next_move(-dy, -dx)

    def __repr__(self):
        return "red"


def test_phage():
    res = []
    for _ in range(0, 100):
        genome = create_random_genome()
        print("Genome:", genome)
        phage = ChloroPhage(genome)
        phage.energy = random.randint(0, 100)
        phage.position = (random.randint(0, 100), random.randint(0, 100))
        res.append(phage.get_next_move(random.randint(-2, 2), random.randint(-2, 2)))
    return res


if __name__ == '__main__':
    res = test_phage()
    for string in ["Left", "Right", "Up", "Down"]:
        print(string, len(list(filter(lambda x: x.name == string, res))))
