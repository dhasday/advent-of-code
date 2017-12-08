package dhasday.adventofcode.dec2016;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2016.solvers0x.*;
import dhasday.adventofcode.dec2016.solvers1x.*;

public class PuzzleRunner2016 {

    public static void main(String[] args) {
        solveAndPrintDay(new Dec2016Day1Solver());
        solveAndPrintDay(new Dec2016Day2Solver());
        solveAndPrintDay(new Dec2016Day3Solver());
        solveAndPrintDay(new Dec2016Day4Solver());
        solveAndPrintDay(new Dec2016Day5Solver());

        solveAndPrintDay(new Dec2016Day6Solver());
        solveAndPrintDay(new Dec2016Day7Solver());
        solveAndPrintDay(new Dec2016Day8Solver());
        solveAndPrintDay(new Dec2016Day9Solver());
        solveAndPrintDay(new Dec2016Day10Solver());

//        solveAndPrintDay(new Dec2016Day11Solver());
        solveAndPrintDay(new Dec2016Day12Solver());
        solveAndPrintDay(new Dec2016Day13Solver());
        solveAndPrintDay(new Dec2016Day14Solver());
        solveAndPrintDay(new Dec2016Day15Solver());

        solveAndPrintDay(new Dec2016Day16Solver());
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(String.format("%2d-1: %s", solver.getDayNumber(), String.valueOf(solver.solvePuzzleOne())));
        System.out.println(String.format("%2d-2: %s", solver.getDayNumber(), String.valueOf(solver.solvePuzzleTwo())));
    }
}
