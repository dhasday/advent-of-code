package dhasday.adventofcode.dec2016.solvers1x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.dec2016.common.AssembunnyProcessor;

public class Dec2016Day12Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/12-input";

    private AssembunnyProcessor assembunnyProcessor = new AssembunnyProcessor();

    @Override
    public int getDayNumber() {
        return 12;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> instructions = getAllFileLines(INPUT_FILE);

        Map<String, Integer> state = initializeState("a", "b", "c", "d");

        assembunnyProcessor.process(state, instructions, null);

        return state.get("a");
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> instructions = getAllFileLines(INPUT_FILE);
;
        Map<String, Integer> state = initializeState("a", "b", "c", "d");
        state.put("c", 1);

        assembunnyProcessor.process(state, instructions, null);

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
