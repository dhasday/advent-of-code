package dhasday.adventofcode.dec2015.solvers2x;

import dhasday.adventofcode.DaySolver;

public class Dec2015Day20Solver implements DaySolver<Integer> {

    private static final Integer INPUT_PUZZLE_ONE = 29000000;

    @Override
    public int getDayNumber() {
        return 20;
    }

    @Override
    public Integer solvePuzzleOne() {
        return findFirstHouseWithAtLeastNPresents(INPUT_PUZZLE_ONE, 10, null);
    }

    @Override
    public Integer solvePuzzleTwo() {
        return findFirstHouseWithAtLeastNPresents(INPUT_PUZZLE_ONE, 11, 50);
    }

    Integer findFirstHouseWithAtLeastNPresents(Integer numPresents, Integer presentMultiplier, Integer houseLimit) {
        int worstCaseHouse = (numPresents / presentMultiplier) + presentMultiplier;

        for (int i = 1; i < worstCaseHouse; i++) {
            Integer presentsForHouse = calculatePresentsForHouse(i, presentMultiplier, houseLimit);

            if (presentsForHouse >= numPresents) {
                return i;
            }
        }

        return null;
    }

    Integer calculatePresentsForHouse(Integer houseNumber, Integer presentMultiplier, Integer houseLimit) {
        int totalPresents = 0;

        int maxFactor = (int) Math.sqrt(houseNumber);

        for (int i = 1; i <= maxFactor; i++) {
            if (houseNumber % i == 0) {
                if (willDeliver(houseNumber, i, houseLimit)) {
                    totalPresents += (i * presentMultiplier);
                }

                int matchingFactor = houseNumber / i;
                if (matchingFactor != i && willDeliver(houseNumber, matchingFactor, houseLimit)) {
                    totalPresents += (matchingFactor * presentMultiplier);
                }
            }
        }

        return totalPresents;
    }

    private boolean willDeliver(Integer houseNumber, Integer elfNumber, Integer houseLimit) {
        return houseLimit == null || houseNumber <= (elfNumber * houseLimit);
    }
}
