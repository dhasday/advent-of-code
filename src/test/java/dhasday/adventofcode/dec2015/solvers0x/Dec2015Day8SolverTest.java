package dhasday.adventofcode.dec2015.solvers0x;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class Dec2015Day8SolverTest {

    private Dec2015Day8Solver underTest = new Dec2015Day8Solver();

    @Test
    public void getCodeCharacterCount() {
        validateCodeCharacterCount("\"\"", 2);
        validateCodeCharacterCount("\"abc\"", 5);
        validateCodeCharacterCount("\"aaa\\\"aaa\"", 10);
        validateCodeCharacterCount("\"\\x27\"", 6);
        validateCodeCharacterCount("\"\\xae\"", 6);
        validateCodeCharacterCount("\"\\\\zrs\\\\syur\"", 13);
    }

    @Test
    public void getStringCharacterCount() {
        validateStringCharacterCount("\"\"", 0);
        validateStringCharacterCount("\"abc\"", 3);
        validateStringCharacterCount("\"aaa\\\"aaa\"", 7);
        validateStringCharacterCount("\"\\x27\"", 1);
        validateStringCharacterCount("\"\\xae\"", 1);
        validateStringCharacterCount("\"\\\\zrs\\\\syur\"", 9);
    }

    @Test
    public void getEscapedCharacterCount() {
        validateEscapedCharacterCount("\"\"", 6);
        validateEscapedCharacterCount("\"abc\"", 9);
        validateEscapedCharacterCount("\"aaa\\\"aaa\"", 16);
        validateEscapedCharacterCount("\"\\x27\"", 11);
    }

    private void validateCodeCharacterCount(String input, int expected) {
        int actual = underTest.getCodeCharacterCount(input);

        assertEquals(expected, actual);
    }

    private void validateStringCharacterCount(String input, int expected) {
        int actual = underTest.getStringCharacterCount(input);

        assertEquals(expected, actual);
    }

    private void validateEscapedCharacterCount(String input, int expected) {
        int actual = underTest.getEscapedCharacterCount(input);

        assertEquals(expected, actual);
    }

}