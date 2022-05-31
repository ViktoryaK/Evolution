"""
A module for a map of a simulation. Logic for maps updates.
Processes each creature's move, checks if a move is valid.
-----------------------------------------------------------
         Developed by Mr. Korch on last day of spring
                No rights reserved.
              For commercial use only.
-----------------------------------------------------------
"""
from copy import deepcopy
from random import sample
from phage import *
from brain import *


class Map:
    """
    Map class
    Enter the length of side of a square
    """

    def __init__(self, size=100) -> None:
        """
        creating 2D array representation
        """
        self.size = size
        self.map = [[None for _ in range(self.size)] for _ in range(self.size)]

    def generate_creatures(self, num_of_enemies: int, num_of_preys: int) -> None:
        """
        Fills a map with organisms.
        """
        for position in self.get_random_positions(num_of_enemies):
            self.set_org_on_map(organism=HunterPhage(create_random_genome()), coords=position)

        for position in self.get_random_positions(num_of_preys):
            self.set_org_on_map(organism=ChloroPhage(create_random_genome()), coords=position)

    def set_org_on_map(self, organism, coords: tuple) -> None:
        """
        Sets a map with one 'organism'
        :param organism: Creature
        :param coords: tuple (y, x)
        :return: None
        """
        self.map[coords[0]][coords[1]] = organism

    def get_random_positions(self, number: int) -> list[tuple]:
        """
        Returns a list of random, not yet filled positions
        """
        free_squares = [(height, length) for height in range(self.size) for length in range(self.size) if
                        self.map[height][length] is None]
        return sample(free_squares, number)

    def __repr__(self):
        return "\n".join([str([item for item in self.map[i]]) for i in range(self.size)])

    @staticmethod
    def give_to_vika(one_board: list[list]) -> list[list]:
        """
        Simplifies a map for showing it on a video
        """
        return [[repr(item) for item in one_board[i]] for i in range(len(one_board))]

    def cycle(self, generations: int) -> list[list[list]]:
        """
        Runs a simulation 'generations' times
        Puts each state into a list to be processed later
        """
        all_states = []
        for i in range(generations):
            # iterating through map, asking creatures their desires
            phage_wantings = dict()
            for hey, row in enumerate(self.map):
                for leng, elem in enumerate(row):
                    if elem is not None:
                        dx, dy = None, None
                        # TODO: NAZAR WTF шо то dx i dy таке
                        phage_wantings[(hey, leng)] = elem.get_next_move(dx, dy)

            # performing what they want:
            # ....

            all_states.append(deepcopy(self.map))
        return all_states


if __name__ == "__main__":
    board = Map(100)
    board.generate_creatures(num_of_enemies=40, num_of_preys=100)
    simulation = board.cycle(100)
    give_vika = list(map(lambda state: Map.give_to_vika(state), simulation))
    # print(board)
