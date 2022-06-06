"""
A module for a map of a simulation. Logic for maps updates.
Processes each creature's move, checks if a move is valid.



-----------------------------------------------------------
         Designed by Mr. Korch on last day of spring
                No rights reserved.
              For commercial use only.
-----------------------------------------------------------



"""
from __future__ import annotations

from time import perf_counter
from copy import deepcopy
from random import sample, shuffle
from phage import *
from brain import *
from reproducing import *
from transform_to_file import *
# from visualisation import magic


def prepare_map_visualisation(one_board: list[list]) -> list[list]:
    """
    Simplifies a map for showing it on a video
    """
    return [[repr(item) for item in one_board[i]] for i in range(len(one_board))]


class Map:
    """
    Map class
    Enter the length of side of a square
    """
    # 7 8 9
    # 7 7 6
    loss_for_move = 7
    loss_for_stay = 6
    one_move_gain = 22
    kill_gain = 40
    when_make_kids = 20

    def __init__(self, size=100) -> None:
        """
        creating 2D array representation
        """
        self.size = size
        self.map = [[None for _ in range(size)] for _ in range(size)]
        self.phage_positions = []
        self.compare_val = int(0.075 * self.size ** 2)

    def __getitem__(self, position: tuple) -> None | Phage:
        """
        Returns an object by pos on a map
        Easy access to the board
        position - coords
        """
        return self.map[position[0]][position[1]]

    def __setitem__(self, position: tuple, value: None | Phage) -> None:
        """
        Easy access to the changes of a board
        position - coords
        """
        self.map[position[0]][position[1]] = value

    def generate_random_phages(self, num_of_enemies: int, num_of_preys: int) -> None:
        """
        Fills a map with organisms.
        """
        for position in self.get_random_positions(num_of_enemies):
            self.set_phage_on_map(organism=HunterPhage(create_random_genome()), coords=position)

        for position in self.get_random_positions(num_of_preys):
            self.set_phage_on_map(organism=ChloroPhage(create_random_genome()), coords=position)

    def set_phage_on_map(self, organism: Phage, coords: tuple) -> None:
        """
        Sets a map with one 'organism'
        :param organism: Creature
        :param coords: tuple (y, x)
        :return: None
        """
        self[coords] = organism
        organism.position = coords
        self.phage_positions.append(coords)

    def process_phages_death(self, position: tuple) -> None:
        """
        Processes death of a phage
        """
        self[position] = None
        self.phage_positions.remove(position)

    def get_random_positions(self, number: int) -> list[tuple]:
        """
        Returns a list of random, not yet filled positions
        """
        free_squares = [(height, length) for height in range(self.size) for length in range(self.size) if
                        self[height, length] is None]
        try:
            return sample(free_squares, number)
        except ValueError:
            shuffle(free_squares)
            return free_squares

    def __repr__(self) -> str:
        return "\n".join([str([item for item in self.map[i]]) for i in range(self.size)])

    def division_into_types(self) -> tuple[list, list]:
        """
        Returns two lists of phages of different types
        Special for Olli with love
        first - ChloroPhage, second - HunterPhage
        """
        chloro, hunter = [], []
        for pos in self.phage_positions:
            obj = self[pos]
            chloro.append(obj) if isinstance(obj, ChloroPhage) else hunter.append(obj)
        return chloro, hunter

    def get_nearest_opponents(self, position: tuple, stranger, distance=2) -> list[tuple]:
        """
        Returns a list of the closest strangers by number of steps to get to
        position - position of a Phage
        stranger - rival (opposite) class
        distance - radius of searching
        """
        result = []
        for height in range(2 * distance + 1):
            for length in range(2 * distance + 1):
                new_height, new_length = position[0] - distance + height, position[1] - distance + length
                if 0 <= new_height < self.size and 0 <= new_length < self.size:
                    square = self[new_height, new_length]
                    if square is not None and isinstance(square, stranger):
                        result.append((new_height, new_length))
        return result

    @staticmethod
    def choose_closest_opponent(pos: tuple, strangers: list[tuple]) -> tuple:
        """
        Returns the closest stranger to Phage's position - pos
        Strangers positions - 'strangers'
        """
        return list(sorted(strangers, key=lambda item: abs(pos[0] - item[0]) + abs(pos[1] - item[1])))[
            0] if strangers else None

    def get_phages_states(self) -> dict:
        """
        Iterating through map, asking creatures their desires
        """
        phage_wantings = dict()
        for position in self.phage_positions:
            phage = self[position]
            strangers = self.get_nearest_opponents(position=position,
                                                   distance=10,
                                                   stranger=ChloroPhage if isinstance(phage, HunterPhage)
                                                   else HunterPhage)
            if strangers:
                position_of_stranger = self.choose_closest_opponent(position, strangers)
                dy, dx = position[0] - position_of_stranger[0], position[1] - position_of_stranger[1]
            else:
                dy, dx = None, None
            phage_wantings[position] = phage.get_next_move(dy, dx)

        key_value_list = [(position, action) for position, action in phage_wantings.items()]
        shuffle(key_value_list)
        return {item[0]: item[1] for item in key_value_list}

    def get_coords(self, now: tuple, action: str) -> tuple | None:
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
        phage = self[now]
        if self[future] is None:
            phage.energy -= self.loss_for_move
            self.set_phage_on_map(phage, future)
            self.process_phages_death(now)
        else:
            phage.energy -= self.loss_for_stay

    def find_by_radius(self, obj_type, radius: int, position: tuple) -> tuple | None:
        """
        Finds the first occurrence of object of given type on a map
        with some radius at given position
        """
        for height in range(2 * radius + 1):
            for length in range(2 * radius + 1):
                new_height, new_length = position[0] - radius + height, position[1] - radius + length
                if 0 <= new_height < self.size and 0 <= new_length < self.size:
                    square = self[new_height, new_length]
                    if isinstance(square, obj_type):
                        return new_height, new_length

    def kill_if_possible(self, position: tuple, phage: Phage) -> None:
        """
        For HunterPhage, kills a ChloroPhage if possible,
        otherwise stays and loses energy
        """
        chloro_pos = self.find_by_radius(obj_type=ChloroPhage, radius=3, position=position)
        if chloro_pos:
            self.process_phages_death(chloro_pos)
            phage.energy = min([100, phage.energy + self.kill_gain])
        else:
            phage.energy -= self.loss_for_stay

    def give_energy(self, position: tuple) -> None:
        """
        Gives the energy to the phage
        """
        phage = self[position]
        if isinstance(phage, ChloroPhage):
            add_value = self.one_move_gain * (self.size - phage.position[0]) // self.size
            phage.energy = min([100, phage.energy + add_value])
        elif isinstance(phage, HunterPhage):
            self.kill_if_possible(position=position, phage=phage)
        else:
            print("something went wrong :(")
            exit(1)

    def satisfy_desires(self, phage_wants: dict) -> None:
        """
        Gives phages exactly what they want
        """
        for position, action in phage_wants.items():
            if self[position] is not None:
                action = action.name
                coords = self.get_coords(position, action)
                if coords is None:
                    self.give_energy(position) if action == "Energy" else self.process_phages_death(position)
                else:
                    self.make_phage_move(now=position, future=coords)

    def reproduce(self) -> None:
        """
        Function that processes multiplication of phages and add children to the map
        """
        # two lists of phages of different types are created
        chloro, hunters = self.division_into_types()
        correct_order = [chloro, hunters] if len(chloro) <= len(hunters) else [hunters, chloro]
        for similar_phages in correct_order:
            kids_phages = start_reproducing(deepcopy(similar_phages))
            for dead in similar_phages:
                self.process_phages_death(dead.position)
            for kid, position in zip(kids_phages, self.get_random_positions(len(kids_phages))):
                self.set_phage_on_map(kid, position)

    def cut_the_population(self):
        """
        Cuts the number of phages on the map if their quantity is too large
        """
        if len(self.phage_positions) > self.compare_val:
            shuffle(self.phage_positions)
            for pos in self.phage_positions[self.compare_val:]:
                self.process_phages_death(pos)

    def cycle(self, generations: int) -> list[list[list]]:
        """
        Runs a simulation 'generations' times
        Puts each state into a list to be processed later
        """
        all_states = []
        for i in range(generations):
            if not i % self.when_make_kids:
                self.reproduce()  # processes multiplication of phages
            self.cut_the_population()  # cuts phages population if filled more than 10 percent of the map
            phage_wants = self.get_phages_states()  # iterating through map, asking creatures their desires:
            self.satisfy_desires(phage_wants)  # performing what they want
            all_states.append(prepare_map_visualisation(self.map))  # saving map state
        write_in_csv_file([self[position] for position in self.phage_positions])  # writes phages to the file
        return all_states

    @staticmethod
    def create_map_from_file(path: str = 'phages.csv', size: int = 100):
        """
        Creates a new map object fulfilled with phages
        that were saved previously in the file
        """
        phages_info = read_csv_file(path)
        new_map = Map(size)
        for genome, position, type_of_obj in phages_info:
            new_map.set_phage_on_map(globals()[type_of_obj](genome), position)
        return new_map


if __name__ == "__main__":
    start = perf_counter()
    board = Map(100)
    board.generate_random_phages(num_of_enemies=80, num_of_preys=150)
    simulation = board.cycle(200)
    print(perf_counter() - start)

    # magic(simulation)
    # new_board = Map.create_map_from_file("phages.csv")
    # new_board.cycle(15)
