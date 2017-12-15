package dhasday.adventofcode.dec2017.solvers0x;

import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;

public class Dec2017Day9Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/9-input";

    @Override
    public int getDayNumber() {
        return 9;
    }

    @Override
    public Integer solvePuzzleOne() {
        return cleanAndScore(getOnlyFileLine(INPUT_FILE)).getKey();
    }

    @Override
    public Integer solvePuzzleTwo() {
        return cleanAndScore(getOnlyFileLine(INPUT_FILE)).getValue();
    }

    private Pair<Integer, Integer> cleanAndScore(String fullInput) {
        int score = 0;
        int garbageCount = 0;
        int openBraceCount = 0;
        boolean inGarbage = false;

        for (int i = 0; i < fullInput.length(); i++) {
            char currentChar = fullInput.charAt(i);

            if (!inGarbage) {
                switch (currentChar) {
                    case '{':
                        openBraceCount++;
                        score += openBraceCount;
                        break;
                    case '}':
                        openBraceCount--;
                        break;
                    case '<':
                        inGarbage = true;
                        break;
                }
            } else {
                switch (currentChar) {
                    case '!':
                        i++;
                        break;
                    case '>':
                        inGarbage = false;
                        break;
                    default:
                        garbageCount++;
                }
            }

        }
        return new Pair<>(score, garbageCount);
    }
}
