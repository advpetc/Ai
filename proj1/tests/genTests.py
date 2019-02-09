import os
from random import randrange, choice

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def gen(n, a, c, alg, order):
    grid = [[0] * n for _ in range(n)]
    coord = []
    for _ in range(a):
        x, y = randrange(n), randrange(n)
        grid[x][y] += 1
        coord += [(x, y)]
    fname = "{}.txt".format(order)
    with open(os.path.join(__location__, fname), "w+") as tf:
        tf.write(str(n) + "\n")
        tf.write(str(c) + "\n")
        tf.write(str(len(coord)) + "\n")
        tf.write(alg + "\n")
        for x, y in coord:
            tf.write("{},{}\n".format(x, y))


for order in range(10):
    n = 14
    a = randrange(n * n * 2)
    c = randrange(n)
    alg = choice(["dfs", "astar"])
    gen(n, a, c, alg, order)
