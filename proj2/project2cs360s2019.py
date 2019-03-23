import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

test_path = "test_case/test_case/"


class User:
    def __init__(self, player):
        self.player = player    # True is me, False is opp
        self.heros = list()     # store all the picked ids

    def addHero(self, hero):
        self.heros.append(hero)

    def popHero(self):
        self.heros.pop()

    def getScore(self):
        score = 0
        s = set()
        for hero in self.heros:
            s.add(hero.ID % 10)
            if self.player:
                score += hero.p * hero.my_m
            else:
                score += hero.p * hero.op_m
        if len(s) == 5:
            return score + 120
        else:
            return score


class Hero:
    def __init__(self, ID, p, my_m, op_m, state):
        self.ID = ID
        self.p = p
        self.my_m = my_m
        self.op_m = op_m
        self.state = state  # who picked or not


class Solver:
    def __init__(self, alg, me, opp, available):
        self.alg = alg
        self.me = me
        self.opp = opp
        self.available = available

    def solve(self):
        def minimax(player, start):
            if len(self.me.heros) == 5 and len(self.opp.heros) == 5:
                return self.me.getScore() - self.opp.getScore(), self.me.heros[start].ID
            if player:
                value = float("-inf")
                hero_id = self.available[-1].ID     # default to last hero
                for h in self.available:
                    if h.state != 0:
                        continue
                    self.me.addHero(h)
                    h.state = 1
                    _value, _hero_id = minimax(False, start)
                    if _value > value:
                        value = _value
                        hero_id = _hero_id
                    elif _value == value:
                        if _hero_id < hero_id:
                            hero_id = _hero_id
                    self.me.popHero()
                    # make it available again
                    h.state = 0
                return value, hero_id
            else:
                value = float("inf")
                hero_id = self.available[-1].ID     # default to last hero
                for h in self.available:
                    if h.state != 0:
                        continue
                    self.opp.addHero(h)
                    h.state = 2
                    _value, _hero_id = minimax(True, start)
                    if _value < value:
                        value = _value
                        hero_id = _hero_id
                    elif _value == value:
                        if _hero_id < hero_id:
                            hero_id = _hero_id
                    self.opp.popHero()
                    # make it available again
                    h.state = 0
                return value, hero_id

        def ab(player, start, alpha, beta):
            if len(self.me.heros) == 5 and len(self.opp.heros) == 5:
                return self.me.getScore() - self.opp.getScore(), self.me.heros[start].ID
            if player:
                value = float("-inf")
                hero_id = self.available[-1].ID     # default to last hero
                for h in self.available:
                    if h.state != 0:
                        continue
                    self.me.addHero(h)
                    h.state = 1
                    _value, _hero_id = ab(False, start, alpha, beta)
                    if _value > value:
                        value = _value
                        hero_id = _hero_id
                    elif _value == value:
                        if _hero_id < hero_id:
                            hero_id = _hero_id
                    self.me.popHero()
                    # make it available again
                    h.state = 0
                    # break the branch
                    if value > beta:
                        return value, hero_id
                    alpha = max(value, alpha)

                return value, hero_id
            else:
                value = float("inf")
                hero_id = self.available[-1].ID     # default to last hero
                for h in self.available:
                    if h.state != 0:
                        continue
                    self.opp.addHero(h)
                    h.state = 2
                    _value, _hero_id = ab(True, start, alpha, beta)
                    if _value < value:
                        value = _value
                        hero_id = _hero_id
                    elif _value == value:
                        if _hero_id < hero_id:
                            hero_id = _hero_id
                    self.opp.popHero()
                    # make it available again
                    h.state = 0
                    # break the branch
                    if value < alpha:
                        return value, hero_id
                    beta = min(value, beta)

                return value, hero_id

        nextHero = None
        if self.alg == 'minimax':
            _, nextHero = minimax(True, len(self.me.heros))
        else:
            _, nextHero = ab(True, len(self.me.heros), float("-inf"), float("inf"))

        print(nextHero)
        with open(os.path.join(__location__, 'output.txt'), 'w') as outfile:
            outfile.write(str(nextHero))


def main():

    with open(os.path.join(__location__, test_path + 'input0.txt'), 'r') as infile:
        # Number of heros to be used
        n = int(infile.readline())
        # Algorithm to be used: minimax or ab
        alg = infile.readline().strip()
        # has already been picked by you (1)
        me = User(True)
        # picked by the opponent (2)
        opp = User(False)
        # is still available in the pool (0)
        available = []
        for _in in infile:
            data = _in.strip().split(",")
            ID, p, my_m, op_m, indicator = int(data[0]), float(data[1]), float(data[2]), float(data[3]), int(data[4])
            hero = Hero(ID, p, my_m, op_m, indicator)
            if indicator == 0:
                available.append(hero)
            elif indicator == 1:
                me.addHero(hero)
            elif indicator == 2:
                opp.addHero(hero)
        heros = sorted(available, key=lambda hero: hero.ID)
        solver = Solver(alg, me, opp, heros)
        solver.solve()


if __name__ == "__main__":
    main()
