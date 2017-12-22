package dhasday.adventofcode;

import java.util.List;

import com.google.common.collect.Lists;

import dhasday.adventofcode.common.DaySolver;
import dhasday.adventofcode.dec2015.Dec2015DaySolver;
import dhasday.adventofcode.dec2015.solvers0x.*;
import dhasday.adventofcode.dec2015.solvers1x.*;
import dhasday.adventofcode.dec2015.solvers2x.*;
import dhasday.adventofcode.dec2016.Dec2016DaySolver;
import dhasday.adventofcode.dec2016.solvers0x.*;
import dhasday.adventofcode.dec2016.solvers1x.*;
import dhasday.adventofcode.dec2016.solvers2x.*;
import dhasday.adventofcode.dec2017.Dec2017DaySolver;
import dhasday.adventofcode.dec2017.solvers0x.*;
import dhasday.adventofcode.dec2017.solvers1x.*;
import dhasday.adventofcode.dec2017.solvers2x.Dec2017Day20Solver;
import dhasday.adventofcode.dec2017.solvers2x.Dec2017Day21Solver;

public class AdventOfCode {
    /**
     *  Slow running solvers:
     *
     *  2015
     *    * Day  4  ~  2000 ms
     *    * Day 17  ~  2000 ms
     *    * Day 20  ~  3400 ms
     *
     *  2016
     *    * Day  5  ~ 18000 ms
     *    * Day 12  ~  1800 ms
     *    * Day 14  ~ 26000 ms
     *    * Day 23  ~155000 ms
     *
     *  2017
     *    * Day XX  ~       ms
     */

    public static void main(String[] args) {
        long startTime = System.currentTimeMillis();

        getSolvers2015().forEach(AdventOfCode::runSolverClass);
        System.out.println();
        getSolvers2016().forEach(AdventOfCode::runSolverClass);
        System.out.println();
        getSolvers2017().forEach(AdventOfCode::runSolverClass);

        long endTime = System.currentTimeMillis();

        System.out.println(String.format("%n%nTotal Elapsed Time: %d ms", (endTime - startTime)));
    }

    private static void runSolverClass(Class<? extends DaySolver<?>> solverClass) {
        try {
            solverClass.newInstance().printResults();
        } catch (InstantiationException|IllegalAccessException e) {
            throw new RuntimeException("Failed to create instance of solver for class: " + solverClass.getSimpleName(), e);
        }
    }

    private static List<Class<? extends Dec2015DaySolver<?>>> getSolvers2015() {
        return Lists.newArrayList(
                Dec2015Day1Solver.class,    Dec2015Day2Solver.class,    Dec2015Day3Solver.class,    Dec2015Day4Solver.class,    Dec2015Day5Solver.class,
                Dec2015Day6Solver.class,    Dec2015Day7Solver.class,    Dec2015Day8Solver.class,    Dec2015Day9Solver.class,    Dec2015Day10Solver.class,
                Dec2015Day11Solver.class,   Dec2015Day12Solver.class,   Dec2015Day13Solver.class,   Dec2015Day14Solver.class,   Dec2015Day15Solver.class,
                Dec2015Day16Solver.class,   Dec2015Day17Solver.class,   Dec2015Day18Solver.class,   Dec2015Day19Solver.class,   Dec2015Day20Solver.class,
                Dec2015Day21Solver.class,   Dec2015Day22Solver.class,   Dec2015Day23Solver.class,   Dec2015Day24Solver.class,   Dec2015Day25Solver.class
        );
    }

    private static List<Class<? extends Dec2016DaySolver<?>>> getSolvers2016() {
        return Lists.newArrayList(
                Dec2016Day1Solver.class,    Dec2016Day2Solver.class,    Dec2016Day3Solver.class,    Dec2016Day4Solver.class,    Dec2016Day5Solver.class,
                Dec2016Day6Solver.class,    Dec2016Day7Solver.class,    Dec2016Day8Solver.class,    Dec2016Day9Solver.class,    Dec2016Day10Solver.class,
                Dec2016Day11Solver.class,   Dec2016Day12Solver.class,   Dec2016Day13Solver.class,   Dec2016Day14Solver.class,   Dec2016Day15Solver.class,
                Dec2016Day16Solver.class,   Dec2016Day17Solver.class,   Dec2016Day18Solver.class,   Dec2016Day19Solver.class,   Dec2016Day20Solver.class,
                Dec2016Day21Solver.class,   Dec2016Day22Solver.class,   Dec2016Day23Solver.class,   Dec2016Day24Solver.class,   Dec2016Day25Solver.class
        );
    }

    private static List<Class<? extends Dec2017DaySolver<?>>> getSolvers2017() {
        return Lists.newArrayList(
                Dec2017Day1Solver.class,    Dec2017Day2Solver.class,    Dec2017Day3Solver.class,    Dec2017Day4Solver.class,    Dec2017Day5Solver.class,
                Dec2017Day6Solver.class,    Dec2017Day7Solver.class,    Dec2017Day8Solver.class,    Dec2017Day9Solver.class,    Dec2017Day10Solver.class,
                Dec2017Day11Solver.class,   Dec2017Day12Solver.class,   Dec2017Day13Solver.class,   Dec2017Day14Solver.class,   Dec2017Day15Solver.class,
                Dec2017Day16Solver.class,   Dec2017Day17Solver.class,   Dec2017Day18Solver.class,   Dec2017Day19Solver.class,   Dec2017Day20Solver.class,
                Dec2017Day21Solver.class//,   Dec2017Day22Solver.class//,   Dec2017Day23Solver.class//,   Dec2017Day24Solver.class//,   Dec2017Day25Solver.class
        );
    }
}
