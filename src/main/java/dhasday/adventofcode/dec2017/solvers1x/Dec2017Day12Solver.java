package dhasday.adventofcode.dec2017.solvers1x;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day12Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/12-input";

    @Override
    public int getDay() {
        return 12;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allInputLines = getAllFileLines(INPUT_FILE);

        Map<Integer, Set<Integer>> connectedNodes = loadAllConnectedNodes(allInputLines);

        Set<Integer> allConnectedToZero = findNodesConnectedToTarget(connectedNodes, 0);

        return allConnectedToZero.size();
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allInputLines = getAllFileLines(INPUT_FILE);

        Map<Integer, Set<Integer>> connectedNodes = loadAllConnectedNodes(allInputLines);

        Set<Set<Integer>> allGroups = new HashSet<>();
        Set<Integer> closedSet = new HashSet<>();

        for (Integer node : connectedNodes.keySet()) {
            if (closedSet.contains(node)) {
                continue;
            }

            Set<Integer> nodeGroup = findNodesConnectedToTarget(connectedNodes, node);
            allGroups.add(nodeGroup);
            closedSet.addAll(nodeGroup);
        }

        return allGroups.size();
    }

    private Map<Integer, Set<Integer>> loadAllConnectedNodes(List<String> inputLines) {
        // Input Format : 0 <-> 412, 480, 777, 1453

        Map<Integer, Set<Integer>> connectedNodes = new HashMap<>();
        for (String inputLine : inputLines) {
            String[] splitLine = inputLine.split(" <-> ");

            Set<Integer> connections = Arrays.stream(splitLine[1].split(", "))
                    .map(Integer::valueOf)
                    .collect(Collectors.toSet());

            connectedNodes.put(Integer.valueOf(splitLine[0]), connections);
        }
        return connectedNodes;
    }

    private Set<Integer> findNodesConnectedToTarget(Map<Integer, Set<Integer>> allNodes, Integer target) {
        Set<Integer> openSet = new HashSet<>();
        Set<Integer> closedSet = new HashSet<>();

        Set<Integer> allConnected = new HashSet<>();

        openSet.add(target);
        allConnected.add(target);

        while (!openSet.isEmpty()) {
            Integer next = openSet.iterator().next();
            openSet.remove(next);
            closedSet.add(next);

            Set<Integer> connectedNodes = allNodes.get(next);

            allConnected.addAll(connectedNodes);

            for (Integer node : connectedNodes) {
                if (closedSet.contains(node) || openSet.contains(node)) {
                    continue;
                }

                openSet.add(node);
            }
        }

        return allConnected;
    }
}
