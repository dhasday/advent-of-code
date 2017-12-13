package dhasday.adventofcode.dec2016.solvers0x;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;

import dhasday.adventofcode.common.DaySolver;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.StringUtils;

public class Dec2016Day5Solver implements DaySolver<String> {
    private static final String INPUT = "reyedfim";

    @Override
    public int getDayNumber() {
        return 5;
    }

    @Override
    public String solvePuzzleOne() {
        // return "f97c354d";
        return determinePasswordOne(INPUT);
    }

    @Override
    public String solvePuzzleTwo() {
        // return "863dde27";
        return determinePasswordTwo(INPUT);
    }

    private String determinePasswordOne(String input) {
        String password = "";

        int index = 0;
        while (password.length() < 8) {
            String toHash = input + index;
            String md5 = DigestUtils.md5Hex(toHash);
            if (md5.startsWith("00000")) {
                password += md5.charAt(5);
            }
            index++;
        }

        return password;
    }

    private String determinePasswordTwo(String input) {
        List<Character> passwordChars = new ArrayList<>();
        for (int i = 0; i < 8; i++) {
            passwordChars.add(null);
        }

        int index = 0;
        while (!isPasswordComplete(passwordChars)) {
            String toHash = input + index;
            String md5 = DigestUtils.md5Hex(toHash);
            if (md5.startsWith("00000")) {
                Integer pwIndex = getIndex(md5.charAt(5));

                if (pwIndex != null
                        && pwIndex < 8
                        && passwordChars.get(pwIndex) == null) {
                    passwordChars.set(pwIndex, md5.charAt(6));
                }
            }
            index++;
        }

        String password = "";
        for (Character character : passwordChars) {
            password += character;
        }
        return password;
    }

    private boolean isPasswordComplete(List<Character> password) {
        return password.stream().noneMatch(Objects::isNull);
    }

    private Integer getIndex(Character character) {
        if (StringUtils.isNumeric(character + "")) {
            return character - '0';
        } else {
            return null;
        }
    }
}
