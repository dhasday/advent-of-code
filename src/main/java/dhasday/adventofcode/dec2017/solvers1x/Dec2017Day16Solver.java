package dhasday.adventofcode.dec2017.solvers1x;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;
import org.apache.commons.lang3.StringUtils;

public class Dec2017Day16Solver extends Dec2017DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/16-input";

    private static final String INITIAL_STATE = "abcdefghijklmnop";

    @Override
    public int getDay() {
        return 16;
    }

    @Override
    public String solvePuzzleOne() {
        List<Instruction> allInstructions = loadAllInstructions();

        return processAllInstructions(allInstructions, INITIAL_STATE);
    }

    @Override
    public String solvePuzzleTwo() {
        List<Instruction> allInstructions = loadAllInstructions();

        List<String> danceLoop = findLoopSequence(allInstructions, INITIAL_STATE);

        return danceLoop.get(1000000000 % danceLoop.size());
    }

    private List<Instruction> loadAllInstructions() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(this::loadInstruction)
                .collect(Collectors.toList());
    }

    private Instruction loadInstruction(String line) {
        char symbol = line.charAt(0);
        String[] operands = line.substring(1).split("/");

        return Op.forSymbol(symbol).loadInstruction(operands);
    }

    private String processAllInstructions(List<Instruction> allInstructions, String initialState) {
        String currentState = initialState;

        for (Instruction instruction : allInstructions) {
            currentState = instruction.op.processState(instruction.operandOne, instruction.operandTwo, currentState);
        }

        return currentState;
    }

    private List<String> findLoopSequence(List<Instruction> instructions, String initialState) {
        int maxLoopSize = 200;

        List<String> seenStates = new ArrayList<>();
        seenStates.add(initialState);

        String currentState = initialState;
        for (int i = 0; i < maxLoopSize; i++) {
            currentState = processAllInstructions(instructions, currentState);
            if (initialState.equals(currentState)) {
                return seenStates;
            }
            seenStates.add(currentState);
        }

        throw new RuntimeException("No loop found within " + maxLoopSize + " iterations");
    }

    private static class Instruction {
        private final Op op;
        private final Operand operandOne;
        private final Operand operandTwo;

        Instruction(Op op, Integer one) {
            this(op, new Operand(one), null);
        }

        Instruction(Op op, Integer one, Integer two) {
            this(op, new Operand(one), new Operand(two));
        }

        Instruction(Op op, String one, String two) {
            this(op, new Operand(one), new Operand(two));
        }

        Instruction(Op op, Operand operandOne, Operand operandTwo) {
            this.op = op;
            this.operandOne = operandOne;
            this.operandTwo = operandTwo;
        }


    }

    private static class Operand {
        private final String letter;
        private final Integer num;

        Operand(String letter) {
            this.letter = letter;
            this.num = null;
        }

        Operand(Integer num) {
            this.letter = null;
            this.num = num;
        }

    }

    private enum Op {
        SPIN('s') {
            @Override
            Instruction loadInstruction(String[] operands) {
                return new Instruction(this, Integer.valueOf(operands[0]));
            }

            @Override
            String processState(Operand operandOne, Operand operandTwo, String state) {
                return StringUtils.rotate(state, operandOne.num);
            }
        },
        EXCHANGE('x') {
            @Override
            Instruction loadInstruction(String[] operands) {
                return new Instruction(this, Integer.valueOf(operands[0]), Integer.valueOf(operands[1]));
            }

            @Override
            String processState(Operand operandOne, Operand operandTwo, String state) {
                char charOne = state.charAt(operandOne.num);
                char charTwo = state.charAt(operandTwo.num);

                return StringUtils.replaceChars(state, "" + charOne + charTwo, "" + charTwo + charOne);
            }
        },
        PARTNER('p') {
            @Override
            Instruction loadInstruction(String[] operands) {
                return new Instruction(this, operands[0], operands[1]);
            }

            @Override
            String processState(Operand operandOne, Operand operandTwo, String state) {
                return StringUtils.replaceChars(
                        state,
                        operandOne.letter + operandTwo.letter,
                        operandTwo.letter + operandOne.letter
                );
            }
        };

        private final char symbol;

        Op(char symbol) {
            this.symbol = symbol;
        }

        abstract Instruction loadInstruction(String[] operands);
        abstract String processState(Operand operandOne, Operand operandTwo, String state);

        private static Op forSymbol(char symbol) {
            return Arrays.stream(Op.values())
                    .filter(o -> o.symbol == symbol)
                    .findFirst()
                    .orElseThrow(() -> new RuntimeException("No match for symbol: " + symbol));

        }
    }


}