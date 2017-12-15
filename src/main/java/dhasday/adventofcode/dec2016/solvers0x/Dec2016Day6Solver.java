package dhasday.adventofcode.dec2016.solvers0x;

import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import dhasday.adventofcode.common.DaySolver;

public class Dec2016Day6Solver extends DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/6-input";

    @Override
    public int getDayNumber() {
        return 6;
    }

    @Override
    public String solvePuzzleOne() {
        List<String> allMessages = getAllFileLines(INPUT_FILE);

        return errorCorrectMessages(allMessages, (e1, e2) -> Integer.compare(e2.getValue(), e1.getValue()));
    }

    @Override
    public String solvePuzzleTwo() {
        List<String> allMessages = getAllFileLines(INPUT_FILE);

        return errorCorrectMessages(allMessages, Comparator.comparingInt(Map.Entry::getValue));
    }

    private String errorCorrectMessages(List<String> allMessages, Comparator<Map.Entry<Character, Integer>> comparator) {
        int messageSize = allMessages.get(0).length();

        String correctedMessage = "";
        for (int i = 0; i < messageSize; i++) {
            correctedMessage += getCorrectedCharacter(allMessages, i, comparator);
        }
        return correctedMessage;
    }

    private Character getCorrectedCharacter(List<String> allMessages, int index, Comparator<Map.Entry<Character, Integer>> comparator) {
        Map<Character, Integer> charFreq = new HashMap<>();

        for (String message : allMessages) {
            Character character = message.charAt(index);

            if (!charFreq.containsKey(character)) {
                charFreq.put(character, 0);
            }

            charFreq.put(character, charFreq.get(character) + 1);
        }

        return charFreq.entrySet()
                .stream()
                .sorted(comparator)
                .map(Map.Entry::getKey)
                .limit(1)
                .findFirst()
                .get();
    }
}
