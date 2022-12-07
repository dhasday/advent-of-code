from aoc.common.day_solver import DaySolver

TOTAL_DISK_SIZE = 70000000
FREE_DISK_TARGET = 30000000


class Day07Solver(DaySolver):
    year = 2022
    day = 7

    def solve_puzzles(self):
        lines = self.load_all_input_lines()
        root_node = Directory('/')
        cur_node = root_node

        for cur_line in lines:
            cmd = cur_line.split(' ')
            if cur_line.startswith('$'):
                if cmd[1] == 'cd':
                    if cmd[2] == '/':
                        cur_node = root_node
                    elif cmd[2] == '..':
                        cur_node = cur_node.parent
                    else:
                        if cmd[2] not in cur_node.dirs:
                            cur_node.add_dir(cmd[2])
                        cur_node = cur_node.dirs.get(cmd[2])
            elif cur_line.startswith('dir '):
                cur_node.add_dir(cmd[1])
            else:
                cur_node.add_file(cmd[0])

        ans_one = self._sum_nodes_smaller(root_node, 100000)
        ans_two = self._get_min_usable_dir_size(
            root_node,
            FREE_DISK_TARGET - (TOTAL_DISK_SIZE - root_node.size)
        )

        return ans_one, ans_two

    def _sum_nodes_smaller(self, root_node, max_size):
        total = 0
        root_size = root_node.size
        if root_size <= max_size:
            total += root_size
        for d in root_node.dirs.values():
            total += self._sum_nodes_smaller(d, max_size)
        return total

    def _get_min_usable_dir_size(self, node, needed_space):
        min_size = node.size
        if min_size < needed_space:
            return None
        for d in node.dirs.values():
            dir_min = self._get_min_usable_dir_size(d, needed_space)
            if dir_min and dir_min < min_size:
                min_size = dir_min
        return min_size


class Directory(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.dirs = {}
        self.files_size = 0

        self._size = None

    def add_item(self, line):

        if line.startswith('dir'):
            self.add_dir(line)

    def add_dir(self, name):
        self.dirs[name] = Directory(name, parent=self)

    def add_file(self, size):
        self.files_size += int(size)

    @property
    def size(self):
        if self._size is None:
            self._size = sum(d.size for d in self.dirs.values()) + self.files_size
        return self._size

    def print(self, prefix=''):
        print(f'{prefix}{self.name} ({self.size})')
        if self.files_size:
            print(f'{prefix}  {self.files_size} Files')
        for d in self.dirs.values():
            d.print(f'{prefix}  ')
