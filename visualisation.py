import random

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from celluloid import Camera

"""
Looks bad, but works perfectly
------------------------------
"""
from map import Map
all = []
# board = Map(10)

# print(board)
# board.generate_creatures(4, 10)
for i in range(20):
    obj = Map(100)
    obj.generate_creatures(4, 10)
    all.append(obj)

# print(all)


plt.axis([0, 100, 0, 100])
# plt.xlim(0, 30)
# plt.ylim(0, 30)

# numpoints = 10
# # points = np.random.random((2, numpoints))
# # colors = cm.rainbow(np.linspace(0, 1, numpoints))
c = ['#5fb458', '#bb1212']
fig = plt.figure()
camera = Camera(fig)
for board in all:
    for y in range(board.size):
        for x in range(board.size):
            # points += 0.1 * (np.random.random((2, numpoints)) - .5)
            if board.map[y][x]:
                # y = abs(y - board.size) - 1
                if board.map[y][x] == "enemy":
                    # print("enemy " + str(y))
                    abs_y = abs(y - board.size) - 1
                    # print(x, abs_y)
                    plt.scatter(x, abs_y, c=c[1], s=1, marker=8)
                else:
                    # print("prey " + str(y))
                    abs_y = abs(y - board.size) - 1
                    # print(x, abs_y)
                    plt.scatter(x, abs_y, c=c[0], s=1, marker=(7, 2, 45))
    camera.snap()
anim = camera.animate(blit=True, interval=500)
anim.save('my.mp4')
# plt.show()