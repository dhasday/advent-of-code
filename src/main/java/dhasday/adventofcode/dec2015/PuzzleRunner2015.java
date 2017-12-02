package dhasday.adventofcode.dec2015;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2015.solvers0x.*;
import dhasday.adventofcode.dec2015.solvers1x.*;

public class PuzzleRunner2015 {

    public static void main(String[] args) {
        solveAndPrintDay(new Dec2015Day1Solver());
        solveAndPrintDay(new Dec2015Day2Solver());
        solveAndPrintDay(new Dec2015Day3Solver());
        solveAndPrintDay(new Dec2015Day4Solver());
        solveAndPrintDay(new Dec2015Day5Solver());

        solveAndPrintDay(new Dec2015Day6Solver());
        solveAndPrintDay(new Dec2015Day7Solver());
        solveAndPrintDay(new Dec2015Day8Solver());
        solveAndPrintDay(new Dec2015Day9Solver());
        solveAndPrintDay(new Dec2015Day10Solver());
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(String.format("%2d-1: %d", solver.getDayNumber(), solver.solvePuzzleOne()));
        System.out.println(String.format("%2d-2: %d", solver.getDayNumber(), solver.solvePuzzleTwo()));
    }
}
