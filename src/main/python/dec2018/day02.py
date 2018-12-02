from day_solver import DaySolver


class Day02Solver(DaySolver):
    year = 2018
    day = 2

    def solve_puzzle_one(self):
        package_ids = self._load_all_input_lines()

        num_doubles = 0
        num_triples = 0

        for package_id in package_ids:
            letter_counts = self._count_letters(package_id)

            has_double = False
            has_triple = False
            for letter in letter_counts:
                count = letter_counts[letter]
                if count == 2:
                    has_double = True
                elif count == 3:
                    has_triple = True

            num_doubles += 1 if has_double else 0
            num_triples += 1 if has_triple else 0

        return num_doubles * num_triples

    def solve_puzzle_two(self):
        package_ids = self._load_all_input_lines()

        valid_packages = self._get_valid_packages(package_ids)

        for p1 in valid_packages:
            for p2 in valid_packages:
                if p1 == p2 or len(p1) != len(p2):
                    continue
                if self._are_similar(p1, p2):
                    return self._calculate_answer(p1, p2)

        raise Exception('No match found')

    def _count_letters(self, package_id):
        letter_counts = dict()
        for letter in package_id:
            if letter not in letter_counts:
                letter_counts[letter] = 0

            letter_counts[letter] = letter_counts[letter] + 1

        return letter_counts

    def _get_valid_packages(self, package_ids):
        valid_packages = []
        for package_id in package_ids:
            letter_counts = self._count_letters(package_id)
            for letter in letter_counts:
                count = letter_counts[letter]
                if count == 2 or count == 3:
                    valid_packages.append(package_id)
                    break
        return valid_packages

    def _are_similar(self, package_one, package_two):
        found_different = False
        for i in range(0, len(package_one)):
            if package_one[i] != package_two[i]:
                if found_different:
                    return False
                found_different = True
        return found_different

    def _calculate_answer(self, package_one, package_two):
        answer = ''

        for i in range(0, len(package_one)):
            if package_one[i] == package_two[i]:
                answer += package_one[i]

        return answer
