package dhasday.adventofcode.dec2015.solvers1x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import com.google.common.collect.Maps;
import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day15Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2015/15-input";

    private static final String INPUT_REGEX = "([A-Za-z]+): .* (-?\\d+), .* (-?\\d+), .* (-?\\d+), .* (-?\\d+), .* (-?\\d+)";

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);

    @Override
    public int getDayNumber() {
        return 15;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Ingredient> allIngredients = allFileLines.stream()
                .map(this::loadIngredient)
                .collect(Collectors.toList());

        return determineMaxScore(new HashMap<>(), allIngredients, 100);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        List<Ingredient> allIngredients = allFileLines.stream()
                .map(this::loadIngredient)
                .collect(Collectors.toList());

        return determineMaxScoreWithCalories(new HashMap<>(), allIngredients, 100, 500);
    }

    private Ingredient loadIngredient(String input) {
        Matcher matcher = inputPattern.matcher(input);

        if (!matcher.matches()) {
            throw new RuntimeException("Unable to extract data from input: " + input);
        }

        return new Ingredient(
                matcher.group(1),
                Integer.valueOf(matcher.group(2)),
                Integer.valueOf(matcher.group(3)),
                Integer.valueOf(matcher.group(4)),
                Integer.valueOf(matcher.group(5)),
                Integer.valueOf(matcher.group(6))
        );
    }

    private Integer determineMaxScore(Map<Ingredient, Integer> currentRecipe,
                                      List<Ingredient> ingredients,
                                      int numTeaspoons) {
        if (numTeaspoons < 0
                || (ingredients.isEmpty() && numTeaspoons > 0)) {
            return 0;
        }
        if (ingredients.isEmpty() && numTeaspoons == 0) {
            return determineScore(currentRecipe);
        }

        Integer maxScore = 0;

        Ingredient currentIngredient = ingredients.get(0);
        List<Ingredient> remainingIngredients = ingredients.subList(1, ingredients.size());

        for (int i = 0; i <= numTeaspoons; i++) {
            Map<Ingredient, Integer> recipe = Maps.newHashMap(currentRecipe);
            recipe.put(currentIngredient, i);

            Integer currentScore = determineMaxScore(recipe, remainingIngredients, numTeaspoons - i);

            maxScore = Math.max(maxScore, currentScore);
        }

        return maxScore;
    }

    private Integer determineMaxScoreWithCalories(Map<Ingredient, Integer> currentRecipe,
                                                  List<Ingredient> ingredients,
                                                  int numTeaspoons,
                                                  int numCalories) {
        if (numTeaspoons < 0
                || numCalories < 0
                || (ingredients.isEmpty() && numTeaspoons > 0)
                || (ingredients.isEmpty() && numCalories != 0)) {
            return 0;
        }
        if (ingredients.isEmpty() && numTeaspoons == 0) {
            return determineScore(currentRecipe);
        }

        Integer maxScore = 0;

        Ingredient currentIngredient = ingredients.get(0);
        List<Ingredient> remainingIngredients = ingredients.subList(1, ingredients.size());

        for (int i = 0; i <= numTeaspoons; i++) {
            Map<Ingredient, Integer> recipe = Maps.newHashMap(currentRecipe);
            recipe.put(currentIngredient, i);

            Integer remainingTeaspoons = numTeaspoons - i;
            Integer remainingCalories = numCalories - (i * currentIngredient.calories);

            Integer currentScore = determineMaxScoreWithCalories(recipe, remainingIngredients, remainingTeaspoons, remainingCalories);

            maxScore = Math.max(maxScore, currentScore);
        }

        return maxScore;
    }

    private Integer determineScore(Map<Ingredient, Integer> ingredients) {
        int capacity = 0;
        int durabilility = 0;
        int flavor = 0;
        int texture = 0;

        for (Map.Entry<Ingredient, Integer> entry : ingredients.entrySet()) {
            Ingredient ingredient = entry.getKey();
            Integer amount = entry.getValue();

            capacity += (ingredient.capacity * amount);
            durabilility += (ingredient.durability * amount);
            flavor += (ingredient.flavor * amount);
            texture += (ingredient.texture * amount);
        }

        if (capacity < 0
                || durabilility < 0
                || flavor < 0
                || texture < 0) {
            return 0;
        }

        return capacity * durabilility * flavor * texture;
    }

    private class Ingredient {
        private String name;
        private Integer capacity;
        private Integer durability;
        private Integer flavor;
        private Integer texture;
        private Integer calories;

        Ingredient(String name,
                   Integer capacity,
                   Integer durability,
                   Integer flavor,
                   Integer texture,
                   Integer calories) {
            this.name = name;
            this.capacity = capacity;
            this.durability = durability;
            this.flavor = flavor;
            this.texture = texture;
            this.calories = calories;
        }
    }
}
