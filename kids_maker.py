'''
to generate children
'''
import random

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

def int_genertor():
    '''
    help function to generate gens
    '''
    empty = []
    for _ in range(18):
        empty.append(random.randint(0, 200))
    return empty

def get_childs(phag1, phag2):
    '''
    return genoms' children
    '''
    # genom1 = phag1.genom
    # genom2 = phag2.genom
    number_of_children = random.randint(1, 4)
    list_of_children = []
    for _ in range(number_of_children):
        list_of_children.append(get_pair_genome(genom1, genom2))
    return list_of_children

# genom1 = int_genertor()
# print(genom1)
# genom2 = int_genertor()
# print(genom2)
genom1 = [15, 112, 3, 120, 176, 71, 137, 121, 62, 42, 197, 1, 60, 108, 155, 135, 160, 43]
genom2 = [20, 107, 91, 77, 153, 54, 153, 149, 104, 46, 180, 145, 89, 49, 107, 187, 14, 143]

# print(get_childs(genom1, genom2))
