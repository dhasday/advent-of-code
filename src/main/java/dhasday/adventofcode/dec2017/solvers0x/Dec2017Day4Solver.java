package dhasday.adventofcode.dec2017.solvers0x;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day4Solver extends Dec2017DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/4-input";

    @Override
    public int getDay() {
        return 4;
    }

    @Override
    public Long solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        return allFileLines.stream()
                .filter(l -> isValidPassword(l, w -> w))
                .count();
    }

    @Override
    public Long solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        return allFileLines.stream()
                .filter(l -> isValidPassword(l, this::getCharMap))
                .count();
    }

    private <T> boolean isValidPassword(String input, Function<String, T> getPossiblyUsedWord) {
        Set<T> usedWords = new HashSet<>();

        for (String word : input.split(" ")) {
            T possibleWord = getPossiblyUsedWord.apply(word);

            if (usedWords.contains(possibleWord)) {
                return false;
            }

            usedWords.add(possibleWord);
        }

        return true;
    }

    private Map<Character, Long> getCharMap(String word) {
        return word.chars()
                .boxed()
                .collect(Collectors.groupingBy(i -> (char) i.intValue(), Collectors.counting()));
    }
}
