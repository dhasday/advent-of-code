package dhasday.adventofcode.dec2015.solvers1x;

import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.google.common.collect.Sets;
import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day14Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/14-input";

    private static final String INPUT_REGEX = "([A-Za-z]+) .* (\\d+) .* (\\d+) .* (\\d+) .*";

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);

    @Override
    public int getDayNumber() {
        return 14;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        return allFileLines.stream()
                .map(this::processInputLine)
                .map(reindeer -> calculateDistance(reindeer, 2503))
                .max(Comparator.naturalOrder())
                .orElseThrow(() -> new RuntimeException("Are you sure that there was data in that file?"));
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        Set<Reindeer> allReindeer = allFileLines.stream()
                .map(this::processInputLine)
                .collect(Collectors.toSet());

        Map<String, Integer> scores = calculateScores(allReindeer, 2503);

        return scores.values()
                .stream()
                .max(Comparator.naturalOrder())
                .orElseThrow(() -> new RuntimeException("Are you sure that there was data in that file?"));
    }

    private Reindeer processInputLine(String inputLine) {
        //    Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.

        Matcher matcher = inputPattern.matcher(inputLine);

        if (!matcher.matches()) {
            throw new RuntimeException("Unable to extract data from input: " + inputLine);
        }

        return new Reindeer(
                matcher.group(1),
                Integer.valueOf(matcher.group(2)),
                Integer.valueOf(matcher.group(3)),
                Integer.valueOf(matcher.group(4))
        );
    }

    private Integer calculateDistance(Reindeer reindeer, int time) {
        for (int t = 0; t < time; t++) {
            reindeer.processSecond();
        }

        return reindeer.distanceTravelled;
    }

    private Map<String, Integer> calculateScores(Set<Reindeer> reindeers, int time) {
        Map<String, Integer> currentScores = new HashMap<>();
        reindeers.forEach(reindeer -> currentScores.put(reindeer.name, 0));

        for (int t = 0; t < time; t++) {
            reindeers.forEach(Reindeer::processSecond);

            Set<String> leadReindeers = new HashSet<>();
            Integer leadDistance = null;

            for (Reindeer reindeer : reindeers) {
                if (leadDistance == null || reindeer.distanceTravelled > leadDistance) {
                    leadReindeers = Sets.newHashSet(reindeer.name);
                    leadDistance = reindeer.distanceTravelled;
                } else if (reindeer.distanceTravelled.equals(leadDistance)) {
                    leadReindeers.add(reindeer.name);
                }
            }

            leadReindeers.forEach(reindeer -> currentScores.put(reindeer, currentScores.get(reindeer) + 1));
        }

        return currentScores;
    }

    private class Reindeer {
        private String name;
        private Integer velocity;
        private Integer flyTime;
        private Integer restTime;

        private Integer currentVelocity;
        private Integer stateRemainingTime;
        private Integer distanceTravelled;

        Reindeer(String name, Integer velocity, Integer flyTime, Integer restTime) {
            this.name = name;
            this.velocity = velocity;
            this.flyTime = flyTime;
            this.restTime = restTime;

            this.currentVelocity = velocity;
            this.stateRemainingTime = flyTime;
            this.distanceTravelled = 0;
        }

        void processSecond() {
            distanceTravelled += currentVelocity;

            if (stateRemainingTime == 1) {
                if (currentVelocity == 0) {
                    currentVelocity = velocity;
                    stateRemainingTime = flyTime;
                } else {
                    currentVelocity = 0;
                    stateRemainingTime = restTime;
                }
            } else {
                stateRemainingTime--;
            }
        }
    }
}
