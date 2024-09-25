import random

class MazeSearch:
    def __init__(self):
        self.maze = [[' '] * 25 for _ in range(25)]
        self.walls = [[4, 5, 17, 18],
                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                      [0, 1, 2, 3, 4, 8, 14, 15, 16, 17, 18, 19, 20],
                      [3, 4, 5, 8, 14, 15, 16, 17, 18, 19, 20],
                      [3, 4, 5, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20],
                      [8, 9, 10],
                      [8, 9, 10, 14, 15, 16, 17, 18, 19, 20],
                      [0, 1, 2, 3, 4, 5, 6, 8],
                      [10, 24],
                      [10, 23, 24],
                      [8, 9, 10, 11, 12, 15, 16, 22, 23, 24],
                      [10, 15, 16, 21, 22, 23, 24],
                      [10, 15, 16, 18, 21, 24],
                      [4, 15, 16, 18, 21],
                      [15, 16, 18, 21],
                      [18, 21],
                      [2, 3, 4, 18, 21],
                      [2, 3, 4, 6, 7, 10, 11, 12, 18],
                      [2, 6, 7, 10, 11, 12, 18, 19, 20, 21, 22, 23],
                      [0, 1, 2, 6, 7, 10, 11, 12, 18, 19, 20, 21],
                      [0, 1, 2, 6, 7, 10, 11, 12, 18, 19],
                      [6, 7, 10, 11, 12, 18, 19],
                      [10, 11, 12, 18, 19],
                      [18, 19],
                      []]
        self.start = None
        self.end1 = None
        self.end2 = None

    def set_walls(self, walls):
        self.walls = walls

    def generate_maze(self):
        if self.walls is None:
            return self.maze

        for i in range(0, len(self.walls)):
            for j in self.walls[i]:
                self.maze[i][j] = 'X'

        for i in range(0, 3):
            x = random.randint(0, len(self.walls) - 1)
            y = random.randint(0, len(self.walls) - 1)
            while self.maze[x][y] == 'X':
                x = random.randint(0, len(self.walls) - 1)
                y = random.randint(0, len(self.walls) - 1)
            if i == 0:
                self.start = (x, y)
                self.maze[x][y] = 'S'
            if i == 1:
                self.end1 = (x, y)
                self.maze[x][y] = 'O'
            if i == 2:
                self.end2 = (x, y)
                self.maze[x][y] = '0'

    def print_maze(self):
        print('-' * (len(self.maze[0])*2+3))
        for i in range(0, len(self.maze)):
            line = '| '
            for j in range(0, len(self.maze)):
                line += self.maze[i][j] + ' '
            print(line + "|")
        print('-' * (len(self.maze[0])*2+3))

mz = MazeSearch()
mz.generate_maze()
mz.print_maze()