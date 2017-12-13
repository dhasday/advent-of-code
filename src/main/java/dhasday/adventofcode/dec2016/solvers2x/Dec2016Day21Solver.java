package dhasday.adventofcode.dec2016.solvers2x;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.google.common.collect.Sets;
import dhasday.adventofcode.common.DaySolver;
import org.apache.commons.lang3.StringUtils;

public class Dec2016Day21Solver implements DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/21-input";

    @Override
    public int getDayNumber() {
        return 21;
    }

    @Override
    public String solvePuzzleOne() {
        List<Instruction> allInstructions = getAllInstructions();

        String input = "abcdefgh";

        return processAllInstructions(allInstructions, input);
    }

    @Override
    public String solvePuzzleTwo() {
        List<Instruction> allInstructions = getAllInstructions();

        String output = "fbgdceah";

        return findMatchingInput(allInstructions, output);
    }

    private List<Instruction> getAllInstructions() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(this::parseInstruction)
                .collect(Collectors.toList());
    }

    private Instruction parseInstruction(String input) {
        Pattern swapPosPattern = Pattern.compile("swap position (\\d+) with position (\\d+)");
        Matcher swapPosMatcher = swapPosPattern.matcher(input);
        if (swapPosMatcher.matches()) {
            return new Instruction(
                    Op.SWAP_POSITION,
                    Integer.valueOf(swapPosMatcher.group(1)),
                    Integer.valueOf(swapPosMatcher.group(2))
            );
        }

        Pattern swapLetterPattern = Pattern.compile("swap letter ([a-z]) with letter ([a-z])");
        Matcher swapLetterMatcher = swapLetterPattern.matcher(input);
        if (swapLetterMatcher.matches()) {
            return new Instruction(
                    Op.SWAP_LETTER,
                    swapLetterMatcher.group(1).charAt(0),
                    swapLetterMatcher.group(2).charAt(0)
            );
        }

        Pattern rotateDirectionPattern = Pattern.compile("rotate (left|right) (\\d+) steps?");
        Matcher rotateDirectionMatcher = rotateDirectionPattern.matcher(input);
        if (rotateDirectionMatcher.matches()) {
            return new Instruction(
                    "left".equals(rotateDirectionMatcher.group(1)) ? Op.ROTATE_LEFT : Op.ROTATE_RIGHT,
                    Integer.valueOf(rotateDirectionMatcher.group(2))
            );
        }

        Pattern rotateRelativePattern = Pattern.compile("rotate based on position of letter ([a-z])");
        Matcher rotateRelativeMatcher = rotateRelativePattern.matcher(input);
        if (rotateRelativeMatcher.matches()) {
            return new Instruction(
                    Op.ROTATE_RELATIVE,
                    rotateRelativeMatcher.group(1).charAt(0)
            );
        }

        Pattern reversePattern = Pattern.compile("reverse positions ([\\d]+) through ([\\d]+)");
        Matcher reverseMatcher = reversePattern.matcher(input);
        if (reverseMatcher.matches()) {
            return new Instruction(
                    Op.REVERSE,
                    Integer.valueOf(reverseMatcher.group(1)),
                    Integer.valueOf(reverseMatcher.group(2))
            );
        }

        Pattern movePattern = Pattern.compile("move position ([\\d]+) to position ([\\d]+)");
        Matcher moveMatcher = movePattern.matcher(input);
        if (moveMatcher.matches()) {
            return new Instruction(
                    Op.MOVE,
                    Integer.valueOf(moveMatcher.group(1)),
                    Integer.valueOf(moveMatcher.group(2))
            );
        }

        throw new RuntimeException("Fix your matchers: " + input);
    }

    private String processAllInstructions(List<Instruction> instructions, String input) {
        String currentValue = input;

        for (Instruction instruction : instructions) {
            currentValue = instruction.op.processInstruction(currentValue, instruction);
        }

        return currentValue;
    }

    private String findMatchingInput(List<Instruction> instructions, String output) {
        Set<String> allPossibleInputs = getAllPossibleInputs(output);

        for (String possibleInput : allPossibleInputs) {
            String result = processAllInstructions(instructions, possibleInput);

            if (result.equals(output)) {
                return possibleInput;
            }
        }

        return null;
    }

    private Set<String> getAllPossibleInputs(String output) {
        Set<Character> chars = output.chars().mapToObj(i -> (char) i).collect(Collectors.toSet());

        return getPossibleInputs("", chars);
    }

    private Set<String> getPossibleInputs(String prefix, Set<Character> remainingChars) {
        if (remainingChars.isEmpty()) {
            return Sets.newHashSet(prefix);
        }

        Set<String> possibleInputs = new HashSet<>();

        for (Character c : remainingChars) {
            Set<Character> newRemainingChars = Sets.newHashSet(remainingChars);
            newRemainingChars.remove(c);

            String newPrefix = prefix + c;

            possibleInputs.addAll(getPossibleInputs(newPrefix, newRemainingChars));
        }

        return possibleInputs;
    }

    private class Instruction {
        private final Op op;

        private final Integer posOne;
        private final Integer posTwo;

        private final Character letterOne;
        private final Character letterTwo;

        // Rotate Left/Right
        Instruction(Op op, Integer posOne) {
            this(op, posOne, null, null, null);
        }

        // Swap Pos, Reverse Pos, Move
        Instruction(Op op, Integer posOne, Integer posTwo) {
            this(op, posOne, posTwo, null, null);
        }

        // Rotate character
        Instruction(Op op, Character letterOne) {
            this(op, null, null, letterOne, null);
        }

        // Swap Letter
        Instruction(Op op, Character letterOne, Character letterTwo) {
            this(op, null, null, letterOne, letterTwo);
        }

        Instruction(Op op,
                    Integer posOne,
                    Integer posTwo,
                    Character letterOne,
                    Character letterTwo) {
            this.op = op;
            this.posOne = posOne;
            this.posTwo = posTwo;
            this.letterOne = letterOne;
            this.letterTwo = letterTwo;
        }
    }

    private enum Op {
        SWAP_POSITION {
            @Override
            String processInstruction(String input, Instruction instruction) {
                char charOne = input.charAt(instruction.posOne);
                char charTwo = input.charAt(instruction.posTwo);
                return StringUtils.replaceChars(
                        input,
                        charOne + "" + charTwo,
                        charTwo + "" + charOne
                );
            }
        },
        SWAP_LETTER {
            @Override
            String processInstruction(String input, Instruction instruction) {
                return StringUtils.replaceChars(
                        input,
                        instruction.letterOne + "" + instruction.letterTwo,
                        instruction.letterTwo + "" + instruction.letterOne
                );
            }
        },
        ROTATE_LEFT {
            @Override
            String processInstruction(String input, Instruction instruction) {
                return StringUtils.rotate(input, - instruction.posOne);
            }
        },
        ROTATE_RIGHT {
            @Override
            String processInstruction(String input, Instruction instruction) {
                return StringUtils.rotate(input, instruction.posOne);
            }
        },
        ROTATE_RELATIVE {
            @Override
            String processInstruction(String input, Instruction instruction) {
                int index = input.indexOf(instruction.letterOne);

                int numRotations = 1 + index;
                if (index >= 4) {
                    numRotations++;
                }

                return StringUtils.rotate(input, numRotations);
            }
        },
        REVERSE {
            @Override
            String processInstruction(String input, Instruction instruction) {
                return input.substring(0, instruction.posOne)
                        + StringUtils.reverse(input.substring(instruction.posOne, instruction.posTwo + 1))
                        + input.substring(instruction.posTwo + 1, input.length());
            }
        },
        MOVE {
            @Override
            String processInstruction(String input, Instruction instruction) {
                String tmp = input.substring(0, instruction.posOne) + input.substring(instruction.posOne + 1);
                return tmp.substring(0, instruction.posTwo)
                        + input.charAt(instruction.posOne)
                        + tmp.substring(instruction.posTwo);
            }
        };

        abstract String processInstruction(String input, Instruction instruction);
    }
}
