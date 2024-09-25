import random

# heuristic function
def h_n(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def print_path(maze, path):
    for x, y in path:
        maze[x][y] = "."

    print('-' * (len(maze[0]) * 2 + 3))
    for i in range(0, len(maze)):
        line = '| '
        for j in range(0, len(maze)):
            line += maze[i][j] + ' '
        print(line + "|")
    print('-' * (len(maze[0]) * 2 + 3))



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

    def generate_maze(self, is_rand = True):
        if self.walls is None:
            return self.maze

        for i in range(0, len(self.walls)):
            for j in self.walls[i]:
                self.maze[i][j] = 'X'
        if is_rand:
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
        else:
            self.start = (13, 2)
            self.maze[self.start[0]][self.start[1]] = 'S'
            self.end1 = (5, 23)
            # self.end1 = (24, 20)
            self.maze[self.end1[0]][self.end1[1]] = 'O'
            self.end2 = (3, 2)
            self.maze[self.end2[0]][self.end2[1]] = '0'

    def print_maze(self):
        print('-' * (len(self.maze[0])*2+3))
        for i in range(0, len(self.maze)):
            line = '| '
            for j in range(0, len(self.maze)):
                line += self.maze[i][j] + ' '
            print(line + "|")
        print('-' * (len(self.maze[0])*2+3))

    def bfs(self, start, end):
        # directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        pass


    def dfs(self, start, end):
        # (x, y) -> x is vertical and y is horizontal
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        stack = [(start, [start])]
        visited = set()

        while stack:
            print(visited)
            (x, y), path = stack.pop()

            if (x, y) == end:
                print_path(self.maze, path)
                return path
            if (x, y) in visited:
                continue

            visited.add((x, y))

            for dx, dy in directions:
                x, y = x + dx, y + dy
                if 0 <= x < len(self.maze) and 0 <= y < len(self.maze[0]) and self.maze[x][y] != 'X' and (x, y) not in visited:
                    stack.append(((x, y), path + [(x, y)]))
        for x, y in visited:
            self.maze[x][y] = '/'

        return None

    def dfs_recursive(self, x, y, end, path, visited):
        # Base case: if we've reached the end
        if (x, y) == end:
            return path + [(x, y)]

        # Mark current node as visited
        visited.add((x, y))
        self.maze[x][y] = '/'  # Optionally mark the maze to show the path visually

        # Directions: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new position is within bounds, not a wall, and not visited
            if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] != 'X' and (nx, ny) not in visited:
                result = self.dfs_recursive(nx, ny, end, path + [(x, y)], visited)
                if result:  # If a path is found, return it
                    return result

        # If no path is found from this node, return None (backtrack)
        return None

    def a_star(self):
        pass


mz = MazeSearch()
mz.generate_maze(is_rand=True)
mz.print_maze()
x = mz.dfs_recursive(mz.start[0], mz.start[1], mz.end1, list(), set())
mz.print_maze()
print_path(mz.maze, x)
