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
        
    def add_heap(self, cost, node):
        """
        Add a new node or update the cost of an existing node
        """
        
        for i in range(len(self.pq) - 1):
            if self.pq[i][1] == node:
                self.pq.remove(self.pq[i])
                heapq.heapify(self.pq)
        entry = [cost, node]
        heapq.heappush(self.pq, entry)

    def path_cost(self, path):
        """
        Calculate the path total cost and returns it.

        :param path: The path as a sequence of (x, y) positions: [(x1,y1),(x2,y2),(x3,y3),...,(xn,yn)].
        :type path: List of tuples.
        :return: The path's cost.
        :rtype: float.
        """

        total = 0
        for i in range(0, len(path) - 1):
            total += self.cost_map.get_edge_cost(path[i], path[i + 1])
        return total

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

    def dijkstra(self, successorNode, node, start_position, goal_position):
        """
        Plans a path using the Dijkstra algorithm.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
  
        if successorNode.g > node.g + self.cost_map.get_edge_cost([node.i, node.j], successorNode.get_position()):
            successorNode.g = node.g + self.cost_map.get_edge_cost([node.i, node.j], successorNode.get_position())
            successorNode.set_parent(node)
            self.add_heap(successorNode.g, successorNode)

    def greedy(self, successorNode, node, start_position, goal_position):
        """
        Plans a path using greedy search.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
       
        successorNode.set_parent(node)
        successorNode.h = successorNode.distance_to(goal_position[0], goal_position[1])
        self.add_heap(successorNode.h, successorNode)
                    
    def a_star(self, successorNode, node, start_position, goal_position):
        """
        Plans a path using A*.

        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """
        
        distance_goal_point = successorNode.distance_to(goal_position[0], goal_position[1])
        edge_cost = self.cost_map.get_edge_cost([node.i, node.j], successorNode.get_position())
        if successorNode.g + distance_goal_point > node.g + edge_cost + distance_goal_point:
            successorNode.set_parent(node)
            successorNode.h = successorNode.distance_to(goal_position[0], goal_position[1])
            successorNode.g = node.g + edge_cost
            self.add_heap(successorNode.h + successorNode.g, successorNode)
    
    def search(self, algorithm, start_position, goal_position):
        """
        Plans a path using the choosed algorithm.

        :param algorithm: algorithm used to search goal_position.
        :type algorithm: function.
        :param start_position: position where the planning stars as a tuple (x, y).
        :type start_position: tuple.
        :param goal_position: goal position of the planning as a tuple (x, y).
        :type goal_position: tuple.
        :return: the path as a sequence of positions and the path cost.
        :rtype: list of tuples and float.
        """

        self.pq = []
        root = self.node_grid.get_node(start_position[0], start_position[1])
        root.g = 0
        
        self.add_heap(root.g, root)

        while self.pq:
            _, node = heapq.heappop(self.pq)
            node.close_node()

            if (node.get_position()) == goal_position:
                path = self.construct_path(self.node_grid.get_node(goal_position[0], goal_position[1]))
                total_cost = self.path_cost(path) 

                self.node_grid.reset()
                return path, total_cost

            for successor in self.node_grid.get_successors(node.i, node.j):
                successorNode = self.node_grid.get_node(successor[0], successor[1])

                if not successorNode.closed:
                    algorithm(successorNode, node, start_position, goal_position)