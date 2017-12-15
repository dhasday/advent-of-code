package dhasday.adventofcode.dec2015;

import java.util.Date;

import dhasday.adventofcode.dec2015.solvers0x.*;
import dhasday.adventofcode.dec2015.solvers1x.*;
import dhasday.adventofcode.dec2015.solvers2x.*;

public class PuzzleRunner2015 {
    public static void main(String[] args) {
        Date startTime = new Date();

        new Dec2015Day1Solver().run();
        new Dec2015Day2Solver().run();
        new Dec2015Day3Solver().run();
        new Dec2015Day4Solver().run();
        new Dec2015Day5Solver().run();

        new Dec2015Day6Solver().run();
        new Dec2015Day7Solver().run();
        new Dec2015Day8Solver().run();
        new Dec2015Day9Solver().run();
        new Dec2015Day10Solver().run();

        new Dec2015Day11Solver().run();
        new Dec2015Day12Solver().run();
        new Dec2015Day13Solver().run();
        new Dec2015Day14Solver().run();
        new Dec2015Day15Solver().run();

        new Dec2015Day16Solver().run();
        new Dec2015Day17Solver().run();
        new Dec2015Day18Solver().run();
        new Dec2015Day19Solver().run();
        new Dec2015Day20Solver().run();

        new Dec2015Day21Solver().run();
        new Dec2015Day22Solver().run();
        new Dec2015Day23Solver().run();
        new Dec2015Day24Solver().run();
        new Dec2015Day25Solver().run();

        Date endTime = new Date();

        System.out.println("Start   : " + startTime);
        System.out.println("End     : " + endTime);
        System.out.println("Elapsed : " + (endTime.getTime() - startTime.getTime()));
    }
}
