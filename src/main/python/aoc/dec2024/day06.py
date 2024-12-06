from aoc.common.day_solver import DaySolver


DIR_OFFSETS = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0),
}
NEXT_DIRS = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^',
}

class Day06Solver(DaySolver):
    year = 2024
    day = 6

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        obstacles = set()
        original_pos = None
        original_dir = None

        size_x = len(lines[0])
        size_y = len(lines)

        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                if val == '#':
                    obstacles.add((x, y))
                elif val in '^v><':
                    original_pos = (x, y)
                    original_dir = val

        visited_no_change = set()
        current_pos = original_pos
        current_dir = original_dir
        while 0 <= current_pos[0] < size_x and 0 <= current_pos[1] < size_y:
            visited_no_change.add(current_pos)

            offset = DIR_OFFSETS[current_dir]
            next_pos = current_pos[0] + offset[0], current_pos[1] + offset[1]
            if next_pos not in obstacles:
                current_pos = next_pos
            else:
                current_dir = NEXT_DIRS[current_dir]

        total_variations = 0
        for new_obstacle in visited_no_change:
            if new_obstacle == original_pos:
                continue
            current_pos = original_pos
            current_dir = original_dir
            visited = set()
            obstacles.add(new_obstacle)
            while 0 <= current_pos[0] < size_x and 0 <= current_pos[1] < size_y:
                hashed = current_pos[0], current_pos[1], current_dir
                if hashed in visited:
                    total_variations += 1
                    break
                visited.add(hashed)

                offset = DIR_OFFSETS[current_dir]
                next_pos = current_pos[0] + offset[0], current_pos[1] + offset[1]
                if next_pos not in obstacles:
                    current_pos = next_pos
                else:
                    current_dir = NEXT_DIRS[current_dir]
            obstacles.remove(new_obstacle)

        return len(visited_no_change), total_variations
