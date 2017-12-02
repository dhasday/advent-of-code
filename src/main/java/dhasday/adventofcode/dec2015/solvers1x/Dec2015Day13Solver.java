package dhasday.adventofcode.dec2015.solvers1x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.common.base.Joiner;
import com.google.common.collect.Lists;
import com.google.common.collect.Sets;
import dhasday.adventofcode.DaySolver;

public class Dec2015Day13Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/13-input";

    private static final String HAPPINESS_DELTA_REGEX = "([A-Za-z]+) .* (gain|lose) (\\d+) .* ([A-Za-z]+)\\.";

    private Pattern happinessDeltaPattern = Pattern.compile(HAPPINESS_DELTA_REGEX);

    @Override
    public int getDayNumber() {
        return 13;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allLines = getAllFileLines(INPUT_FILE);

        Map<String, Map<String, Integer>> happinessDeltas = loadHappinessDeltas(allLines);

        return determineMaxHappinessDelta(happinessDeltas);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allLines = getAllFileLines(INPUT_FILE);

        Map<String, Map<String, Integer>> happinessDeltas = loadHappinessDeltas(allLines);
        happinessDeltas = addExtraPerson(happinessDeltas, "Me", 0);

        return determineMaxHappinessDelta(happinessDeltas);
    }

    private Map<String, Map<String, Integer>> loadHappinessDeltas(List<String> allDeltas) {
        Map<String, Map<String, Integer>> happinessDeltas = new HashMap<>();

        allDeltas.forEach(input -> {
            Matcher matcher = happinessDeltaPattern.matcher(input);

            if (!matcher.matches()) {
                throw new RuntimeException("Unable to extract data from input: " + input);
            }

            String personOne = matcher.group(1);
            String personTwo = matcher.group(4);

            int delta = Integer.valueOf(matcher.group(3));
            if ("lose".equals(matcher.group(2))) {
                delta = - delta;
            }

            addDelta(happinessDeltas, personOne, personTwo, delta);
            addDelta(happinessDeltas, personTwo, personOne, delta);
        });

        return happinessDeltas;
    }

    private Map<String, Map<String, Integer>> addExtraPerson(Map<String, Map<String, Integer>> currentDeltas,
                                                             String newPerson,
                                                             int delta) {
        Set<String> existingPersons = currentDeltas.keySet();

        Map<String, Integer> newPersonDeltas = new HashMap<>();

        for (String person : existingPersons) {
            currentDeltas.get(person).put(newPerson, delta);
            newPersonDeltas.put(person, delta);
        }

        currentDeltas.put(newPerson, newPersonDeltas);

        return currentDeltas;
    }

    private void addDelta(Map<String, Map<String,Integer>> happinessDeltas,
                          String personOne,
                          String personTwo,
                          int delta) {
        Map<String, Integer> personDeltas;

        if (!happinessDeltas.containsKey(personOne)) {
            personDeltas = new HashMap<>();
            happinessDeltas.put(personOne, personDeltas);
        } else {
            personDeltas = happinessDeltas.get(personOne);
        }

        int newDelta = delta;
        if (personDeltas.containsKey(personTwo)) {
            newDelta += personDeltas.get(personTwo);
        }

        personDeltas.put(personTwo, newDelta);
    }

    private Integer determineMaxHappinessDelta(Map<String, Map<String, Integer>> happinessDeltas) {
        Set<String> allPersons = happinessDeltas.keySet();

        Integer maxDelta = null;

        for (String person : allPersons) {
            Set<String> remainingPersons = Sets.newHashSet(allPersons);
            remainingPersons.remove(person);

            List<String> seatingOrder = Lists.newArrayList(person);

            Integer currentMaxDelta = determineMaxDelta(happinessDeltas, seatingOrder, remainingPersons, 0);

            if (maxDelta != null) {
                maxDelta = Math.max(maxDelta, currentMaxDelta);
            } else {
                maxDelta = currentMaxDelta;
            }
        }

        return maxDelta;
    }

    private Integer determineMaxDelta(Map<String, Map<String, Integer>> happinessDeltas,
                                      List<String> seatingOrder,
                                      Set<String> remainingPersons,
                                      int currentDelta) {
        if (remainingPersons.isEmpty()) {
            String firstPerson = seatingOrder.get(0);
            String lastPerson = seatingOrder.get(seatingOrder.size() - 1);

            return currentDelta + happinessDeltas.get(firstPerson).get(lastPerson);
        }

        Integer maxDelta = null;

        String currentPerson = seatingOrder.get(seatingOrder.size() - 1);
        Map<String, Integer> currentPersonDeltas = happinessDeltas.get(currentPerson);

        for (String person : remainingPersons) {
            Set<String> personsLeft = Sets.newHashSet(remainingPersons);
            personsLeft.remove(person);

            List<String> currentSeatingOrder = Lists.newArrayList(seatingOrder);
            currentSeatingOrder.add(person);

            Integer delta = currentDelta + currentPersonDeltas.get(person);

            Integer currentMaxDelta = determineMaxDelta(happinessDeltas, currentSeatingOrder, personsLeft, delta);

            if (maxDelta != null) {
                maxDelta = Math.max(maxDelta, currentMaxDelta);
            } else {
                maxDelta = currentMaxDelta;
            }
        }

        return maxDelta;
    }

}
