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
    c = ['#5fb458', '#bb1212']
    fig = plt.figure()
    camera = Camera(fig)
    for board in give_vika:
        for y in range(len(board)):
            for x in range(len(board)):
                if board[y][x]:
                    if board[y][x] == "red":
                        abs_y = abs(y - len(board)) - 1
                        plt.scatter(x, abs_y, c=c[1], s=5, marker=8)
                    elif board[y][x] == "green":
                        abs_y = abs(y - len(board)) - 1
                        plt.scatter(x, abs_y, c=c[0], s=5, marker=(7, 2, 45))
        camera.snap()
    anim = camera.animate(blit=True, interval=200)
    anim.save('my.mp4')
