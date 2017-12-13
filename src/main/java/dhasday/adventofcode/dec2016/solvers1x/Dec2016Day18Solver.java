package dhasday.adventofcode.dec2016.solvers1x;

import dhasday.adventofcode.common.DaySolver;

public class Dec2016Day18Solver implements DaySolver<Integer> {

    private static final String INPUT = "^.....^.^^^^^.^..^^.^.......^^..^^^..^^^^..^.^^.^.^....^^...^^.^^.^...^^.^^^^..^^.....^.^...^.^.^^.^";

    @Override
    public int getDayNumber() {
        return 18;
    }

    @Override
    public Integer solvePuzzleOne() {
        boolean[] rowOne = loadInput();

        boolean[][] allRows = generateRows(rowOne, 40);

        return countFalses(allRows);
    }

    @Override
    public Integer solvePuzzleTwo() {
        boolean[] rowOne = loadInput();

        boolean[][] allRows = generateRows(rowOne, 400000);

        return countFalses(allRows);
    }

    private boolean[] loadInput() {
        boolean[] rowOne = new boolean[INPUT.length()];

        for (int i = 0; i < INPUT.length(); i++) {
            rowOne[i] = '^' == INPUT.charAt(i);
        }

        return rowOne;
    }

    private boolean[][] generateRows(boolean[] rowOne, int numRowsTotal) {
        boolean[][] allRows = new boolean[numRowsTotal][rowOne.length];
        allRows[0] = rowOne;

        for (int i = 1; i < numRowsTotal; i++) {
            allRows[i] = computeNextRow(allRows[i - 1]);
        }

        return allRows;
    }

    private boolean[] computeNextRow(boolean[] currentRow) {
        boolean[] nextRow = new boolean[currentRow.length];

        for (int i = 0; i < currentRow.length; i++) {
            boolean left = i > 0 && currentRow[i - 1];
            boolean right = i < (currentRow.length -1) && currentRow[i + 1];

            nextRow[i] = isTrap(left, right);
        }

        return nextRow;
    }


    private boolean isTrap(boolean l, boolean r) {
        return l ^ r;
    }

    private int countFalses(boolean[][] matrix) {
        int sum = 0;
        for (boolean[] row : matrix) {
            for (boolean cell : row) {
                sum += cell ? 0 : 1;
            }
        }
        return sum;
    }

}
