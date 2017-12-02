package dhasday.adventofcode.dec2015.solvers0x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.common.collect.Sets;
import dhasday.adventofcode.DaySolver;

public class Dec2015Day9Solver implements DaySolver {

    private static final String INPUT_FILE = "src/main/resources/dec2015/9-input";

    private Pattern inputPattern = Pattern.compile("([0-9A-Za-z]+) to ([0-9A-Za-z]+) = (\\d+)");

    @Override
    public int getDayNumber() {
        return 9;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allStrings = getAllFileLines(INPUT_FILE);

        Map<String, Map<String, Integer>> travelDistances = loadTravelDistances(allStrings);

        return findShortestPath(travelDistances);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allStrings = getAllFileLines(INPUT_FILE);

        Map<String, Map<String, Integer>> travelDistances = loadTravelDistances(allStrings);

        return findLongestPath(travelDistances);
    }

    private Map<String, Map<String, Integer>> loadTravelDistances(List<String> allDistances) {
        Map<String, Map<String, Integer>> distances = new HashMap<>();

        allDistances.forEach(input -> {
            Matcher matcher = inputPattern.matcher(input);

            if (!matcher.matches()) {
                throw new RuntimeException("Unable to extract data from input: " + input);
            }

            String pointOne = matcher.group(1);
            String pointTwo = matcher.group(2);
            Integer distance = Integer.parseInt(matcher.group(3));

            if (!distances.containsKey(pointOne)) {
                distances.put(pointOne, new HashMap<>());
            }
            distances.get(pointOne).put(pointTwo, distance);

            if (!distances.containsKey(pointTwo)) {
                distances.put(pointTwo, new HashMap<>());
            }
            distances.get(pointTwo).put(pointOne, distance);
        });

        return distances;
    }

    private Integer findShortestPath(Map<String, Map<String, Integer>> travelDistances) {
        Set<String> allDestinations = travelDistances.keySet();

        Integer shortestPath = null;

        for (String destination : allDestinations) {
            Set<String> remainingDestinations = Sets.newHashSet(allDestinations);
            remainingDestinations.remove(destination);

            Integer currentShortestPath = findShortestPath(travelDistances, destination, remainingDestinations, 0);

            if (shortestPath != null) {
                shortestPath = Math.min(shortestPath, currentShortestPath);
            } else {
                shortestPath = currentShortestPath;
            }
        }

        return shortestPath;
    }

    private Integer findShortestPath(Map<String, Map<String, Integer>> travelDistances,
                                     String currentLocation,
                                     Set<String> remainingDestinations,
                                     Integer currentPathLength) {
        if (remainingDestinations.isEmpty()) {
            return currentPathLength;
        }

        Map<String, Integer> travelFromCurrentLocation = travelDistances.get(currentLocation);

        Integer shortestPath = null;

        for (String destination : remainingDestinations) {
            Set<String> destinationsLeft = Sets.newHashSet(remainingDestinations);
            destinationsLeft.remove(destination);
            Integer pathLength = currentPathLength + travelFromCurrentLocation.get(destination);

            Integer currentShortestPath = findShortestPath(travelDistances, destination, destinationsLeft, pathLength);

            if (shortestPath != null) {
                shortestPath = Math.min(shortestPath, currentShortestPath);
            } else {
                shortestPath = currentShortestPath;
            }
        }

        return shortestPath;
    }

    private Integer findLongestPath(Map<String, Map<String, Integer>> travelDistances) {
        Set<String> allDestinations = travelDistances.keySet();

        Integer longestPath = null;

        for (String destination : allDestinations) {
            Set<String> remainingDestinations = Sets.newHashSet(allDestinations);
            remainingDestinations.remove(destination);

            Integer currentLongestPath = findLongestPath(travelDistances, destination, remainingDestinations, 0);

            if (longestPath != null) {
                longestPath = Math.max(longestPath, currentLongestPath);
            } else {
                longestPath = currentLongestPath;
            }
        }

        return longestPath;
    }

    private Integer findLongestPath(Map<String, Map<String, Integer>> travelDistances,
                                     String currentLocation,
                                     Set<String> remainingDestinations,
                                     Integer currentPathLength) {
        if (remainingDestinations.isEmpty()) {
            return currentPathLength;
        }

        Map<String, Integer> travelFromCurrentLocation = travelDistances.get(currentLocation);

        Integer longestPath = null;

        for (String destination : remainingDestinations) {
            Set<String> destinationsLeft = Sets.newHashSet(remainingDestinations);
            destinationsLeft.remove(destination);
            Integer pathLength = currentPathLength + travelFromCurrentLocation.get(destination);

            Integer currentLongestPath = findLongestPath(travelDistances, destination, destinationsLeft, pathLength);

            if (longestPath != null) {
                longestPath = Math.max(longestPath, currentLongestPath);
            } else {
                longestPath = currentLongestPath;
            }
        }

        return longestPath;
    }
}
