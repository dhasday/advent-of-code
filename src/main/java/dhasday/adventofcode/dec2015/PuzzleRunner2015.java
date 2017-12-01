package dhasday.adventofcode.dec2015;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2015.solvers.*;

public class PuzzleRunner2015 {

    public static void main(String[] args) {
        solveAndPrintDay(new Dec2015Day1Solver());
        solveAndPrintDay(new Dec2015Day2Solver());
        solveAndPrintDay(new Dec2015Day3Solver());
        solveAndPrintDay(new Dec2015Day4Solver());
        solveAndPrintDay(new Dec2015Day5Solver());
        solveAndPrintDay(new Dec2015Day6Solver());
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(solver.getDayNumber() + "-1: " + solver.solvePuzzleOne());
        System.out.println(solver.getDayNumber() + "-2: " + solver.solvePuzzleTwo());
    }
}
