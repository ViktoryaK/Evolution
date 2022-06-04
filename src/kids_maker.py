"""
Helpful module to create a new generation
Create pairs, return dead phages
"""

import random
from phage import Phage, ChloroPhage, HunterPhage


# TODO:


def get_pair_genome(genom1, genom2, prob=0.05):
    """
    get father's and mother's genoms, merge them and return child
    """
    child = []
    for i in range(len(genom1)):
        child_genome = (genom1[i] + genom2[i]) // 2
        child.append(child_genome)
    strange = random.uniform(0, 1)
    if strange <= prob:
        minus = False
        rand_ind = random.randint(0, len(child) - 1)
        random_int_to_mutation = child[rand_ind]
        if int(random_int_to_mutation) < 0:
            int_to_change = bin(random_int_to_mutation)[3:]
            minus = True
        else:
            int_to_change = bin(random_int_to_mutation)[2:]
        list_of_bin_int = [elem for elem in int_to_change]
        if len(list_of_bin_int) == 1:
            child[rand_ind] = 1 if list_of_bin_int[0] == "0" else 0
        else:
            slicer = len(list_of_bin_int) // 2
            first_part = list_of_bin_int[:slicer]
            second_part = list_of_bin_int[slicer:]
            change_better_part = random.uniform(0, 1)
            if change_better_part < 0.2:
                random_ind = random.randint(0, len(first_part) - 1)
                if first_part[random_ind] == "1":
                    first_part[random_ind] = "0"
                else:
                    first_part[random_ind] = "1"
            elif change_better_part >= 0.2:
                random_ind = random.randint(0, len(second_part) - 1)
                if second_part[random_ind] == "1":
                    second_part[random_ind] = "0"
                else:
                    second_part[random_ind] = "1"

            binary_to_merge = first_part + second_part
            joined_int = int("".join(binary_to_merge), 2)
            if minus:
                joined_int = int("-" + str(joined_int))
            child[rand_ind] = joined_int
    return child


def distance_satisfies(phage1: Phage, phage2: Phage):
    """
    check if phages are close enough to each other
    """
    distance = abs(phage1.position[0] - phage2.position[0]) + abs(phage1.position[1] - phage2.position[1])
    return distance <= 10


def create_pairs(list_of_phages: list) -> list[tuple]:
    """
    Creates list of tuples - two parents
    """
    pairs = []
    dead_phages = []

    def help(phages: list[Phage]):
        if not phages:
            return pairs
        first = phages[0]
        for phage in phages[1:]:
            if distance_satisfies(first, phage):
                pairs.append((first, phage))
                for elem in (first, phage):
                    phages.remove(elem)
                    dead_phages.append(elem)
                help(phages)
                return
        phages.remove(first)
        # dead_phages.append(first)
        help(phages)

    help(list_of_phages)
    return pairs, dead_phages


def start_reproducing(list_of_phages: list):
    """
    create pairs, make kids
    return list of kids(full of objects), dead phages
    """
    if len(list_of_phages) == 0:
        return [], []
    result_of_reproduction = []
    type_of_phage = ChloroPhage if isinstance(list_of_phages[0], ChloroPhage) is True else HunterPhage
    pairs, dead_phages = create_pairs(list_of_phages)
    for pair in pairs:
        list_of_children = get_children(*pair, type_of_phage)
        for kid in list_of_children:
            result_of_reproduction.append(kid)
    return result_of_reproduction, dead_phages


def get_children(phage1: Phage, phage2: Phage, type_of_phage):
    """
    return list of children's objects
    """
    genome_1 = phage1.genome
    genome_2 = phage2.genome
    number_of_children = random.randint(1, 4)
    list_of_children = []
    parents_pos = [phage1.position, phage2.position]
    random.shuffle(parents_pos)
    for child in range(number_of_children):
        new_phage = type_of_phage(get_pair_genome(genome_1, genome_2))
        new_phage.position = parents_pos[child % 2]
        list_of_children.append(new_phage)
    return list_of_children
