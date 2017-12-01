package dhasday.adventofcode.dec2015.solvers;

import static org.junit.jupiter.api.Assertions.assertEquals;

import dhasday.adventofcode.dec2015.domain.Day1FloorTracker;
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
        Day1FloorTracker actual = underTest.processInput(input);

        assertEquals(expected, actual.getCurrentFloor());
    }

    private void validatePuzzleTwo(String input, Integer expected) {
        Day1FloorTracker actual = underTest.processInput(input);

        assertEquals(expected, actual.getFirstBasementFloor());
    }
}