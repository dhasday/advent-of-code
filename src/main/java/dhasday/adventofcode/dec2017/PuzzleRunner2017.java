package dhasday.adventofcode.dec2017;

import dhasday.adventofcode.DaySolver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day1Solver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day2Solver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day3Solver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day4Solver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day5Solver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day6Solver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day7Solver;
import dhasday.adventofcode.dec2017.solvers0x.Dec2017Day8Solver;

public class PuzzleRunner2017 {

    public static void main(String[] args) {
        solveAndPrintDay(new Dec2017Day1Solver());
        solveAndPrintDay(new Dec2017Day2Solver());
        solveAndPrintDay(new Dec2017Day3Solver());
        solveAndPrintDay(new Dec2017Day4Solver());
        solveAndPrintDay(new Dec2017Day5Solver());

        solveAndPrintDay(new Dec2017Day6Solver());
        solveAndPrintDay(new Dec2017Day7Solver());
        solveAndPrintDay(new Dec2017Day8Solver());
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(solver.getDayNumber() + "-1: " + solver.solvePuzzleOne());
        System.out.println(solver.getDayNumber() + "-2: " + solver.solvePuzzleTwo());
    }
}
