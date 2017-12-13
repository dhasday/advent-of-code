package dhasday.adventofcode.dec2016.solvers2x;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Function;

import com.google.common.base.Joiner;
import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.common.AStarSearch;
import javafx.util.Pair;

public class Dec2016Day22Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/22-input-cleaned";

    private AStarSearch aStarSearch = new AStarSearch();

    @Override
    public int getDayNumber() {
        return 22;
    }

    @Override
    public Integer solvePuzzleOne() {
        int sizeX = 37;
        int sizeY = 28;

        Drive[][] drives = loadDrives(sizeX, sizeY);

        return countViablePairs(drives);
    }

    @Override
    public Integer solvePuzzleTwo() {
        int sizeX = 37;
        int sizeY = 28;

        Drive[][] drives = loadDrives(sizeX, sizeY);

        Drive emptyDrive = findEmptyDrive(drives);
        Drive firstTarget = drives[sizeX - 2][0]; // Next to the drive we want to move

        List<Drive> distanceToFirstTargetMove = aStarSearch.findShortestPath(
                emptyDrive,
                firstTarget,
                (p1, p2) -> Math.abs(p2.x - p1.x) + Math.abs(p2.y - p1.y),
                getAdjacentNodeLocator(drives)
        );

        // Once we're in position with a blank drive behind us, it's 5 moves to cycle forward 1 space
        // and since we're moving into one of the spaces, we need to move 1 less
        // # # * - # | # # * # # | # # * # # | # # * # # | # - * # # | # * - # #
        // # # # # # | # # # - # | # # - # # | # - # # # | # # # # # | # # # # #

        return distanceToFirstTargetMove.size() + ((sizeX - 2) * 5);
    }

    private void printAllDrives(Drive[][] drives, int sizeX, int sizeY) {
        for (int y = 0; y < sizeY; y++) {
            List<String> rowValues = new ArrayList<>();
            for (int x = 0; x < sizeX; x++) {
                Drive drive = drives[x][y];
                if (drive.total <= 100) {
                    rowValues.add("[" + drive.used + "/" + drive.total + "]");
                } else {
                    rowValues.add("   |   ");
                }

            }
            System.out.println(Joiner.on("\t").join(rowValues));
        }
    }

    private Drive[][] loadDrives(int sizeX, int sizeY) {
        Drive[][] drives = new Drive[sizeX][sizeY];

        for (String line : getAllFileLines(INPUT_FILE)) {
            String[] split = line.split(" ");

            Integer x = Integer.valueOf(split[0]);
            Integer y = Integer.valueOf(split[1]);
            Integer used = Integer.valueOf(split[2]);
            Integer avail = Integer.valueOf(split[3]);
            drives[x][y] = new Drive(x, y, used, avail);
        }

        return drives;
    }

    private Integer countViablePairs(Drive[][] drives) {
        int viablePairsCount = 0;

        for (int x = 0; x < drives.length; x++) {
            for (int y = 0; y < drives[x].length; y++) {
                int used = drives[x][y].used;
                if (used == 0) {
                    continue;
                }

                for (int x2 = 0; x2 < drives.length; x2++) {
                    for (int y2 = 0; y2 < drives[x2].length; y2++) {
                        if ((x2 != x || y2 != y)
                                && isEnoughAvailSpace(drives, used, x2, y2)) {
                            viablePairsCount++;
                        }
                    }
                }
            }
        }

        return viablePairsCount;
    }

    private boolean isEnoughAvailSpace(Drive[][] drives, int used, int x, int y) {
        try {
            return drives[x][y].avail >= used;
        } catch (ArrayIndexOutOfBoundsException aioobe) {
            return false;
        }
    }

    private Function<Drive, Set<Pair<Drive, Integer>>> getAdjacentNodeLocator(Drive[][] drives) {
        return (drive) -> {
            int sizeX = drives.length;
            int sizeY = drives[drive.x].length;

            int curX = drive.x;
            int curY = drive.y;

            Set<Pair<Drive, Integer>> adjacentPairs = new HashSet<>();

            if (curX > 0) {
                int newX = curX - 1;
                int newY = curY;

                if (drives[newX][newY].total <= 100) {
                    adjacentPairs.add(new Pair<>(drives[newX][newY], 1));
                }
            }
            if (curX < (sizeX - 1)) {
                int newX = curX + 1;
                int newY = curY;

                if (drives[newX][newY].total <= 100) {
                    adjacentPairs.add(new Pair<>(drives[newX][newY], 1));
                }
            }

            if (curY > 0) {
                int newX = curX;
                int newY = curY - 1;

                if (drives[newX][newY].total <= 100) {
                    adjacentPairs.add(new Pair<>(drives[newX][newY], 1));
                }
            }
            if (curY < (sizeY - 1)) {
                int newX = curX;
                int newY = curY + 1;

                if (drives[newX][newY].total <= 100) {
                    adjacentPairs.add(new Pair<>(drives[newX][newY], 1));
                }
            }

            return adjacentPairs;
        };
    }

    private Drive findEmptyDrive(Drive[][] drives) {
        for (int x = 0; x < drives.length; x++) {
            for (int y = 0; y < drives[x].length; y++) {
                if (drives[x][y].used == 0) {
                    return drives[x][y];
                }
            }
        }
        return null;
    }

    private class Drive {
        private final int x;
        private final int y;

        private final int used;
        private final int avail;
        private final int total;

        Drive(int x, int y, int used, int avail) {
            this.x = x;
            this.y = y;
            this.used = used;
            this.avail = avail;
            this.total = used + avail;
        }
    }
}
