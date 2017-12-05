package dhasday.adventofcode.dec2016;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2016.solvers0x.*;

public class PuzzleRunner2016 {

    public static void main(String[] args) {
        solveAndPrintDay(new Dec2016Day1Solver());
        solveAndPrintDay(new Dec2016Day2Solver());
        solveAndPrintDay(new Dec2016Day3Solver());
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(String.format("%2d-1: %s", solver.getDayNumber(), String.valueOf(solver.solvePuzzleOne())));
        System.out.println(String.format("%2d-2: %s", solver.getDayNumber(), String.valueOf(solver.solvePuzzleTwo())));
    }
}
