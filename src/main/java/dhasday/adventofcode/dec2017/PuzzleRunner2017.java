package dhasday.adventofcode.dec2017;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2017.solvers.Dec2017Day1Solver;

public class PuzzleRunner2017 {

    public static void main(String[] args) {
        solveAndPrintDay(new Dec2017Day1Solver());
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(solver.getDayNumber() + "-1: " + solver.solvePuzzleOne());
        System.out.println(solver.getDayNumber() + "-2: " + solver.solvePuzzleTwo());
    }
}
