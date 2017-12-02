package dhasday.adventofcode.dec2015.solvers1x;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.junit.jupiter.api.Test;

class Dec2015Day12SolverTest {

    private Dec2015Day12Solver underTest = new Dec2015Day12Solver();

    @Test
    public void puzzleOneExamples() {
        validatePuzzleOne("[1,2,3]", 6);
        validatePuzzleOne("{\"a\":2,\"b\":4}", 6);
        validatePuzzleOne("[[[3]]]", 3);
        validatePuzzleOne("{\"a\":{\"b\":4},\"c\":-1}", 3);
        validatePuzzleOne("{\"a\":[-1,1]}", 0);
        validatePuzzleOne("[-1,{\"a\":1}]", 0);
        validatePuzzleOne("[]", 0);
        validatePuzzleOne("{}", 0);
    }

    @Test
    public void puzzleTwoExamples() {
        validatePuzzleTwo("[1,2,3]", 6);
        validatePuzzleTwo("[1,{\"c\":\"red\",\"b\":2},3]", 4);
        validatePuzzleTwo("{\"d\":\"red\",\"e\":[1,2,3,4],\"f\":5}", 0);
        validatePuzzleTwo("[1,\"red\",5]", 6);
    }

    private void validatePuzzleOne(String input, Integer expected) {
        Integer actual = underTest.sumAllNumbersInString(input);

        assertEquals(expected, actual);
    }

    private void validatePuzzleTwo(String input, Integer expected) {
        Integer actual = underTest.sumAllNonRedObjectsInJson(input);

        assertEquals(expected, actual);
    }
}