package dhasday.adventofcode.dec2017;

import java.util.Date;

import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.dec2017.solvers0x.*;
import dhasday.adventofcode.dec2017.solvers1x.*;

public class PuzzleRunner2017 {
    public static void main(String[] args) {
        Date startTime = new Date();

        new Dec2017Day1Solver().run();
        new Dec2017Day2Solver().run();
        new Dec2017Day3Solver().run();
        new Dec2017Day4Solver().run();
        new Dec2017Day5Solver().run();

        new Dec2017Day6Solver().run();
        new Dec2017Day7Solver().run();
        new Dec2017Day8Solver().run();
        new Dec2017Day9Solver().run();
        new Dec2017Day10Solver().run();

        new Dec2017Day11Solver().run();
        new Dec2017Day12Solver().run();
        new Dec2017Day13Solver().run();
        new Dec2017Day14Solver().run();
//        new Dec2017Day15Solver().run();
//
//        new Dec2017Day16Solver().run();
//        new Dec2017Day17Solver().run();
//        new Dec2017Day18Solver().run();
//        new Dec2017Day19Solver().run();
//        new Dec2017Day20Solver().run();
//
//        new Dec2017Day21Solver().run();
//        new Dec2017Day22Solver().run();
//        new Dec2017Day23Solver().run();
//        new Dec2017Day24Solver().run();
//        new Dec2017Day25Solver().run();

        Date endTime = new Date();

        System.out.println("Start   : " + startTime);
        System.out.println("End     : " + endTime);
        System.out.println("Elapsed : " + (endTime.getTime() - startTime.getTime()));
    }
}
