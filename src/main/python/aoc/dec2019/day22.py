from aoc.common.day_solver import DaySolver

INS_DEAL_NEW_STACK = 'deal into new stack'
INS_CUT = 'cut '
INS_DEAL_INCREMENT = 'deal with increment '


class Day22Solver(DaySolver):
    year = 2019
    day = 22

    def solve_puzzle_one(self):
        card_count = 10007
        num_shuffles = 1
        target_value = 2019

        increment, offset = self.get_coefficients(card_count, num_shuffles)

        for idx in range(card_count):
            result = (offset + (idx * increment)) % card_count
            if result == target_value:
                return idx
        raise Exception('404 - Answer Not Found')

    def solve_puzzle_two(self):
        card_count = 119315717514047
        num_shuffles = 101741582076661
        target_index = 2020

        increment, offset = self.get_coefficients(card_count, num_shuffles)

        return (offset + (target_index * increment)) % card_count

    def get_coefficients(self, num_cards, num_iters):
        instructions = self.load_all_input_lines()

        increment_mul = 1
        offset_diff = 0
        for ins in instructions:
            if ins == INS_DEAL_NEW_STACK:
                increment_mul = (- increment_mul) % num_cards
                offset_diff = (offset_diff + increment_mul) % num_cards
            elif ins.startswith(INS_DEAL_INCREMENT):
                val = int(ins[20:])
                increment_mul = (increment_mul * self._inverse(num_cards, val)) % num_cards
            elif ins.startswith(INS_CUT):
                val = int(ins[4:])
                offset_diff = (offset_diff + (val * increment_mul)) % num_cards
            else:
                raise Exception('Unmatched instruction: ' + ins)

        increment = pow(increment_mul, num_iters, num_cards)
        offset = offset_diff * (1 - increment) * self._inverse(num_cards, (1 - increment_mul) % num_cards)
        offset %= num_cards
        return increment, offset

    def _inverse(self, num_cards, value):
        return pow(value, num_cards - 2, num_cards)
