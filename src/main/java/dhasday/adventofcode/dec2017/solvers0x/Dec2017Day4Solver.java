package dhasday.adventofcode.dec2017.solvers0x;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import dhasday.adventofcode.DaySolver;

public class Dec2017Day4Solver implements DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/4-input";

    @Override
    public int getDayNumber() {
        return 4;
    }

    @Override
    public Long solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        return allFileLines.stream()
                .filter(this::isValidPasswordOne)
                .count();
    }

    @Override
    public Long solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        return allFileLines.stream()
                .filter(this::isValidPasswordTwo)
                .count();
    }

    private boolean isValidPasswordOne(String input) {
        Set<String> usedWords = new HashSet<>();

        for (String word : input.split(" ")) {
            if (usedWords.contains(word)) {
                return false;
            }

            usedWords.add(word);
        }

        return true;
    }

    private boolean isValidPasswordTwo(String input) {
        Set<Map<Character, Integer>> usedWords = new HashSet<>();

        for (String word : input.split(" ")) {
            Map<Character, Integer> charMap = getCharMap(word);

            if (usedWords.contains(charMap)) {
                return false;
            }

            usedWords.add(charMap);
        }

        return true;
    }

    private Map<Character, Integer> getCharMap(String word) {
        Map<Character, Integer> letterMap = new HashMap<>();

        for (int i = 0; i < word.length(); i++) {
            char curChar = word.charAt(i);

            Integer curCount = letterMap.get(curChar);

            if (curCount == null) {
                curCount = 0;
            }

            letterMap.put(curChar, curCount + 1);
        }

        return letterMap;
    }
}
