package dhasday.adventofcode.dec2016.solvers1x;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import com.google.common.collect.Lists;
import com.google.common.collect.Sets;
import dhasday.adventofcode.DaySolver;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

public class Dec2016Day11Solver implements DaySolver<Integer> {

    private static final Boolean HARD_FAIL = true;

    @Override
    public int getDayNumber() {
        return 11;
    }

    public Integer solveExample() {
        State initialState = new State(
                0,
                Lists.newArrayList(
                        Sets.newHashSet(),
                        Sets.newHashSet(Element.A),
                        Sets.newHashSet(Element.B),
                        Sets.newHashSet()
                ),
                Lists.newArrayList(
                        Sets.newHashSet(Element.A, Element.B),
                        Sets.newHashSet(),
                        Sets.newHashSet(),
                        Sets.newHashSet()
                )
        );

        return findShortestPath(initialState, 15);
    }

    @Override
    public Integer solvePuzzleOne() {
        //        generators    microchips  elevator
        //    1 - A,D,E         E           *
        //    2 -               A,D
        //    3 - B,C           B,C
        //    4 -

        if (HARD_FAIL) {
            throw new RuntimeException("Fix your implementation");
        }
        State initialState = new State(
                0,
                Lists.newArrayList(
                        Sets.newHashSet(Element.A, Element.D, Element.E),
                        Sets.newHashSet(),
                        Sets.newHashSet(Element.B, Element.C),
                        Sets.newHashSet()
                ),
                Lists.newArrayList(
                        Sets.newHashSet(Element.E),
                        Sets.newHashSet(Element.A, Element.D),
                        Sets.newHashSet(Element.B, Element.C),
                        Sets.newHashSet()
                )
        );

        return findShortestPath(initialState, 35);
    }

    @Override
    public Integer solvePuzzleTwo() {
        //        generators    microchips  elevator
        //    1 - A,D,E,F,G     E,F,G       *
        //    2 -               A,D
        //    3 - B,C           B,C
        //    4 -

        if (HARD_FAIL) {
            throw new RuntimeException("Fix your implementation");
        }
        State initialState = new State(
                0,
                Lists.newArrayList(
                        Sets.newHashSet(Element.A, Element.D, Element.E, Element.F, Element.G),
                        Sets.newHashSet(),
                        Sets.newHashSet(Element.B, Element.C),
                        Sets.newHashSet()
                ),
                Lists.newArrayList(
                        Sets.newHashSet(Element.E, Element.F, Element.G),
                        Sets.newHashSet(Element.A, Element.D),
                        Sets.newHashSet(Element.B, Element.C),
                        Sets.newHashSet()
                )
        );

        return findShortestPath(initialState, 60);
    }

    private Integer findShortestPath(State currentState, int maxMoves) {
        return findShortestPath(new HashSet<>(), currentState, 0, maxMoves);
    }

    private Integer findShortestPath(Set<State> visitedStates, State currentState, int curMoves, int remainingMoves) {
        if (isEndState(currentState)) {
            return curMoves;
        }
        if (remainingMoves <= 0 || wasVisited(visitedStates, currentState)) {
            return null;
        }

        Set<State> newVisitedStates = Sets.newHashSet(visitedStates);
        newVisitedStates.add(currentState);

        Integer minMoves = null;
        for (State nextState : findValidNextStates(currentState)) {
            int newRemainingMoves;
            if (minMoves != null) {
                newRemainingMoves = minMoves - curMoves - 1;
            } else {
                newRemainingMoves = remainingMoves - 1;
            }
            Integer possibleMin = findShortestPath(newVisitedStates, nextState, curMoves + 1, newRemainingMoves);

            if (possibleMin != null) {
                if (minMoves == null) {
                    minMoves = possibleMin;
                } else {
                    minMoves = Math.min(minMoves, possibleMin);
                }
            }
        }

        return minMoves;
    }

    private boolean isEndState(State state) {
        return state.elevatorFloor == 3
                && state.generators.stream().limit(state.generators.size() - 1).allMatch(Set::isEmpty)
                && state.microchips.stream().limit(state.microchips.size() - 1).allMatch(Set::isEmpty);
    }

    private boolean wasVisited(Set<State> visitedStates, State state) {
        return visitedStates.contains(state) // Exact match
                || visitedStates.stream().anyMatch(visitedState -> areStatesEquivalent(visitedState, state));

    }

    private boolean areStatesEquivalent(State stateOne, State stateTwo) {
        if (stateOne.elevatorFloor != stateTwo.elevatorFloor) {
            return false;
        }

        for (int i = 0; i < stateOne.generators.size(); i++) {
            if (stateOne.generators.get(i).size() != stateTwo.generators.get(i).size()) {
                return false;
            }
            if (stateOne.microchips.get(i).size() != stateTwo.microchips.get(i).size()) {
                return false;
            }
        }

        return true;
    }

    private Set<State> findValidNextStates(State currentState) {
        Set<State> nextStates = getAllNextStates(currentState, 1);
        nextStates.addAll(getAllNextStates(currentState, -1));

        return nextStates.stream()
                .filter(this::isValidState)
                .collect(Collectors.toSet());
    }

    private Set<State> getAllNextStates(State currentState, int floorOffset) {
        int currentFloor = currentState.elevatorFloor;
        int nextFloor = currentFloor + floorOffset;

        if (nextFloor < 0 || nextFloor >= currentState.generators.size()) {
            return new HashSet<>();
        }

        Set<Element> curGenerators = currentState.generators.get(currentFloor);
        Set<Element> curMicrochips = currentState.microchips.get(currentFloor);

        Set<State> allNextStates = new HashSet<>();
        for (Element genOne : curGenerators) {
            State nextStateOne = new State(currentState, nextFloor);
            nextStateOne.generators.get(currentFloor).remove(genOne);
            nextStateOne.generators.get(nextFloor).add(genOne);
            allNextStates.add(nextStateOne);

            for (Element genTwo : curGenerators) {
                State nextStateTwo = new State(currentState, nextFloor);
                nextStateTwo.generators.get(currentFloor).remove(genOne);
                nextStateTwo.generators.get(currentFloor).remove(genTwo);
                nextStateTwo.generators.get(nextFloor).add(genOne);
                nextStateTwo.generators.get(nextFloor).add(genTwo);
                allNextStates.add(nextStateTwo);
            }

            for (Element chipOne : curMicrochips) {
                State nextStateThree = new State(currentState, nextFloor);
                nextStateThree.generators.get(currentFloor).remove(genOne);
                nextStateThree.microchips.get(currentFloor).remove(chipOne);
                nextStateThree.generators.get(nextFloor).add(genOne);
                nextStateThree.microchips.get(nextFloor).add(chipOne);
                allNextStates.add(nextStateThree);
            }
        }

        for (Element chipOne : curMicrochips) {
            State nextStateFour = new State(currentState, nextFloor);
            nextStateFour.microchips.get(currentFloor).remove(chipOne);
            nextStateFour.microchips.get(nextFloor).add(chipOne);
            allNextStates.add(nextStateFour);

            for (Element chipTwo : curMicrochips) {
                State nextStateFive = new State(currentState, nextFloor);
                nextStateFive.microchips.get(currentFloor).remove(chipOne);
                nextStateFive.microchips.get(currentFloor).remove(chipTwo);
                nextStateFive.microchips.get(nextFloor).add(chipOne);
                nextStateFive.microchips.get(nextFloor).add(chipTwo);
                allNextStates.add(nextStateFive);
            }
        }

        return allNextStates;
    }

    private boolean isValidState(State state) {
        for (int i = 0; i < state.generators.size(); i++) {
            Set<Element> generators = state.generators.get(i);
            Set<Element> microchips = state.microchips.get(i);

            if (!generators.isEmpty() && microchips.stream().anyMatch(chip -> !generators.contains(chip))) {
                return false;
            }
        }
        return true;
    }

    private class State {
        private final int elevatorFloor;

        private final List<Set<Element>> generators;
        private final List<Set<Element>> microchips;

        State(int elevatorFloor, List<Set<Element>> generators, List<Set<Element>> microchips) {
            this.elevatorFloor = elevatorFloor;
            this.generators = generators;
            this.microchips = microchips;
        }

        State(State other, int elevatorFloor) {
            this.elevatorFloor = elevatorFloor;
            this.generators = other.generators.stream().map(Sets::newHashSet).collect(Collectors.toList());
            this.microchips = other.microchips.stream().map(Sets::newHashSet).collect(Collectors.toList());
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

    private enum Element {
        A, B, C, D, E, F, G
    }

}
