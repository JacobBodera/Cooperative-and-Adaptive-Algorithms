from graph import WeightedGraph

g = WeightedGraph()
g.add_node('S')
g.add_node('A')
g.add_node('B')
g.add_node('C')
g.add_node('D')
g.add_node('E')
g.add_node('F')
g.add_node('G')
g.add_node('H')


g.add_edge('S', 'A', 3)
g.add_edge('S', 'D', 4)
g.add_edge('A', 'B', 4)
g.add_edge('A', 'D', 5)
g.add_edge('B', 'C', 3)
g.add_edge('B', 'H', 4)
g.add_edge('D', 'E', 2)
g.add_edge('E', 'B', 5)
g.add_edge('E', 'C', 4)
g.add_edge('E', 'F', 4)
g.add_edge('F', 'H', 5)
g.add_edge('H', 'G', 1)


print("BFS:", g.bfs('A', 'G'))
print("DFS:", g.dfs('A', 'G'))