package dhasday.adventofcode.dec2017.solvers0x;

import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day5Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/5-input";

    @Override
    public int getDay() {
        return 5;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Integer> instructions = loadAllInstructions();

        return numInstructionsToExit(instructions, i -> i + 1);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Integer> instructions = loadAllInstructions();

        return numInstructionsToExit(instructions, i -> i >= 3 ? i - 1 : i + 1);
    }

    private List<Integer> loadAllInstructions() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(Integer::valueOf)
                .collect(Collectors.toList());
    }

    private Integer numInstructionsToExit(List<Integer> allInstructions,
                                          Function<Integer, Integer> updateInstructionValue) {
        int instructionCount = 0;
        int curInstruction = 0;

        while (curInstruction >= 0 && curInstruction < allInstructions.size()) {
            Integer jumpAmount = allInstructions.get(curInstruction);
            allInstructions.set(curInstruction, updateInstructionValue.apply(jumpAmount));
            curInstruction += jumpAmount;
            instructionCount++;
        }

        return instructionCount;
    }
}
