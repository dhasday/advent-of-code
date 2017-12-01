package dhasday.adventofcode.dec2015.solvers;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class Dec2015Day5SolverTest {

    private Dec2015Day5Solver underTest = new Dec2015Day5Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne("ugknbfddgicrmopn", true);
        validatePuzzleOne("aaa", true);
        validatePuzzleOne("jchzalrnumimnmhp", false);
        validatePuzzleOne("haegwjzuvuyypxyu", false);
        validatePuzzleOne("dvszwmarrgswjxmb", false);
    }

    @Test
    public void puzzleTwoExamples() {
        validatePuzzleTwo("qjhvhtzxzqqjkmpb", true);
        validatePuzzleTwo("xxyxx", true);
        validatePuzzleTwo("uurcxstgmygtbstg", false);
        validatePuzzleTwo("ieodomkazucvgmuy", false);
    }

    private void validatePuzzleOne(String input, boolean expected) {
        boolean actual = underTest.isStringValidV1(input);

        assertEquals(expected, actual);
    }

    private void validatePuzzleTwo(String input, boolean expected) {
        boolean actual = underTest.isStringValidV2(input);

        assertEquals(expected, actual);
    }

}