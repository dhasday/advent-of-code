package dhasday.adventofcode.dec2015.solvers0x;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class Dec2015Day4SolverTest {

    private Dec2015Day4Solver underTest = new Dec2015Day4Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne("abcdef", 609043);
        validatePuzzleOne("pqrstuv", 1048970);
    }

    private void validatePuzzleOne(String input, int expected) {
        int actual = underTest.getFirstLeadingMultizeroHash(input, 5);

        assertEquals(expected, actual);
    }


}