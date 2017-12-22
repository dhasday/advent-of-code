package dhasday.adventofcode.dec2017.solvers2x;

import java.util.*;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day21Solver extends Dec2017DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/21-input";
    private static final String[] INITIAL_STATE = { ".#.", "..#", "###" };

    @Override
    public int getDay() {
        return 21;
    }

    @Override
    public Long solvePuzzleOne() {
        return solveForNumIterations(5);
    }

    @Override
    public Long solvePuzzleTwo() {
        return solveForNumIterations(18);
    }

    private Long solveForNumIterations(int num) {
        List<String> input = Arrays.asList(INITIAL_STATE);
        Translations translations = loadTranslations();

        for (int i = 0; i < num; i++) {
            input = enhanceImage(translations, input);
        }

        return input.stream()
                .flatMapToInt(CharSequence::chars)
                .filter(c -> c == '#')
                .count();
    }

    private Translations loadTranslations() {
        Translations translations = new Translations(new HashMap<>(), new HashMap<>());

        for (String line : getAllFileLines(INPUT_FILE)) {
            String[] ioPair = line.split(" => ");

            int size = ioPair[0].split("/").length;
            List<String> inputValues = Arrays.asList(ioPair[0].split("/"));

            Set<List<String>> allInputs = rotateAll(inputValues);
            allInputs.addAll(reflectAll(allInputs));

            List<String> outputValues = Arrays.asList(ioPair[1].split("/"));
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

    private Set<List<String>> rotateAll(List<String> inputValues) {
        Set<List<String>> allRotations = new HashSet<>();
        allRotations.add(inputValues);

        List<String> rot90 = rotate(inputValues);
        allRotations.add(rot90);

        List<String> rot180 = rotate(rot90);
        allRotations.add(rot180);

        List<String> rot270 = rotate(rot180);
        allRotations.add(rot270);

        return allRotations;
    }

    private List<String> rotate(List<String> inputValues) {
        List<String> rotated = new ArrayList<>();

        for (int y = 0; y < inputValues.size(); y++) {
            StringBuilder sb = new StringBuilder();
            for (int x = inputValues.size() - 1; x >= 0; x--) {
                sb.append(inputValues.get(x).charAt(y));
            }
            rotated.add(sb.toString());
        }

        return rotated;
    }

    private Set<List<String>> reflectAll(Set<List<String>> allInputs) {
        Set<List<String>> xReflections = allInputs.stream()
                .map(this::reflectX)
                .collect(Collectors.toSet());

        Set<List<String>> yReflections = allInputs.stream()
                .map(this::reflectY)
                .collect(Collectors.toSet());

        Set<List<String>> allReflections = new HashSet<>();
        allReflections.addAll(xReflections);
        allReflections.addAll(yReflections);
        return allReflections;
    }

    private List<String> reflectX(List<String> inputValues) {
        List<String> reflected = new ArrayList<>();

        for (int i = inputValues.size() - 1; i >= 0; i--) {
            reflected.add(inputValues.get(i));
        }

        return reflected;
    }

    private List<String> reflectY(List<String> inputValues) {
        return inputValues.stream()
                .map(StringUtils::reverse)
                .collect(Collectors.toList());
    }

    private List<String> enhanceImage(Translations translations, List<String> input) {
        int size = input.size();

        int processSize = size % 2 == 0 ? 2 : 3;

        List<String> output = new ArrayList<>();

        for (int x = 0; x < size; x += processSize) {
            StringBuilder[] sb = new StringBuilder[processSize + 1];
            for (int i = 0; i < processSize + 1; i++) {
                sb[i] = new StringBuilder();
            }

            for (int y = 0; y < size; y += processSize) {
                List<String> enhanced = enhanceSection(translations, input, x, y, processSize);
                for (int i = 0; i < processSize + 1; i++) {
                    sb[i].append(enhanced.get(i));
                }
            }
            for (int i = 0; i < processSize + 1; i++) {
                output.add(sb[i].toString());
            }
        }

        return output;
    }

    private List<String> enhanceSection(Translations translations,
                                        List<String> input,
                                        int startX,
                                        int startY,
                                        int processSize) {
        List<String> section = new ArrayList<>();

        for (int x = startX; x < startX + processSize; x++) {
            section.add(input.get(x).substring(startY, startY + processSize));
        }

        return translations.find(processSize, section);
    }

    private class Translations {
        private final Map<List<String>, List<String>> twoTranslations;
        private final Map<List<String>, List<String>> threeTranslations;

        private Translations(Map<List<String>, List<String>> twoTranslations,
                             Map<List<String>, List<String>> threeTranslations) {
            this.twoTranslations = twoTranslations;
            this.threeTranslations = threeTranslations;
        }

        private List<String> find(int processSize, List<String> values) {
            if (processSize == 2) {
                return twoTranslations.get(values);
            } else {
                return threeTranslations.get(values);
            }
        }
    }
}
