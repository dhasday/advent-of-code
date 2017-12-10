package dhasday.adventofcode.common;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;

import javafx.util.Pair;

public class AStarSearch<T> {

    public List<T> findShortestPath(T start,
                                    T end,
                                    BiFunction<T, T, Integer> heuristicCostEstimate,
                                    Function<T, Set<Pair<T, Integer>>> findAdjacentNodes) {
        Map<T, AStarNode> closedSet = new HashMap<>();
        Map<T, AStarNode> openSet = new HashMap<>();

        AStarNode startNode = new AStarNode(start, null, 0, heuristicCostEstimate.apply(start, end));
        openSet.put(start, startNode);

        while (!openSet.isEmpty()) {
            AStarNode currentNode = getNodeWithLowestFScore(openSet);
            if (currentNode.value.equals(end)) {
                return reconstructPathToNode(currentNode);
            }

            openSet.remove(currentNode.value);
            closedSet.put(currentNode.value, currentNode);

            Set<Pair<T, Integer>> adjacentValues = findAdjacentNodes.apply(currentNode.value);
            for (Pair<T, Integer> adjacentValueDistancePair : adjacentValues) {
                T adjacentValue = adjacentValueDistancePair.getKey();
                Integer adjacentDistance = adjacentValueDistancePair.getValue();

                if (closedSet.containsKey(adjacentValue)) {
                    continue;
                }

                AStarNode adjacentNode = openSet.get(adjacentValue);
                int possibleGScore = currentNode.gScore + adjacentDistance;

                if (adjacentNode == null || adjacentNode.gScore < possibleGScore) {
                    adjacentNode = new AStarNode(
                            adjacentValue,
                            currentNode,
                            possibleGScore,
                            heuristicCostEstimate.apply(adjacentValue, end)
                    );
                }

                openSet.put(adjacentValue, adjacentNode);
            }
        }

        return null;
    }

    private AStarNode getNodeWithLowestFScore(Map<T, AStarNode> openSet) {
        AStarNode lowestNode = null;

        for (AStarNode node : openSet.values()) {
            if (lowestNode == null || node.fScore < lowestNode.fScore) {
                lowestNode = node;
            }
        }

        return lowestNode;
    }

    private List<T> reconstructPathToNode(AStarNode node) {
        List<T> path = new LinkedList<>();
        path.add(0, node.value);

        if (node.previousNode != null) {
            path.addAll(0, reconstructPathToNode(node.previousNode));
        }

        return path;
    }

    private class AStarNode {
        private T value;
        private AStarNode previousNode;

        private int gScore;
        private int hScore;
        private int fScore;

        AStarNode(T value, AStarNode previousNode, int gScore, int hScore) {
            this.value = value;
            this.previousNode = previousNode;

            this.gScore = gScore;
            this.hScore = hScore;
            this.fScore = gScore + hScore;
        }
    }
}
