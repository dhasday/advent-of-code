package dhasday.adventofcode.dec2017.solvers2x;

import com.google.common.math.LongMath;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

/**
 *  Most of this one ended up being manually investigating what the instructions were doing and
 *  then doing these minor calculations to determine the results.
 *
 *  Simplified Instruction Translation
 *  ----------------------------------
 *  Init all registers to 0
 *
 *  b = 79
 *  c = 79
 *
 *  Part 2 (Extra) Setup
 *      a = 1
 *      b = b * 100 + 100000 = 107900
 *      c = b + 17000        = 124900
 *
 *  for (n = b; n < b + 17000; n += 17)
 *      f = 1
 *
 *      for (d = 2; d < b; d++)
 *          for (e = 2; 2 < b; e++)
 *              if (d * e - b == 0)
 *                  f = 0
 *
 *      if (f == 0) {
 *          h++
 *      }
 *
 *  Original Translation
 *  --------------------
 *
 *  Map<String, Long> state = new HashMap<>();
 *  state.put("a", 1L);
 *  state.put("b", 0L);
 *  state.put("c", 0L);
 *  state.put("d", 0L);
 *  state.put("e", 0L);
 *  state.put("f", 0L);
 *  state.put("g", 0L);
 *  state.put("h", 0L);
 *
 *  // Part One Setup Instructions
 *  state.put("b", 79L);
 *  state.put("c", 79L);
 *
 *  // Part Two Setup Instructions
 *  state.put("b", 79 * 100 + 100000);
 *  state.put("c", state.get("b") + 17000);
 *
 *  do {
 *      state.put("f", 1L);
 *      state.put("d", 2L);
 *
 *      do {
 *          state.put("e", 2L);
 *
 *          do {
 *              state.put("g", state.get("d") * state.get("e") - state.get("b"));
 *
 *              if (state.get("g") == 0) {
 *                  state.put("f", 0L);
 *              }
 *
 *              state.put("e", state.get("e") + 1);
 *              state.put("g", state.get("e") - state.get("b"));
 *
 *          } while (state.get("g") != 0);
 *
 *          state.put("d", state.get("d") + 1);
 *          state.put("g", state.get("d") - state.get("b"));
 *
 *      } while (state.get("g") != 0);
 *
 *      if (state.get("f") == 0) {
 *          state.put("h", state.get("h") + 1);
 *      }
 *
 *      state.put("g", state.get("b") - state.get("c"));
 *
 *      if (state.get("g") != 0) {
 *          state.put("b", state.get("b") + 17);
 *      }
 *  } while (state.get("g") != 0);
 *
 *  return state.get("h");
 */
public class Dec2017Day23Solver extends Dec2017DaySolver<Integer> {

    private static final Integer INPUT = 79;

    @Override
    public int getDay() {
        return 23;
    }

    /**
     *  Original solution just built on {@link dhasday.adventofcode.dec2017.solvers1x.Dec2017Day18Solver}
     *  modifying the instruction execution logic to count the number of multiply operations instead of
     *  handling sounds. Updated to this simplified form based on results from part 2.
     *
     *  Part one was just ends up iterating over 2->79 in registers 'd' and 'e', multiplying them together
     *  and comparing to 79 (the value in 'b')
     */
    @Override
    public Integer solvePuzzleOne() {
        return (INPUT - 2) * (INPUT - 2);
    }

    @Override
    public Integer solvePuzzleTwo() {
        int startNum = (INPUT * 100) + 100000;

        int nonPrimeCount = 0;

        for (int num = startNum; num <= startNum + 17000; num += 17) {
            if (!LongMath.isPrime(num)) {
                nonPrimeCount++;
            }
        }

        return nonPrimeCount;
    }
}
