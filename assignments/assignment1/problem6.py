from mazeSearch import *


# Create maze
mz = MazeSearch()
mz.generate_maze(is_rand=False)

# Print original maze
print("################# ORIGINAL MAZE #################")
mz.print_maze()

# Run breadth first search with path shown
print("################# BREADTH FIRST SEARCH #################")
bfs_path = mz.bfs(mz.start, mz.end1)
print_path(mz.maze, bfs_path)

# Run depth first search with path shown
print("################# DEPTH FIRST SEARCH #################")
dfs_path = mz.dfs_recursive(mz.start[0], mz.start[1], mz.end1, list(), set())
print_path(mz.maze, dfs_path)

# Run A* search with path shown
print("################# A* SEARCH #################")
a_star_path = mz.a_star(mz.start, mz.end1)
print_path(mz.maze, a_star_path)

