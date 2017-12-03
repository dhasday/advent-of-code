package dhasday.adventofcode.dec2015.solvers1x;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;

import com.google.common.collect.Lists;
import org.junit.jupiter.api.Test;

class Dec2015Day17SolverTest {

    private Dec2015Day17Solver underTest = new Dec2015Day17Solver();

    @Test
    public void puzzleOneExample() {
        List<Integer> containers = Lists.newArrayList(20, 15, 10, 5, 5);
        Integer numLiters = 25;

        Integer expected = 4;

        Integer actual = underTest.getSolutionCount(containers, numLiters);

        assertEquals(expected, actual);
    }
}