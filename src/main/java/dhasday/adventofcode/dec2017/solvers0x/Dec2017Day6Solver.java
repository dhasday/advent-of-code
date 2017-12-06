package dhasday.adventofcode.dec2017.solvers0x;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.google.common.collect.Lists;
import dhasday.adventofcode.DaySolver;

public class Dec2017Day6Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/6-input";

    private static final String INPUT_REGEX = "";

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);

    @Override
    public int getDayNumber() {
        return 6;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Integer> registerValues = loadRegisterValues();
        return getNumCyclesBeforeRepeat(registerValues);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Integer> registerValues = loadRegisterValues();
        return getNumCyclesInLoop(registerValues);
    }

    private List<Integer> loadRegisterValues() {
        return Arrays.stream(getOnlyFileLine(INPUT_FILE).split("\t"))
                .map(Integer::valueOf)
                .collect(Collectors.toList());
    }

    private Integer getNumCyclesBeforeRepeat(List<Integer> registerValues) {
        List<Integer> currentValues = Lists.newArrayList(registerValues);

        List<List<Integer>> seenValues = new ArrayList<>();

        int iterations = 0;
        while (!seenValues.contains(currentValues)) {
            seenValues.add(currentValues);
            currentValues = processOnce(currentValues);
            iterations++;
        }

        return iterations;
    }

    private Integer getNumCyclesInLoop(List<Integer> registerValues) {
        List<List<Integer>> seenValues = new ArrayList<>();
        List<Integer> currentValues = Lists.newArrayList(registerValues);

        while (!seenValues.contains(currentValues)) {
            seenValues.add(currentValues);
            currentValues = processOnce(currentValues);
        }

        return seenValues.size() - findFirstPatternIndex(seenValues, currentValues);
    }

    private List<Integer> processOnce(List<Integer> currentValues) {
        List<Integer> registerValues = Lists.newArrayList(currentValues);

        int maxValueIndex = getIndexOfMaxValue(registerValues);
        int toDistribute = registerValues.get(maxValueIndex);
        int nextIndex = (maxValueIndex + 1) % registerValues.size();
        registerValues.set(maxValueIndex, 0);
        for (int i = 0; i < toDistribute; i++) {
            registerValues.set(nextIndex, registerValues.get(nextIndex) + 1);
            nextIndex = (nextIndex + 1) % registerValues.size();
        }

        return registerValues;
    }

    private int getIndexOfMaxValue(List<Integer> values) {
        int maxValue = values.get(0);
        int maxValueIndex = 0;

        for (int i = 1; i < values.size(); i++){
            Integer curValue = values.get(i);
            if (curValue > maxValue) {
                maxValue = curValue;
                maxValueIndex = i;
            }
        }

        return maxValueIndex;
    }

    private int findFirstPatternIndex(List<List<Integer>> seenValues, List<Integer> pattern) {
        for (int i = 0; i < seenValues.size(); i++) {
            if (seenValues.get(i).equals(pattern)) {
                return i;
            }
        }

        throw new RuntimeException("this shouldn't happen");
    }
}
