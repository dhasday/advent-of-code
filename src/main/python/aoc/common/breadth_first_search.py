from collections import deque


class BreadthFirstSearch(object):

    class BreadthFirstSearchNode(object):
        def __init__(self, value, previous_node=None):
            self.value = value
            self.previous_node = previous_node

        def build_path(self):
            path = list()

            cur_node = self
            while cur_node is not None:
                value = cur_node.value
                path.insert(0, value)
                cur_node = cur_node.previous_node

            return path

    def __init__(self, find_adjacent_nodes):
        """
        :param find_adjacent_nodes: A function that takes 1 node and returns a list containing pairs
                                    of all nodes that are directly accessible from that node and
                                    their distance from the current node ( node, distance )
        """
        self.find_adjacent_nodes = find_adjacent_nodes

    def find_path(self, start, end):
        """
        Returns the shortest path from start to end using Breadth First Search Algorithm

        :param start: The initial node
        :param end: The target node
        :return: The shortest path from start to end
        """
        return self.find_path_to_any(start, [end])

    def find_path_to_any(self, start, targets):
        """
        Returns the shortest path from start to any target using Breadth First Search Algorithm

        :param start: The initial node
        :param targets: The target nodes
        :return: The shortest path from start to any target
        """
        closed_set = set()
        open_set = deque()

        open_set.append(self.BreadthFirstSearchNode(start))
        while open_set:
            current_node = open_set.popleft()
            if current_node.value in targets:
                return current_node.build_path()

            if current_node.value in closed_set:
                continue

            closed_set.add(current_node.value)

            adjacent_values = self.find_adjacent_nodes(current_node.value)
            for adjacent_value in adjacent_values:

                if adjacent_value in closed_set:
                    continue

                open_set.append(self.BreadthFirstSearchNode(adjacent_value, current_node))

        return None

