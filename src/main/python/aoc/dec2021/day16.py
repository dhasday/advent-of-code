from aoc.common.day_solver import DaySolver
from aoc.common.helpers import *


class Day16Solver(DaySolver):
    year = 2021
    day = 16

    def solve_puzzles(self):
        raw_packet = hex_to_binary(self.load_only_input_line())

        packet, cur_pos = self._parse_packet(raw_packet, 0)

        part_1 = self._sum_version_numbers(packet)
        part_2 = packet.get_value()
        return part_1, part_2

    def _parse_packet(self, raw_packet, cur_pos):
        packet = Packet()
        packet.version, cur_pos = self._read_bits(raw_packet, cur_pos, 3)
        packet.type_id, cur_pos = self._read_bits(raw_packet, cur_pos, 3)

        if packet.type_id == 4:
            packet.literal, cur_pos = self._get_literal(raw_packet, cur_pos)
        else:
            packet.length_type, cur_pos = self._read_bits(raw_packet, cur_pos, 1)
            if packet.length_type == 0:
                packets_length, cur_pos = self._read_bits(raw_packet, cur_pos, 15)
                start_pos = cur_pos
                while cur_pos < start_pos + packets_length:
                    subpacket, cur_pos = self._parse_packet(raw_packet, cur_pos)
                    packet.subpackets.append(subpacket)
            else:
                num_packets, cur_pos = self._read_bits(raw_packet, cur_pos, 11)
                for _ in range(num_packets):
                    subpacket, cur_pos = self._parse_packet(raw_packet, cur_pos)
                    packet.subpackets.append(subpacket)
        return packet, cur_pos

    def _read_bits(self, raw_packet, cur_pos, num_bits):
        value = binary_to_decimal(raw_packet[cur_pos: cur_pos + num_bits])
        return value, cur_pos + num_bits

    def _get_literal(self, raw_packet, cur_pos):
        literal = ''
        while raw_packet[cur_pos] == '1':
            literal += raw_packet[cur_pos + 1:cur_pos + 5]
            cur_pos += 5
        literal += raw_packet[cur_pos + 1:cur_pos + 5]
        return binary_to_decimal(literal), cur_pos + 5

    def _sum_version_numbers(self, packet):
        total = packet.version
        total += sum(self._sum_version_numbers(s) for s in packet.subpackets)
        return total


class Packet:
    def __init__(self):
        self.version = None
        self.type_id = None
        self.literal = None
        self.length_type = None
        self.subpackets = []

    def get_value(self):
        if self.literal is not None:
            return self.literal

        values = [s.get_value() for s in self.subpackets]
        if self.type_id == 0:
            return sum(values)
        elif self.type_id == 1:
            total = values[0]
            for v in values[1:]:
                total *= v
            return total
        elif self.type_id == 2:
            return min(values)
        elif self.type_id == 3:
            return max(values)
        elif self.type_id == 5:
            return 1 if values[0] > values[1] else 0
        elif self.type_id == 6:
            return 1 if values[0] < values[1] else 0
        elif self.type_id == 7:
            return 1 if values[0] == values[1] else 0
