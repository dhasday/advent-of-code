package dhasday.adventofcode.dec2016.solvers0x;

import javafx.util.Pair;
import org.apache.commons.codec.digest.DigestUtils;

import dhasday.adventofcode.dec2016.Dec2016DaySolver;

public class Dec2016Day5Solver extends Dec2016DaySolver<String> {

    private static final String INPUT = "reyedfim";

    private static final int PASSWORD_LENGTH = 8;

    @Override
    public int getDay() {
        return 5;
    }

    @Override
    protected Pair<String, String> solvePuzzles() {
        StringBuilder passwordOne = new StringBuilder();
        char[] passwordTwo = new char[PASSWORD_LENGTH];

        int index = 0;
        while (passwordOne.length() < 8 || isPasswordIncomplete(passwordTwo)) {
            String toHash = INPUT + index;
            String md5 = DigestUtils.md5Hex(toHash);

            if (md5.startsWith("00000")) {
                if (passwordOne.length() < 8) {
                    passwordOne.append(md5.charAt(5));
                }

                if (isPasswordIncomplete(passwordTwo)) {
                    Integer pwIndex = md5.charAt(5) - '0';

                    if (pwIndex < PASSWORD_LENGTH
                            && passwordTwo[pwIndex] == 0) {
                        passwordTwo[pwIndex] = md5.charAt(6);
                    }
                }

            }

            index++;
        }

        return new Pair<>(passwordOne.toString(), new String(passwordTwo));
    }

    private boolean isPasswordIncomplete(char[] password) {
        for (char c : password) {
            if (c == 0) {
                return true;
            }
        }

        return false;
    }
}
