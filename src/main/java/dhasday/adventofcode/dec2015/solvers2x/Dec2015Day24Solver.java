package dhasday.adventofcode.dec2015.solvers2x;

import java.util.Collection;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import com.google.common.collect.Lists;
import com.google.common.collect.Sets;
import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;

public class Dec2015Day24Solver implements DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/24-input";

    private static final int MAX_GROUP_SIZE = 6; // Based on input and 3 groups

    private static int sumGroup(Collection<Integer> group) {
        if (group == null) {
            return 0;
        }

        return group.stream().mapToInt(i -> i).sum();
    }

    @Override
    public int getDayNumber() {
        return 24;
    }

    @Override
    public Long solvePuzzleOne() {
        List<Integer> packageSizes = loadPackageSizes();

        Pair<Integer, Long> sizeEntanglementPair = determineMinEntanglement(packageSizes, 3);
        return sizeEntanglementPair.getValue();
    }

    @Override
    public Long solvePuzzleTwo() {
        List<Integer> packageSizes = loadPackageSizes();

        Pair<Integer, Long> sizeEntanglementPair = determineMinEntanglement(packageSizes, 4);

        return sizeEntanglementPair.getValue();
    }

    private List<Integer> loadPackageSizes() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(Integer::valueOf)
                .sorted(Comparator.reverseOrder())
                .collect(Collectors.toList());
    }

    Pair<Integer, Long> determineMinEntanglement(List<Integer> packageSizes, int numPackages) {
        int totalSum = sumGroup(packageSizes);
        int expectedGroupSize = totalSum / numPackages;

        Set<Set<Integer>> groups = findAllPossibleGroups(packageSizes, new HashSet<>(), expectedGroupSize, MAX_GROUP_SIZE);

        return findEntanglementForSmallestGroup(groups);
    }

    private Set<Set<Integer>> findAllPossibleGroups(List<Integer> remainingPackages,
                                                    Set<Integer> currentPackages,
                                                    int remainingSum,
                                                    int maxSize) {
        if (remainingSum == 0) {
            Set<Set<Integer>> validGroups = new HashSet<>();
            validGroups.add(currentPackages);
            return validGroups;
        }
        if (remainingSum < 0
                || remainingPackages.isEmpty()
                || currentPackages.size() >= maxSize) {
            return new HashSet<>();
        }

        Set<Set<Integer>> allGroups = new HashSet<>();
        List<Integer> newRemainingPackages = Lists.newArrayList(remainingPackages);
        for (Integer value : remainingPackages) {
            newRemainingPackages.remove(value);

            Set<Integer> newCurrentPackages = Sets.newHashSet(currentPackages);
            newCurrentPackages.add(value);

            allGroups.addAll(findAllPossibleGroups(newRemainingPackages, newCurrentPackages, remainingSum - value, maxSize));
        }
        return allGroups;
    }

    private Pair<Integer, Long> findEntanglementForSmallestGroup(Set<Set<Integer>> groups) {
        Integer currentMinSize = null;
        Long currentEntanglement = null;

        for (Set<Integer> group : groups) {
            int groupSize = group.size();
            long entanglement = 1;

            for (Integer value : group) {
                entanglement = entanglement * value;
            }

            if (currentMinSize == null || currentMinSize > groupSize) {
                currentMinSize = groupSize;
                currentEntanglement = entanglement;
            } else if (currentMinSize == groupSize) {
                currentEntanglement = Math.min(entanglement, currentEntanglement);
            }
        }

        return new Pair(currentMinSize, currentEntanglement);
    }
}
