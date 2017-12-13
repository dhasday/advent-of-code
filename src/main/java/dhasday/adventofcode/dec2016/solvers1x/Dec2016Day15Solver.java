package dhasday.adventofcode.dec2016.solvers1x;

import java.util.Comparator;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import com.google.common.collect.Lists;
import dhasday.adventofcode.common.DaySolver;

public class Dec2016Day15Solver implements DaySolver<Integer> {

    @Override
    public int getDayNumber() {
        return 15;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Disc> discs = Lists.newArrayList(
                new Disc(13, 10),   // Disc #1 has 13 positions; at time=0, it is at position 10.
                new Disc(17, 15),   // Disc #2 has 17 positions; at time=0, it is at position 15.
                new Disc(19, 17),   // Disc #3 has 19 positions; at time=0, it is at position 17.
                new Disc(7, 1),     // Disc #4 has 7 positions; at time=0, it is at position 1.
                new Disc(5, 0),     // Disc #5 has 5 positions; at time=0, it is at position 0.
                new Disc(3, 1)      // Disc #6 has 3 positions; at time=0, it is at position 1.
        );

        return findFirstTimeToPressButton(discs, 250000);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Disc> discs = Lists.newArrayList(
                new Disc(13, 10),   // Disc #1 has 13 positions; at time=0, it is at position 10.
                new Disc(17, 15),   // Disc #2 has 17 positions; at time=0, it is at position 15.
                new Disc(19, 17),   // Disc #3 has 19 positions; at time=0, it is at position 17.
                new Disc(7, 1),     // Disc #4 has 7 positions; at time=0, it is at position 1.
                new Disc(5, 0),     // Disc #5 has 5 positions; at time=0, it is at position 0.
                new Disc(3, 1),     // Disc #6 has 3 positions; at time=0, it is at position 1.
                new Disc(11, 0)     // Disc #7 has 11 positions; at time=0, it is at position 10.
        );

        return findFirstTimeToPressButton(discs, 2500000);
    }

    private Integer findFirstTimeToPressButton(List<Disc> discs, int maxNumber) {
        Set<Integer> possibleTimes = IntStream.range(0, maxNumber).boxed().collect(Collectors.toSet());

        for (int i = 0; i < discs.size(); i++) {
            Disc currentDisc = discs.get(i);

            // Get first positive t where this disc would be aligned
            int firstAlignmentAdjustment = (currentDisc.numPositions + currentDisc.firstZero - (i + 1)) % currentDisc.numPositions;
            possibleTimes = possibleTimes.stream()
                    .filter(t -> (t >= firstAlignmentAdjustment) && (t - firstAlignmentAdjustment) % currentDisc.numPositions == 0)
                    .collect(Collectors.toSet());
        }

        return possibleTimes.stream()
                .min(Comparator.comparingInt(i -> i))
                .orElse(null);
    }

    private class Disc {
        private final int numPositions;
        private final int firstZero;

        Disc(int numPositions, int curPosition) {
            this.numPositions = numPositions;
            this.firstZero = (numPositions - curPosition) % numPositions;
        }
    }
}
