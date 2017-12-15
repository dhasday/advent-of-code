package dhasday.adventofcode.dec2016.solvers2x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.dec2016.common.AssembunnyProcessor;

public class Dec2016Day25Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/25-input";

    private AssembunnyProcessor assembunnyProcessor = new AssembunnyProcessor();

    @Override
    public int getDayNumber() {
        return 25;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> instructions = getAllFileLines(INPUT_FILE);

        String expectedZero = "0101010101010101010101010";
        String expectedOne =  "1010101010101010101010101";
        for (int i = 1; i < 250; i++) {
            Map<String, Integer> state = initializeState("a", "b", "c", "d");
            state.put("a", i);
            String actual = assembunnyProcessor.process(state, instructions, 25);

            if (expectedZero.equals(actual) || expectedOne.equals(actual)) {
                return i;
            }
        }

        return null;
    }

    @Override
    public Integer solvePuzzleTwo() {
        return null;
    }

    private Map<String, Integer> initializeState(String... registers) {
        Map<String, Integer> state = new HashMap<>();
        for (String register : registers) {
            state.put(register, 0);
        }
        return state;
    }
}
