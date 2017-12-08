package dhasday.adventofcode.dec2016.solvers1x;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import dhasday.adventofcode.DaySolver;

public class Dec2016Day12Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/12-input";

    @Override
    public int getDayNumber() {
        return 12;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Instruction> instructions = loadInstructions();

        Map<String, Integer> state = initializeState("a", "b", "c", "d");

        processInstructions(instructions, state);

        return state.get("a");
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Instruction> instructions = loadInstructions();
;
        Map<String, Integer> state = initializeState("a", "b", "c", "d");
        state.put("c", 1);

        processInstructions(instructions, state);

        return state.get("a");
    }

    private List<Instruction> loadInstructions() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(this::loadInstruction)
                .collect(Collectors.toList());
    }

    private Instruction loadInstruction(String input) {
        String inputRegex = "([a-z]{3}) (-?[a-z\\d]+)( )?(-?[a-z\\d]+)?";
        Pattern inputPattern = Pattern.compile(inputRegex);

        Matcher matcher = inputPattern.matcher(input);

        if (!matcher.matches()) {
            throw new RuntimeException("Fix your matcher: " + input);
        }

        return new Instruction(
                Op.forKey(matcher.group(1)),
                new Operand(matcher.group(2)),
                new Operand(matcher.group(4))
        );
    }

    private Map<String, Integer> initializeState(String... registers) {
        Map<String, Integer> state = new HashMap<>();
        for (String register : registers) {
            state.put(register, 0);
        }
        return state;
    }

    private void processInstructions(List<Instruction> instructions, Map<String, Integer> state) {
        int currentInstruction = 0;

        while (currentInstruction >= 0 && currentInstruction < instructions.size()) {
            Instruction instruction = instructions.get(currentInstruction);

            Op operation = instruction.operation;
            operation.processState(state, instruction.operandOne, instruction.operandTwo);
            currentInstruction += operation.nextInstructionOffset(state, instruction.operandOne, instruction.operandTwo);
        }
    }

    private class Instruction {
        private final Op operation;

        private final Operand operandOne;
        private final Operand operandTwo;

        Instruction(Op operation, Operand operandOne, Operand operandTwo) {
            this.operation = operation;
            this.operandOne = operandOne;
            this.operandTwo = operandTwo;
        }
    }

    private class Operand {
        private final String register;
        private final Integer value;

        Operand(String inputValue) {
            Integer numberValue = null;
            String stringValue = null;

            try {
                numberValue = Integer.valueOf(inputValue);
            } catch (NumberFormatException nfe) {
                stringValue = inputValue;
            }

            this.register = stringValue;
            this.value = numberValue;
        }

        Integer resolveValue(Map<String, Integer> state) {
            if (value != null) {
                return value;
            }

            return state.get(register);
        }
    }

    private enum Op {
        COPY("cpy") {
            @Override
            void processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                Integer valueOne = operandOne.resolveValue(state);
                state.put(operandTwo.register, valueOne);
            }
        },
        INCREASE("inc") {
            @Override
            void processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                String register = operandOne.register;
                state.put(register, state.get(register) + 1);
            }
        },
        DECREASE("dec") {
            @Override
            void processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                String register = operandOne.register;
                state.put(register, state.get(register) - 1);
            }
        },
        JUMP_NOT_ZERO("jnz") {
            @Override
            void processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                // No state change
            }

            @Override
            int nextInstructionOffset(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                Integer valueOne = operandOne.resolveValue(state);

                if (0 == valueOne) {
                    return super.nextInstructionOffset(state, operandOne, operandTwo);
                } else {
                    return operandTwo.value;
                }
            }
        };

        final String key;
        abstract void processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo);

        static Op forKey(String key) {
            return Arrays.stream(values())
                    .filter(op -> key.equals(op.key))
                    .findFirst()
                    .orElseThrow(() -> new RuntimeException("Unknown instruction key: " + key));
        }

        Op(String key) {
            this.key = key;
        }

        int nextInstructionOffset(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
            return 1;
        }
    }
}
