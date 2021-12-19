from collections import defaultdict

from aoc.common.day_solver import DaySolver

POINT_ROTATIONS = [
    lambda p: (p[0], p[1], p[2]),
    lambda p: (-p[0], -p[1], p[2]),
    lambda p: (-p[0], p[1], -p[2]),
    lambda p: (p[0], -p[1], -p[2]),
    lambda p: (p[1], p[2], p[0]),
    lambda p: (-p[1], -p[2], p[0]),
    lambda p: (-p[1], p[2], -p[0]),
    lambda p: (p[1], -p[2], -p[0]),
    lambda p: (p[2], p[0], p[1]),
    lambda p: (-p[2], -p[0], p[1]),
    lambda p: (-p[2], p[0], -p[1]),
    lambda p: (p[2], -p[0], -p[1]),
    lambda p: (-p[0], p[2], p[1]),
    lambda p: (p[0], -p[2], p[1]),
    lambda p: (p[0], p[2], -p[1]),
    lambda p: (-p[0], -p[2], -p[1]),
    lambda p: (-p[1], p[0], p[2]),
    lambda p: (p[1], -p[0], p[2]),
    lambda p: (p[1], p[0], -p[2]),
    lambda p: (-p[1], -p[0], -p[2]),
    lambda p: (-p[2], p[1], p[0]),
    lambda p: (p[2], -p[1], p[0]),
    lambda p: (p[2], p[1], -p[0]),
    lambda p: (-p[2], -p[1], -p[0]),
]


class Day19Solver(DaySolver):
    year = 2021
    day = 19

    rotation_memo = {}

    def solve_puzzles(self):
        scanners = self._load_all_scanners()

        all_beacons, oriented_scanners = self._locate_scanners(scanners)

        part_1 = len(all_beacons)
        part_2 = self._max_scanner_distance(list(oriented_scanners.values()))

        return part_1, part_2

    def _load_all_scanners(self, filename=None):
        lines = self.load_all_input_lines(filename)

        scanners = []
        cur_scanner = None
        for line in lines:
            if line.startswith('---'):
                cur_scanner = []
                scanners.append(cur_scanner)
            elif line == '':
                continue
            else:
                point = list(int(d) for d in line.split(','))
                cur_scanner.append(point)
        return scanners

    def _locate_scanners(self, scanners):
        all_beacons = set(tuple(p) for p in scanners[0])
        oriented_scanners = {0: (0, 0, 0)}
        to_orient = set(range(1, len(scanners)))

        while to_orient:
            found = []
            for idx in to_orient:
                scanner_pos, oriented_beacons = self._detect_scanner_overlap(all_beacons, idx, scanners[idx])
                if scanner_pos is not None:
                    for beacon in oriented_beacons:
                        all_beacons.add(tuple(beacon))
                    oriented_scanners[idx] = scanner_pos
                    found.append(idx)

            if not found:
                raise Exception('Infinite loop detected - Some scanners do not overlap: {}'.format(to_orient))
            to_orient.difference_update(found)

        return all_beacons, oriented_scanners

    def _max_scanner_distance(self, scanner_locations):
        num_scanners = len(scanner_locations)

        distances = set()
        for idx_1 in range(num_scanners):
            for idx_2 in range(idx_1 + 1, num_scanners):
                distance = self._node_distance(scanner_locations[idx_1], scanner_locations[idx_2])
                distances.add(abs(distance[0]) + abs(distance[1]) + abs(distance[2]))

        return max(distances)

    def _detect_scanner_overlap(self, all_beacons, idx, scanner):
        for rot_num, do_rotate in enumerate(POINT_ROTATIONS):
            key = idx, rot_num
            if key not in self.rotation_memo:
                self.rotation_memo[key] = list(do_rotate(p) for p in scanner)
            rotated = self.rotation_memo[key]

            # Get counts of deltas between beacons
            distance_counts = defaultdict(int)
            for test_beacon in rotated:
                for beacon in all_beacons:
                    distance_counts[self._node_distance(beacon, test_beacon)] += 1

            # If enough beacons are accessible, then we've located this scanner
            for delta, count in distance_counts.items():
                if count >= 12:
                    pos = delta
                    oriented_beacons = [self._apply_offset(b, delta) for b in rotated]
                    return pos, oriented_beacons

        return None, []

    def _node_distance(self, node_1, node_2):
        return node_1[0] - node_2[0], node_1[1] - node_2[1], node_1[2] - node_2[2]

    def _apply_offset(self, node, delta):
        return node[0] + delta[0], node[1] + delta[1], node[2] + delta[2]
