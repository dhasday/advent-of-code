package dhasday.adventofcode.dec2015.solvers2x;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class Dec2015Day20SolverTest {

    private Dec2015Day20Solver underTest = new Dec2015Day20Solver();

    @Test
    public void calculatePresentsForHouse() {
        validatePuzzleOne(1, 10);
        validatePuzzleOne(2, 30);
        validatePuzzleOne(3, 40);
        validatePuzzleOne(4, 70);
        validatePuzzleOne(5, 60);
        validatePuzzleOne(6, 120);
        validatePuzzleOne(7, 80);
        validatePuzzleOne(8, 150);
        validatePuzzleOne(9, 130);
    }

    private void validatePuzzleOne(int houseNumber, Integer expected) {
        Integer actual = underTest.calculatePresentsForHouse(houseNumber, 10, null);

        assertEquals(expected, actual);
    }

}