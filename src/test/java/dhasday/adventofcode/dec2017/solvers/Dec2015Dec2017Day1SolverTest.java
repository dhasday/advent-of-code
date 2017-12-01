package dhasday.adventofcode.dec2017.solvers;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class Dec2015Dec2017Day1SolverTest {

    private Dec2017Day1Solver underTest = new Dec2017Day1Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne("1122", 3);
        validatePuzzleOne("1111", 4);
        validatePuzzleOne("1234", 0);
        validatePuzzleOne("91212129", 9);
    }

    @Test
    public void puzzleTwoExamples() {
        validatePuzzleTwo("1212", 6);
        validatePuzzleTwo("1221", 0);
        validatePuzzleTwo("123425", 4);
        validatePuzzleTwo("123123", 12);
        validatePuzzleTwo("12131415", 4);
    }

    private void validatePuzzleOne(String input, int expected) {
        int actual = underTest.sumOfConsecutiveDigits(input);

        assertEquals(expected, actual);
    }

    private void validatePuzzleTwo(String input, int expected) {
        int actual = underTest.sumOfRotatedDigits(input);

        assertEquals(expected, actual);
    }
}