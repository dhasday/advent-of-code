package dhasday.adventofcode.dec2015.solvers1x;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import com.google.common.collect.Sets;
import dhasday.adventofcode.dec2015.Dec2015DaySolver;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

public class Dec2015Day17Solver extends Dec2015DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/17-input";

    @Override
    public int getDay() {
        return 17;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Integer> containerSizes = loadContainerSizes();

        return getSolutionCount(containerSizes, 150);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Integer> containerSizes = loadContainerSizes();

        return getMinimumContainerOptions(containerSizes, 150);
    }

    private List<Integer> loadContainerSizes() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(Integer::valueOf)
                .collect(Collectors.toList());
    }

    Integer getSolutionCount(List<Integer> containers, int numLiters) {
        Set<Container> allContainers = new HashSet<>();
        for (int i = 0; i < containers.size(); i++) {
            allContainers.add(new Container(i, containers.get(i)));
        }

        return getUniqueSolutions(allContainers, new HashSet<>(), numLiters).size();
    }

    Integer getMinimumContainerOptions(List<Integer> containers, int numLiters) {
        Set<Container> allContainers = new HashSet<>();
        for (int i = 0; i < containers.size(); i++) {
            allContainers.add(new Container(i, containers.get(i)));
        }

        Set<Set<Container>> uniqueSolutions = getUniqueSolutions(allContainers, new HashSet<>(), numLiters);

        Integer minContainers = null;
        Integer numOptions = 0;

        for (Set<Container> validSolution : uniqueSolutions) {
            int numContainers = validSolution.size();

            if (minContainers == null || minContainers > numContainers) {
                minContainers = numContainers;
                numOptions = 1;
            } else if (minContainers == numContainers) {
                numOptions++;
            }
        }

        return numOptions;
    }

    private Set<Set<Container>> getUniqueSolutions(Set<Container> allContainers, Set<Container> containersUsed, Integer numLiters) {
        if (numLiters < 0) {
            return new HashSet<>();
        }

        if (numLiters == 0) {
            Set<Set<Container>> validSolutions = new HashSet<>();
            validSolutions.add(containersUsed);
            return validSolutions;
        }

        if (allContainers.isEmpty() && numLiters > 0) {
            return new HashSet<>();
        }

        Set<Set<Container>> validSolutions = new HashSet<>();

        Set<Container> testedContainers = new HashSet<>();

        for (Container container : allContainers) {
            Set<Container> usedContainers = Sets.newHashSet(containersUsed);
            usedContainers.add(container);

            int remainingLiters = numLiters - container.size;
            if (remainingLiters == 0) {
                validSolutions.add(usedContainers);
            }

            if (remainingLiters > 0) {
                Set<Container> remainingContainers = Sets.newHashSet(allContainers);
                remainingContainers.remove(container);
                remainingContainers.removeAll(testedContainers);

                validSolutions.addAll(getUniqueSolutions(remainingContainers, usedContainers, remainingLiters));
            }
            testedContainers.add(container);
        }

        return validSolutions;
    }

    private class Container {
        private final int index;
        private final Integer size;

        Container(int index, Integer size) {
            this.index = index;
            this.size = size;
        }

        @Override
        public boolean equals(Object o) {
            return EqualsBuilder.reflectionEquals(this, o);
        }

        @Override
        public int hashCode() {
            return HashCodeBuilder.reflectionHashCode(this);
        }

        @Override
        public String toString() {
            return ToStringBuilder.reflectionToString(this, ToStringStyle.SHORT_PREFIX_STYLE);
        }
    }
}
