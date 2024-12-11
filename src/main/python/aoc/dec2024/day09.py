from aoc.common.day_solver import DaySolver


class Day09Solver(DaySolver):
    year = 2024
    day = 9

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        disk_contents = []
        is_block = True
        next_idx = 0
        for char in line:
            size = int(char)

            value = int(next_idx) if is_block else None
            disk_contents.extend([value] * size)
            if is_block:
                next_idx += 1
            is_block = not is_block

        last_index = len(disk_contents) - 1
        for i in range(last_index):
            if i >= last_index:
                break
            if disk_contents[i] is None:
                while disk_contents[last_index] is None and last_index > 0:
                    last_index -= 1
                if i >= last_index:
                    break
                disk_contents[i], disk_contents[last_index] = disk_contents[last_index], None

        checksum = 0
        for idx, file_id in enumerate(disk_contents):
            if file_id is not None:
                checksum += idx * file_id
        return checksum

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        disk_contents = []
        is_block = True
        next_idx = 0
        blocks = []
        free_blocks = []
        for char in line:
            size = int(char)

            if is_block:
                blocks.append((size, len(disk_contents)))
                disk_contents.extend([int(next_idx)] * size)
                next_idx += 1
            else:
                free_blocks.append((len(disk_contents), size))
                disk_contents.extend([None] * size)
            is_block = not is_block

        for block_id in range(next_idx - 1, 0, -1):
            size, start_idx = blocks[block_id]
            for idx, (block_start, block_size) in enumerate(free_blocks):
                if block_start > start_idx:
                    break
                if block_size >= size:
                    for i in range(size):
                        disk_contents[block_start + i], disk_contents[start_idx + i] = disk_contents[start_idx + i], disk_contents[block_start + i]
                    if block_size == size:
                        free_blocks.remove((block_start, block_size))
                    else:
                        free_blocks[idx] = (block_start + size, block_size - size)
                    break

        checksum = 0
        for idx, file_id in enumerate(disk_contents):
            if file_id is not None:
                checksum += idx * file_id
        return checksum
