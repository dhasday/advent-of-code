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
                path.insert(0, cur_node.value)
                cur_node = cur_node.previous_node

            return path

    def find_path(self, start, end, find_adjacent_nodes):
        """
        Returns the shortest path from start to end using Breadth First Search Algorithm

        :param start: The initial node
        :param end: The target node
        :param find_adjacent_nodes: A function that takes 1 node and returns a list containing pairs
                                    of all nodes that are directly accessible from that node and
                                    their distance from the current node ( node, distance )
        :return: The shortest path from start to end
        """
        return self.find_path_multiple_targets(start, [end], find_adjacent_nodes)

    def find_path_multiple_targets(self, start, targets, find_adjacent_nodes):
        """
        Returns the shortest path from start to any target using Breadth First Search Algorithm

        :param start: The initial node
        :param targets: The target nodes
        :param find_adjacent_nodes: A function that takes 1 node and returns a list containing pairs
                                    of all nodes that are directly accessible from that node and
                                    their distance from the current node ( node, distance )
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

            adjacent_values = find_adjacent_nodes(current_node.value)
            for adjacent_value in adjacent_values:

                if adjacent_value in closed_set:
                    continue

                open_set.append(self.BreadthFirstSearchNode(adjacent_value, current_node))

        return None

