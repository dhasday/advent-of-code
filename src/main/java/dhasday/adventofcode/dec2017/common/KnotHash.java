package dhasday.adventofcode.dec2017.common;

import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import com.google.common.collect.Lists;

public class KnotHash {

    private static final int[] ADDITIONAL_LENGTHS = new int[] {17, 31, 73, 47, 23};
    private static final int NUM_ROUNDS = 64;

    public String computeHexHash(String input) {
        return computeHash(input, this::generateHexHash);
    }

    public String computeBinaryHash(String input) {
        return computeHash(input, this::generateBinaryHash);
    }

    private String computeHash(String input, Function<List<Integer>, String> generateHash) {
        List<Integer> lengths = loadLengths(input);

        List<Integer> startValues = IntStream.range(0, 256)
                .boxed()
                .collect(Collectors.toList());

        List<Integer> finalValues = processNRounds(lengths, startValues, NUM_ROUNDS);

        return generateHash.apply(finalValues);
    }

    public List<Integer> processNRounds(List<Integer> inputs, List<Integer> startingValues, int numRounds) {
        State state = new State(Lists.newArrayList(startingValues), 0, 0);

        for (int i = 0; i < numRounds; i++) {
            for (Integer value : inputs) {
                state.values = processLength(state.values, state.curIndex, value);
                state.curIndex = (state.curIndex + value + state.skipSize) % state.values.size();
                state.skipSize++;
            }
        }

        return state.values;
    }

    private List<Integer> loadLengths(String input) {
        List<Integer> lengths = input.chars()
                .boxed()
                .collect(Collectors.toList());

        Arrays.stream(ADDITIONAL_LENGTHS)
                .forEach(lengths::add);

        return lengths;
    }

    private List<Integer> processLength(List<Integer> current, int curPos, int length) {
        List<Integer> result;
        if (current.size() <= curPos + length) {
            // need to process 2 halves
            int endOfListSize = current.size() - curPos;
            int startOfListSize = length - endOfListSize;

            List<Integer> toReverse = current.subList(curPos, current.size());
            toReverse.addAll(current.subList(0, startOfListSize));
            List<Integer> reversed = Lists.reverse(toReverse);

            result = Lists.newArrayList(reversed.subList(endOfListSize, reversed.size()));
            result.addAll(current.subList(startOfListSize, curPos));
            result.addAll(reversed.subList(0, endOfListSize));
        } else {
            int endOfInput = curPos + length;
            List<Integer> toReverse = current.subList(curPos, curPos + length);
            List<Integer> reversed = Lists.reverse(toReverse);

            result = Lists.newArrayList(current.subList(0, curPos));
            result.addAll(reversed);

            result.addAll(current.subList(endOfInput, current.size()));
        }

        return result;
    }

    private String generateHexHash(List<Integer> values) {
        return generateHash(values, (i -> String.format("%02X", i).toLowerCase()));
    }

    private String generateBinaryHash(List<Integer> values) {
        return generateHash(values, (i -> String.format("%8s", Integer.toBinaryString(i))))
                .replaceAll(" ", "0");
    }

    private String generateHash(List<Integer> values, Function<Integer, String> convertToString) {
        String result = "";

        for (int i = 0; i < values.size() / 16; i++) {
            int startIndex = i * 16;
            Integer xorResult = values.get(startIndex);

            for (int j = 1; j < 16; j++) {
                xorResult = xorResult ^ values.get(startIndex + j);
            }

            result += convertToString.apply(xorResult);
        }

        return result;
    }

    private class State {
        private List<Integer> values;
        private int curIndex;
        private int skipSize;

        State(List<Integer> values, int curIndex, int skipSize) {
            this.values = values;
            this.curIndex = curIndex;
            this.skipSize = skipSize;
        }
    }

}
