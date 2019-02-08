import time

from heapq import heappush, heappop


class Camera:
    def __init__(self, n, c, a, alg):
        self.n = n  # width and height
        self.c = c  # number of camera
        self.a = a  # number of animal
        self.alg = alg  # algorithm to use: dfs or astar
        self.grid = [[0] * n for _ in range(n)]
        self.score = 0
        self.placement = []

    def put_animals(self, coordinates):
        for x, y in coordinates:
            try:
                self.grid[x][y] += 1
            except IndexError:
                print (x, y)

    def solver(self):
        def dfs(queens, xy_sum, xy_diff):
            count = len(queens)
            if count == self.c:  # row number: if equals to n -> found one sol
                # self.score = max(self.score, get_current_score(queens))
                local_max = get_current_score(queens)
                if self.score < local_max:
                    self.placement = queens
                    self.score = local_max
                return None
            start = 0 if count == 0 else queens[-1][0] + 1
            for p in range(start, self.n):  # row number
                if self.n - p < self.c - count:
                    break
                current_score = get_current_score(queens)
                future_score = get_future(p)
                if current_score + future_score < self.score:
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
                if len(node[1]) == self.c:
                    self.score = max(self.score, -node[0])
                start_p = 0 if len(node[1]) == 0 else node[1][-1][0] + 1
                current_score = -node[0]
                current_state = node[1]
                xy_sum = node[2]
                xy_diff = node[3]
                for p in range(start_p, self.n):
                    if self.n - p < self.c - len(current_state):
                        break
                    future_score = get_future(p)
                    if current_score + future_score < self.score:
                        break
                    for q in range(self.n):
                        valid = True
                        for r, c in current_state:
                            if q == c:
                                valid = False
                                break
                        if valid and p + q not in xy_sum and p - q not in xy_diff:
                            heappush(open_set, (-current_score - self.grid[p][q],
                                                list(current_state + [(p, q)]),
                                                list(xy_sum + [p + q]),
                                                list(xy_diff + [p - q])))

        def get_current_score(res):
            local_score = 0
            for r, c in res:
                local_score += self.grid[r][c]
            return local_score

        def get_future(next_row):
            local_score = 0
            for r in range(next_row, self.n):
                for c in range(self.n):
                    local_score += self.grid[r][c]
            return local_score

        if "dfs" in self.alg:
            dfs([], [], [])
            print self.placement
        else:
            astar()
        for row in self.grid:
            print row
        print "score is: %d" % self.score


def main():
    animals = []
    with open('input8.txt', 'r') as infile:
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
