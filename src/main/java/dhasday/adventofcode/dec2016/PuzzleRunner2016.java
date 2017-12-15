package dhasday.adventofcode.dec2016;

import java.util.Date;

import dhasday.adventofcode.dec2016.solvers0x.*;
import dhasday.adventofcode.dec2016.solvers1x.*;
import dhasday.adventofcode.dec2016.solvers2x.*;

public class PuzzleRunner2016 {
    public static void main(String[] args) {
        Date startTime = new Date();

        new Dec2016Day1Solver().run();
        new Dec2016Day2Solver().run();
        new Dec2016Day3Solver().run();
        new Dec2016Day4Solver().run();
        new Dec2016Day5Solver().run();  // ~15 sec

        new Dec2016Day6Solver().run();
        new Dec2016Day7Solver().run();
        new Dec2016Day8Solver().run();
        new Dec2016Day9Solver().run();
        new Dec2016Day10Solver().run();

        new Dec2016Day11Solver().run();
        new Dec2016Day12Solver().run();
        new Dec2016Day13Solver().run();
        new Dec2016Day14Solver().run(); // ~22 sec
        new Dec2016Day15Solver().run();

        new Dec2016Day16Solver().run();
        new Dec2016Day17Solver().run();
        new Dec2016Day18Solver().run();
        new Dec2016Day19Solver().run();
        new Dec2016Day20Solver().run();

        new Dec2016Day21Solver().run();
        new Dec2016Day22Solver().run();
        new Dec2016Day23Solver().run(); // ~125 sec
        new Dec2016Day24Solver().run();
        new Dec2016Day25Solver().run();

        Date endTime = new Date();

        System.out.println("Start   : " + startTime);
        System.out.println("End     : " + endTime);
        System.out.println("Elapsed : " + (endTime.getTime() - startTime.getTime()));
    }
}
