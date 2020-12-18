from aoc.common.day_solver import DaySolver


class Day18Solver(DaySolver):
    year = 2020
    day = 18

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        priority_on_stack = {"+": 3, "*": 3, "(": 1, ")": 6, "#": 0}
        priority_next_token = {"+": 2, "*": 2, "(": 6, ")": 1, "#": 0}

        total = 0
        for line in lines:
            total += self._evalulate(line, priority_on_stack, priority_next_token)
        return total

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        priority_on_stack = {"+": 5, "*": 3, "(": 1, ")": 6, "#": 0}
        priority_next_token = {"+": 4, "*": 2, "(": 6, ")": 1, "#": 0}
        total = 0

        for line in lines:
            total += self._evalulate(line, priority_on_stack, priority_next_token)
        return total

    def _evalulate(self, expr, on_stack_priority, next_token_priority):
        # Convert to postfix first using the operator priorities specified
        postfix_expr = []
        token_stack = ["#"]
        i = 0
        while i < len(expr):
            if expr[i] == ' ':
                i += 1
            elif expr[i].isdigit():
                postfix_expr.append(int(expr[i]))
                i += 1
            else:
                p1 = on_stack_priority[token_stack[-1]]
                p2 = next_token_priority[expr[i]]

                if p1 < p2:
                    token_stack.append(expr[i])
                    i += 1
                elif p1 > p2:
                    postfix_expr.append(token_stack.pop())
                else:
                    token_stack.pop()
                    i += 1
        while token_stack[-1] != "#":
            postfix_expr += token_stack.pop()

        # Then evaluate
        eval_stack = []
        for token in postfix_expr:
            if isinstance(token, int):
                eval_stack.append(token)
            else:
                op_2 = eval_stack.pop()
                op_1 = eval_stack.pop()

                if token == '+':
                    eval_stack.append(op_1 + op_2)
                elif token == '*':
                    eval_stack.append(op_1 * op_2)

        return eval_stack[0]

