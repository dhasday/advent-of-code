package dhasday.adventofcode.dec2016.solvers0x;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;
import org.apache.commons.lang3.StringUtils;

public class Dec2016Day7Solver extends DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/7-input";

    @Override
    public int getDayNumber() {
        return 7;
    }

    @Override
    public Long solvePuzzleOne() {
        List<String> allMessages = getAllFileLines(INPUT_FILE);

        return allMessages.stream()
                .filter(this::supportsTLS)
                .count();
    }

    @Override
    public Long solvePuzzleTwo() {
        List<String> allMessages = getAllFileLines(INPUT_FILE);

        return allMessages.stream()
                .filter(this::supportsSSL)
                .count();
    }

    private boolean supportsTLS(String input) {
        boolean hasAbbaOutsideBrackets = Arrays.stream(input.split("\\[[a-z]*]")).anyMatch(this::fragmentSupportsTLS);
        boolean hasAbbaInsideBrackets = Arrays.stream(input.split("[a-z]*\\["))
                .filter(StringUtils::isNotBlank)
                .map(value -> value.substring(0, value.lastIndexOf("]")))
                .anyMatch(this::fragmentSupportsTLS);

        return hasAbbaOutsideBrackets && !hasAbbaInsideBrackets;
    }

    private boolean fragmentSupportsTLS(String fragment) {
        if (fragment.length() < 4) {
            return false;
        }

        for (int i = 3; i < fragment.length(); i++) {
            char charOne = fragment.charAt(i - 3);
            char charTwo = fragment.charAt(i - 2);
            char charThree = fragment.charAt(i - 1);
            char charFour = fragment.charAt(i);

            if (charOne == charFour && charTwo == charThree && charOne != charTwo) {
                return true;
            }
        }

        return false;
    }

    private boolean supportsSSL(String input) {
        Set<Pair<Character, Character>> allABAPairs = new HashSet<>();
        for (String fragment : input.split("\\[[a-z]*]")) {
            allABAPairs.addAll(findAllABAPairs(fragment));
        }

        List<String> supernetFragments = Arrays.stream(input.split("[a-z]*\\["))
                .filter(StringUtils::isNotBlank)
                .map(value -> value.substring(0, value.lastIndexOf("]")))
                .collect(Collectors.toList());
        Set<Pair<Character, Character>> allBABPairs = new HashSet<>();
        for (String fragment : supernetFragments) {
            allBABPairs.addAll(findAllBABPairs(fragment));
        }

        for (Pair<Character, Character> abaPair : allABAPairs) {
            if (allBABPairs.contains(abaPair)) {
                return true;
            }
        }
        return false;
    }

    private Set<Pair<Character, Character>> findAllABAPairs(String fragment) {
        if (fragment.length() < 3) {
            return new HashSet<>();
        }
        
        Set<Pair<Character, Character>> allPairs = new HashSet<>();
        for (int i = 2; i < fragment.length(); i++) {
            char charOne = fragment.charAt(i - 2);
            char charTwo = fragment.charAt(i - 1);
            char charThree = fragment.charAt(i);

            if (charOne == charThree && charOne != charTwo) {
                allPairs.add(new Pair<>(charOne, charTwo));
            }
        }
        return allPairs;
    }

    private Set<Pair<Character, Character>> findAllBABPairs(String fragment) {
        return findAllABAPairs(fragment).stream()
                .map(pair -> new Pair<>(pair.getValue(), pair.getKey()))
                .collect(Collectors.toSet());
    }
}
