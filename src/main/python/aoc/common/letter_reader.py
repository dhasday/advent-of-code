from aoc.common.helpers import split_layers

LETTER_MAPS = {
    # TODO: D I M N O Q S T V W X
    #     2    3    4    5    6
    ' 00  0  0 0  0 0000 0  0 0  0 ': 'A',
    '000  0  0 000  0  0 0  0 000  ': 'B',
    ' 00  0  0 0    0    0  0  00  ': 'C',
    '0000 0    000  0    0    0000 ': 'E',
    '0000 0    000  0    0    0    ': 'F',
    ' 00  0  0 0    0 00 0  0  000 ': 'G',
    '0  0 0  0 0000 0  0 0  0 0  0 ': 'H',
    '  00    0    0    0 0  0  00  ': 'J',
    '0  0 0 0  00   0 0  0 0  0  0 ': 'K',
    '0    0    0    0    0    0000 ': 'L',
    '000  0  0 0  0 000  0    0    ': 'P',
    '000  0  0 0  0 000  0 0  0  0 ': 'R',
    '0  0 0  0 0  0 0  0 0  0  00  ': 'U',
    '0   00   0 0 0   0    0    0  ': 'Y',
    '0000    0   0   0   0    0000 ': 'Z',
}


def read_output_from_points(points, size_x, size_y):
    lines = []
    for y in range(size_y):
        line = ''
        for x in range(size_x):
            line += '0' if (x, y) in points else ' '
        lines.append(line)

    return read_output(lines)


def read_output(lines):
    chars = []
    for line in lines:
        if not chars:
            for segment in split_layers(line, 5):
                chars.append(segment)
        else:
            for idx, segment in enumerate(split_layers(line, 5)):
                chars[idx] += segment.ljust(5, ' ')

    output = ''
    for char in chars:
        letter = LETTER_MAPS.get(char)
        output += letter if letter else '?'
    return output
