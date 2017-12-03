package dhasday.adventofcode.dec2015.solvers1x;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

import com.google.common.collect.Lists;
import org.junit.jupiter.api.Test;

class Dec2015Day19SolverTest {

    private Dec2015Day19Solver underTest = new Dec2015Day19Solver();

    @Test
    public void puzzleTwoExampleOne() {
        List<Dec2015Day19Solver.Substitution> substitutions = Lists.newArrayList(
                new Dec2015Day19Solver.Substitution("e", "H"),
                new Dec2015Day19Solver.Substitution("e", "O"),
                new Dec2015Day19Solver.Substitution("H", "HO"),
                new Dec2015Day19Solver.Substitution("H", "OH"),
                new Dec2015Day19Solver.Substitution("O", "HH")
        );
        String sequence = "HOH";
        Integer startMoveCount = 0;

        Integer expected = 3;

        Integer actual = underTest.deconstructSequence(substitutions, sequence, startMoveCount);

        assertEquals(expected, actual);
    }

    @Test
    public void puzzleTwoExampleTwo() {
        List<Dec2015Day19Solver.Substitution> substitutions = Lists.newArrayList(
                new Dec2015Day19Solver.Substitution("e", "H"),
                new Dec2015Day19Solver.Substitution("e", "O"),
                new Dec2015Day19Solver.Substitution("H", "HO"),
                new Dec2015Day19Solver.Substitution("H", "OH"),
                new Dec2015Day19Solver.Substitution("O", "HH")
        );
        String sequence = "HOHOHO";
        Integer startMoveCount = 0;

        Integer expected = 6;

        Integer actual = underTest.deconstructSequence(substitutions, sequence, startMoveCount);

        assertEquals(expected, actual);
    }
}