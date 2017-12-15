package dhasday.adventofcode.dec2017.solvers0x;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.google.common.collect.Lists;
import com.google.common.collect.Sets;
import dhasday.adventofcode.common.DaySolver;
import org.apache.commons.lang3.StringUtils;

public class Dec2017Day7Solver extends DaySolver<String> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/7-input";

    private static final String INPUT_REGEX = "([a-z]+) \\((\\d+)\\)( -> ([a-z, ]+))?";

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);


    @Override
    public int getDayNumber() {
        return 7;
    }

    @Override
    public String solvePuzzleOne() {
        Map<String, Node> allNodes = loadInput();

        return findRootNodeName(allNodes);
    }

    @Override
    public String solvePuzzleTwo() {
        Map<String, Node> allNodes = loadInput();

        String rootNodeName = findRootNodeName(allNodes);

        Node nodeTree = buildNodeTree(allNodes, rootNodeName);
        Node unbalancedParentNode = findParentOfLowestUnbalancedNode(nodeTree);

        return String.valueOf(getWeightToBalanceTree(unbalancedParentNode));
    }

    private Map<String, Node> loadInput() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(this::loadInput)
                .collect(Collectors.toMap(node -> node.name, Function.identity()));
    }

    private Node loadInput(String line) {
        Matcher matcher = inputPattern.matcher(line);

        if (!matcher.matches()) {
            throw new RuntimeException("Fix your regex");
        }

        List<String> subNodes;
        if (StringUtils.isBlank(matcher.group(4))) {
            subNodes = Lists.newArrayList();
        } else {
            String[] nodeArray = matcher.group(4).split(", ");
            subNodes = Lists.newArrayList(nodeArray);
        }

        return new Node(
                matcher.group(1),
                Integer.valueOf(matcher.group(2)),
                subNodes
        );
    }

    private String findRootNodeName(Map<String, Node> allNodes) {
        Set<String> allNodeNames = Sets.newHashSet(allNodes.keySet());

        for (Node node : allNodes.values()) {
            allNodeNames.removeAll(node.subNodesNames);
        }

        return allNodeNames.stream().findFirst().get();
    }

    private Node buildNodeTree(Map<String, Node> allNodes, String rootNodeName) {
        Node rootNode = allNodes.get(rootNodeName);

        for (String subNodeName : rootNode.subNodesNames) {
            Node node = buildNodeTree(allNodes, subNodeName);
            rootNode.subNodes.add(node);
        }

        rootNode.fullWeight = getNodeWeight(rootNode);

        return rootNode;
    }

    private int getNodeWeight(Node node) {
        int weight = node.weight;

        for (Node subNode : node.subNodes) {
            weight += getNodeWeight(subNode);
        }

        return weight;
    }

    private Node findParentOfLowestUnbalancedNode(Node node) {
        if (isBalanced(node)) {
            return null;
        }

        for (Node child : node.subNodes) {
            if (!isBalanced(child)) {
                return findParentOfLowestUnbalancedNode(child);
            }
        }

        return node;
    }

    private boolean isBalanced(Node node) {
        Set<Integer> childValues = node.subNodes
                .stream()
                .map(child -> child.fullWeight)
                .collect(Collectors.toSet());

        return childValues.size() < 2;
    }

    private Integer getWeightToBalanceTree(Node unbalancedParent) {
        Integer expectedWeight = getExpectedChildWeight(unbalancedParent);

        for (Node child : unbalancedParent.subNodes) {
            int offset = expectedWeight - child.fullWeight;
            if (offset != 0) {
                return child.weight + offset;
            }
        }

        return null;
    }

    private Integer getExpectedChildWeight(Node parent) {
        List<Node> subNodes = parent.subNodes;
        if (subNodes.isEmpty()) {
            throw new RuntimeException("Is this a trick question? This node doesn't have any children");
        }

        if (subNodes.size() == 2) {
            throw new RuntimeException("How do I know which child is unbalanced if there are only 2?");
        }

        Map<Integer, Integer> childWeightOccurences = new HashMap<>();
        for (Node child : subNodes) {
            Integer curCount = childWeightOccurences.getOrDefault(child.fullWeight, 0);
            childWeightOccurences.put(child.fullWeight, curCount + 1);
        }
        return childWeightOccurences.entrySet()
                .stream()
                .sorted((e1, e2) -> e2.getValue().compareTo(e1.getValue()))
                .findFirst()
                .get() // It'll be ok IntelliJ, don't fret over this optional check
                .getKey();
    }

    private class Node {
        private final String name;
        private final int weight;
        private final List<String> subNodesNames;
        private final List<Node> subNodes;
        private Integer fullWeight;

        public Node(String name, int weight, List<String> subNodesNames) {
            this.name = name;
            this.weight = weight;
            this.subNodesNames = subNodesNames;
            this.subNodes = new ArrayList<>();
            this.fullWeight = null;
        }
    }
}
