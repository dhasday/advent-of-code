package dhasday.adventofcode.dec2017.solvers1x;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import com.google.common.collect.Lists;
import dhasday.adventofcode.DaySolver;

public class Dec2017Day10Solver implements DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/10-input";

    @Override
    public int getDayNumber() {
        return 10;
    }

    @Override
    public String solvePuzzleOne() {
        List<Integer> inputs = loadIntInput();

        List<Integer> values = IntStream.range(0, 256)
                .boxed()
                .collect(Collectors.toList());

        List<Integer> result = processNRounds(inputs, values, 1);

        return String.valueOf(result.get(0) * result.get(1));
    }

    @Override
    public String solvePuzzleTwo() {
        List<Integer> inputs = loadAsciiInput();
        inputs.addAll(Lists.newArrayList(17, 31, 73, 47, 23));

        List<Integer> values = IntStream.range(0, 256)
                .boxed()
                .collect(Collectors.toList());

        List<Integer> result = processNRounds(inputs, values, 64);

        return generateDenseHash(result);
    }

    private List<Integer> loadIntInput() {
        return Arrays.stream(getOnlyFileLine(INPUT_FILE).split(","))
                .map(Integer::valueOf)
                .collect(Collectors.toList());
    }

    private List<Integer> loadAsciiInput() {
        return getOnlyFileLine(INPUT_FILE).chars()
                .boxed()
                .collect(Collectors.toList());
    }

    private List<Integer> processNRounds(List<Integer> inputs, List<Integer> startingValues, int numRounds) {
        Result result = new Result();
        result.curIndex = 0;
        result.skipSize = 0;
        result.values = Lists.newArrayList(startingValues);

        for (int i = 0; i < numRounds; i++) {
            processOneRound(inputs, result);
        }

        return result.values;
    }

    private void processOneRound(List<Integer> inputs, Result result) {
        for (Integer value : inputs) {
            result.values = processOnceInput(result.values, result.curIndex, value);
            result.curIndex = (result.curIndex + value + result.skipSize) % result.values.size();
            result.skipSize++;
        }
    }

    private List<Integer> processOnceInput(List<Integer> current, int curPos, Integer value) {
        List<Integer> result;
        if (current.size() <= curPos + value) {
            // need to process 2 halves
            int endOfListSize = current.size() - curPos;
            int startOfListSize = value - endOfListSize;

            List<Integer> toReverse = current.subList(curPos, current.size());
            toReverse.addAll(current.subList(0, startOfListSize));
            List<Integer> reversed = Lists.reverse(toReverse);

            result = Lists.newArrayList(reversed.subList(endOfListSize, reversed.size()));
            result.addAll(current.subList(startOfListSize, curPos));
            result.addAll(reversed.subList(0, endOfListSize));
        } else {
            int endOfInput = curPos + value;
            List<Integer> toReverse = current.subList(curPos, curPos + value);
            List<Integer> reversed = Lists.reverse(toReverse);

            result = Lists.newArrayList(current.subList(0, curPos));
            result.addAll(reversed);

            result.addAll(current.subList(endOfInput, current.size()));
        }
        return result;
    }

    private String generateDenseHash(List<Integer> sparseHash) {
        String result = "";
        for (int i = 0; i < sparseHash.size() / 16; i++) {
            int startIndex = i * 16;
            Integer xorResult = null;
            for (int j = 0; j < 16; j++) {
                Integer value = sparseHash.get(startIndex + j);

                if (xorResult == null) {
                    xorResult = value;
                } else {
                    xorResult = xorResult ^ value;
                }
            }

            result += String.format("%02X", xorResult).toLowerCase();
        }

        return result;
    }

    private class Result {
        private List<Integer> values;
        private int curIndex;
        private int skipSize;
    }
}
