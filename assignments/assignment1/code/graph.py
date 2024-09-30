from collections import deque

def back_path(predecessors, goal):
    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = predecessors[current]

    path.reverse()  # Reverse the path to get the correct order from start to goal
    return path


class WeightedGraph:
    def __init__(self):
        self.graph = {}
    
    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
    
    def add_edge(self, node1, node2, weight = 1):
        if node1 in self.graph and node2 in self.graph:
            self.graph[node1].append((node2, weight))
        else:
            raise Exception("One or both of the nodes do not exist.")
    
    def bfs(self, root, goal):

        if root not in self.graph or goal not in self.graph:
            raise Exception("One or both of the nodes does not exist in graph.")

        visited = set()
        queue = deque([root])
        predecessors = {root: None}

        while queue:
            node = queue.popleft()
            
            if node == goal:
                return back_path(predecessors, goal)

            if node not in visited:
                visited.add(node)

                for neighbour, _ in self.graph[node]:
                    if neighbour not in visited and neighbour not in predecessors:
                        queue.append(neighbour)
                        predecessors[neighbour] = node
        return None

    def dfs(self, root, goal):
        visited = set()
        stack = [root]
        predecessors = {root: None}

        while stack:
            node = stack.pop()  # Pop a node from the stack
            if node == goal:
                return back_path(predecessors, goal)
            
            if node not in visited:
                visited.add(node)
                for neighbor, _ in self.graph[node]:
                    if neighbor not in visited and neighbor not in predecessors:
                        stack.append(neighbor)
                        predecessors[neighbor] = node

        return None

    def display(self):
        # Print out the graph for debugging
        for node in self.graph:
            print(f"{node}: {self.graph[node]}")