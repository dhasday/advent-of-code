import dataclasses

from aoc.common.day_solver import DaySolver


ACCEPT = 'A'
REJECT = 'R'

ALL_COMPONENTS = 'xmas'

COMPARATORS = {
    '<': lambda component, value, part: part.values.get(component) < value,
    '>': lambda component, value, part: part.values.get(component) > value,
}


@dataclasses.dataclass
class WorkflowCheck:
    if_true: str
    component: str = None
    operation: str = None
    value: int = None
    negate: bool = False

    def part_matches(self, part):
        if self.operation is None:
            return True

        return COMPARATORS.get(self.operation)(self.component, self.value, part)

    def copy_negate(self):
        return WorkflowCheck(
            component=self.component,
            operation=self.operation,
            value=self.value,
            if_true=self.if_true,
            negate=not self.negate,
        )

class Workflow:
    def __init__(self, line):
        part, workflows = line.split('{')
        self.name = part
        self.checks = []

        workflows = workflows[:-1].split(',')
        for workflow in workflows:
            parts = workflow.split(':')
            if_true = parts[-1]
            component = operation = value = None

            if len(parts) > 1:
                component = parts[0][0]
                operation = parts[0][1]
                value = int(parts[0][2:])

            self.checks.append(
                WorkflowCheck(
                    component=component,
                    operation=operation,
                    value=value,
                    if_true=if_true,
                )
            )

    def apply(self, part):
        for check in self.checks:
            if check.part_matches(part):
                return check.if_true

        raise Exception('How did we get here?')


class Part:
    def __init__(self, line):
        components = line[1:-1].split(',')
        self.values = {}

        for component in components:
            c, val = component.split('=')
            self.values[c] = int(val)

    def rating(self):
        return sum(self.values.values())


class Day19Solver(DaySolver):
    year = 2023
    day = 19

    workflows = None
    parts = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.workflows = {}
        self.parts = []
        loading_instructions = True
        for line in lines:
            if line == '':
                loading_instructions = False
                continue

            if loading_instructions:
                workflow = Workflow(line)
                self.workflows[workflow.name] = workflow
            else:
                self.parts.append(Part(line))

    def solve_puzzle_one(self):
        start_workflow = 'in'

        total = 0
        for part in self.parts:
            cur_workflow = start_workflow
            while cur_workflow not in [ACCEPT, REJECT]:
                workflow = self.workflows.get(cur_workflow)
                cur_workflow = workflow.apply(part)
            if cur_workflow == ACCEPT:
                total += part.rating()

        return total

    def solve_puzzle_two(self):
        start_workflow = 'in'
        min_value = 1
        max_value = 4000

        valid_workflows = self._flatten_workflows(self.workflows, start_workflow)

        total = 0
        for valid_workflow in valid_workflows:
            assert valid_workflow[-1].if_true == ACCEPT
            total += self._get_num_valid_combinations(valid_workflow, min_value, max_value)

        return total

    def _flatten_workflows(self, workflows, current_node):
        if current_node == REJECT:
            return []
        if current_node == ACCEPT:
            return [[WorkflowCheck(if_true=ACCEPT)]]

        flattened = []
        current_workflow = workflows[current_node]
        prev_checks = []
        for workflow_check in current_workflow.checks:
            options = self._flatten_workflows(workflows, workflow_check.if_true)
            for option in options:
                full_option = prev_checks + [workflow_check] + option
                flattened.append(full_option)
            prev_checks.append(workflow_check.copy_negate())
        return flattened

    def _get_num_valid_combinations(self, workflow, min_value, max_value):
        minimums = {c: min_value for c in ALL_COMPONENTS}
        maximums = {c: max_value for c in ALL_COMPONENTS}

        for condition in workflow:
            if condition.operation is None:
                continue

            if condition.negate:
                if condition.operation == '>':
                    maximums[condition.component] = min(maximums[condition.component], condition.value)
                else:
                    minimums[condition.component] = max(minimums[condition.component], condition.value)
            else:
                if condition.operation == '>':
                    minimums[condition.component] = max(minimums[condition.component], condition.value + 1)
                else:
                    maximums[condition.component] = min(maximums[condition.component], condition.value - 1)

        total = 1
        for component in ALL_COMPONENTS:
            total *= (maximums[component] - minimums[component] + 1)
        return total
