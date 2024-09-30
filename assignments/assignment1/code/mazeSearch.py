import heapq
import math
import random
import copy

# heuristic function
def h_n(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def print_path(maze, path):
    m = copy.deepcopy(maze)
    path = path[1:len(path) - 1]
    for x, y in path:
        m[x][y] = "."

    print('-' * (len(m[0]) * 2 + 3))
    for i in range(0, len(m)):
        line = '| '
        for j in range(0, len(m)):
            line += m[i][j] + ' '
        print(line + "|")
    print('-' * (len(m[0]) * 2 + 3))

class MazeSearch:
    def __init__(self, start=None, end1=None, end2=None):
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
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.start = start
        self.end1 = end1
        self.end2 = end2

    def set_walls(self, walls):
        self.walls = walls

    def generate_maze(self):
        if self.walls is None:
            return self.maze

        for i in range(0, len(self.walls)):
            for j in self.walls[i]:
                self.maze[i][j] = 'X'
        if self.start is None or self.end1 is None or self.end2 is None:
            for i in range(0, 3):
                x = random.randint(0, len(self.walls) - 1)
                y = random.randint(0, len(self.walls) - 1)
                while self.maze[x][y] == 'X' or self.maze[x][y] == 'S' or self.maze[x][y] == '1':
                    x = random.randint(0, len(self.walls) - 1)
                    y = random.randint(0, len(self.walls) - 1)
                if i == 0:
                    self.start = (x, y)
                    self.maze[x][y] = 'S'
                if i == 1:
                    self.end1 = (x, y)
                    self.maze[x][y] = '1'
                if i == 2:
                    self.end2 = (x, y)
                    self.maze[x][y] = '2'
        else:
            self.maze[self.start[0]][self.start[1]] = 'S'
            self.maze[self.end1[0]][self.end1[1]] = '1'
            self.maze[self.end2[0]][self.end2[1]] = '2'

    def print_maze(self):
        print('-' * (len(self.maze[0])*2+3))
        for i in range(0, len(self.maze)):
            line = '| '
            for j in range(0, len(self.maze)):
                line += self.maze[i][j] + ' '
            print(line + "|")
        print('-' * (len(self.maze[0])*2+3))

    def bfs(self, start, end):
        queue = [(start, [start])]
        visited = {start}

        while queue:
            (x, y), path = queue.pop(0)

            if (x, y) == end:
                print("Number of visited positions: " + str(len(visited)))
                print("Cost: " + str(len(path)))
                return path

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] != 'X' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        return None

    def dfs_recursive(self, x, y, end, path, visited, count=0):
        # Base case - goal is reached
        if (x, y) == end:
            print("Number of visited positions: " + str(count))
            print("Cost: " + str(len(path)))
            return path + [(x, y)]

        # Mark current node as visited
        visited.add((x, y))
        count += 1

        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy

            # Check if the new position is within bounds, not a wall, and not visited
            if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] != 'X' and (nx, ny) not in visited:
                result = self.dfs_recursive(nx, ny, end, path + [(x, y)], visited, count)
                if result:
                    return result

        # If no path is found from this node, return None (backtrack)
        return None

    def a_star(self, start, end):
        # ( f(n), g(n), (x, y), path )
        priority_queue = [(0 + h_n(start, end), 0, start, [start])]
        visited = set()
        count = 0

        while priority_queue:
            _, g_n, (x, y), path = heapq.heappop(priority_queue)

            if (x, y) == end:
                print("Number of visited positions: " + str(count))
                print("Cost: " + str(len(path)))
                return path

            count += 1

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < len(self.maze) and 0 <= ny < len(self.maze[0]) and self.maze[nx][ny] != 'X' and (nx, ny) not in visited:
                    new_g_n = g_n + 1
                    f_n = new_g_n + h_n((nx, ny), end)
                    visited.add((nx, ny))
                    heapq.heappush(priority_queue, (f_n, new_g_n, (nx, ny), path + [(nx, ny)]))

        return None
