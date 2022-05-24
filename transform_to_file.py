'''
write a file and read from file to get information
'''
import csv

def transform_list_to_dict(list_of_phages):
    '''
    make a dictionary from list
    '''
    collection_of_phages = []
    for phage in list_of_phages:
        info = {"b":phage[0],
        "a":phage[1],
        "x":phage[2],
        "y":phage[3],
        "dx":phage[4],
        "dy":phage[5],
        "x1":phage[6],
        "y1":phage[7],
        "dx1":phage[8],
        "dy1":phage[9],
        "x2":phage[10],
        "y2":phage[11],
        "dx2":phage[12],
        "dy2":phage[13],
        "x3":phage[14],
        "y3":phage[15],
        "dx3":phage[16],
        "dy3":phage[17],
        }
        collection_of_phages.append(info)
    return collection_of_phages

def write_in_csv_file(list_of_phages):
    '''
    get a list of phages gen's and write down
    in csv file
    '''
    fieldnames = ["b", "a", "x", "y", "dx", "dy",\
         "x1", "y1", "dx1", "dy1",\
         "x2", "y2", "dx2", "dy2",\
         "x3", "y3", "dx3", "dy3",]
    #create csv file form dictionary
    with open('phages.csv', 'w', encoding='UTF8', newline='') as phages:
        writer = csv.DictWriter(phages, fieldnames)
        writer.writeheader()
        writer.writerows(list_of_phages)

def read_csv_file(path):
    '''
    read csv file and return phage's gen
    '''
    with open(path, "r") as file:
        content = file.readlines()
    rows = content[1:]
    result = []
    #make integers from string
    for row in rows:
        row = row[:-1].split(",")
        result.append(list(map(int, row)))
    return result

start = [[8, 3, 6, 3, 7, 5, 8, 5, 6, 4, 7, 5, 7, 3, 1, 3, 9, 5],\
    [1, 6, 6, 9, 7, 2, 8, 3, 6, 9, 7, 5, 1, 3, 3, 3, 5, 2],\
    [1, 3, 2, 3, 8, 4, 8, 3, 1, 3, 9, 5, 8, 7, 6, 2, 7, 5],\
    [2, 3, 7, 3, 8, 9, 8, 3, 1, 3, 4, 5, 2, 3, 5, 3, 3, 5],\
    [1, 3, 9, 4, 7, 8, 8, 3, 6, 3, 9, 5, 1, 3, 2, 3, 5, 5]]
res = transform_list_to_dict(start)
write_in_csv_file(res)
print(read_csv_file("phages.csv"))