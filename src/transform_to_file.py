"""
write a file and read from file to get information
"""
import os

from phage import Phage, create_random_genome, ChloroPhage, HunterPhage
import random

def write_in_csv_file(list_of_phages: list[Phage]):
    """
    get a list of phages objects and write down
    in csv file
    """
    with open("phages.csv", "w", encoding="utf-8", newline="") as phages:
        # check if size of file is 0
        if os.stat("phages.csv").st_size == 0:
            phages.write("a,b,x,y,dx,dy,x1,y1,dx1,dy1,x2,y2,dx2,dy2,x3,y3,dx3,dy3")
            phages.write("\n")
        for phage in list_of_phages:
            str_class = "ChloroPhage" if isinstance(phage, ChloroPhage) else "HunterPhage"
            new_list = list(map(str, phage.genome))
            phages.write(" ".join(new_list))
            phages.write(" " + f"{phage.position}")
            phages.write(" " + f"{str_class}")
            phages.write("\n")
        phages.write("\n")

def read_csv_file(path):
    """
    read csv file and return phage's genome
    return [[[genome], (x, y), "class"]]
    """
    with open(path, "r") as file:
        content = file.readlines()
    rows = content[1:]
    result = []
    #make integers from string
    for row in rows:
        if row != "\n":
            splited_row = row.split(" ")
            row = splited_row[:-1]
            phage_class = splited_row[-1][:-1]
            str_pos = (row[-2] + row[-1])[1:][:-1]
            pos = tuple(map(int, str_pos.split(",")))
            result.append([list(map(int, row[:-2])), pos, phage_class])
    return result

# list_of_phages = []
# for _ in range(8):
#     new_genome = create_random_genome()
#     phage = ChloroPhage(new_genome)
#     phage.position = (random.randint(0, 100), random.randint(0, 100))
#     list_of_phages.append(phage)
# write_in_csv_file(list_of_phages)
# print(read_csv_file("phages.csv"))
