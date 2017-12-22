package dhasday.adventofcode.dec2017.solvers2x;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import javafx.util.Pair;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day21Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/21-input";
    private static final String[] INITIAL_STATE = { ".#.", "..#", "###" };

    public static void main(String[] args) {
        new Dec2017Day21Solver().printResults();
    }

    @Override
    public int getDay() {
        return 21;
    }

    @Override
    public Integer solvePuzzleOne() {
        return solveForNumIterations(5);
    }

    @Override
    public Integer solvePuzzleTwo() {
        return solveForNumIterations(18);
    }

    private Integer solveForNumIterations(int num) {
        State input = new State(INITIAL_STATE[0].length(), loadValues(INITIAL_STATE));
        Translations translations = loadTranslations();

        for (int i = 0; i < num; i++) {
            input = enhanceImage(translations, input);
        }

        return input.values.size();
    }

    private Set<Pair<Integer, Integer>> loadValues(String[] input) {
        Set<Pair<Integer, Integer>> values = new HashSet<>();

        for (int i = 0; i < input.length; i++) {
            for (int j = 0; j < input[i].length(); j++) {
                if (input[i].charAt(j) == '#') {
                    values.add(new Pair<>(i, j));
                }
            }
        }

        return values;
    }

    private Translations loadTranslations() {
        Translations translations = new Translations(new HashMap<>(), new HashMap<>());

        for (String line : getAllFileLines(INPUT_FILE)) {
            String[] ioPair = line.split(" => ");

            int size = ioPair[0].split("/").length;
            Set<Pair<Integer, Integer>> inputValues = loadValues(ioPair[0].split("/"));

            Set<Set<Pair<Integer, Integer>>> allInputs = rotateAll(size, inputValues);
            allInputs.addAll(reflectAll(size, allInputs));

            Set<Pair<Integer, Integer>> outputValues = loadValues(ioPair[1].split("/"));
            allInputs.forEach(i -> {
                if (size == 2) {
                    translations.twoTranslations.put(i, outputValues);
                } else {
                    translations.threeTranslations.put(i, outputValues);
                }
            });
        }

        return translations;
    }

    private Set<Set<Pair<Integer, Integer>>> rotateAll(int totalSize, Set<Pair<Integer, Integer>> inputValues) {
        Set<Set<Pair<Integer, Integer>>> allRotations = new HashSet<>();
        allRotations.add(inputValues);

        Set<Pair<Integer, Integer>> rot90 = rotate(totalSize, inputValues);
        allRotations.add(rot90);

        Set<Pair<Integer, Integer>> rot180 = rotate(totalSize, rot90);
        allRotations.add(rot180);

        Set<Pair<Integer, Integer>> rot270 = rotate(totalSize, rot180);
        allRotations.add(rot270);

        return allRotations;
    }

    private Set<Pair<Integer, Integer>> rotate(int totalSize, Set<Pair<Integer, Integer>> inputValues) {
        return inputValues.stream()
                .map(p -> new Pair<>(p.getValue(), totalSize - 1 - p.getKey()))
                .collect(Collectors.toSet());
    }

    private Set<Set<Pair<Integer, Integer>>> reflectAll(int totalSize, Set<Set<Pair<Integer, Integer>>> allInputs) {
        Set<Set<Pair<Integer, Integer>>> xReflections = allInputs.stream()
                .map(v -> reflectX(totalSize, v))
                .collect(Collectors.toSet());

        Set<Set<Pair<Integer, Integer>>> yReflections = allInputs.stream()
                .map(v -> reflectY(totalSize, v))
                .collect(Collectors.toSet());

        Set<Set<Pair<Integer, Integer>>> allReflections = new HashSet<>();
        allReflections.addAll(xReflections);
        allReflections.addAll(yReflections);
        return allReflections;
    }

    private Set<Pair<Integer, Integer>> reflectX(int totalSize, Set<Pair<Integer, Integer>> inputValues) {
        return inputValues.stream()
                .map(p -> new Pair<>(totalSize - 1 - p.getKey(), p.getValue()))
                .collect(Collectors.toSet());
    }

    private Set<Pair<Integer, Integer>> reflectY(int totalSize, Set<Pair<Integer, Integer>> inputValues) {
        return inputValues.stream()
                .map(p -> new Pair<>(p.getKey(), totalSize - 1 - p.getValue()))
                .collect(Collectors.toSet());
    }

    private State enhanceImage(Translations translations, State input) {
        int processSize = input.size % 2 == 0 ? 2 : 3;

        int outputSize = input.size + (input.size / processSize); // 2 -> 3, 3 -> 4 is +1 per batch

        return processNextState(
                translations,
                outputSize,
                processSize,
                // Get a map of the unique value sets to all the start points of that set
                getUniqueValuePairs(input, processSize)
        );
    }

    private Map<Set<Pair<Integer, Integer>>, Set<Pair<Integer, Integer>>> getUniqueValuePairs(State input,
                                                                                              int processSize) {
        Map<Set<Pair<Integer, Integer>>, Set<Pair<Integer, Integer>>> uniqueValuesToLocations = new HashMap<>();

        for (int x = 0; x < input.size; x += processSize) {
            for (int y = 0; y < input.size; y += processSize) {
                Set<Pair<Integer, Integer>> sectionValues = getValuesInSection(input.values, x, y, processSize);

                uniqueValuesToLocations.computeIfAbsent(sectionValues, v -> new HashSet<>())
                        .add(new Pair<>(x, y));
            }
        }

        return uniqueValuesToLocations;
    }

    private Set<Pair<Integer, Integer>> getValuesInSection(Set<Pair<Integer, Integer>> allValues,
                                                           int startX,
                                                           int startY,
                                                           int processSize) {
        Set<Pair<Integer, Integer>> sectionValues = new HashSet<>();

        for (int x = startX; x < startX + processSize; x++) {
            for (int y = startY; y < startY + processSize; y++) {
                if (allValues.contains(new Pair<>(x, y))) {
                    sectionValues.add(new Pair<>(x - startX, y - startY));
                }
            }
        }

        return sectionValues;
    }

    private State processNextState(Translations translations,
                                   int outputSize,
                                   int processSize,
                                   Map<Set<Pair<Integer, Integer>>, Set<Pair<Integer, Integer>>> uniqueValuePairs) {
        State output = new State(outputSize, new HashSet<>());

        uniqueValuePairs.forEach((inputValues, pairs) -> {
            Set<Pair<Integer, Integer>> outputValues = translations.find(processSize, inputValues);

            pairs.forEach(ip -> {
                int offsetX = ip.getKey() + (ip.getKey() / processSize);
                int offsetY = ip.getValue() + (ip.getValue() / processSize);

                outputValues.forEach(op ->
                        output.values.add(new Pair<>(op.getKey() + offsetX, op.getValue() + offsetY))
                );
            });
        });

        return output;
    }

    private class State {
        private final int size;
        private final Set<Pair<Integer, Integer>> values;

        private State(int size, Set<Pair<Integer, Integer>> values) {
            this.size = size;
            this.values = values;
        }
    }

    private class Translations {
        private final Map<Set<Pair<Integer, Integer>>, Set<Pair<Integer, Integer>>> twoTranslations;
        private final Map<Set<Pair<Integer, Integer>>, Set<Pair<Integer, Integer>>> threeTranslations;

        private Translations(Map<Set<Pair<Integer, Integer>>, Set<Pair<Integer, Integer>>> twoTranslations,
                            Map<Set<Pair<Integer, Integer>>, Set<Pair<Integer, Integer>>> threeTranslations) {
            this.twoTranslations = twoTranslations;
            this.threeTranslations = threeTranslations;
        }

        private Set<Pair<Integer, Integer>> find(int processSize, Set<Pair<Integer, Integer>> values) {
            if (processSize == 2) {
                return twoTranslations.get(values);
            } else {
                return threeTranslations.get(values);
            }
        }
    }
}
