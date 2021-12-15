import heapq


def _cmp(v1, v2):
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0


class DijkstraSearch(object):

    class DijkstraNode(object):
        def __init__(self, value, distance, previous_node=None):
            self.value = value
            self.distance = distance
            self.previous_node = previous_node

        def __cmp__(self, other):
            cmp_distance = _cmp(self.distance, other.distance)
            if cmp_distance:
                return cmp_distance
            else:
                return _cmp(self.value, other.value)

        def set_distance(self, distance, previous_node):
            self.distance = distance
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
        :param find_adjacent_nodes: A function that takes 1 node and returns pairs of all nodes
                                    that are directly accessible from that node and their distance
                                    ( node, distance )
        """
        self.find_adjacent_nodes = find_adjacent_nodes

    def find_shortest_path(self, start, end):
        """
        Returns the shortest path from start to end using Dijkstra Search Algorithm

        :param start: The initial node
        :param end: The target node
        :return: A pair containing the shortest path from start to end and the total distance
        """
        closed_set = self._execute_search(start)

        if end not in closed_set:
            return None, None
        else:
            return closed_set[end].build_path(), closed_set[end].distance

    def find_shortest_path_to_any(self, start, ends):
        """
        Returns the shortest path from start to end using Dijkstra Search Algorithm

        :param start: The initial node
        :param ends: An array of target values
        :return: A pair containing the shortest path from start to any end and the total distance
        """
        closed_set = self._execute_search(start)

        end_node = None
        for end in ends:
            if end in closed_set:
                node = closed_set[end]
                if not end_node or node.distance < end_node.distance:
                    end_node = node

        if end_node:
            return end_node.build_path(), end_node.distance
        else:
            return None, None

    def _execute_search(self, start):
        open_set = []
        closed_set = dict()

        heapq.heappush(open_set, (0, start))
        closed_set[start] = self.DijkstraNode(start, 0)
        while open_set:
            cur_distance, cur_value = heapq.heappop(open_set)

            cur_node = closed_set.get(cur_value)
            if cur_node.distance < cur_distance:
                continue

            for (adj_value, adj_distance) in self.find_adjacent_nodes(cur_value):
                adj_node = closed_set.get(adj_value)
                new_distance = cur_distance + adj_distance

                if not adj_node:
                    closed_set[adj_value] = self.DijkstraNode(adj_value, new_distance, cur_node)
                    heapq.heappush(open_set, (new_distance, adj_value))
                elif new_distance < adj_node.distance:
                    adj_node.set_distance(new_distance, cur_node)
                    heapq.heappush(open_set, (new_distance, adj_value))

        return closed_set
