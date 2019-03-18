import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

test_path = "test_case/test_case/"

class User:
    def __init__(self, player):
        self.score = 0
        self.heros = list()
        self.player = player # 1 is me, 2 is opp
        self.s = set() # synergy: recording the num of different last digit

    def __str__(self):
         return "Current player is {0}\n" \
                "Current score is {1}\n" \
                "Current Heros is {2}\n" \
                "Current Synergy is {3}".format(
                        self.player, self.score, self.heros, self.s)

    def addHero(self, hero):
        # determine if has bounce points
        last_digit = hero.ID[-1]
        self.s.add(last_digit)
        # only have can pick 5 heros at most
        if len(self.s) == 5: self.score += 120
        if self.player == 1:
            self.score += hero.p * hero.my_m
        else:
            self.score += hero.p * hero.op_m
        # TODO
        self.heros.append(hero)

class Hero:
    def __init__(self, ID, p, my_m, op_m, state):
        self.ID = ID
        self.p = p
        self.my_m = my_m
        self.op_m = op_m
        self.state = state # who picked or not

class Solver:
    def __init__(self, alg, me, opp, avaliable):
        self.alg = alg
        self.me = me
        self.opp = opp
        self.avaliable = avaliable
        self.next_ID = None

    def solve(self):
        # hero: Hero, count: int, player: True (me) False (opp)
        def minimax(hero, count, player):
            if count == 0 or len(self.available) == 0:
                print("reach")
                self.next_ID = hero.ID
                return self.me.score - self.opp.score
            if player:
                value = float("-inf")
                neighbours = len(self.available)
                for i in range(neighbours):
                    h = self.avaliable[i]
                    self.me.addHero(h)
                    self.avaliable.remove(h)
                    value = max(value, minmax(h, count - 1, False))
                return value
            else:
                value = float("inf")
                neighbours = len(self.available)
                for i in range(neighbours):
                    h = self.avaliable[i]
                    self.opp.addHero(h)
                    self.avaliable.remove(h)
                    value = max(value, minmax(h, count - 1, True))
                return value

        def ab():
            pass

        print(self.alg)
        print(len(self.avaliable))
        print(5 - len(self.me.heros))
        if self.alg == "minimax":
            print("reach here")
            minimax(self.avaliable[0], 5 - len(self.me.heros), True)
        else:
            ab()

        with open(os.path.join(__location__, 'output.txt'), 'w') as outfile:
            outfile.write(str(self.next_ID))

def main():

    with open(os.path.join(__location__, test_path + 'input0.txt'), 'r') as infile:
        # Number of heros to be used
        n = int(infile.readline())
        # Algorithm to be used: minimax or ab
        alg = infile.readline()
        # has already been picked by you (1)
        me = User(1)
        # picked by the opponent (2)
        opp = User(2)
        # is still available in the pool (0)
        avaliable = []
        for _in in infile:
            data = _in.strip().split(",")
            ID, p, my_m, op_m, indicator = data[0], float(data[1]), float(data[2]), float(data[3]), data[4]
            hero = Hero(ID, p, my_m, op_m, indicator)
            if indicator == "0":
                avaliable.append(hero)
            elif indicator == "1":
                me.addHero(hero)
            elif indicator == "2":
                opp.addHero(hero)
        solver = Solver(alg, me, opp, avaliable)
        solver.solve()

if __name__ == "__main__":
    main()
