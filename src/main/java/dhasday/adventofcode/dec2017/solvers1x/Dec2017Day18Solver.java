package dhasday.adventofcode.dec2017.solvers1x;

import java.util.*;
import java.util.function.BiFunction;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day18Solver extends Dec2017DaySolver<Long> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/18-input";

    @Override
    public int getDay() {
        return 18;
    }

    @Override
    public Long solvePuzzleOne() {
        List<String> instructions = getAllFileLines(INPUT_FILE);
        Map<String, Long> state = loadInitialState();

        return findFirstRecoveredValue(instructions, state);
    }

    @Override
    public Long solvePuzzleTwo() {
        List<String> instructions = getAllFileLines(INPUT_FILE);

        Map<String, Long> stateZero = loadInitialState();
        stateZero.put("p", 0L);

        Map<String, Long> stateOne = loadInitialState();
        stateOne.put("p", 1L);

        Queue<Long> zeroValues = new LinkedList<>();
        Queue<Long> oneValues = new LinkedList<>();

        Program programZero = new Program(instructions, stateZero, zeroValues, oneValues);
        Program programOne = new Program(instructions, stateOne, oneValues, zeroValues);

        while (true) {
            if (!programZero.runStep() && !programOne.runStep()) {
                return programOne.outputCount;
            }
        }
    }

    private Map<String, Long> loadInitialState() {
        Map<String, Long> state = new HashMap<>();
        state.put("a", 0L);
        state.put("b", 0L);
        state.put("f", 0L);
        state.put("i", 0L);
        state.put("p", 0L);
        return state;
    }

    private Long findFirstRecoveredValue(List<String> instructions, Map<String, Long> state) {
        Deque<Long> values = new LinkedList<>();

        Program program = new Program(instructions, state, values, values);

        Long lastSound = null;

        while (true) {
            String[] instruction = program.getCurrentInstruction();
            if (instruction == null) {
                return null;
            }
            Op currentOp = Op.forSymbol(instruction[0]);

            switch (currentOp) {
                case SOUND:
                    lastSound = program.getValue(instruction[1]);
                    break;
                case RECOVER:
                    if (program.getValue(instruction[1]) != 0) {
                        return lastSound;
                    }
                    break;
            }

            program.runStep();
        }
    }

    private static class Program {
        private List<String> instructions;
        private Map<String, Long> state;

        private Queue<Long> inputQueue;
        private Queue<Long> outputQueue;

        private int curIns;
        private long outputCount;

        Program(List<String> instructions,
                Map<String, Long> state,
                Queue<Long> inputQueue,
                Queue<Long> outputQueue) {
            this.instructions = instructions;
            this.state = state;

            this.inputQueue = inputQueue;
            this.outputQueue = outputQueue;

            this.curIns = 0;
            this.outputCount = 0;
        }

        private long getValue(String input) {
            try {
                return Long.valueOf(input);
            } catch (NumberFormatException nfe) {
                return state.computeIfAbsent(input, i -> 0L);
            }
        }

        private String[] getCurrentInstruction() {
            if (curIns < 0 || curIns >= instructions.size()) {
                return null;
            }

            return instructions.get(curIns).split(" ");
        }

        private boolean runStep() {
            if (curIns < 0 || curIns >= instructions.size()) {
                return false;
            }

            String[] ins = instructions.get(curIns).split(" ");

            return Op.forSymbol(ins[0]).processFunction.apply(ins, this);
        }
    }

    private enum Op {
        SOUND("snd", (ins, program) -> {
            program.outputQueue.add(program.getValue(ins[1]));
            program.outputCount++;
            program.curIns++;
            return true;
        }),
        RECOVER("rcv", (ins, program) -> {
            Long possibleValue = program.inputQueue.poll();
            if (possibleValue == null) {
                return false;
            } else {
                program.state.put(ins[1], possibleValue);
                program.curIns++;
                return true;
            }
        }),
        JUMP_GREATER_THAN_ZERO("jgz",  (ins, program) -> {
            if (program.getValue(ins[1]) > 0) {
                program.curIns += program.getValue(ins[2]);
            } else {
                program.curIns++;
            }
            return true;
        }),
        SET("set", (ins, program) -> {
            program.state.put(ins[1], program.getValue(ins[2]));
            program.curIns++;
            return true;
        }),
        ADD("add", (ins, program) -> {
            program.state.put(ins[1], program.getValue(ins[1]) + program.getValue(ins[2]));
            program.curIns++;
            return true;
        }),
        MULTIPLY("mul", (ins, program) -> {
            program.state.put(ins[1], program.getValue(ins[1]) * program.getValue(ins[2]));
            program.curIns++;
            return true;
        }),
        MODULO("mod", (ins, program) -> {
            program.state.put(ins[1], program.getValue(ins[1]) % program.getValue(ins[2]));
            program.curIns++;
            return true;
        }),
        ;

        final String symbol;
        final BiFunction<String[], Program, Boolean> processFunction;

        Op(String symbol, BiFunction<String[], Program, Boolean> processFunction) {
            this.symbol = symbol;
            this.processFunction = processFunction;
        }

        private static Op forSymbol(String symbol) {
            return Arrays.stream(values())
                    .filter(o -> o.symbol.equals(symbol))
                    .findFirst()
                    .orElseThrow(() -> new RuntimeException("Unknown symbol: " + symbol));
        }
    }
}
