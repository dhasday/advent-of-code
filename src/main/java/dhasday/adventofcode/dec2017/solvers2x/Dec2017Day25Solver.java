package dhasday.adventofcode.dec2017.solvers2x;

import java.util.HashSet;
import java.util.Set;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

/**
 *  Begin in state A.
 *   Perform a diagnostic checksum after 12368930 steps.

 *   In state A:
 *       If the current value is 0:
 *           - Write the value 1.
 *           - Move one slot to the right.
 *           - Continue with state B.
 *       If the current value is 1:
 *           - Write the value 0.
 *           - Move one slot to the right.
 *           - Continue with state C.
 *   In state B:
 *       If the current value is 0:
 *           - Write the value 0.
 *           - Move one slot to the left.
 *           - Continue with state A.
 *       If the current value is 1:
 *           - Write the value 0.
 *           - Move one slot to the right.
 *           - Continue with state D.
 *   In state C:
 *       If the current value is 0:
 *           - Write the value 1.
 *           - Move one slot to the right.
 *           - Continue with state D.
 *       If the current value is 1:
 *           - Write the value 1.
 *           - Move one slot to the right.
 *           - Continue with state A.
 *   In state D:
 *       If the current value is 0:
 *           - Write the value 1.
 *           - Move one slot to the left.
 *           - Continue with state E.
 *       If the current value is 1:
 *           - Write the value 0.
 *           - Move one slot to the left.
 *           - Continue with state D.
 *   In state E:
 *       If the current value is 0:
 *           - Write the value 1.
 *           - Move one slot to the right.
 *           - Continue with state F.
 *       If the current value is 1:
 *           - Write the value 1.
 *           - Move one slot to the left.
 *           - Continue with state B.
 *   In state F:
 *       If the current value is 0:
 *           - Write the value 1.
 *           - Move one slot to the right.
 *           - Continue with state A.
 *       If the current value is 1:
 *           - Write the value 1.
 *           - Move one slot to the right.
 *           - Continue with state E.
 */
public class Dec2017Day25Solver extends Dec2017DaySolver<Integer> {

    @Override
    public int getDay() {
        return 25;
    }

    @Override
    public Integer solvePuzzleOne() {
        int numSteps = 12368930;

        Set<Integer> activeBits = new HashSet<>();

        int cursor = 0;
        State curState = State.A;
        for (int i = 0; i < numSteps; i++) {
            boolean wasZero = !activeBits.contains(cursor);

            curState.processState(activeBits, cursor, wasZero);
            cursor = curState.nextCursor(cursor, wasZero);
            curState = curState.nextState(wasZero);
        }

        return activeBits.size();
    }

    @Override
    public Integer solvePuzzleTwo() {
        return null;
    }

    private enum State {
        A {
            // If the current value is 0: 1; + 1, -> B
            // If the current value is 1: 0; + 1, -> C
            @Override
            void processState(Set<Integer> activeBits, Integer cursor, boolean wasZero) {
                if (wasZero) {
                    activeBits.add(cursor);
                } else {
                    activeBits.remove(cursor);
                }
            }

            @Override
            int nextCursor(Integer cursor, boolean wasZero) {
                return cursor + 1;
            }

            @Override
            State nextState(boolean wasZero) {
                return wasZero ? B : C;
            }
        },
        B {
            // If the current value is 0: 0; - 1, -> A
            // If the current value is 1: 0; + 1, -> D
            @Override
            void processState(Set<Integer> activeBits, Integer cursor, boolean wasZero) {
                activeBits.remove(cursor);
            }

            @Override
            int nextCursor(Integer cursor, boolean wasZero) {
                return wasZero ? cursor - 1 : cursor + 1;
            }

            @Override
            State nextState(boolean wasZero) {
                return wasZero ? A : D;
            }
        },
        C {
            // If the current value is 0: 1, + 1, -> D
            // If the current value is 1: 1, + 1, -> A
            @Override
            void processState(Set<Integer> activeBits, Integer cursor, boolean wasZero) {
                activeBits.add(cursor);
            }

            @Override
            int nextCursor(Integer cursor, boolean wasZero) {
                return cursor + 1;
            }

            @Override
            State nextState(boolean wasZero) {
                return wasZero ? D : A;
            }
        },
        D {
            // If the current value is 0: 1, - 1, -> E
            // If the current value is 1: 0, - 1, -> D
            @Override
            void processState(Set<Integer> activeBits, Integer cursor, boolean wasZero) {
                if (wasZero) {
                    activeBits.add(cursor);
                } else {
                    activeBits.remove(cursor);
                }
            }

            @Override
            int nextCursor(Integer cursor, boolean wasZero) {
                return cursor - 1;
            }

            @Override
            State nextState(boolean wasZero) {
                return wasZero ? E : D;
            }
        },
        E {
            // If the current value is 0: 1, + 1, -> F
            // If the current value is 1: 1, - 1, -> B
            @Override
            void processState(Set<Integer> activeBits, Integer cursor, boolean wasZero) {
                activeBits.add(cursor);
            }

            @Override
            int nextCursor(Integer cursor, boolean wasZero) {
                return wasZero ? cursor + 1 : cursor - 1;
            }

            @Override
            State nextState(boolean wasZero) {
                return wasZero ? F : B;
            }
        },
        F {
            // If the current value is 0: 1, + 1, -> A
            // If the current value is 1: 1, + 1, -> E
            @Override
            void processState(Set<Integer> activeBits, Integer cursor, boolean wasZero) {
                activeBits.add(cursor);
            }

            @Override
            int nextCursor(Integer cursor, boolean wasZero) {
                return cursor + 1;
            }

            @Override
            State nextState(boolean wasZero) {
                return wasZero ? A : E;
            }
        };

        abstract void processState(Set<Integer> activeBits, Integer cursor, boolean wasZero);
        abstract int nextCursor(Integer cursor, boolean wasZero);
        abstract State nextState(boolean wasZero);
    }
}