package dhasday.adventofcode.dec2016.solvers2x;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;

import com.google.common.collect.Sets;
import dhasday.adventofcode.common.AStarSearch;
import dhasday.adventofcode.dec2016.Dec2016DaySolver;
import javafx.util.Pair;

public class Dec2016Day24Solver extends Dec2016DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/24-input";

    private AStarSearch aStarSearch = new AStarSearch();

    @Override
    public int getDay() {
        return 24;
    }

    @Override
    public Integer solvePuzzleOne() {
        char[][] grid = loadGrid(INPUT_FILE);

        Map<Integer, Pair<Integer, Integer>> points = findPoints(grid);

        return findShortestPath(grid, points, false);
    }

    @Override
    public Integer solvePuzzleTwo() {
        char[][] grid = loadGrid(INPUT_FILE);

        Map<Integer, Pair<Integer, Integer>> points = findPoints(grid);

        return findShortestPath(grid, points, true);
    }

    private char[][] loadGrid(String inputFile) {
        int sizeX = 183;
        int sizeY =39;

        char[][] grid = new char[183][39];

        List<String> allFileLines = getAllFileLines(inputFile);

        for (int i = 0; i < sizeY; i++) {
            String currentRow = allFileLines.get(i);
            for (int j = 0; j < sizeX; j++) {
                grid[j][i] = currentRow.charAt(j);
            }
        }

        return grid;
    }

    private Map<Integer, Pair<Integer, Integer>> findPoints(char[][] grid) {
        Map<Integer, Pair<Integer, Integer>> points = new HashMap<>();

        for (int x = 0; x < grid.length; x++) {
            for (int y = 0; y < grid[x].length; y++) {
                char val = grid[x][y];
                if (val != '#' && val != '.') {
                    points.put(Integer.valueOf(val + ""), new Pair<>(x, y));
                }
            }
        }

        return points;
    }

    private Integer findShortestPath(char[][] grid, Map<Integer, Pair<Integer, Integer>> points, boolean returnToZero) {
        Map<Pair<Integer, Integer>, Integer> shortestPairs = new HashMap<>();

        for (Map.Entry<Integer, Pair<Integer, Integer>> start : points.entrySet()) {
            for (Map.Entry<Integer, Pair<Integer, Integer>> end : points.entrySet()) {
                if (start == end) {
                    continue;
                }

                List<Pair<Integer, Integer>> shortestPath = aStarSearch.findShortestPath(
                        start.getValue(),
                        end.getValue(),
                        getCostEstimator(),
                        getAdjacentNodeLocator(grid)
                );

                shortestPairs.put(new Pair<>(start.getKey(), end.getKey()), shortestPath.size() - 1);
            }
        }

        return determineShortestPathSum(shortestPairs, returnToZero);
    }

    private BiFunction<Pair<Integer, Integer>, Pair<Integer, Integer>, Integer> getCostEstimator() {
        return (p1, p2) -> Math.abs(p2.getValue() - p1.getValue()) + Math.abs(p2.getKey() - p1.getKey());
    }

    private Function<Pair<Integer, Integer>, Set<Pair<Pair<Integer, Integer>, Integer>>> getAdjacentNodeLocator(char[][] grid) {
        return (p) -> {
            int sizeX = grid.length;
            int sizeY = grid[p.getKey()].length;

            int curX = p.getKey();
            int curY = p.getValue();

            Set<Pair<Pair<Integer, Integer>, Integer>> adjacentPairs = new HashSet<>();

            if (curX > 0) {
                int newX = curX - 1;
                int newY = curY;

                if (grid[newX][newY] != '#') {
                    adjacentPairs.add(new Pair<>(new Pair<>(newX, newY), 1));
                }
            }
            if (curX < (sizeX - 1)) {
                int newX = curX + 1;
                int newY = curY;

                if (grid[newX][newY] != '#') {
                    adjacentPairs.add(new Pair<>(new Pair<>(newX, newY), 1));
                }
            }

            if (curY > 0) {
                int newX = curX;
                int newY = curY - 1;

                if (grid[newX][newY] != '#') {
                    adjacentPairs.add(new Pair<>(new Pair<>(newX, newY), 1));
                }
            }
            if (curY < (sizeY - 1)) {
                int newX = curX;
                int newY = curY + 1;

                if (grid[newX][newY] != '#') {
                    adjacentPairs.add(new Pair<>(new Pair<>(newX, newY), 1));
                }
            }

            return adjacentPairs;
        };
    }

    private Integer determineShortestPathSum(Map<Pair<Integer, Integer>, Integer> shortestPairs, boolean returnToZero) {
        Map<Integer, Map<Integer, Integer>> expandedPairs = new HashMap<>();

        for (Map.Entry<Pair<Integer, Integer>, Integer> shortPair : shortestPairs.entrySet()) {
            int pointOne = shortPair.getKey().getKey();
            int pointTwo = shortPair.getKey().getValue();

            if (!expandedPairs.containsKey(pointOne)) {
                expandedPairs.put(pointOne, new HashMap<>());
            }
            if (!expandedPairs.containsKey(pointTwo)) {
                expandedPairs.put(pointTwo, new HashMap<>());
            }

            expandedPairs.get(pointOne).put(pointTwo, shortPair.getValue());
            expandedPairs.get(pointTwo).put(pointOne, shortPair.getValue());
        }


        Set<Integer> remainingPoints = Sets.newHashSet(expandedPairs.keySet());
        remainingPoints.remove(0);
        return determineShortestPathSum(expandedPairs, 0, remainingPoints, returnToZero);
    }

    private Integer determineShortestPathSum(Map<Integer, Map<Integer, Integer>> expandedPairs,
                                             int currentPoint,
                                             Set<Integer> remainingPoints,
                                             boolean returnToZero) {
        if (remainingPoints.isEmpty()) {
            if (returnToZero) {
                return expandedPairs.get(currentPoint).get(0);
            } else {
                return 0;
            }
        }

        Map<Integer, Integer> distancesFromStart = expandedPairs.get(currentPoint);

        Integer shortestSum = null;

        for (Integer nextPoint : remainingPoints) {
            if (nextPoint == currentPoint) {
                continue;
            }

            Set<Integer> newRemainingPoints = Sets.newHashSet(remainingPoints);
            newRemainingPoints.remove(nextPoint);

            Integer possibleShortest = determineShortestPathSum(expandedPairs, nextPoint, newRemainingPoints, returnToZero);

            if (possibleShortest != null) {
                if (shortestSum == null) {
                    shortestSum = possibleShortest + distancesFromStart.get(nextPoint);
                } else {
                    shortestSum = Math.min(shortestSum, possibleShortest + distancesFromStart.get(nextPoint));
                }
            }
        }

        return shortestSum;
    }
}
