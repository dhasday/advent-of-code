package dhasday.adventofcode.dec2017.solvers0x;

import dhasday.adventofcode.common.DaySolver;

public class Dec2017Day3Solver implements DaySolver<Integer> {

    private static final Integer TARGET_VALUE = 361527;

    @Override
    public int getDayNumber() {
        return 3;
    }

    @Override
    public Integer solvePuzzleOne() {
        int originOffset = determineOriginOffset(TARGET_VALUE);
        int[][] field = buildInitialField(originOffset);

        return processSpiralOne(field, originOffset, TARGET_VALUE);
    }

    @Override
    public Integer solvePuzzleTwo() {
        int originOffset = determineOriginOffset(TARGET_VALUE);
        int[][] field = buildInitialField(originOffset);

        return processSpiralTwo(field, originOffset, TARGET_VALUE);
    }

    private int determineOriginOffset(int number) {
        int fieldSize = (int) Math.sqrt(number) + 3;
        return fieldSize / 2;
    }

    private int[][] buildInitialField(int originOffset) {
        int[][] field = new int[originOffset * 2][originOffset * 2];

        field[originOffset][originOffset] = 1;

        return field;
    }
    
    private Integer processSpiralOne(int[][] field, int originOffset, int target) {
        int curEdge = 1;
        int curNum = 2;
        int curX = originOffset;
        int curY = originOffset + 1;

        field[curX][curY] = curNum;
        if (curNum >= target) {
            return calculateDistance(originOffset, curX, curY);
        }
        curNum++;
        Direction currentDirection = Direction.POSITIVE_Y;

        while (curNum <= target) {
            while (!currentDirection.reachedEdge(curX, curY, originOffset, curEdge)) {
                curX = curX + currentDirection.xChange;
                curY = curY + currentDirection.yChange;

                field[curX][curY] = curNum;
                if (curNum >= target) {
                    return Math.abs(curX - originOffset) + Math.abs(curY - originOffset);
                }
                curNum++;
            }

            if (currentDirection.incrementEdge) {
                curEdge++;
            }
            currentDirection = currentDirection.next();
        }

        return null;
    }

    private Integer processSpiralTwo(int[][] field, int originOffset, int target) {
        int curEdge = 1;
        int curX = originOffset;
        int curY = originOffset + 1;

        int lastNum = sumAdjacent(field, curX, curY);
        field[curX][curY] = lastNum;
        if (lastNum >= target) {
            return lastNum;
        }
        Direction currentDirection = Direction.POSITIVE_Y;

        while (lastNum < target) {
            while (!currentDirection.reachedEdge(curX, curY, originOffset, curEdge)) {
                curX = curX + currentDirection.xChange;
                curY = curY + currentDirection.yChange;

                lastNum = sumAdjacent(field, curX, curY);
                field[curX][curY] = lastNum;
                if (lastNum >= target) {
                    return lastNum;
                }
            }

            if (currentDirection.incrementEdge) {
                curEdge++;
            }
            currentDirection = currentDirection.next();
        }

        return null;
    }

    private int sumAdjacent(int[][] field, int curX, int curY) {
        int sum = 0;

        for (int x = (curX - 1); x <= (curX + 1); x++) {
            for (int y = (curY - 1); y <= (curY + 1); y++) {
                try {
                    sum += field[x][y];
                } catch (IndexOutOfBoundsException ioobe) {
                    // Ignore
                }
            }
        }

        return sum;
    }

    private int calculateDistance(int origin, int x, int y) {
        return Math.abs(x - origin) + Math.abs(y - origin);
    }

    private enum Direction {
        POSITIVE_Y(false, 0, 1) {
            @Override
            Direction next() {
                return NEGATIVE_X;
            }

            @Override
            boolean reachedEdge(int x, int y, int originOffset, int edge) {
                return y == originOffset + edge;
            }
        },
        NEGATIVE_X(false, -1, 0) {
            @Override
            Direction next() {
                return NEGATIVE_Y;
            }

            @Override
            boolean reachedEdge(int x, int y, int originOffset, int edge) {
                return x == originOffset - edge;
            }
        },
        NEGATIVE_Y(false, 0, -1) {
            @Override
            Direction next() {
                return POSITIVE_X;
            }

            @Override
            boolean reachedEdge(int x, int y, int originOffset, int edge) {
                return y == originOffset - edge;
            }
        },
        POSITIVE_X(true, 1, 0) {
            @Override
            Direction next() {
                return POSITIVE_Y;
            }

            @Override
            boolean reachedEdge(int x, int y, int originOffset, int edge) {
                return x == originOffset + edge;
            }
        };

        abstract Direction next();
        abstract boolean reachedEdge(int x, int y, int originOffset, int edge);

        boolean incrementEdge;
        int xChange;
        int yChange;

        Direction(boolean incrementEdge, int xChange, int yChange) {
            this.incrementEdge = incrementEdge;
            this.xChange = xChange;
            this.yChange = yChange;
        }
    }

}
