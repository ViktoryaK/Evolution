'''
write a file and read from file to get information
'''
import os

from phage import Phage, create_random_genome, ChloroPhage
import random

def write_in_csv_file(list_of_phages: list[Phage]):
    '''
    get a list of phages objects and write down
    in csv file
    '''
    with open('phages.csv', 'a', encoding='UTF8', newline='') as phages:
        # check if size of file is 0
        if os.stat('phages.csv').st_size == 0:
            phages.write('a,b,x,y,dx,dy,x1,y1,dx1,dy1,x2,y2,dx2,dy2,x3,y3,dx3,dy3')
            phages.write('\n')
        for phage in list_of_phages:
            new_list = list(map(str, phage.genome))
            phages.write(' '.join(new_list))
            phages.write(' ' + f'{phage.position}')
            phages.write('\n')
        phages.write('\n')

def read_csv_file(path):
    '''
    read csv file and return phage's gen
    return [[[genome], (x, y)]]
    '''
    with open(path, "r") as file:
        content = file.readlines()
    rows = content[1:]
    result = []
    #make integers from string
    for row in rows:
        if row != '\n':
            row = row.split(' ')
            str_pos = (row[-2] + row[-1])[1:-2]
            pos = tuple(map(int, str_pos.split(',')))
            result.append([list(map(int, row[:-2])), pos])
    return result

# start = [[8, 3, 6, 3, 7, 5, 8, 5, 6, 4, 7, 5, 7, 3, 1, 3, 9, 5],\
#     [1, 6, 6, 9, 7, 2, 8, 3, 6, 9, 7, 5, 1, 3, 3, 3, 5, 2],\
#     [1, 3, 2, 3, 8, 4, 8, 3, 1, 3, 9, 5, 8, 7, 6, 2, 7, 5],\
#     [2, 3, 7, 3, 8, 9, 8, 3, 1, 3, 4, 5, 2, 3, 5, 3, 3, 5],\
#     [1, 3, 9, 4, 7, 8, 8, 3, 6, 3, 9, 5, 1, 3, 2, 3, 5, 5]]

# list_of_phages = []
# for _ in range(8):
#     new_genome = create_random_genome()
#     phage = ChloroPhage(new_genome)
#     phage.position = (random.randint(0, 100), random.randint(0, 100))
#     list_of_phages.append(phage)
# write_in_csv_file(list_of_phages)
# read_csv_file("phages.csv")
