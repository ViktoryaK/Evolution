import matplotlib.pyplot as plt
from celluloid import Camera
"""
            Map visualization
-------------------------------------------------------
#      Developed by Viktoria somewhere in time and space    #
#             All rights are mine                           #
#               Use for fun                                 #
-------------------------------------------------------
"""

def magic(give_vika):
    plt.axis([0, 100, 0, 100])
    c2 = ['#576b37', '#e44b30']
    fig = plt.figure()
    camera = Camera(fig)
    plt.xticks(color='w')
    plt.yticks(color='w')
    i = 1
    for board in give_vika:
        plt.text(40, 105, s="Generation: " + str(i//20+1), animated=True)
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x]:
                    if board[y][x] == "red":
                        plt.plot(x, y, c=c2[1], marker=4)
                    elif board[y][x] == "green":
                        plt.plot(x, y, c=c2[0], marker="h")
        camera.snap()
        print(i)
        i += 1
    anim = camera.animate(blit=True, interval=200)
    anim.save('try6.mp4')
