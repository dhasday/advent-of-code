package dhasday.adventofcode.dec2016.solvers1x;

import java.util.HashSet;
import java.util.Set;
import java.util.function.BiFunction;

import com.google.common.collect.Sets;
import dhasday.adventofcode.common.DaySolver;
import javafx.util.Pair;
import org.apache.commons.codec.digest.DigestUtils;

public class Dec2016Day17Solver extends DaySolver<String> {

    private static final Set<Character> UNLOCKED_CHARACTERS = Sets.newHashSet('b', 'c', 'd', 'e', 'f');

    private static final String INPUT = "pxxbnzuo";

    @Override
    public int getDayNumber() {
        return 17;
    }

    @Override
    public String solvePuzzleOne() {
        Pair<Integer, Integer> startPos = new Pair<>(1, 4);
        Pair<Integer, Integer> targetPos = new Pair<>(4, 1);

        return getPath(startPos, targetPos, INPUT, "", (p1, p2) -> {
            if (p1 == null) {
                return p2;
            }
            if (p2 == null) {
                return p1;
            }
            return p1.length() < p2.length() ? p1 : p2;
        });
    }

    @Override
    public String solvePuzzleTwo() {
        Pair<Integer, Integer> startPos = new Pair<>(1, 4);
        Pair<Integer, Integer> targetPos = new Pair<>(4, 1);

        String longestPath = getPath(startPos, targetPos, INPUT, "", (p1, p2) -> {
            if (p1 == null) {
                return p2;
            }
            if (p2 == null) {
                return p1;
            }
            return p1.length() < p2.length() ? p2 : p1;
        });

        return String.valueOf(longestPath.length());
    }

    private String getPath(Pair<Integer, Integer> curPos,
                           Pair<Integer, Integer> targetPos,
                           String passcode,
                           String curPath,
                           BiFunction<String, String, String> biFunction) {
        if (curPos.equals(targetPos)) {
            return curPath;
        }
        Set<Direction> availableDirections = getAvailableDirections(passcode, curPath);
        String optimalPath = null;
        for (Direction direction : availableDirections) {
            Pair<Integer, Integer> nextPos = new Pair<>(curPos.getKey() + direction.xChange, curPos.getValue() + direction.yChange);
            if (isHardLocked(nextPos)) {
                continue;
            }

            String nextPath = curPath + direction.symbol;

            String possiblePath = getPath(nextPos, targetPos, passcode, nextPath, biFunction);
            optimalPath = biFunction.apply(optimalPath, possiblePath);
        }

        return optimalPath;
    }

    private Set<Direction> getAvailableDirections(String passcode, String currentPath) {
        String md5 = DigestUtils.md5Hex(passcode + currentPath);

        Set<Direction> openDirections = new HashSet<>();
        if (UNLOCKED_CHARACTERS.contains(md5.charAt(0))) {
            openDirections.add(Direction.UP);
        }
        if (UNLOCKED_CHARACTERS.contains(md5.charAt(1))) {
            openDirections.add(Direction.DOWN);
        }
        if (UNLOCKED_CHARACTERS.contains(md5.charAt(2))) {
            openDirections.add(Direction.LEFT);
        }
        if (UNLOCKED_CHARACTERS.contains(md5.charAt(3))) {
            openDirections.add(Direction.RIGHT);
        }

        return openDirections;
    }

    private boolean isHardLocked(Pair<Integer, Integer> pos) {
        return (pos.getKey() < 1 || pos.getKey() > 4) || (pos.getValue() < 1 || pos.getValue() > 4);
    }

    private enum Direction {
        UP('U', 0, 1),
        DOWN('D', 0, -1),
        LEFT('L', -1, 0),
        RIGHT('R', 1, 0);

        final char symbol;
        final int xChange;
        final int yChange;

        Direction(char symbol, int xChange, int yChange) {
            this.symbol = symbol;
            this.xChange = xChange;
            this.yChange = yChange;
        }
    }
}
