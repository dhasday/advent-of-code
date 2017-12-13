package dhasday.adventofcode.dec2016.common;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class AssembunnyProcessor {

    public String process(Map<String, Integer> state, List<String> instructions, Integer outputLimit) {
        List<Instruction> allInstructions = loadInstructions(instructions);

        // TODO: Optimize Instructions

        return processInstructions(allInstructions, state, outputLimit);
    }

    private List<Instruction> loadInstructions(List<String> instructions) {
        return instructions.stream()
                .map(this::loadInstruction)
                .collect(Collectors.toList());
    }

    private Instruction loadInstruction(String input) {
        String inputRegex = "([a-z]{3}) (-?[a-z\\d]+)( (-?[a-z\\d]+))?";
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

    private String processInstructions(List<Instruction> instructions,
                                       Map<String, Integer> state,
                                       Integer outputLimit) {
        int currentInstruction = 0;

        String output = "";
        while (currentInstruction >= 0 && currentInstruction < instructions.size()) {
            Instruction instruction = instructions.get(currentInstruction);

            Op operation = instruction.operation;
            switch (operation) {
                case TOGGLE:
                    handleToggle(state, instructions, currentInstruction);
                    break;
                default:
                    output += operation.processState(state, instruction.operandOne, instruction.operandTwo);
            }

            if (outputLimit != null && output.length() >= outputLimit) {
                return output;
            }

            currentInstruction += operation.nextInstructionOffset(state, instruction.operandOne, instruction.operandTwo);
        }

        return output;
    }

    private void handleToggle(Map<String, Integer> state, List<Instruction> allInstructions, int curInstruction) {
        Instruction instruction = allInstructions.get(curInstruction);

        int instructionToChange = curInstruction + instruction.operandOne.resolveValue(state);
        if (instructionToChange < 0 || instructionToChange >= allInstructions.size()) {
            return;
        }

        Instruction toModify = allInstructions.get(instructionToChange);
        Instruction newInstruction;
        switch (toModify.operation) {
            case INCREASE:
                newInstruction = new Instruction(Op.DECREASE, toModify.operandOne, toModify.operandTwo);
                break;
            case DECREASE:
                newInstruction = new Instruction(Op.INCREASE, toModify.operandOne, toModify.operandTwo);
                break;
            case TOGGLE:
                newInstruction = new Instruction(Op.INCREASE, toModify.operandOne, toModify.operandTwo);
                break;
            case COPY:
                newInstruction = new Instruction(Op.JUMP_NOT_ZERO, toModify.operandOne, toModify.operandTwo);
                break;
            case JUMP_NOT_ZERO:
                newInstruction = new Instruction(Op.COPY, toModify.operandOne, toModify.operandTwo);
                break;
            default:
                throw new RuntimeException("Wat?!");
        }
        allInstructions.remove(instructionToChange);
        allInstructions.add(instructionToChange, newInstruction);

    }

    private class Instruction {
        private Op operation;

        private Operand operandOne;
        private Operand operandTwo;

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
            String processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                if (operandTwo.register == null) {
                    return "";
                }

                Integer valueOne = operandOne.resolveValue(state);
                state.put(operandTwo.register, valueOne);
                return "";
            }
        },
        INCREASE("inc") {
            @Override
            String processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                if (operandOne.register == null) {
                    return "";
                }

                String register = operandOne.register;
                state.put(register, state.get(register) + 1);
                return "";
            }
        },
        DECREASE("dec") {
            @Override
            String processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                if (operandOne.register == null) {
                    return "";
                }

                String register = operandOne.register;
                state.put(register, state.get(register) - 1);
                return "";
            }
        },
        JUMP_NOT_ZERO("jnz") {
            @Override
            String processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                // No state change
                return "";
            }

            @Override
            int nextInstructionOffset(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                Integer valueOne = operandOne.resolveValue(state);

                if (0 == valueOne) {
                    return super.nextInstructionOffset(state, operandOne, operandTwo);
                } else {
                    return operandTwo.resolveValue(state);
                }
            }
        },
        TOGGLE("tgl") {
            @Override
            String processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                throw new RuntimeException("Need a custom case for this");
            }
        },
        OUTPUT("out") {
            @Override
            String processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo) {
                return operandOne.resolveValue(state) + "";
            }
        };

        final String key;
        abstract String processState(Map<String, Integer> state, Operand operandOne, Operand operandTwo);

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
