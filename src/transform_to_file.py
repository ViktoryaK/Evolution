'''
write a file and read from file to get information
'''
import os

def write_in_csv_file(list_of_phages):
    '''
    get a list of phages gen's and write down
    in csv file
    '''
    with open('phages.csv', 'a', encoding='UTF8', newline='') as phages:
        # check if size of file is 0
        if os.stat('phages.csv').st_size == 0:
            phages.write('a,b,x,y,dx,dy,x1,y1,dx1,dy1,x2,y2,dx2,dy2,x3,y3,dx3,dy3')
            phages.write('\n')
        for genom in list_of_phages:
            new_list = list(map(str, genom))
            phages.write(' '.join(new_list))
            phages.write('\n')
        phages.write('\n')

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
        if row != '\n':
            row = row.split(' ')
            result.append(list(map(int, row)))
    return result

# start = [[8, 3, 6, 3, 7, 5, 8, 5, 6, 4, 7, 5, 7, 3, 1, 3, 9, 5],\
#     [1, 6, 6, 9, 7, 2, 8, 3, 6, 9, 7, 5, 1, 3, 3, 3, 5, 2],\
#     [1, 3, 2, 3, 8, 4, 8, 3, 1, 3, 9, 5, 8, 7, 6, 2, 7, 5],\
#     [2, 3, 7, 3, 8, 9, 8, 3, 1, 3, 4, 5, 2, 3, 5, 3, 3, 5],\
#     [1, 3, 9, 4, 7, 8, 8, 3, 6, 3, 9, 5, 1, 3, 2, 3, 5, 5]]

# write_in_csv_file(start)
# read_csv_file("phages.csv")