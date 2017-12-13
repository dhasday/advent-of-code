package dhasday.adventofcode.dec2017.solvers0x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import dhasday.adventofcode.common.DaySolver;

public class Dec2017Day8Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/8-input";

    private Map<String, Integer> state = null;
    private Integer maxValue = null;

    @Override
    public int getDayNumber() {
        return 8;
    }

    @Override
    public Integer solvePuzzleOne() {
        processState();

        return state.entrySet()
                .stream()
                .mapToInt(Map.Entry::getValue)
                .max()
                .orElseThrow(() -> new RuntimeException("No max value?!?!?"));
    }

    @Override
    public Integer solvePuzzleTwo() {
        processState();

        return maxValue;
    }

    private void processState() {
        if (state != null) {
            return;
        }

        List<String> allInstructions = getAllFileLines(INPUT_FILE);
        state = new HashMap<>();
        maxValue = processAllInstructions(state, allInstructions);
    }

    private Integer processAllInstructions(Map<String, Integer> state, List<String> allInstructions) {
        int maxValue = 0;

        for (String instructionStr : allInstructions) {
            String[] instr = instructionStr.split(" ");

            if (!shouldExecute(state.getOrDefault(instr[4], 0), instr[5], Integer.valueOf(instr[6]))) {
                continue;
            }

            String modifyReg = instr[0];
            int changeAmt = Integer.valueOf(instr[2]);

            int newValue = state.getOrDefault(modifyReg, 0) + ("inc".equals(instr[1]) ? changeAmt : - changeAmt);

            maxValue = Math.max(newValue, maxValue);
            state.put(modifyReg, newValue);
        }

        return maxValue;
    }

    private boolean shouldExecute(Integer valueOne, String operator, Integer valueTwo) {
        switch (operator) {
            case "==":
                return valueOne.equals(valueTwo);
            case "!=":
                return !valueOne.equals(valueTwo);
            case "<":
                return valueOne < valueTwo;
            case "<=":
                return valueOne <= valueTwo;
            case ">":
                return valueOne > valueTwo;
            case ">=":
                return valueOne >= valueTwo;
            default:
                throw new RuntimeException("Unknown operator: " + operator);
        }
    }
}
