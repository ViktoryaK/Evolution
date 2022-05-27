"""
A module for a map of a simulation. Logic for maps updates.
Processes each creature's move, checks if a move is valid.
"""
import random


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
            self.set_org_on_map(organism="enemy", coords=position)

        for position in self.get_random_positions(num_of_preys):
            self.set_org_on_map(organism="prey", coords=position)

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
        return random.sample(free_squares, number)

    def __repr__(self):
        return "\n".join([str([item for item in self.map[i]]) for i in range(self.size)])


# board = Map(10)
# board.generate_creatures(10, 40)
# print(board.map)

if __name__ == "__main__":
    board = Map(10)
    board.generate_creatures(4, 10)
    print(board)
