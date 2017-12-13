package dhasday.adventofcode.dec2017;

import java.util.Date;

import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.dec2017.solvers0x.*;
import dhasday.adventofcode.dec2017.solvers1x.*;

public class PuzzleRunner2017 {

    public static void main(String[] args) {
        Date startTime = new Date();

        solveAndPrintDay(new Dec2017Day1Solver());
        solveAndPrintDay(new Dec2017Day2Solver());
        solveAndPrintDay(new Dec2017Day3Solver());
        solveAndPrintDay(new Dec2017Day4Solver());
        solveAndPrintDay(new Dec2017Day5Solver());

        solveAndPrintDay(new Dec2017Day6Solver());
        solveAndPrintDay(new Dec2017Day7Solver());
        solveAndPrintDay(new Dec2017Day8Solver());
        solveAndPrintDay(new Dec2017Day9Solver());
        solveAndPrintDay(new Dec2017Day10Solver());

        solveAndPrintDay(new Dec2017Day11Solver());
        solveAndPrintDay(new Dec2017Day12Solver());
        solveAndPrintDay(new Dec2017Day13Solver());
//        solveAndPrintDay(new Dec2017Day14Solver());
//        solveAndPrintDay(new Dec2017Day15Solver());
//
//        solveAndPrintDay(new Dec2017Day16Solver());
//        solveAndPrintDay(new Dec2017Day17Solver());
//        solveAndPrintDay(new Dec2017Day18Solver());
//        solveAndPrintDay(new Dec2017Day19Solver());
//        solveAndPrintDay(new Dec2017Day20Solver());
//
//        solveAndPrintDay(new Dec2017Day21Solver());
//        solveAndPrintDay(new Dec2017Day22Solver());
//        solveAndPrintDay(new Dec2017Day23Solver());
//        solveAndPrintDay(new Dec2017Day24Solver());
//        solveAndPrintDay(new Dec2017Day25Solver());

        Date endTime = new Date();

        System.out.println("Start   : " + startTime);
        System.out.println("End     : " + endTime);
        System.out.println("Elapsed : " + (endTime.getTime() - startTime.getTime()));
    }

    private static void solveAndPrintDay(DaySolver solver) {
        System.out.println(solver.getDayNumber() + "-1: " + solver.solvePuzzleOne());
        System.out.println(solver.getDayNumber() + "-2: " + solver.solvePuzzleTwo());
    }
}
