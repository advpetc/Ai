import os
from random import randrange, choice, uniform, shuffle

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
directory = "my_tests/"

class TestHero:
    def __init__(self, ID):
        self.ID = ID
        self.p = uniform(0.0, 200.0)
        self.my_m = uniform(0.0, 1.0)
        self.opp_m = uniform(0.0, 1.0)
        self.state = 0

    def setMem(self, state):
        self.state = state

    def __repr__(self):
        return "{0},{1},{2},{3},{4}\n".format(self.ID,
                self.p, self.my_m, self.opp_m, self.state)

for order in range(10):
    fname = directory + "input{}.txt".format(order)
    with open(os.path.join(__location__, fname), "w+") as tf:
        num_heros = randrange(400)
        IDS = [ID for ID in range(10001, 100000)]
        shuffle(IDS)
        alg = choice(["minimax", "ab"])
        tf.write(str(num_heros) + "\n")
        tf.write(alg + "\n")
        for i in range(num_heros):
            t = TestHero(IDS[i])
            if i < 5:
                state = choice(["1", "2"])
                t.setMem(state)
            tf.write(repr(t))
