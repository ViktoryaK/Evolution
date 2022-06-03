"""
Brain class implementation.
---------------------------------------------
#    Developed by Mr. DamnChuk 27.05.2022   #
#           All rights reserved.            #
#         For educational use only.         #
---------------------------------------------
"""
import random


class State:
    """
    Represents a state in the Brain.
    Can be Terminal or non-Terminal.
    """

    def __init__(self, name='', is_term=False):
        self.name = name
        self.is_terminal = is_term
        self.connections = []

    def add_connection(self, state, conditions: list, weights: list):
        """
        Adds a directed connection between two states.
        """
        self.connections.append([state, conditions, weights])

    @staticmethod
    def satisfies(input_list: list, conditions: list, weights: list):
        """
        Checks if the connection satisfies our parameters.
        """
        for _ in range(len(weights)):
            # Exceptional use
            if conditions[_] == 'ignore' or input_list[_] is None:
                continue
            # Evaluating whether condition was satisfied by input.
            if eval(str(input_list[_]) + conditions[_] + str(weights[_])) is True:
                return True
        return False

    def __repr__(self):
        return "State(" + self.name + ")"


class Brain:
    """
    Brain class.
    """

    def __init__(self, genome: list):
        try:
            assert self.is_correct_genome(genome)
        except AssertionError:
            print("INCORRECT GENOME - YOU KILLED A PHAGE")
            raise ValueError
        self.input_state = None
        self._build_brain(genome)

    def _build_brain(self, genome: list):
        """
        Builds a brain of the phage.
        !!! genome must be correct !!!
        """
        self.input_state = State("Input")
        death_state = State("Death", True)
        energy_state = State("Energy", True)
        move_state = State("Move", False)
        self.input_state.add_connection(death_state, ['<='], [0])
        self.input_state.add_connection(move_state, ['>='], [genome[0]])
        self.input_state.add_connection(energy_state, ['<='], [genome[1]])
        left_state = State("Left", True)
        right_state = State("Right", True)
        up_state = State("Up", True)
        down_state = State("Down", True)
        move_state.add_connection(left_state, ['<=', 'ignore', '<=', 'ignore'],
                                  [genome[2], genome[3], genome[4], genome[5]])
        move_state.add_connection(right_state, ['>=', 'ignore', '>=', 'ignore'],
                                  [genome[6], genome[7], genome[8], genome[9]])
        move_state.add_connection(up_state, ['ignore', '<=', 'ignore', '<='],
                                  [genome[10], genome[11], genome[12], genome[13]])
        move_state.add_connection(down_state, ['ignore', '>=', 'ignore', '>='],
                                  [genome[14], genome[15], genome[16], genome[17]])

    @staticmethod
    def is_correct_genome(genome: list):
        """
        Returns True if genome is correct and False otherwise.
        """
        # For now, we assume that genome length is 18
        if len(genome) != 18:
            return False
        # We can move only when we have enough energy
        # and gain energy when we are alive.
        if genome[0] <= 0 or genome[1] <= 0:
            return False
        # TODO: add asserts for dx and dy in [1, 2, -1, -2]
        return True

    @staticmethod
    def forward(state: State, input_list: list):
        """
        Moves to the new state due to input and weights on edges.
        Performs only one step.
        """
        # Receiving possible next states to go
        next_states = []
        for next_state, conditions, weights in state.connections:
            if State.satisfies(input_list, conditions, weights):
                next_states.append(next_state)
        # Removing used inputs
        # print("Possible next states:", next_states)
        # print("All state connections:", state.connections)
        input_list[:] = input_list[len(state.connections[1][1]):]
        # print(f"Input now: {input_list}")
        if not next_states:
            conn = random.choice(state.connections)
            return conn[0]
        return next_states[0] if next_states[0].name == 'Death' else random.choice(next_states)

    def get_final_state(self, input_list: list):
        """
        Traverses the state machine completely.
        Guaranteed to end up in one of the finite states.
        input_list contains 5 integers: E, x, y, dx, dy.
        dx = x - x* and dy = y - y*.
        """
        # print(f"Input list: {input_list}")
        current_state = self.input_state
        while not current_state.is_terminal:
            current_state = self.forward(current_state, input_list)
        return current_state


def create_random_genome():
    """
    Creates random genome that is correct by the definition.
    """
    while True:
        try:
            genome = [random.randint(0, 100) for _ in range(18)]
            for gen in 4, 5, 8, 9, 12, 13, 16, 17:
                genome[gen] = random.choice([-2, -1, 1, 2])
            assert Brain.is_correct_genome(genome)
            return genome
        except AssertionError:
            continue


if __name__ == '__main__':
    print(create_random_genome())
