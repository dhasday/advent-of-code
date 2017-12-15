package dhasday.adventofcode.dec2017.solvers1x;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;
import dhasday.adventofcode.dec2017.common.KnotHash;

public class Dec2017Day10Solver extends Dec2017DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/10-input";

    private KnotHash knotHash = new KnotHash();

    @Override
    public int getDay() {
        return 10;
    }

    @Override
    public String solvePuzzleOne() {
        List<Integer> inputs = loadIntInput();

        List<Integer> values = IntStream.range(0, 256)
                .boxed()
                .collect(Collectors.toList());

        List<Integer> result = knotHash.processNRounds(inputs, values, 1);

        return String.valueOf(result.get(0) * result.get(1));
    }

    @Override
    public String solvePuzzleTwo() {
        return knotHash.computeHexHash(getOnlyFileLine(INPUT_FILE));
    }

    private List<Integer> loadIntInput() {
        return Arrays.stream(getOnlyFileLine(INPUT_FILE).split(","))
                .map(Integer::valueOf)
                .collect(Collectors.toList());
    }
}
