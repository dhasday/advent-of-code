package dhasday.adventofcode.dec2015.solvers1x;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Sets;
import dhasday.adventofcode.DaySolver;

public class Dec2015Day16Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/16-input";

    private static final String INPUT_REGEX = "Sue ([\\d]+): ([a-z]+): (-?\\d+), ([a-z]+): (-?\\d+), ([a-z]+): (-?\\d+)";

    private static final Set<String> EQUAL_OR_HIGHER_ATTRIBUTES = Sets.newHashSet("cats", "trees");
    private static final Set<String> EQUAL_OR_LOWER_ATTRIBUTES = Sets.newHashSet("pomeranians", "goldfish");

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);

    @Override
    public int getDayNumber() {
        return 16;
    }

    @Override
    public Integer solvePuzzleOne() {
        Map<String, Integer> mfcsamResults = ImmutableMap.<String, Integer>builder()
                .put("children", 3)
                .put("cats", 7)
                .put("samoyeds", 2)
                .put("pomeranians", 3)
                .put("akitas", 0)
                .put("vizslas", 0)
                .put("goldfish", 5)
                .put("trees", 3)
                .put("cars", 2)
                .put("perfumes", 1)
                .build();

        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Aunt> allAunts = allFileLines.stream()
                .map(this::loadAunt)
                .collect(Collectors.toList());

        Aunt matchingAunt = findExactMatchingAunt(mfcsamResults, allAunts);

        return matchingAunt.number;
    }

    @Override
    public Integer solvePuzzleTwo() {
        Map<String, Integer> mfcsamResults = ImmutableMap.<String, Integer>builder()
                .put("children", 3)
                .put("cats", 7)
                .put("samoyeds", 2)
                .put("pomeranians", 3)
                .put("akitas", 0)
                .put("vizslas", 0)
                .put("goldfish", 5)
                .put("trees", 3)
                .put("cars", 2)
                .put("perfumes", 1)
                .build();

        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Aunt> allAunts = allFileLines.stream()
                .map(this::loadAunt)
                .collect(Collectors.toList());

        Aunt matchingAunt = findFuzzyMatchingAunt(mfcsamResults, allAunts);

        return matchingAunt.number;
    }

    private Aunt loadAunt(String input) {
        Matcher matcher = inputPattern.matcher(input);

        if (!matcher.matches()) {
            throw new RuntimeException("Unable to extract data from input: " + input);
        }

        return new Aunt(
                Integer.valueOf(matcher.group(1)),
                ImmutableMap.of(
                        matcher.group(2), Integer.valueOf(matcher.group(3)),
                        matcher.group(4), Integer.valueOf(matcher.group(5)),
                        matcher.group(6), Integer.valueOf(matcher.group(7))
                )
        );
    }

    private Aunt findExactMatchingAunt(Map<String, Integer> testResults, List<Aunt> allAunts) {
        return allAunts.stream()
                .filter(aunt -> doesAuntMatchExact(testResults, aunt))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("No matching aunt found."));
    }

    private boolean doesAuntMatchExact(Map<String, Integer> testResults, Aunt aunt) {
        return aunt.attributes.entrySet()
                .stream()
                .allMatch(entry -> entry.getValue().equals(testResults.get(entry.getKey())));
    }

    private Aunt findFuzzyMatchingAunt(Map<String, Integer> testResults, List<Aunt> allAunts) {
        return allAunts.stream()
                .filter(aunt -> doesAuntMatchFuzzy(testResults, aunt))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("No matching aunt found."));
    }

    private boolean doesAuntMatchFuzzy(Map<String, Integer> testResults, Aunt aunt) {
        return aunt.attributes.entrySet()
                .stream()
                .allMatch(entry -> {
                    Integer actual = entry.getValue();
                    Integer expected = testResults.get(entry.getKey());

                    if (EQUAL_OR_HIGHER_ATTRIBUTES.contains(entry.getKey())) {
                        return expected < actual;
                    }

                    if (EQUAL_OR_LOWER_ATTRIBUTES.contains(entry.getKey())) {
                        return expected > actual;
                    }

                    return expected.equals(actual);
                });
    }

    private class Aunt {
        private Integer number;
        private Map<String, Integer> attributes;

        public Aunt(Integer number, Map<String, Integer> attributes) {
            this.number = number;
            this.attributes = attributes;
        }
    }
}
