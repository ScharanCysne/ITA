from grid import Node, NodeGrid
from math import inf
import heapq

class PathPlanner(object):
    """
    Represents a path planner, which may use Dijkstra, Greedy Search or A* to plan a path.
    """
    def __init__(self, cost_map):
        """
        Creates a new path planner for a given cost map.

        :param cost_map: cost used in this path planner.
        :type cost_map: CostMap.
        """
        self.cost_map = cost_map
        self.node_grid = NodeGrid(cost_map)
        self.pq = []                            # Priority Queue for minimum distances to root node

    def add_heap(self, cost, node):
        
        'Add a new node or update the cost of an existing node'
        
        for i in range(len(self.pq) - 1):
            if self.pq[i][1] == node:
                self.pq.remove(self.pq[i])
                heapq.heapify(self.pq)
        entry = [cost, node]
        heapq.heappush(self.pq, entry)

    @staticmethod
    def construct_path(goal_node):
        """
        Extracts the path after a planning was executed.

        :param goal_node: node of the grid where the goal was found.
        :type goal_node: Node.
        :return: the path as a sequence of (x, y) positions: [(x1,y1),(x2,y2),(x3,y3),...,(xn,yn)].
        :rtype: list of tuples.
        """
        node = goal_node
        # Since we are going from the goal node to the start node following the parents, we
        # are transversing the path in reverse
        reversed_path = []
        while node is not None:
            reversed_path.append(node.get_position())
            node = node.parent
        return reversed_path[::-1]  # This syntax creates the reverse list

    def dijkstra(self, start_position, goal_position):
        """
        Plans a path using the Dijkstra algorithm.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """

        total_cost = 0        
        root = self.node_grid.get_node(start_position[0], start_position[1])
        root.g = 0
        
        self.add_heap(root.g, root)

        while self.pq:
            cost, node = heapq.heappop(self.pq)
            for successor in self.node_grid.get_successors(node.i, node.j):
                successorNode = self.node_grid.get_node(successor[0], successor[1])
                if successorNode.g > node.g + self.cost_map.get_edge_cost([node.i, node.j], successor):
                    successorNode.g = node.g + self.cost_map.get_edge_cost([node.i, node.j], successor)
                    successorNode.set_parent(node)
                    self.add_heap(successorNode.g, successorNode)
        
        path = self.construct_path(self.node_grid.get_node(goal_position[0], goal_position[1]))

        for node in path:
            total_cost += self.node_grid.get_node(node[0],node[1]).g
        
        self.node_grid.reset()
        return path, total_cost  

    def greedy(self, start_position, goal_position):
        """
        Plans a path using greedy search.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
        total_cost = 0        
        root = self.node_grid.get_node(start_position[0], start_position[1])
        root.h = root.distance_to(goal_position[0], goal_position[1])
        
        self.add_heap(root.h, root)

        while self.pq:
            cost, node = heapq.heappop(self.pq)
            node.close_node()
            for successor in self.node_grid.get_successors(node.i, node.j):
                successorNode = self.node_grid.get_node(successor[0], successor[1])
                if not successorNode.closed:
                    successorNode.set_parent(node)
                    i, k = successorNode.get_position()
                    if (i, k) == goal_position:
                        path = self.construct_path(self.node_grid.get_node(goal_position[0], goal_position[1]))
                        for node in path:
                            total_cost += self.node_grid.get_node(node[0],node[1]).g
                        self.node_grid.reset()
                        return path, total_cost

                    successorNode.h = successorNode.distance_to(goal_position[0], goal_position[1])
                    self.add_heap(successorNode.h, successorNode)  

    def a_star(self, start_position, goal_position):
        """
        Plans a path using A*.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
        # Todo: implement the A* algorithm
        # The first return is the path as sequence of tuples (as returned by the method construct_path())
        # The second return is the cost of the path
        self.node_grid.reset()
        return [], inf  # Feel free to change this line of code
