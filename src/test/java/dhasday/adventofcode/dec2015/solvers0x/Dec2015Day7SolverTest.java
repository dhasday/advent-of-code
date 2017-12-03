package dhasday.adventofcode.dec2015.solvers0x;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.Map;

import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Lists;
import org.junit.jupiter.api.Test;

class Dec2015Day7SolverTest {

    private Dec2015Day7Solver underTest = new Dec2015Day7Solver();

    @Test
    public void puzzleOneExampleOne() {
        List<String> exampleOneInput = Lists.newArrayList(
                "123 -> x",
                "456 -> y",
                "x AND y -> d",
                "x OR y -> e",
                "x LSHIFT 2 -> f",
                "y RSHIFT 2 -> g",
                "NOT x -> h",
                "NOT y -> i"
        );
        Map<String, Integer> expected = ImmutableMap.<String, Integer>builder()
                .put("d", 72)
                .put("e", 507)
                .put("f", 492)
                .put("g", 114)
                .put("h", 65412)
                .put("i", 65079)
                .put("x", 123)
                .put("y", 456)
                .build();

        Map<String, Integer> actual = underTest.processAllInstructions(exampleOneInput, ImmutableMap.of());

        assertEquals(expected, actual);
    }

    @Test
    public void puzzleOneExampleTwo() {
        List<String> exampleOneInput = Lists.newArrayList(
                "x AND y -> d",
                "x OR y -> e",
                "x LSHIFT 2 -> f",
                "y RSHIFT 2 -> g",
                "NOT x -> h",
                "NOT y -> i",
                "123 -> x",
                "456 -> y"
        );
        Map<String, Integer> expected = ImmutableMap.<String, Integer>builder()
                .put("d", 72)
                .put("e", 507)
                .put("f", 492)
                .put("g", 114)
                .put("h", 65412)
                .put("i", 65079)
                .put("x", 123)
                .put("y", 456)
                .build();

        Map<String, Integer> actual = underTest.processAllInstructions(exampleOneInput, ImmutableMap.of());

        assertEquals(expected, actual);
    }

}