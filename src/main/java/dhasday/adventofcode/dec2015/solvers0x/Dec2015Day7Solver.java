package dhasday.adventofcode.dec2015.solvers0x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.common.collect.ImmutableMap;
import dhasday.adventofcode.common.DaySolver;
import org.apache.commons.lang3.StringUtils;

public class Dec2015Day7Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/7-input";

    private static final Integer UNSIGNED_SHORT_BIT_MASK = 0xffff;

    private Pattern assignmentPattern = Pattern.compile("(NOT )?([a-z]+|[0-9]+) -> ([a-z]+)");
    private Pattern operationPattern = Pattern.compile("([a-z]+|[0-9]+) (AND|OR|LSHIFT|RSHIFT) ([a-z]+|[0-9]+) -> ([a-z]+)");

    @Override
    public int getDayNumber() {
        return 7;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allInstructions = getAllFileLines(INPUT_FILE);

        Map<String, Integer> initialState = ImmutableMap.of();

        Map<String, Integer> result = processAllInstructions(allInstructions, initialState);

        return result.get("a");
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allInstructions = getAllFileLines(INPUT_FILE);

        Map<String, Integer> initialState = ImmutableMap.of("b", 956);

        Map<String, Integer> result = processAllInstructions(allInstructions, initialState);

        return result.get("a");
    }

    Map<String, Integer> processAllInstructions(List<String> allInstructions, Map<String, Integer> initialState) {
        Map<String, VariableState> state = loadInstructions(allInstructions);

        for (String variable : state.keySet()) {
            Integer setValue = initialState.get(variable);

            VariableState variableState = state.get(variable);

            if (setValue != null) {
                variableState.value = setValue;
                variableState.reprocess = false;
            } else {
                variableState.value = 0;
                variableState.reprocess = true;
            }
        }

        return processInstructions(state);
    }

    private Map<String, VariableState> loadInstructions(List<String> instructions) {
        Map<String, VariableState> state = new HashMap<>();

        instructions.forEach(instruction -> {
            BitwiseOperation operation = parseOperation(instruction);
            state.put(operation.target, new VariableState(operation, null));
        });

        return state;
    }

    private Map<String, Integer> processInstructions(Map<String, VariableState> state) {
        Map<String, Integer> result = new HashMap<>();

        state.keySet()
                .forEach(variable -> {
                    Integer value = processValue(state, variable);
                    result.put(variable, value);
                });

        return result;
    }

    private BitwiseOperation parseOperation(String input) {
        Matcher assignmentMatcher = assignmentPattern.matcher(input);
        if (assignmentMatcher.matches()) {
            return new BitwiseOperation(
                    assignmentMatcher.group(1) == null ? Operation.ASSIGN : Operation.ASSIGN_INVERSE,
                    assignmentMatcher.group(2),
                    null,
                    assignmentMatcher.group(3)
            );
        }

        Matcher operationMatcher = operationPattern.matcher(input);
        if (operationMatcher.matches()) {
            return new BitwiseOperation(
                    Operation.valueOf(operationMatcher.group(2)),
                    operationMatcher.group(1),
                    operationMatcher.group(3),
                    operationMatcher.group(4)
            );
        }

        throw new RuntimeException("Unable to parse instruction: " + input);
    }

    private class VariableState {
        private BitwiseOperation operation;
        private Integer value;
        private boolean reprocess = false;

        VariableState(BitwiseOperation operation, Integer value) {
            this.operation = operation;
            this.value = value;
        }
    }

    private class BitwiseOperation {
        private Operation operation;
        private String operandOne;
        private String operandTwo;
        private String target;

        BitwiseOperation(Operation operation, String operandOne, String operandTwo, String target) {
            this.operation = operation;
            this.operandOne = operandOne;
            this.operandTwo = operandTwo;
            this.target = target;
        }
    }

    private enum Operation {
        ASSIGN {
            @Override
            Integer process(Map<String, VariableState> state, BitwiseOperation operation) {
                return parseOrProcessValue(state, operation.operandOne);
            }
        },
        ASSIGN_INVERSE {
            @Override
            Integer process(Map<String, VariableState> state, BitwiseOperation operation) {
                Integer newValue = parseOrProcessValue(state, operation.operandOne);
                return clearHighBits(~ newValue);
            }
        },
        AND {
            @Override
            Integer process(Map<String, VariableState> state, BitwiseOperation operation) {
                Integer valueOne = parseOrProcessValue(state, operation.operandOne);
                Integer valueTwo = parseOrProcessValue(state, operation.operandTwo);
                return clearHighBits(valueOne & valueTwo);
            }
        },
        OR {
            @Override
            Integer process(Map<String, VariableState> state, BitwiseOperation operation) {
                Integer valueOne = parseOrProcessValue(state, operation.operandOne);
                Integer valueTwo = parseOrProcessValue(state, operation.operandTwo);
                return clearHighBits(valueOne | valueTwo);
            }
        },
        LSHIFT {
            @Override
            Integer process(Map<String, VariableState> state, BitwiseOperation operation) {
                Integer valueOne = parseOrProcessValue(state, operation.operandOne);
                Integer valueTwo = parseOrProcessValue(state, operation.operandTwo);
                return clearHighBits(valueOne << valueTwo);
            }
        },
        RSHIFT {
            @Override
            Integer process(Map<String, VariableState> state, BitwiseOperation operation) {
                Integer valueOne = parseOrProcessValue(state, operation.operandOne);
                Integer valueTwo = parseOrProcessValue(state, operation.operandTwo);
                return clearHighBits(valueOne >> valueTwo);
            }
        };

        abstract Integer process(Map<String, VariableState> state, BitwiseOperation operation);
    }

    private static Integer parseOrProcessValue(Map<String, VariableState> state, String operand) {
        if (StringUtils.isNumeric(operand)) {
            return parseNumber(operand);
        } else {
            return processValue(state, operand);
        }
    }

    private static Integer parseNumber(String number) {
        return clearHighBits(Integer.valueOf(number));
    }

    private static Integer clearHighBits(Integer input) {
        return input & UNSIGNED_SHORT_BIT_MASK;
    }

    private static Integer processValue(Map<String, VariableState> state, String variable) {
        VariableState variableState = state.get(variable);
        if (variableState == null) {
            throw new RuntimeException("Unable to process value for unknown variable: " + variable);
        }

        if (variableState.value == null || variableState.reprocess) {
            BitwiseOperation operation = variableState.operation;
            // Updating the reference so it should be updated in the map
            variableState.value = operation.operation.process(state, operation);
            variableState.reprocess = false;
        }

        return variableState.value;
    }

}
