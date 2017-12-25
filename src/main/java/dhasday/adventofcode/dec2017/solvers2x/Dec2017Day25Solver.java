package dhasday.adventofcode.dec2017.solvers2x;

import java.util.HashSet;
import java.util.Set;
import java.util.function.BiConsumer;

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

    public static void main(String[] args) {
        new Dec2017Day25Solver().printResults();
    }

    @Override
    public Integer solvePuzzleOne() {
        int numSteps = 12368930;

        Set<Integer> activeBits = new HashSet<>();

        int cursor = 0;
        State curState = State.A;
        for (int i = 0; i < numSteps; i++) {
            boolean wasZero = !activeBits.contains(cursor);

            if (wasZero) {
                curState.zeroOp.accept(activeBits, cursor);
                cursor += curState.zeroOffset;
            } else {
                curState.oneOp.accept(activeBits, cursor);
                cursor += curState.oneOffset;
            }

            curState = curState.nextState(wasZero);
        }

        return activeBits.size();
    }

    @Override
    public Integer solvePuzzleTwo() {
        return null;
    }

    private enum Op implements BiConsumer<Set<Integer>, Integer> {
        ADD() {
            @Override
            public void accept(Set<Integer> activeBits, Integer integer) {
                activeBits.add(integer);
            }
        },
        REMOVE {
            @Override
            public void accept(Set<Integer> activeBits, Integer integer) {
                activeBits.remove(integer);
            }
        };
    }

    private enum State {
        A(Op.ADD, Op.REMOVE, 1, 1) {
            // If the current value is 0: 1, + 1, -> B
            // If the current value is 1: 0, + 1, -> C
            @Override
            State nextState(boolean wasZero) {
                return wasZero ? B : C;
            }
        },
        B(Op.REMOVE, Op.REMOVE, -1, 1) {
            // If the current value is 0: 0; - 1, -> A
            // If the current value is 1: 0; + 1, -> D
            @Override
            State nextState(boolean wasZero) {
                return wasZero ? A : D;
            }
        },
        C(Op.ADD, Op.ADD, 1, 1) {
            // If the current value is 0: 1, + 1, -> D
            // If the current value is 1: 1, + 1, -> A
            @Override
            State nextState(boolean wasZero) {
                return wasZero ? D : A;
            }
        },
        D(Op.ADD, Op.REMOVE, -1, -1) {
            // If the current value is 0: 1, - 1, -> E
            // If the current value is 1: 0, - 1, -> D
            @Override
            State nextState(boolean wasZero) {
                return wasZero ? E : D;
            }
        },
        E(Op.ADD, Op.ADD, 1, -1) {
            // If the current value is 0: 1, + 1, -> F
            // If the current value is 1: 1, - 1, -> B
            @Override
            State nextState(boolean wasZero) {
                return wasZero ? F : B;
            }
        },
        F(Op.ADD, Op.ADD, 1, 1) {
            // If the current value is 0: 1, + 1, -> A
            // If the current value is 1: 1, + 1, -> E
            @Override
            State nextState(boolean wasZero) {
                return wasZero ? A : E;
            }
        };

        private final Op zeroOp;
        private final Op oneOp;
        private final int zeroOffset;
        private final int oneOffset;

        abstract State nextState(boolean wasZero);

        State(Op zeroOp, Op oneOp, int zeroOffset, int oneOffset) {
            this.zeroOp = zeroOp;
            this.oneOp = oneOp;
            this.zeroOffset = zeroOffset;
            this.oneOffset = oneOffset;
        }
    }
}