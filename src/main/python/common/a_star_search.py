class AStarSearch(object):

    class AStarNode(object):
        def __init__(self, value, previous_node, g_score, h_score):
            self.value = value
            self.previous_node = previous_node

            self.g_score = g_score
            self.h_score = h_score
            self.f_score = g_score + h_score

    def find_shortest_path(self, start, end, heuristic_cost_estimate, find_adjacent_nodes):
        """
        Returns the shortest path from start to end using A* Search Algorithm

        :param start: The initial node
        :param end: The target node
        :param heuristic_cost_estimate: A function that takes 2 nodes and calculates the expected
                                        cost to get from the first to the second
        :param find_adjacent_nodes: A function that takes 1 node and returns pairs of all nodes
                                    that are directly accessible from that node and their distance
                                    ( node, distance )
        :return: The shortest path from start to end
        """
        closed_set = dict()
        open_set = dict()

        start_node = self.AStarNode(start, None, 0, heuristic_cost_estimate(start, end))
        open_set[start] = start_node

        while open_set:
            current_node = self._get_node_with_lowest_f_score(open_set)
            if current_node.value == end:
                return self._reconstruct_path_to_node(current_node)

            del open_set[current_node.value]
            closed_set[current_node.value] = current_node

            adjacent_values = find_adjacent_nodes(current_node.value)
            for (adjacent_value, adjacent_distance) in adjacent_values:
                if adjacent_value in closed_set:
                    continue

                adjacent_node = open_set.get(adjacent_value)
                possible_g_score = current_node.g_score + adjacent_distance

                if adjacent_node is None or adjacent_node.g_score < possible_g_score:
                    adjacent_node = self.AStarNode(
                        adjacent_value,
                        current_node,
                        possible_g_score,
                        heuristic_cost_estimate(adjacent_value, end)
                    )

                open_set[adjacent_value] = adjacent_node

        # We've explored everything and there's no path from start to end
        return None

    def _get_node_with_lowest_f_score(self, open_set):
        lowest_node = None

        for node in open_set.values():
            if lowest_node is None or node.f_score < lowest_node.f_score:
                lowest_node = node

        return lowest_node

    def _reconstruct_path_to_node(self, node):
        path = list()

        cur_node = node
        while cur_node is not None:
            path.insert(0, cur_node.value)
            cur_node = cur_node.previous_node

        return path
