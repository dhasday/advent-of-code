package dhasday.adventofcode.dec2015.solvers2x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import dhasday.adventofcode.dec2015.Dec2015DaySolver;

public class Dec2015Day23Solver extends Dec2015DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/23-input";

    @Override
    public int getDay() {
        return 23;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Instruction> allInstructions = readAllInstructions(allFileLines);

        Map<String, Integer> initialState = new HashMap<>();
        initialState.put("a", 0);
        initialState.put("b", 0);

        Map<String, Integer> finalState = processInstructions(allInstructions, initialState);

        return finalState.get("b");
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Instruction> allInstructions = readAllInstructions(allFileLines);

        Map<String, Integer> initialState = new HashMap<>();
        initialState.put("a", 1);
        initialState.put("b", 0);

        Map<String, Integer> finalState = processInstructions(allInstructions, initialState);

        return finalState.get("b");
    }

    private List<Instruction> readAllInstructions(List<String> inputLines) {
        return inputLines.stream()
                .map(this::readInstruction)
                .collect(Collectors.toList());
    }

    private Instruction readInstruction(String input) {
        String instructionRegex = "([a-z]+) (a|b|[+-]\\d+)(, )?([+-]\\d+)?";

        Pattern pattern = Pattern.compile(instructionRegex);
        Matcher matcher = pattern.matcher(input);

        if (!matcher.matches()) {
            throw new RuntimeException("Failed to map instruction");
        }

        String register = null;
        Integer offset = null;

        String groupTwo = matcher.group(2);
        if (groupTwo.length() == 1) {
            register = groupTwo;
        } else {
            offset = Integer.valueOf(groupTwo);
        }

        String groupFour = matcher.group(4);
        if (groupFour != null) {
            offset = Integer.valueOf(groupFour);
        }

        return new Instruction(Op.forCode(matcher.group(1)), register, offset);
    }

    private Map<String, Integer> processInstructions(List<Instruction> allInstructions, Map<String, Integer> state) {
        int i = 0;

        while (i < allInstructions.size()) {
            Instruction instruction = allInstructions.get(i);

            Op op = instruction.operation;
            op.processInstruction(state, instruction);

            i += op.getNextInstructionOffset(state, instruction);
        }

        return state;
    }

    private class Instruction {
        private final Op operation;
        private final String register;
        private final Integer offset;

        Instruction(Op operation, String register, Integer offset) {
            this.operation = operation;
            this.register = register;
            this.offset = offset;
        }
    }

    private enum Op {
        HALF("hlf") {
            @Override
            void processInstruction(Map<String, Integer> state, Instruction instruction) {
                state.put(instruction.register, state.get(instruction.register) / 2);
            }
        },
        TRIPLE("tpl") {
            @Override
            void processInstruction(Map<String, Integer> state, Instruction instruction) {
                state.put(instruction.register, state.get(instruction.register) * 3);
            }
        },
        INCREMENT("inc") {
            @Override
            void processInstruction(Map<String, Integer> state, Instruction instruction) {
                state.put(instruction.register, state.get(instruction.register) + 1);
            }
        },
        JUMP("jmp") {
            @Override
            int getNextInstructionOffset(Map<String, Integer> state, Instruction instruction) {
                return instruction.offset;
            }
        },
        JUMP_EVEN("jie") {
            @Override
            int getNextInstructionOffset(Map<String, Integer> state, Instruction instruction) {
                if (state.get(instruction.register) % 2 == 0) {
                    return instruction.offset;
                } else {
                    return super.getNextInstructionOffset(state, instruction);
                }
            }
        },
        JUMP_ONE("jio") {
            @Override
            int getNextInstructionOffset(Map<String, Integer> state, Instruction instruction) {
                if (state.get(instruction.register) == 1) {
                    return instruction.offset;
                } else {
                    return super.getNextInstructionOffset(state, instruction);
                }
            }
        };

        String code;

        Op(String code) {
            this.code = code;
        }

        int getNextInstructionOffset(Map<String, Integer> state, Instruction instruction) {
            return 1;
        }
        void processInstruction(Map<String, Integer> state, Instruction instruction) {
            // Do Nothing
        }

        static Op forCode(String code) {
            for (Op op : values()) {
                if (op.code.equals(code)) {
                    return op;
                }
            }

            throw new RuntimeException("No Op with code: " + code);
        }
    }
}
