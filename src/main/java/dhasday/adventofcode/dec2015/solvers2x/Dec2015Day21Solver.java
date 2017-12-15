package dhasday.adventofcode.dec2015.solvers2x;

import java.util.HashSet;
import java.util.Set;

import com.google.common.collect.Sets;
import dhasday.adventofcode.dec2015.Dec2015DaySolver;

public class Dec2015Day21Solver extends Dec2015DaySolver<Integer> {

    private static final int STARTING_HEALTH_PLAYER = 100;

    private static final Set<Item> WEAPONS = Sets.newHashSet(
            new Item(ItemType.WEAPON, 8, 4, 0),
            new Item(ItemType.WEAPON, 10, 5, 0),
            new Item(ItemType.WEAPON, 25, 6, 0),
            new Item(ItemType.WEAPON, 40, 7, 0),
            new Item(ItemType.WEAPON, 74, 8, 0)
    );
    private static final Set<Item> ARMORS = Sets.newHashSet(
            new Item(ItemType.ARMOR, 13, 0, 1),
            new Item(ItemType.ARMOR, 31, 0, 2),
            new Item(ItemType.ARMOR, 53, 0, 3),
            new Item(ItemType.ARMOR, 75, 0, 4),
            new Item(ItemType.ARMOR, 102, 0, 5)
    );
    private static final Set<Item> RINGS = Sets.newHashSet(
            new Item(ItemType.RING, 25, 1, 0),
            new Item(ItemType.RING, 50, 2, 0),
            new Item(ItemType.RING, 100, 3, 0),
            new Item(ItemType.RING, 20, 0, 1),
            new Item(ItemType.RING, 40, 0, 2),
            new Item(ItemType.RING, 80, 0, 3)
    );

    @Override
    public int getDay() {
        return 21;
    }

    @Override
    public Integer solvePuzzleOne() {
        Character character = new Character(STARTING_HEALTH_PLAYER, 0, 0);
        Character boss = new Character(103, 9, 2);

        return findMinCostToWinFight(character, boss);
    }

    @Override
    public Integer solvePuzzleTwo() {
        Character character = new Character(STARTING_HEALTH_PLAYER, 0, 0);
        Character boss = new Character(103, 9, 2);

        return findMaxCostToLoseFight(character, boss);
    }

    private Integer findMinCostToWinFight(Character character, Character boss) {
        Integer minCost = null;

        Set<Set<Item>> armorOptions = calculateArmorOptions();

        for (Item weapon : WEAPONS) {
            for (Set<Item> armor : armorOptions) {
                Character currentBoss = new Character(boss);
                Character currentCharacter = new Character(character);

                currentCharacter.items = Sets.newHashSet(armor);
                currentCharacter.items.add(weapon); // Weapon is required

                if (doesPlayerWinFight(currentCharacter, currentBoss)) {
                    int itemCost = currentCharacter.calculateItemCost();

                    if (minCost == null) {
                        minCost = itemCost;
                    } else {
                        minCost = Math.min(itemCost, minCost);
                    }
                }
            }
        }

        return minCost;
    }

    private Integer findMaxCostToLoseFight(Character character, Character boss) {
        Integer maxCost = null;

        Set<Set<Item>> armorOptions = calculateArmorOptions();

        for (Item weapon : WEAPONS) {
            for (Set<Item> armor : armorOptions) {
                Character currentBoss = new Character(boss);
                Character currentCharacter = new Character(character);

                currentCharacter.items = Sets.newHashSet(armor);
                currentCharacter.items.add(weapon); // Weapon is required

                if (!doesPlayerWinFight(currentCharacter, currentBoss)) {
                    int itemCost = currentCharacter.calculateItemCost();

                    if (maxCost == null) {
                        maxCost = itemCost;
                    } else {
                        maxCost = Math.max(itemCost, maxCost);
                    }
                }
            }
        }

        return maxCost;
    }

    private Set<Set<Item>> calculateArmorOptions() {
        Set<Set<Item>> armorOptions = new HashSet<>();

        armorOptions.add(new HashSet<>()); // No Armor

        for (Item armor : ARMORS) {
            // Armor No Rings
            Set<Item> armorOnly = Sets.newHashSet(armor);
            armorOptions.add(armorOnly);

            for (Item ringOne : RINGS) {
                // Armor One Ring
                Set<Item> oneRing = Sets.newHashSet(armor, ringOne);
                armorOptions.add(oneRing);

                for (Item ringTwo : RINGS) {
                    // Armor Two Rings
                    Set<Item> twoRings = Sets.newHashSet(armor, ringOne, ringTwo);
                    armorOptions.add(twoRings);
                }
            }
        }

        for (Item ringOne : RINGS) {
            // No Armor One Ring
            Set<Item> oneRing = Sets.newHashSet(ringOne);
            armorOptions.add(oneRing);

            for (Item ringTwo : RINGS) {
                // No Armor Two Rings
                Set<Item> twoRings = Sets.newHashSet(ringOne, ringTwo);
                armorOptions.add(twoRings);
            }
        }

        return armorOptions;
    }

    private boolean doesPlayerWinFight(Character player, Character boss) {
        boolean playerTurn = true;

        while(true) {
            if (playerTurn) {
                handleAttack(player, boss);
                if (boss.currentHealth <= 0) {
                    return true;
                }
            } else {
                handleAttack(boss, player);
                if (player.currentHealth <= 0) {
                    return false;
                }
            }

            playerTurn = ! playerTurn;
        }
    }

    private void handleAttack(Character attacker, Character defender) {
        int damage = Math.max(attacker.calculateDamage() - defender.calculateArmor(), 1);
        defender.currentHealth -= damage;
    }

    private class Character {
        private int currentHealth;
        private int damage;
        private int armor;
        private Set<Item> items;

        Character(int currentHealth, int damage, int armor) {
            this.currentHealth = currentHealth;
            this.damage = damage;
            this.armor = armor;
            this.items = new HashSet<>();
        }

        Character(Character other) {
            this.currentHealth = other.currentHealth;
            this.damage = other.damage;
            this.armor = other.armor;
            this.items = Sets.newHashSet(other.items);
        }

        private Integer calculateDamage() {
            int itemDamage = items.stream()
                    .mapToInt(item -> item.damage)
                    .sum();

            return itemDamage + damage;
        }

        private Integer calculateArmor() {
            int itemDamage = items.stream()
                    .mapToInt(item -> item.armor)
                    .sum();

            return itemDamage + armor;
        }

        private Integer calculateItemCost() {
            return items.stream()
                    .mapToInt(item -> item.cost)
                    .sum();
        }
    }

    private static class Item {
        private final ItemType type;
        private final int cost;
        private final int damage;
        private final int armor;

        Item(ItemType type, int cost, int damage, int armor) {
            this.type = type;
            this.cost = cost;
            this.damage = damage;
            this.armor = armor;
        }
    }

    private enum ItemType {
        WEAPON,
        ARMOR,
        RING
    }
}
