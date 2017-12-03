package dhasday.adventofcode.dec2015.solvers0x;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

public class Dec2015Day1SolverTest {

    private Dec2015Day1Solver underTest = new Dec2015Day1Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne("(())", 0);
        validatePuzzleOne("()()", 0);
        validatePuzzleOne("(((", 3);
        validatePuzzleOne("(()(()(", 3);
        validatePuzzleOne("))(((((", 3);
        validatePuzzleOne("())", -1);
        validatePuzzleOne("))(", -1);
        validatePuzzleOne(")))", -3);
        validatePuzzleOne(")())())", -3);
    }

    @Test
    public void puzzleTwoExamples() {
        validatePuzzleTwo(")", 1);
        validatePuzzleTwo("()())", 5);
        validatePuzzleTwo("()())())", 5);
    }

    private void validatePuzzleOne(String input, int expected) {
        Dec2015Day1Solver.FloorTracker actual = underTest.processInput(input);

        assertEquals(expected, actual.currentFloor);
    }

    private void validatePuzzleTwo(String input, Integer expected) {
        Dec2015Day1Solver.FloorTracker actual = underTest.processInput(input);

        assertEquals(expected, actual.firstBasementFloor);
    }
}