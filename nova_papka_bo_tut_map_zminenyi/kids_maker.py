'''
to generate children
'''

import random
from phage import Phage, ChloroPhage, HunterPhage

# TODO: turn a list of dead phages +


def get_pair_genome(genom1, genom2, prob = 0.05):
    '''
    get father's and mother's genoms, merge them and return child
    '''
    child = []
    for i in range(len(genom1)):
        child_genom = (genom1[i] + genom2[i]) // 2
        child.append(child_genom)
    if random.uniform(0, 1) <= prob:
        minus = False
        rand_ind = random.randint(0, len(child) - 1)
        random_int_to_mutation = child[rand_ind]
        if int(random_int_to_mutation) < 0:
            int_to_change = bin(random_int_to_mutation)[3:]
            minus = True
        else:
            int_to_change = bin(random_int_to_mutation)[2:]
        list_of_bin_int = [elem for elem in int_to_change]
        slicer = len(list_of_bin_int) // 3
        first_part = list_of_bin_int[:slicer]
        slicer2 = len(list_of_bin_int) - slicer
        second_part = list_of_bin_int[slicer:slicer2]
        third_part = list_of_bin_int[slicer2:]
        change_better_part = random.uniform(0, 1)
        if change_better_part < 0.1:
            random_ind = random.randint(0, len(first_part) - 1)
            if first_part[random_ind] == "1":
                first_part[random_ind] == "0"
            else:
                first_part[random_ind] = "1"
        elif change_better_part < 0.7:
            random_ind = random.randint(0, len(second_part) - 1)
            if second_part[random_ind] == "1":
                second_part[random_ind] == "0"
            else:
                second_part[random_ind] = "1"
        elif change_better_part >= 0.7:
            random_ind = random.randint(0, len(third_part) - 1)
            if third_part[random_ind] == "1":
                third_part[random_ind] == "0"
            else:
                third_part[random_ind] = "1"
        binary_to_merge = first_part + second_part + third_part
        joined_int = int("".join(binary_to_merge), 2)
        if minus:
            joined_int = int("-" + str(joined_int))
        child[rand_ind] = joined_int
    return child

def distance_satisfies(phage1: Phage, phage2: Phage):
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
        dead_phages.append(first)
        help(phages)
    help(list_of_phages)
    return pairs, dead_phages

def find_out_type(phage: Phage):
    if isinstance(phage, ChloroPhage):
        return True
    else:
        return

def start_reproducing(list_of_phages: list):
    result_of_reproduction = []
    type_of_phage = find_out_type(list_of_phages[0])
    pairs, dead_phages = create_pairs(list_of_phages)
    for pair in pairs:
        list_of_children = get_childs(*pair, type_of_phage)
        for kid in list_of_children:
            result_of_reproduction.append(kid)
    return result_of_reproduction, dead_phages


def int_generator():
    '''
    help function to generate gens
    '''
    empty = []
    for _ in range(18):
        empty.append(random.randint(0, 200))
    return empty

def get_childs(phage1: Phage, phage2:Phage, type_of_phage):
    '''
    return objects of children
    '''
    genom1 = phage1.genome
    genom2 = phage2.genome
    number_of_children = random.randint(1, 4)
    list_of_children = []
    for _ in range(number_of_children):
        if type_of_phage:
            list_of_children.append(ChloroPhage(get_pair_genome(genom1, genom2)))
        else:
            list_of_children.append(HunterPhage(get_pair_genome(genom1, genom2)))
    return list_of_children

# genom1 = [15, 112, 3, 120, 176, 71, 137, 121, 62, 42, 197, 1, 60, 108, 155, 135, 160, 43]
# genom2 = [20, 107, 91, 77, 153, 54, 153, 149, 104, 46, 180, 145, 89, 49, 107, 187, 14, 143]

# print(get_childs(genom1, genom2))
