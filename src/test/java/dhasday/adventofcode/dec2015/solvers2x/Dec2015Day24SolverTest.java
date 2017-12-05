package dhasday.adventofcode.dec2015.solvers2x;

import java.util.List;

import com.google.common.collect.Lists;
import javafx.util.Pair;
import org.junit.jupiter.api.Test;

class Dec2015Day24SolverTest {

    private Dec2015Day24Solver underTest = new Dec2015Day24Solver();

    @Test
    public void puzzleOneExample() {
        List<Integer> packageSizes = Lists.newArrayList(1, 2, 3, 4, 5, 7, 8, 9, 10, 11);
        packageSizes = Lists.reverse(packageSizes);

        Pair<Integer, Long> sizeEntanglementPair = underTest.determineMinEntanglement(packageSizes, 3);

        System.out.println(sizeEntanglementPair);
    }

}