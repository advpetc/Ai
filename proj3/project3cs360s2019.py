import os

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

test_path = "dev_cases/"
# right, down, left, up
orientation = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Solver(object):
    def __init__(self, grid_size, obstacles, dest):
        self.row, self.col = grid_size, grid_size
        self.dest = dest
        self.reward = dict()
        self.states = set()
        self.obstacles = obstacles
        for x in range(grid_size):
            for y in range(grid_size):
                self.states.add((x, y))
                if (x, y) == dest:
                    self.reward[x, y] = 99
                elif (x, y) in obstacles:
                    self.reward[x, y] = -101
                else:
                    self.reward[x, y] = -1
        
    def prettyPrint(self, U):
        to_print = ""
        for i in range(self.row):
            for j in range(self.col):
                if (i, j) == self.dest:
                    to_print += "101 "
                else:
                    to_print += str(U[i, j]) + " "
            to_print += "\n"
        print(to_print)
        print('------')

    def solve(self):
        U = self.cal_util()
        # self.prettyPrint(U)
        pi = dict()
        for s in self.states:
            up_util = sum([p * U[_s] for (p, _s) in self.T(s, orientation[3])])
            down_util = sum([p * U[_s] for (p, _s) in self.T(s, orientation[1])])
            left_util = sum([p * U[_s] for (p, _s) in self.T(s, orientation[2])])
            right_util = sum([p * U[_s] for (p, _s) in self.T(s, orientation[0])])
            curr_max = max(up_util, down_util, left_util, right_util)
            if curr_max == up_util:
                pi[s] = orientation[3]
            elif curr_max == right_util:
                pi[s] = orientation[0]
            elif curr_max == down_util:
                pi[s] = orientation[1]
            elif curr_max == left_util:
                pi[s] = orientation[2]
        return self.to_grid(pi)

    def to_grid(self, pi):
        grid = [[None for _ in range(self.row)] for _ in range(self.col)]
        for x in (range(self.row)):
            for y in (range(self.col)):
                if (x, y) in self.obstacles:
                    grid[y][x] = 'o'
                elif (x, y) == self.dest:
                    grid[y][x] = '.'
                else:
                    mapping = {(1, 0): '>', (0, 1): 'v', (-1, 0): '<', (0, -1): '^'}
                    grid[y][x] = mapping[pi[(x, y)]]
        with open(os.path.join(__location__, 'output.txt'), 'w') as outfile:
            for row in grid:
                for e in row:
                    outfile.write(e)
                outfile.write('\n')

    def cal_util(self):
        _U = dict([(s, 0) for s in self.states])
        _U[self.dest] = 100
        T, gamma, epsilon = self.T, 0.9, 0.1
        while True:
            U = _U.copy()
            delta = 0
            for s in self.states:
                if s == self.dest: 
                    continue
                reward = self.reward[s[0], s[1]]
                # max_score = 0
                # for action in orientation:
                #     score = 0
                #     for (p, s1) in T(s, action):
                #         u = U[s1]
                #         score += (p * u)
                #     max_score = max(max_score, score)
                # _U[s] = reward + gamma * max_score

                _U[s] = reward + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)])
                                                             for a in orientation])
                delta = max(delta, abs(_U[s] - U[s]))
            if delta < epsilon * (1 - gamma) / gamma:
                return U
        
    def T(self, state, action):
        def go(state, direction):
            curr = (state[0] + direction[0], state[1] + direction[1])
            return curr if curr in self.states else state
        # right, down, left, up
        # left 2 -> back -> right 0
        # left 2 -> right -> up   3
        # left 2 -> left -> down  1

        # right 0 -> back -> left  2
        # right 0 -> right -> down 1
        # right 0 -> left -> up    3

        # up 3 -> back -> down    1
        # up 3 -> right -> right  0
        # up 3 -> left -> left    2

        # down 1 -> back -> up    3
        # down 1 -> right -> left 2
        # down 1 -> left -> right 0
        right = orientation[(orientation.index(action) + 1) % len(orientation)]
        left = orientation[orientation.index(action) - 1] # -1 = 3
        back = orientation[(orientation.index(action) + 2) % len(orientation)]
        return [(0.7, go(state, action)),
                (0.1, go(state, right)),
                (0.1, go(state, left)),
                (0.1, go(state, back))]

def main():
    with open(os.path.join(__location__, test_path + 'input-5.txt'), 'r') as infile:
        grid_size = int(infile.readline())
        num_obstacles = int(infile.readline())
        obstacles = list()
        dest = None
        for i, line in enumerate(infile):
            coords = line.strip().split(",")
            x, y = int(coords[0]), int(coords[1]) 
            if i == num_obstacles:
                dest = (x, y)
            else:
                obstacles.append((x, y))
        # print('grid size is: {}\n'
        #       'num of obstacles is: {}\n'
        #       'obstacles are:\n {}\n'
        #       'dest is: {}'.format(
        #           grid_size,
        #           num_obstacles,
        #           obstacles,
        #           dest))
        solver = Solver(grid_size, obstacles, dest)
        solver.solve()
main()

