package dhasday.adventofcode.dec2015.solvers2x;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import com.google.common.collect.Sets;
import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day22Solver extends DaySolver<Integer> {

    @Override
    public int getDayNumber() {
        return 22;
    }

    @Override
    public Integer solvePuzzleOne() {
        Character player = new Character(50, 0, 0, 500);
        Character boss = new Character(51, 9, 0, 0);

        return findMinManaToWin(player, boss, 0, true, false, 20);
    }

    @Override
    public Integer solvePuzzleTwo() {
        Character player = new Character(50, 0, 0, 500);
        Character boss = new Character(51, 9, 0, 0);

        return findMinManaToWin(player, boss, 0, true, true, 20);
    }

    private Integer findMinManaToWin(Character player,
                                     Character boss,
                                     Integer spentMana,
                                     boolean playerTurn,
                                     boolean hardMode,
                                     Integer maxTurnsRemaining) {
        if (boss.remainingHealth <= 0) {
            return spentMana;   // We won, what was the cost
        } else if (player.remainingHealth <= 0) {
            return null;        // We lost, so cost doesn't matter
        } else if (maxTurnsRemaining <= 0) {
            return null;
        }

        Character curPlayer = new Character(player);
        Character curBoss = new Character(boss);

        if (hardMode && playerTurn) {
            curPlayer.remainingHealth -= 1;

            if (curPlayer.remainingHealth <= 0) {
                return null;
            }
        }

        curPlayer.processEffects();
        if (curPlayer.remainingHealth <= 0) {
            return null;
        }
        curBoss.processEffects();
        if (curBoss.remainingHealth <= 0) {
            return spentMana;
        }

        if (!playerTurn) {
            curPlayer.remainingHealth -= Math.max(curBoss.damage - curPlayer.armor, 1);
            return findMinManaToWin(curPlayer, curBoss, spentMana, true, hardMode, maxTurnsRemaining - 1);
        }

        Integer minMana = null;

        List<Spell> availableSpells = determineAvailableSpells(curPlayer, curBoss);
        for (Spell spell : availableSpells) {
            int curMana = spentMana + spell.manaCost;
            Character currentPlayer = new Character(curPlayer);
            Character currentBoss = new Character(curBoss);

            spell.apply(currentPlayer, currentBoss);

            Integer possibleMin = findMinManaToWin(currentPlayer, currentBoss, curMana, false, hardMode, maxTurnsRemaining - 1);

            if (possibleMin != null) {
                minMana = minMana == null ? possibleMin : Math.min(minMana, possibleMin);
            }
        }

        return minMana;
    }

    private List<Spell> determineAvailableSpells(Character player, Character boss) {
        return Arrays.stream(Spell.values())
                .filter(spell -> player.mana >= spell.manaCost)
                .filter(spell -> player.effects.get(spell) == null)
                .filter(spell -> boss.effects.get(spell) == null)
                .collect(Collectors.toList());
    }

    private class Character {
        private int remainingHealth;
        private int damage;
        private int armor;
        private int mana;

        private Map<Spell, Effect> effects;

        public Character(int remainingHealth, int damage, int armor, int mana) {
            this.remainingHealth = remainingHealth;
            this.damage = damage;
            this.armor = armor;
            this.mana = mana;
            this.effects = new HashMap<>();
        }

        Character(Character other) {
            this.remainingHealth = other.remainingHealth;
            this.damage = other.damage;
            this.armor = other.armor;
            this.mana = other.mana;

            this.effects = new HashMap<>();
            other.effects.forEach((spell, effect) -> this.effects.put(spell, new Effect(effect)));
        }

        void processEffects() {
            Set<Spell> spells = Sets.newHashSet(effects.keySet());

            for (Spell spell : spells) {
                Effect effect = effects.get(spell);
                effect.remainingTurns--;

                remainingHealth += effect.healthChange;
                mana += effect.mana;

                if (effect.remainingTurns <= 0) {
                    if (spell == Spell.SHIELD) {
                        armor = 0;
                    }

                    effects.remove(spell);
                }
            }
        }
    }

    private static class Effect {
        private int remainingTurns;
        private int healthChange;
        private int armor;
        private int mana;

        Effect(int remainingTurns, int healthChange, int armor, int mana) {
            this.remainingTurns = remainingTurns;
            this.healthChange = healthChange;
            this.armor = armor;
            this.mana = mana;
        }

        Effect(Effect other) {
            this.remainingTurns = other.remainingTurns;
            this.healthChange = other.healthChange;
            this.armor = other.armor;
            this.mana = other.mana;
        }
    }

    private enum Spell {
        MAGIC_MISSILE(53) {
            @Override
            void apply(Character caster, Character target) {
                super.apply(caster, target);

                target.remainingHealth -= 4;
            }
        },
        DRAIN(73) {
            @Override
            void apply(Character caster, Character target) {
                super.apply(caster, target);

                caster.remainingHealth += 2;
                target.remainingHealth -= 2;
            }
        },
        SHIELD(113) {
            @Override
            void apply(Character caster, Character target) {
                super.apply(caster, target);

                caster.armor = 7;
                Effect shield = new Effect(6, 0, 7, 0);
                caster.effects.put(this, shield);
            }
        },
        POISON(173) {
            @Override
            void apply(Character caster, Character target) {
                super.apply(caster, target);

                Effect poison = new Effect(6, -3, 0, 0);
                target.effects.put(this, poison);
            }
        },
        RECHARGE(229) {
            @Override
            void apply(Character caster, Character target) {
                super.apply(caster, target);

                Effect recharge = new Effect(5, 0, 0, 101);
                caster.effects.put(this, recharge);
            }
        };

        int manaCost;

        void apply(Character caster, Character target) {
            caster.mana -= manaCost;
        }

        Spell(int manaCost) {
            this.manaCost = manaCost;
        }
    }
}
