package dhasday.adventofcode.dec2015.solvers1x;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class Dec2015Day11SolverTest {

    private Dec2015Day11Solver underTest = new Dec2015Day11Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne("abcdefgh", "abcdffaa");
        validatePuzzleOne("ghijklmn", "ghjaabcc");
    }

    private void validatePuzzleOne(String input, String expected) {
        String actual = underTest.determinNextPassword(input);

        assertEquals(expected, actual);
    }

}