import time

import os
from heapq import heappush, heappop

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Camera:
    def __init__(self, n, c, a, alg):
        self.n = n  # width and height
        self.c = c  # number of camera
        self.a = a  # number of animal
        self.alg = alg  # algorithm to use: dfs or astar
        self.grid = [[0] * n for _ in range(n)]
        self.score = 0
        self.maxRow = [0 * n for _ in range(n)]

    def put_animals(self, coordinates):
        for x, y in coordinates:
            self.grid[x][y] += 1

    def solver(self):
        def dfs(queens, xy_sum, xy_diff):
            count = len(queens)
            if count == self.c:  # row number: if equals to n -> found one sol
                self.score = max(self.score, get_current_score(queens))
                return None
            start = 0 if count == 0 else queens[-1][0] + 1
            for p in range(start, self.n):  # row number
                if self.n - p < self.c - count:
                    break
                current_score = get_current_score(queens)
                if current_score + get_future(p) < self.score:
                    break
                for q in range(self.n):  # col number
                    valid = True
                    for r, c in queens:
                        if q == c:
                            valid = False
                            break
                    if valid and p - q not in xy_diff and p + q not in xy_sum:
                        dfs(queens + [(p, q)], xy_sum + [p + q], xy_diff + [p - q])

        def astar():
            open_set = [(0, [], [], [])]  # 0:current state score; 1: current coordinates; 2: xy_sum; 3: xy_diff
            while len(open_set) != 0:
                node = heappop(open_set)
                current_score = -node[0]
                current_state = node[1]
                xy_sum = node[2]
                xy_diff = node[3]
                if len(current_state) == self.c:
                    self.score = max(self.score, current_score)
                start_p = 0 if len(current_state) == 0 else current_state[-1][0] + 1
                for p in range(start_p, self.n):
                    if self.n - p < self.c - len(current_state):
                        break
                    if current_score + get_future(p) < self.score:
                        break
                    for q in range(self.n):
                        valid = True
                        for r, c in current_state:
                            if q == c:
                                valid = False
                                break
                        if valid and p + q not in xy_sum and p - q not in xy_diff:
                            heappush(open_set, (
                                -current_score - self.grid[p][q],
                                list(current_state + [(p, q)]),
                                list(xy_sum + [p + q]),
                                list(xy_diff + [p - q])
                            )
                                     )

        def get_current_score(res):
            local_score = 0
            for r, c in res:
                local_score += self.grid[r][c]
            return local_score

        def get_future(next_row):
            return self.maxRow[next_row]

        for index, rows in enumerate(reversed(self.grid)):
            max_row = max(rows)
            i = self.n - index - 1
            if i == self.n - 1:
                self.maxRow[i] = max_row
            else:
                self.maxRow[i] = max_row + self.maxRow[i + 1]

        if "dfs" in self.alg:
            dfs([], [], [])
        else:
            astar()
        for row in self.grid:
            print row
        with open(os.path.join(__location__, 'output.txt'), 'w') as outfile:
            outfile.write(str(self.score))
        print "score is: %d" % self.score


def main():

    animals = []
    with open(os.path.join(__location__, 'input7.txt'), 'r') as infile:
        n = int(infile.readline())
        c = int(infile.readline())
        a = int(infile.readline())
        alg = infile.readline()
        for coord in infile:
            coo = coord.strip().split(",")
            animals.append((int(coo[0]), int(coo[1])))
    print "n is %d\nc is %d\na is %d\nalgorithm is %s" % (n, c, a, alg)
    cam = Camera(n, c, a, alg)
    cam.put_animals(animals)
    start_time = time.time()
    print "start time is: %s" % start_time
    cam.solver()
    print "time elapsed: %s second" % (time.time() - start_time)


if __name__ == "__main__":
    main()