package dhasday.adventofcode.dec2015.solvers1x;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.google.common.collect.Sets;
import dhasday.adventofcode.dec2015.Dec2015DaySolver;
import org.apache.commons.lang3.StringUtils;

public class Dec2015Day12Solver extends Dec2015DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/12-input";

    private ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public int getDay() {
        return 12;
    }

    @Override
    public Integer solvePuzzleOne() {
        String input = getOnlyFileLine(INPUT_FILE);

        return sumAllNumbersInString(input);
    }

    @Override
    public Integer solvePuzzleTwo() {
        String input = getOnlyFileLine(INPUT_FILE);

        return sumAllNonRedObjectsInJson(input);
    }

    Integer sumAllNumbersInString(String input) {
        return findAllNumbers(input).stream()
                .mapToInt(i -> i)
                .sum();
    }

    private List<Integer> findAllNumbers(String input) {
        Pattern pattern = Pattern.compile("-?\\d+");
        Matcher matcher = pattern.matcher(input);

        List<String> values = new ArrayList<>();
        while(matcher.find()) {
            values.add(matcher.group(0));
        }

        return values.stream()
                .filter(StringUtils::isNotBlank)
                .map(Integer::valueOf)
                .collect(Collectors.toList());
    }

    Integer sumAllNonRedObjectsInJson(String input) {
        String cleanedInput = removeAllObjectsWithRed(input);
        return sumAllNumbersInString(cleanedInput);
    }

    private String removeAllObjectsWithRed(String input) {
        try {
            JsonNode json = objectMapper.readTree(input);

            if (json.isArray()) {
                json = processJsonArray(json);
            } else if (json.isObject()) {
                json = processJsonObject(json);
            }

            return objectMapper.writeValueAsString(json);
        } catch (IOException e) {
            throw new RuntimeException("Failed to remove red from JSON");
        }
    }

    private JsonNode processJsonArray(JsonNode input) {
        ArrayNode result = objectMapper.createArrayNode();

        for (JsonNode node : input) {
            if (node.isArray()) {
                result.add(processJsonArray(node));
            } else if (node.isObject()) {
                result.add(processJsonObject(node));
            } else {
                result.add(node);
            }
        }

        return result;
    }

    private JsonNode processJsonObject(JsonNode input) {
        ObjectNode result = objectMapper.createObjectNode();

        Set<String> fieldNames = Sets.newHashSet(input.fieldNames());

        for (String fieldName : fieldNames) {
            JsonNode node = input.get(fieldName);

            if (node.isArray()) {
                result.set(fieldName, processJsonArray(node));
            } else if (node.isObject()) {
                result.set(fieldName, processJsonObject(node));
            } else if (node.isTextual() && "red".equalsIgnoreCase(node.textValue())) {
                return objectMapper.createObjectNode();
            } else {
                result.set(fieldName, node);
            }
        }

        return result;
    }

}
