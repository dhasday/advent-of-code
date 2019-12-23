from aoc.common.day_solver import DaySolver


class Day24Solver(DaySolver):
    year = 2018
    day = 24

    class Unit(object):
        def __init__(self, side, num_units, hit_points, attack_type, attack_damage, initiative, weak, immune):
            self.side = side
            self.num_units = num_units
            self.hit_points = hit_points
            self.attack_type = attack_type
            self.attack_damage = attack_damage
            self.initiative = initiative
            self.weak = weak
            self.immune = immune

        @property
        def effective_power(self):
            return self.num_units * self.attack_damage

        @property
        def sort_order(self):
            return self.effective_power, self.initiative

        def get_enemy_damage(self, enemy):
            if enemy.side == self.side:
                return 0
            if self.attack_type in enemy.immune:
                return 0

            damage = self.effective_power
            if self.attack_type in enemy.weak:
                damage *= 2
            return damage

        def deal_damage(self, target):
            damage = self.get_enemy_damage(target)
            lost_units = damage // target.hit_points
            target.num_units -= lost_units

    def solve_puzzles(self):
        immune_units, infection_units = self._load_input()
        immune_units, infection_units = self._run_simulation(immune_units, infection_units)
        ans_one = self._count_units(immune_units, infection_units)

        immune_boost = 0
        while True:
            immune_boost += 1
            immune_units, infection_units = self._load_input(immune_boost)
            immune_units, infection_units = self._run_simulation(immune_units, infection_units)

            if immune_units and not infection_units:
                break

        ans_two = self._count_units(immune_units, infection_units)

        return ans_one, ans_two

    def _load_input(self, immune_boost=0):
        immune_units = []
        infection_units = []

        for l in self.load_all_input_lines(filename='24-parsed'):
            unit_config = l.split(';')

            unit = self.Unit(
                side=unit_config[0],
                num_units=int(unit_config[1]),
                hit_points=int(unit_config[2]),
                weak=unit_config[3].split(',') if unit_config[3] else [],
                immune=unit_config[4].split(',') if unit_config[4] else [],
                attack_damage=int(unit_config[5]),
                attack_type=unit_config[6],
                initiative=int(unit_config[7]),
            )

            if unit.side == 'Immune':
                immune_units.append(unit)
                unit.attack_damage += immune_boost
            elif unit.side == 'Infection':
                infection_units.append(unit)

        return immune_units, infection_units

    def _run_simulation(self, immune_units, infection_units):
        prev_count = self._count_units(immune_units, infection_units)
        while immune_units and infection_units:
            immune_units = self._sort_units_for_attack(immune_units)
            infection_units = self._sort_units_for_attack(infection_units)

            # Target to attacker
            targets = self._target_units(immune_units, infection_units)
            targets.update(self._target_units(infection_units, immune_units))

            # Deal Damage
            for target in sorted(targets, key=lambda u: targets[u][0].initiative, reverse=True):
                unit, damage = targets[target]
                if unit.num_units > 0:
                    unit.deal_damage(target)

            # Clean-up dead units
            immune_units = [u for u in immune_units if u.num_units > 0]
            infection_units = [u for u in infection_units if u.num_units > 0]

            # If we didn't lose any units, end the battle
            next_count = self._count_units(immune_units, infection_units)
            if prev_count == next_count:
                break
            prev_count = next_count

        return immune_units, infection_units

    def _target_units(self, attackers, enemies):
        targeted_enemies = {}

        for attacker in attackers:
            target = None
            for enemy in enemies:
                # Only target each enemy at most once
                if enemy in targeted_enemies:
                    continue

                damage = attacker.get_enemy_damage(enemy)
                if damage:
                    new_target = (damage, enemy.effective_power, enemy.initiative, enemy)
                    if target is None or self._compare(target, new_target) < 0:
                        target = new_target
            if target:
                targeted_enemies[target[3]] = (attacker, target[0])

        return targeted_enemies

    def _sort_units_for_attack(self, units):
        return sorted(units, key=lambda u: u.sort_order, reverse=True)

    def _count_units(self, immune_units, infection_units):
        return sum([u.num_units for u in immune_units]) + sum([u.num_units for u in infection_units])

    def _compare(self, first, second):
        return (first > second) - (first < second)
