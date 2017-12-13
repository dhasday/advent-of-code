package dhasday.adventofcode.dec2016.solvers1x;

import java.util.ArrayList;
import java.util.List;
import java.util.function.BiFunction;
import java.util.stream.IntStream;

import dhasday.adventofcode.common.DaySolver;

public class Dec2016Day19Solver implements DaySolver<Integer> {

    private static final Integer INPUT = 3017957;

    @Override
    public int getDayNumber() {
        return 19;
    }

    @Override
    public Integer solvePuzzleOne() {
        IntStream.range(1, 250)
                .forEach(input -> {
                    Integer bruteForceAnswer = bruteForceKillNextWinner(input);
                    Integer calculatedAnswer = calculateKillNextWinner(input);
                    if (!bruteForceAnswer.equals(calculatedAnswer)) {
                        System.out.println(input + "\t" + bruteForceAnswer + "\t" + calculatedAnswer);
                    }
                });
        return calculateKillNextWinner(INPUT);
    }

    @Override
    public Integer solvePuzzleTwo() {
        IntStream.range(1, 250)
                .forEach(input -> {
                    Integer bruteForceAnswer = bruteForceKillAcrossWinner(input);
                    Integer calculatedAnswer = calculateKillAcrossWinner(input);
                    if (!bruteForceAnswer.equals(calculatedAnswer)) {
                        System.out.println(input + "\t" + bruteForceAnswer + "\t" + calculatedAnswer);
                    }
                });
        return calculateKillAcrossWinner(INPUT);
    }

    private Integer calculateKillNextWinner(int input) {
        Integer nearestPowerOfTwo = findPreviousPowerOfN(input, 2);
        return (input - nearestPowerOfTwo) * 2 + 1;
    }

    private Integer calculateKillAcrossWinner(int input) {
        if (input < 3) {
            return 1;
        }

        Integer nearestPowerOfThree = findPreviousPowerOfN(input, 3);
        if (nearestPowerOfThree == input) {
            return nearestPowerOfThree;
        }

        Integer excess = input - nearestPowerOfThree;

        if (excess <= nearestPowerOfThree) {
            return excess;
        } else {
            return nearestPowerOfThree + ((excess - nearestPowerOfThree) * 2);
        }
    }

    private Integer findPreviousPowerOfN(Integer input, int n) {
        int nextPowerOfTwo = 1;

        while (nextPowerOfTwo <= input) {
            nextPowerOfTwo *= n;
        }

        return nextPowerOfTwo / n;
    }

    private Integer bruteForceKillNextWinner(int input) {
        return findWinningElf(
                input,
                (remainingElves, curIndex) -> (curIndex + 1) % remainingElves.size()
        );
    }

    private Integer bruteForceKillAcrossWinner(int input) {
        return findWinningElf(
                input,
                (remainingElves, curIndex) -> {
                    int curSize = remainingElves.size();
                    return (curIndex + (Math.floorDiv(curSize, 2))) % curSize;
                });
    }

    private Integer findWinningElf(Integer input, BiFunction<List<Integer>, Integer, Integer> offsetToRemove) {
        List<Integer> remainingElves = new ArrayList<>();
        for (int i = 0; i < input; i++) {
            remainingElves.add(i + 1);
        }

        int curIndex = 0;
        while(remainingElves.size() > 1) {
            int toRemove = offsetToRemove.apply(remainingElves, curIndex);

            remainingElves.remove(toRemove);

            if (curIndex < toRemove) { // If we removed something later in the array
                curIndex = (curIndex + 1) % remainingElves.size();
            }

            if (curIndex >= remainingElves.size()) {
                curIndex = 0;
            }
        }

        return remainingElves.iterator().next();
    }
}
