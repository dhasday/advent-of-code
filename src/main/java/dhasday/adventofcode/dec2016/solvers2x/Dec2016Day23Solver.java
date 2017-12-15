package dhasday.adventofcode.dec2016.solvers2x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import dhasday.adventofcode.dec2016.Dec2016DaySolver;
import dhasday.adventofcode.dec2016.common.AssembunnyProcessor;

public class Dec2016Day23Solver extends Dec2016DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/23-input";

    private AssembunnyProcessor assembunnyProcessor = new AssembunnyProcessor();

    @Override
    public int getDay() {
        return 23;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> instructions = getAllFileLines(INPUT_FILE);

        Map<String, Integer> state = initializeState("a", "b", "c", "d");
        state.put("a", 7);

        assembunnyProcessor.process(state, instructions, null);

        // return 12624;
        return state.get("a");
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> instructions = getAllFileLines(INPUT_FILE);

        Map<String, Integer> state = initializeState("a", "b", "c", "d");
        state.put("a", 12);

        assembunnyProcessor.process(state, instructions, null);

//        return 479009184;
        return state.get("a");
    }

    private Map<String, Integer> initializeState(String... registers) {
        Map<String, Integer> state = new HashMap<>();
        for (String register : registers) {
            state.put(register, 0);
        }
        return state;
    }
}