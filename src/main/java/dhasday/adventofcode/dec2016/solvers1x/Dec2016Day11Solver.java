package dhasday.adventofcode.dec2016.solvers1x;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collectors;

import com.google.common.collect.Lists;
import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.common.AStarSearch;
import javafx.util.Pair;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;

public class Dec2016Day11Solver extends DaySolver<Integer> {
//        Part One
//        The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
//        The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
//        The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
//        The fourth floor contains nothing relevant.

//        Part Two
//        The first floor also contains:
//            * An elerium generator.
//            * An elerium-compatible microchip.
//            * A dilithium generator.
//            * A dilithium-compatible microchip.

    private AStarSearch aStarSearch = new AStarSearch();

    @Override
    public int getDayNumber() {
        return 11;
    }

    @Override
    public Integer solvePuzzleOne() {
        State initialState = new State();
        initialState.initialize(Lists.newArrayList(
                new Pair<>(1,2), // PLUTONIUM
                new Pair<>(3,3), // PROMETHIUM
                new Pair<>(3,3), // RUTHENIUM
                new Pair<>(1,2), // STRONTIUM
                new Pair<>(1,1)  // THULIUM
        ));

        List<State> shortestPath = aStarSearch.findShortestPath(
                initialState,
                determineFinalState(initialState),
                getCostEstimator(),
                getAdjacentNodeFinder()
        );

        // return 31;
        return shortestPath == null ? null : shortestPath.size() - 1;
    }

    @Override
    public Integer solvePuzzleTwo() {
        State initialState = new State();
        initialState.initialize(Lists.newArrayList(
                new Pair<>(1,2), // PLUTONIUM
                new Pair<>(3,3), // PROMETHIUM
                new Pair<>(3,3), // RUTHENIUM
                new Pair<>(1,2), // STRONTIUM
                new Pair<>(1,1), // THULIUM
                new Pair<>(1,1), // ELERIUM
                new Pair<>(1,1)  // DILITHIUM
        ));


        List<State> shortestPath = aStarSearch.findShortestPath(
                initialState,
                determineFinalState(initialState),
                getCostEstimator(),
                getAdjacentNodeFinder()
        );

        // return 55;
        return shortestPath == null ? null : shortestPath.size() - 1;
    }

    private State determineFinalState(State initialState) {
        State finalState = new State();
        finalState.elevatorFloor = 4;

        finalState.initialize(
                initialState.sortedGenChipLocations.stream()
                        .map(p -> new Pair<>(4, 4))
                        .collect(Collectors.toList())
        );

        return finalState;
    }

    private BiFunction<State, State, Integer> getCostEstimator() {
        return (s1, s2) -> {
            int distance = (4 - s1.elevatorFloor) * 10;

            for (Pair<Integer, Integer> pair : s1.sortedGenChipLocations) {
                if (pair.getKey() < 4) {
                    distance += ((4 - pair.getKey()) * 10);
                }
                if (pair.getValue() < 4) {
                    distance += ((4 - pair.getValue()) * 10);
                }
            }

            return distance;
        };
    }

    private Function<State, Set<Pair<State, Integer>>> getAdjacentNodeFinder() {
        return (state) -> {
            List<Pair<Integer, Boolean>> movablePairs = findMovablePairs(state);

            Set<Pair<State, Integer>> adjacentNodesWithDistance = new HashSet<>();

            getValidNextStatesSingleMove(state, state.elevatorFloor + 1, movablePairs)
                    .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 1)));
            getValidNextStatesDoubleMove(state, state.elevatorFloor + 1, movablePairs)
                    .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 1)));

            if (!areLowerFloorsEmpty(state)) {
                getValidNextStatesSingleMove(state, state.elevatorFloor - 1, movablePairs)
                        .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 1)));
                getValidNextStatesDoubleMove(state, state.elevatorFloor - 1, movablePairs)
                        .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 1)));
            }

            return adjacentNodesWithDistance;
        };
    }

    private Set<State> getValidNextStatesSingleMove(State currentState,
                                                    int nextFloor,
                                                    List<Pair<Integer, Boolean>> movablePairs) {
        if (nextFloor > 4 || nextFloor < 1) {
            return new HashSet<>();
        }

        return movablePairs.stream()
                .map(pair -> getNextState(currentState, nextFloor, pair))
                .filter(this::isValidState)
                .collect(Collectors.toSet());
    }

    private Set<State> getValidNextStatesDoubleMove(State currentState,
                                                    int nextFloor,
                                                    List<Pair<Integer, Boolean>> movablePairs) {
        if (nextFloor > 4 || nextFloor < 1) {
            return new HashSet<>();
        }

        Set<State> validNextStates = new HashSet<>();
        for (Pair<Integer, Boolean> pairOne : movablePairs) {
            for (Pair<Integer, Boolean> pairTwo : movablePairs) {
                if (pairOne == pairTwo) {
                    continue;
                }

                State possibleNextState = getNextState(currentState, nextFloor, pairOne, pairTwo);
                if (isValidState(possibleNextState)) {
                    validNextStates.add(possibleNextState);
                }
            }
        }
        return validNextStates;
    }

    private List<Pair<Integer, Boolean>> findMovablePairs(State currentState) {
        List<Pair<Integer, Boolean>> movablePairs = new ArrayList<>(); // Element to gen / chip

        int curFloor = currentState.elevatorFloor;
        for (int i = 0; i < currentState.sortedGenChipLocations.size(); i++) {
            Pair<Integer, Integer> itemLocations = currentState.sortedGenChipLocations.get(i);

            if (curFloor == itemLocations.getKey()) {
                movablePairs.add(new Pair<>(i, true));
            }
            if (curFloor == itemLocations.getValue()) {
                movablePairs.add(new Pair<>(i, false));
            }
        }

        return movablePairs;
    }

    private State getNextState(State currentState, int nextFloor, Pair<Integer, Boolean>... items) {
        State newState = new State(currentState);
        newState.elevatorFloor = nextFloor;

        for (Pair<Integer, Boolean> item : items) {
            Pair<Integer, Integer> curItemState = newState.sortedGenChipLocations.get(item.getKey());

            Pair<Integer, Integer> newItemState;
            if (item.getValue()) {
                newItemState = new Pair<>(nextFloor, curItemState.getValue());
            } else {
                newItemState = new Pair<>(curItemState.getKey(), nextFloor);
            }
            newState.updatePair(item.getKey(), newItemState);
        }

        return newState;
    }

    private boolean isValidState(State state) {
        if (state.elevatorFloor > 4 || state.elevatorFloor < 1) {
            return false;
        }

        boolean[] hasUnmatchedChip = new boolean[4];
        boolean[] hasGenerator = new boolean[4];

        for (Pair<Integer, Integer> pair : state.sortedGenChipLocations) {
            Integer genIndex = pair.getKey() - 1;
            Integer chipIndex = pair.getValue() - 1;

            if (genIndex < 0 || genIndex > 3 || chipIndex < 0 || chipIndex > 3) {
                return false;
            }

            hasUnmatchedChip[chipIndex] = hasUnmatchedChip[chipIndex] || !chipIndex.equals(genIndex);
            hasGenerator[genIndex] = true;
        }

        for (int i = 0; i < 4; i++) {
            if (hasUnmatchedChip[i] && hasGenerator[i]) {
                return false;
            }
        }

        return true;
    }

    private boolean areLowerFloorsEmpty(State state) {
        int floor = state.elevatorFloor;

        for (Pair<Integer, Integer> pair : state.sortedGenChipLocations) {
            if (pair.getKey() < floor || pair.getValue() < floor) {
                return false;
            }
        }

        return true;
    }

    private class State {
        private int elevatorFloor;
        private List<Pair<Integer, Integer>> sortedGenChipLocations;

        State() {
            this.elevatorFloor = 1;
            this.sortedGenChipLocations = new ArrayList<>();
        }

        State(State other) {
            this.elevatorFloor = other.elevatorFloor;
            this.sortedGenChipLocations = Lists.newArrayList(other.sortedGenChipLocations);
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
            return elevatorFloor + "-" + sortedGenChipLocations;
        }

        private void updatePair(int index, Pair<Integer, Integer> genChipPair) {
            sortedGenChipLocations.remove(index);
            sortedGenChipLocations.add(genChipPair);

            sortLocations();
        }

        public void initialize(Pair<Integer, Integer>... genChipPairs) {
            initialize(Arrays.asList(genChipPairs));
        }

        public void initialize(List<Pair<Integer, Integer>> genChipPairs) {
            sortedGenChipLocations.addAll(genChipPairs);

            sortLocations();
        }

        private void sortLocations() {
            sortedGenChipLocations.sort((p1, p2) -> {
                if (!p1.getKey().equals(p2.getKey())) {
                    return Integer.compare(p1.getKey(), p2.getKey());
                }
                return Integer.compare(p1.getValue(), p2.getValue());
            });
        }
    }
}