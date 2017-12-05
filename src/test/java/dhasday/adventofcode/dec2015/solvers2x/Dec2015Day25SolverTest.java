package dhasday.adventofcode.dec2015.solvers2x;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class Dec2015Day25SolverTest {

    private Dec2015Day25Solver underTest = new Dec2015Day25Solver();

    @Test
    public void puzzleOneExamples() {
        long startValue = 20151125;

        validatePuzzleOne(startValue, 1, 1, 20151125);
        validatePuzzleOne(startValue, 2, 1, 31916031);
        validatePuzzleOne(startValue, 3, 1, 16080970);
        validatePuzzleOne(startValue, 4, 1, 24592653);
        validatePuzzleOne(startValue, 5, 1, 77061);
        validatePuzzleOne(startValue, 6, 1, 33071741);

        validatePuzzleOne(startValue, 1, 2, 18749137);
        validatePuzzleOne(startValue, 2, 2, 21629792);
        validatePuzzleOne(startValue, 3, 2, 8057251);
        validatePuzzleOne(startValue, 4, 2, 32451966);
        validatePuzzleOne(startValue, 5, 2, 17552253);
        validatePuzzleOne(startValue, 6, 2, 6796745);

        validatePuzzleOne(startValue, 1, 3, 17289845);
        validatePuzzleOne(startValue, 2, 3, 16929656);
        validatePuzzleOne(startValue, 3, 3, 1601130);
        validatePuzzleOne(startValue, 4, 3, 21345942);
        validatePuzzleOne(startValue, 5, 3, 28094349);
        validatePuzzleOne(startValue, 6, 3, 25397450);
    }

    private void validatePuzzleOne(long startValue, int row, int col, long expected) {
        long actual = underTest.calculateValue(startValue, row, col);

        assertEquals(expected, actual);
    }
}