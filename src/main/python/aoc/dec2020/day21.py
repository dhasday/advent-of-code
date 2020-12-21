import re

from aoc.common.day_solver import DaySolver


INPUT_REGEX = re.compile(r'([a-z ]+) \(contains ([a-z, ]+)\)')


class Day21Solver(DaySolver):
    year = 2020
    day = 21

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        products = []
        for line in lines:
            result = INPUT_REGEX.match(line)
            if not result:
                raise Exception('error loading')
            ingredients = result.group(1).split(' ')
            allergens = result.group(2).split(', ')

            products.append((ingredients, allergens))

        allergens = self._determine_allergens(products)

        allergen_ingredients = set(allergens.values())
        ans_one = 0
        for product in products:
            for i in product[0]:
                if i not in allergen_ingredients:
                    ans_one += 1

        sorted_ingredients = []
        for _, ingredient in sorted(allergens.items(), key=lambda al: al[0]):
            sorted_ingredients.append(ingredient)
        ans_two = ','.join(sorted_ingredients)

        return ans_one, ans_two

    def _determine_allergens(self, products):
        allergens = {}
        for product in products:
            for allergen in product[1]:
                if allergen not in allergens:
                    allergens[allergen] = set(product[0])
                else:
                    allergens[allergen].intersection_update(set(product[0]))

        remaining_keys = sorted(allergens.items(), key=lambda p: len(p[1]))
        remaining_keys = {k for k, v in remaining_keys}
        return self._find_valid_configuration(
            allergens,
            remaining_keys,
            {},
        )

    def _find_valid_configuration(self, allergens, remaining_keys, assignments):
        if len(remaining_keys) == 0:
            return assignments

        for key in remaining_keys:
            possibilities = allergens[key]
            possibilities = [p for p in possibilities if p not in assignments.values()]
            if len(possibilities) == 1:
                new_assignments = assignments.copy()
                new_remaining = remaining_keys.copy()

                new_assignments[key] = possibilities[0]
                new_remaining.discard(key)
                return self._find_valid_configuration(allergens, new_remaining, new_assignments)

        return None
