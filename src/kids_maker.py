"""
Helpful module to create a new generation
Create pairs, return dead phages
"""

import random
from phage import Phage, ChloroPhage, HunterPhage
from brain import Brain


def get_pair_genome(genome_1, genome_2, prob=0.05):
    """
    get father's and mother's genoms, merge them and return child
    """
    child = []
    for i in range(len(genome_1)):
        child_genome = (genome_1[i] + genome_2[i]) // 2
        child.append(child_genome)
    dr_strange = random.uniform(0, 1)
    if dr_strange <= prob:
        minus = False
        rand_ind = random.randint(0, 17)
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
                first_part[random_ind] = "0" if first_part[random_ind] == "1" else "1"
            elif change_better_part >= 0.2:
                random_ind = random.randint(0, len(second_part) - 1)
                second_part[random_ind] = "0" if second_part[random_ind] == "1" else "1"

            binary_to_merge = first_part + second_part
            joined_int = int("".join(binary_to_merge), 2)
            if minus:
                joined_int *= -1
            child[rand_ind] = joined_int
    return child


def distance_satisfies(phage1: Phage, phage2: Phage) -> bool:
    """
    check if phages are close enough to each other
    """
    distance = abs(phage1.position[0] - phage2.position[0]) + abs(phage1.position[1] - phage2.position[1])
    return distance <= 10


def create_pairs(list_of_phages: list) -> list:
    """
    Creates list of tuples - two parents
    """
    pairs = []
    while list_of_phages:
        phage1 = list_of_phages.pop()
        for phage2 in list_of_phages[::-1]:
            if distance_satisfies(phage1, phage2):
                pairs.append((phage1, phage2))
                list_of_phages.remove(phage2)
                break
    return pairs


def start_reproducing(list_of_phages: list):
    """
    create pairs, make kids
    return list of kids(full of objects), dead phages
    """
    if len(list_of_phages) == 0:
        return []
    result_of_reproduction = []
    type_of_phage = ChloroPhage if isinstance(list_of_phages[0], ChloroPhage) is True else HunterPhage
    pairs = create_pairs(list_of_phages)
    for pair in pairs:
        list_of_children = get_children(*pair, type_of_phage)
        for kid in list_of_children:
            result_of_reproduction.append(kid)
    return result_of_reproduction


def get_children(phage1: Phage, phage2: Phage, type_of_phage):
    """
    return list of children's objects
    """
    genome_1 = phage1.genome
    genome_2 = phage2.genome
    number_of_children = random.randint(2, 4)
    list_of_children = []
    for _ in range(number_of_children):
        genome = get_pair_genome(genome_1, genome_2)
        if Brain.is_correct_genome(genome):
            new_phage = type_of_phage(genome)
            list_of_children.append(new_phage)
    return list_of_children
