from graph import WeightedGraph

g = WeightedGraph()
g.add_node('1')
g.add_node('2')
g.add_node('3')
g.add_node('4')
g.add_node('5')
g.add_node('6')
g.add_node('7')



g.add_edge('1', '2')
g.add_edge('1', '3')
g.add_edge('2', '4')
g.add_edge('2', '5')
g.add_edge('3', '6')
g.add_edge('3', '7')





# print("BFS:", g.bfs('A', 'G'))
print("DFS:", g.dfs('1', '7'))