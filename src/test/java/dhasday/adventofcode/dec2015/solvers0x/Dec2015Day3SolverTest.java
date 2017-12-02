package dhasday.adventofcode.dec2015.solvers0x;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class Dec2015Day3SolverTest {

    private Dec2015Day3Solver underTest = new Dec2015Day3Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne(">", 2);
        validatePuzzleOne("^>v<", 4);
        validatePuzzleOne("^v^v^v^v^v", 2);
    }

    @Test
    public void puzzleTwoExamples() {
        validatePuzzleTwo("^v", 3);
        validatePuzzleTwo("^>v<", 3);
        validatePuzzleTwo("^v^v^v^v^v", 11);
    }

    private void validatePuzzleOne(String input, int expected) {
        int actual = underTest.deliverPresents(input, 1);

        assertEquals(expected, actual);
    }

    private void validatePuzzleTwo(String input, int expected) {
        int actual = underTest.deliverPresents(input, 2);

        assertEquals(expected, actual);
    }

}