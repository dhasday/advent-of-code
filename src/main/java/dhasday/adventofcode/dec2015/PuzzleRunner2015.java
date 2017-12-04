package dhasday.adventofcode.dec2015;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2015.solvers0x.*;
import dhasday.adventofcode.dec2015.solvers1x.*;
import dhasday.adventofcode.dec2015.solvers2x.*;

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

        solveAndPrintDay(new Dec2015Day11Solver());
        solveAndPrintDay(new Dec2015Day12Solver());
        solveAndPrintDay(new Dec2015Day13Solver());
        solveAndPrintDay(new Dec2015Day14Solver());
        solveAndPrintDay(new Dec2015Day15Solver());

        solveAndPrintDay(new Dec2015Day16Solver());
        solveAndPrintDay(new Dec2015Day17Solver());
        solveAndPrintDay(new Dec2015Day18Solver());
        solveAndPrintDay(new Dec2015Day19Solver());
        solveAndPrintDay(new Dec2015Day20Solver());

        solveAndPrintDay(new Dec2015Day21Solver());
        solveAndPrintDay(new Dec2015Day22Solver());
        solveAndPrintDay(new Dec2015Day23Solver());
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(String.format("%2d-1: %s", solver.getDayNumber(), String.valueOf(solver.solvePuzzleOne())));
        System.out.println(String.format("%2d-2: %s", solver.getDayNumber(), String.valueOf(solver.solvePuzzleTwo())));
    }
}
