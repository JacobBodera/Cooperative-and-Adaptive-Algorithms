from mazeSearch import *

'''
Maze in assignment:
start: (13, 2)
end1: (5, 23)
end2:  (3, 2)
'''

# Create maze
mz = MazeSearch()
mz.generate_maze()

# Print original maze
print("\n################# ORIGINAL MAZE #################")
mz.print_maze()

# Run breath first search with path shown
print("\n################ A* SEARCH (E1) ################")
a_star_path = mz.a_star(mz.start, mz.end1)
print_path(mz.maze, a_star_path)

print("\n################ A* SEARCH (E2) ################")
a_star_path = mz.a_star(mz.start, mz.end2)
print_path(mz.maze, a_star_path)

print("\n######### A* SEARCH (CORNER TO CORNER) #########")
a_star_path = mz.a_star((24, 0), (0, 24))
print_path(mz.maze, a_star_path)


# # Run depth first search with path shown
# print("\n################# DEPTH FIRST SEARCH #################")
# dfs_path = mz.dfs_recursive(mz.start[0], mz.start[1], mz.end1, list(), set())
# print_path(mz.maze, dfs_path)
#
# # Run A* search with path shown
# print("\n################# A* SEARCH #################")
# a_star_path = mz.a_star(mz.start, mz.end1)
# print_path(mz.maze, a_star_path)



# from mazeSearch import *
#
# ### Generates output of example maze for each algorithm'''Maze in assignment:start: (13, 2)end1: (5, 23)end2:  (3, 2)'''# Create maze
# mz = MazeSearch()
# mz.generate_maze()
#
# # Print original maze
# print("\n################# ORIGINAL MAZE #################")
# mz.print_maze()
#
# # Run breath first search with path shown
# print("\n################# BREATH FIRST SEARCH #################")
# bfs_path = mz.bfs(mz.start, mz.end1)
# print_path(mz.maze, bfs_path)
#
# # Run depth first search with path shown
# print("\n################# DEPTH FIRST SEARCH #################")
# dfs_path = mz.dfs_recursive(mz.start[0], mz.start[1], mz.end1, list(), set())
# print_path(mz.maze, dfs_path)
#
# # Run A* search with path shown
# print("\n################# A* SEARCH #################")
# a_star_path = mz.a_star(mz.start, mz.end1)
# print_path(mz.maze, a_star_path)