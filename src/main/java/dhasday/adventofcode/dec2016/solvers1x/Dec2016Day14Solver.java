package dhasday.adventofcode.dec2016.solvers1x;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;
import org.apache.commons.codec.digest.DigestUtils;

public class Dec2016Day14Solver implements DaySolver<Integer> {

    private static final String INPUT_VALUE = "ngcjuoqr";

    private Map<Pair<String, Integer>, Map<Integer, String>> hashCache = new HashMap<>(); // Get it?

    @Override
    public int getDayNumber() {
        return 14;
    }

    @Override
    public Integer solvePuzzleOne() {
//        return 18626
        return findNthKey(INPUT_VALUE, 1, 64);
    }

    @Override
    public Integer solvePuzzleTwo() {
//        return 20092
        return findNthKey(INPUT_VALUE, 2017, 64);
    }

    private Integer findNthKey(String salt, int numHashes, int n) {
        int currentIndex = -1;
        for (int i = 0; i < n; i++) {
            currentIndex++;
            currentIndex = findNextKey(salt, numHashes, currentIndex);
        }
        return currentIndex;
    }

    private int findNextKey(String salt, int numHashes, int startIndex) {
        for(int curIndex = startIndex;;curIndex++) {
            String hashOne = hashNTimes(salt, numHashes, curIndex);
            Character repeatedChar = getRepeatedCharacter(hashOne, 3);
            if (repeatedChar != null) {
                for (int i = curIndex + 1; i <= curIndex + 1000; i++) {
                    String hashTwo = hashNTimes(salt, numHashes, i);
                    if (repeatedChar.equals(getRepeatedCharacter(hashTwo, 5))) {
                        return curIndex;
                    }
                }
            }
        }
    }

    private String hashNTimes(String salt, int numHashes, Integer index) {
        Pair<String, Integer> cacheKey = new Pair<>(salt, numHashes);

        // Get cached hash if present
        Map<Integer, String> cachedHashesForKey = hashCache.get(cacheKey);
        if (cachedHashesForKey != null && cachedHashesForKey.containsKey(index)) {
            return cachedHashesForKey.get(index);
        }

        // Compute hash
        String currentValue = salt + index;
        for(int i = 0; i < numHashes; i++) {
            currentValue = DigestUtils.md5Hex(currentValue);
        }

        // Store hash
        if (cachedHashesForKey == null) {
            cachedHashesForKey = new HashMap<>();
            hashCache.put(cacheKey, cachedHashesForKey);
        }
        cachedHashesForKey.put(index, currentValue);

        return currentValue;
    }

    Character getRepeatedCharacter(String md5, int numRepeats) {
        String regex = "(.)\\1{" + (numRepeats - 1) + "}";
        Pattern pattern = Pattern.compile(regex);

        Matcher matcher = pattern.matcher(md5);
        if (!matcher.find()) {
            return null;
        }
        return matcher.group(1).charAt(0);
    }
}
