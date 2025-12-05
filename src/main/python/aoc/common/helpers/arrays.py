from typing import List, Tuple, Iterable


def split_layers(full_output, layer_size):
    """Splits a single list into layers of the specified size"""
    for i in range(0, len(full_output), layer_size):
        yield full_output[i:i + layer_size]


def merge_ranges_d2(all_ranges: Iterable[Tuple[int, int]]):
    """Takes an iterable list of pairs"""

    all_ranges = sorted(all_ranges)
    merged = []
    for cur in sorted(all_ranges):
        if not merged:
            merged.append(cur)
        else:
            prev_merged = merged[-1]
            if prev_merged[1] < cur[0]:
                merged.append(cur)
            else:
                merged[-1] = prev_merged[0], max(prev_merged[1], cur[1])

    return merged