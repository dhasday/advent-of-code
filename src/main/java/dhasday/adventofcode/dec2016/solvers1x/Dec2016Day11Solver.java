package dhasday.adventofcode.dec2016.solvers1x;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.stream.Collectors;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.common.AStarSearch;
import javafx.util.Pair;
import org.apache.commons.lang3.builder.EqualsBuilder;
import org.apache.commons.lang3.builder.HashCodeBuilder;

public class Dec2016Day11Solver implements DaySolver<Integer> {
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

    private AStarSearch<State> aStarSearch = new AStarSearch<>();

    @Override
    public int getDayNumber() {
        return 11;
    }

    @Override
    public Integer solvePuzzleOne() {
        State initialState = new State();
        initialState.genChipLocations.put(Element.PLUTONIUM, new Pair<>(1,2));
        initialState.genChipLocations.put(Element.PROMETHIUM, new Pair<>(3,3));
        initialState.genChipLocations.put(Element.RUTHENIUM, new Pair<>(3,3));
        initialState.genChipLocations.put(Element.STRONTIUM, new Pair<>(1,2));
        initialState.genChipLocations.put(Element.THULIUM, new Pair<>(1,1));

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
        initialState.genChipLocations.put(Element.PLUTONIUM, new Pair<>(1,2));
        initialState.genChipLocations.put(Element.PROMETHIUM, new Pair<>(3,3));
        initialState.genChipLocations.put(Element.RUTHENIUM, new Pair<>(3,3));
        initialState.genChipLocations.put(Element.STRONTIUM, new Pair<>(1,2));
        initialState.genChipLocations.put(Element.THULIUM, new Pair<>(1,1));
        initialState.genChipLocations.put(Element.ELERIUM, new Pair<>(1,1));
        initialState.genChipLocations.put(Element.DILITHIUM, new Pair<>(1,1));

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

        for (Element element : initialState.genChipLocations.keySet()) {
            finalState.genChipLocations.put(element, new Pair<>(4,4));
        }

        return finalState;
    }

    private BiFunction<State, State, Integer> getCostEstimator() {
        return (s1, s2) -> {
            int distance = 4 - s1.elevatorFloor;

            for (Pair<Integer, Integer> pair : s1.genChipLocations.values()) {
                if (pair.getKey() < 4) {
                    distance += (4 - pair.getKey() ^ 2);
                }
                if (pair.getValue() < 4) {
                    distance += (4 - pair.getValue() ^ 2);
                }
            }

            return distance;
        };
    }

    private Function<State, Set<Pair<State, Integer>>> getAdjacentNodeFinder() {
        return (state) -> {
            List<Pair<Element, Boolean>> movablePairs = findMovablePairs(state);

            Set<Pair<State, Integer>> adjacentNodesWithDistance = new HashSet<>();

            getValidNextStatesSingleMove(state, state.elevatorFloor + 1, movablePairs)
                    .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 2)));
            getValidNextStatesDoubleMove(state, state.elevatorFloor + 1, movablePairs)
                    .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 1)));

            if (!areLowerFloorsEmpty(state)) {
                getValidNextStatesSingleMove(state, state.elevatorFloor - 1, movablePairs)
                        .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 1)));
                getValidNextStatesDoubleMove(state, state.elevatorFloor - 1, movablePairs)
                        .forEach(s -> adjacentNodesWithDistance.add(new Pair<>(s, 2)));
            }

            return adjacentNodesWithDistance;
        };
    }

    private Set<State> getValidNextStatesSingleMove(State currentState,
                                                    int nextFloor,
                                                    List<Pair<Element, Boolean>> movablePairs) {
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
                                                    List<Pair<Element, Boolean>> movablePairs) {
        if (nextFloor > 4 || nextFloor < 1) {
            return new HashSet<>();
        }

        Set<State> validNextStates = new HashSet<>();
        for (Pair<Element, Boolean> pairOne : movablePairs) {
            for (Pair<Element, Boolean> pairTwo : movablePairs) {
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

    private List<Pair<Element, Boolean>> findMovablePairs(State currentState) {
        List<Pair<Element, Boolean>> movablePairs = new ArrayList<>(); // Element to gen / chip

        int curFloor = currentState.elevatorFloor;
        for (Map.Entry<Element, Pair<Integer, Integer>> entry : currentState.genChipLocations.entrySet()) {
            Element element = entry.getKey();

            Pair<Integer, Integer> itemLocations = entry.getValue();

            if (curFloor == itemLocations.getKey()) {
                movablePairs.add(new Pair<>(element, true));
            }
            if (curFloor == itemLocations.getValue()) {
                movablePairs.add(new Pair<>(element, false));
            }
        }

        return movablePairs;
    }

    private State getNextState(State currentState, int nextFloor, Pair<Element, Boolean>... items) {
        State newState = new State(currentState);
        newState.elevatorFloor = nextFloor;

        for (Pair<Element, Boolean> item : items) {
            Pair<Integer, Integer> curItemState = newState.genChipLocations.get(item.getKey());

            Pair<Integer, Integer> newItemState;
            if (item.getValue()) {
                newItemState = new Pair<>(nextFloor, curItemState.getValue());
            } else {
                newItemState = new Pair<>(curItemState.getKey(), nextFloor);
            }
            newState.genChipLocations.put(item.getKey(), newItemState);
        }

        return newState;
    }

    private boolean isValidState(State state) {
        if (state.elevatorFloor > 4 || state.elevatorFloor < 1) {
            return false;
        }

        boolean[] hasUnmatchedChip = new boolean[4];
        boolean[] hasGenerator = new boolean[4];

        for (Pair<Integer, Integer> pair : state.genChipLocations.values()) {
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

        for (Pair<Integer, Integer> pair : state.genChipLocations.values()) {
            if (pair.getKey() < floor || pair.getValue() < floor) {
                return false;
            }
        }

        return true;
    }

    private class State {
        private int elevatorFloor;
        private Map<Element, Pair<Integer, Integer>> genChipLocations;

        State() {
            this.elevatorFloor = 1;
            this.genChipLocations = new HashMap<>();
        }

        State(State other) {
            this.elevatorFloor = other.elevatorFloor;

            this.genChipLocations = new HashMap<>();
            for (Map.Entry<Element, Pair<Integer, Integer>> entry : other.genChipLocations.entrySet()) {
                Pair<Integer, Integer> otherPair = entry.getValue();
                genChipLocations.put(entry.getKey(), new Pair<>(otherPair.getKey(), otherPair.getValue()));
            }
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
            return elevatorFloor + "-" + genChipLocations;
        }
    }

    private enum Element {
        ELERIUM,
        DILITHIUM,
        HYDROGEN,
        LITHIUM,
        PLUTONIUM,
        PROMETHIUM,
        RUTHENIUM,
        STRONTIUM,
        THULIUM;
    }
}