package dhasday.adventofcode.dec2015.solvers;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

public class Dec2015Day2SolverTest {

    private Dec2015Day2Solver underTest = new Dec2015Day2Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne("2x3x4", 58);
        validatePuzzleOne("1x1x10", 43);
    }

    @Test
    public void puzzleTwoExamples() {
        validatePuzzleTwo("2x3x4", 34);
        validatePuzzleTwo("1x1x10", 14);
    }

    private void validatePuzzleOne(String input, int expected) {
        int actual = underTest.calculateNeededWrappingPaper(input);

        assertEquals(expected, actual);
    }

    private void validatePuzzleTwo(String input, int expected) {
        int actual = underTest.calculateNeededRibbon(input);

        assertEquals(expected, actual);
    }
}