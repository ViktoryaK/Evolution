"""
A module for a map of a simulation. Logic for maps updates.
Processes each creature's move, checks if a move is valid.



-----------------------------------------------------------
         Designed by Mr. Korch on last day of spring
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
    loss_for_move = 5
    loss_for_stay = 2
    one_move_gain = 5
    kill_gain = 20

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

    def set_org_on_map(self, organism: Phage, coords: tuple) -> None:
        """
        Sets a map with one 'organism'
        :param organism: Creature
        :param coords: tuple (y, x)
        :return: None
        """
        self.map[coords[0]][coords[1]] = organism
        organism.position = coords

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

    def get_nearest_strangers(self, position: tuple, stranger, distance=2) -> list[tuple]:
        """
        Returns a list of the closest strangers by number of steps to get to
        position - position of a Phage
        stranger - rival (opposite) class
        distance - radius of searching
        """
        res = []
        for height in range(2 * distance + 1):
            for length in range(2 * distance + 1):
                new_height, new_length = position[0] - distance + height, position[1] - distance + length
                if 0 <= new_height < self.size and 0 <= new_length < self.size:
                    square = self.map[new_height][new_length]
                    if square is not None and isinstance(square, stranger):
                        res.append((new_height, new_length))
        return res

    @staticmethod
    def choose_closest_stranger(pos: tuple, strangers: list[tuple]) -> tuple:
        """
        Returns the closest stranger to Phage's position - pos
        Strangers positions - 'strangers'
        """
        return list(sorted(strangers, key=lambda item: abs(pos[0] - item[0]) + abs(pos[1] - item[1])))[
            0] if strangers else None

    def what_they_want_from_me(self) -> dict:
        """
        Iterating through map, asking creatures their desires
        """
        phage_wantings = dict()
        for hey, row in enumerate(self.map):
            for length, elem in enumerate(row):
                if elem is not None:
                    strangers = self.get_nearest_strangers(position=(hey, length),
                                                           distance=2,
                                                           stranger=ChloroPhage if isinstance(elem, HunterPhage)
                                                           else HunterPhage)
                    if strangers:
                        position_of_stranger = self.choose_closest_stranger((hey, length), strangers)
                        dx, dy = hey - position_of_stranger[0], length - position_of_stranger[1]
                    else:
                        dx, dy = None, None
                    phage_wantings[(hey, length)] = elem.get_next_move(dx, dy)
        return phage_wantings

    def get_coords(self, now: tuple, action: str) -> tuple:
        """
        Gets coords of new move, where action - "Up", "Down", "Left", "Right"
        """
        if action == "Up":
            hey, length = now[0] - 1, now[1]
        elif action == "Down":
            hey, length = now[0] + 1, now[1]
        elif action == "Left":
            hey, length = now[0], now[1] - 1
        elif action == "Right":
            hey, length = now[0], now[1] + 1
        else:
            return None

        return (hey, length) if 0 <= hey < self.size and 0 <= length < self.size else (now[0], now[1])

    def make_phage_move(self, now: tuple, future: tuple) -> None:
        """
        Makes a move on a board, frees 'new' square, occupies 'future' one
        """
        phage = self.get_obj_on_pos(now)
        if self.get_obj_on_pos(future) is None:
            phage.energy -= self.loss_for_move
            self.set_org_on_map(phage, future)
            self.map[now[0]][now[1]] = None
        else:
            phage.energy -= self.loss_for_stay

    def get_obj_on_pos(self, pos: tuple):
        """
        Returns an object by pos on a map
        """
        return self.map[pos[0]][pos[1]]

    def kill_if_possible(self, position: tuple) -> None:
        """
        For HunterPhage, kills a ChloroPhage if possible,
        otherwise stays and loses energy
        """
        # TODO: finish, DEBUG
        radius = 1
        phage = self.get_obj_on_pos(position)

        for height in range(2 * radius + 1):
            for length in range(2 * radius + 1):
                new_height, new_length = position[0] - radius + height, position[1] - radius + length
                if 0 <= new_height < self.size and 0 <= new_length < self.size:
                    obj = self.get_obj_on_pos((new_height, new_length))
                    if isinstance(obj, ChloroPhage):
                        self.map[new_height][new_length] = None
                        phage.energy += self.kill_gain
                        return

        phage.energy -= self.loss_for_stay

    def give_energy(self, position: tuple) -> None:
        """
        Gives the energy to the phage
        """
        phage = self.get_obj_on_pos(position)
        if isinstance(phage, ChloroPhage):
            phage.energy += self.one_move_gain
        elif isinstance(phage, HunterPhage):
            self.kill_if_possible(position)
        else:
            print("DUUUUUUUDEEE YOU'VE FUCKED UP :(")
            exit(1)

    def process_death(self, position: tuple) -> None:
        """
        Processes death of a phage
        """
        # TODO: DEBUG this
        self.map[position[0]][position[1]] = None

    def satisfy_desires(self, phage_wants: dict) -> None:
        """
        Gives phages exactly what they want
        """
        for position, action in phage_wants.items():
            if self.get_obj_on_pos(position) is not None:
                action = action.name
                coords = self.get_coords(position, action)
                if coords is None:
                    self.give_energy(position) if action == "Energy" else self.process_death(position)
                else:
                    self.make_phage_move(now=position, future=coords)

    def cycle(self, generations: int) -> list[list[list]]:
        """
        Runs a simulation 'generations' times
        Puts each state into a list to be processed later
        """
        all_states = []
        for i in range(generations):
            phage_wants = self.what_they_want_from_me()  # iterating through map, asking creatures their desires:
            # TODO: shuffle a dictionary for more realistic simulation
            self.satisfy_desires(phage_wants)  # performing what they want
            all_states.append(deepcopy(self.map))  # saving map state
        return all_states


if __name__ == "__main__":
    board = Map(100)
    board.generate_creatures(num_of_enemies=40, num_of_preys=100)
    simulation = board.cycle(100)
    give_vika = list(map(lambda state: Map.give_to_vika(state), simulation))
