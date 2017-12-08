package dhasday.adventofcode.dec2016.solvers1x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import dhasday.adventofcode.DaySolver;
import javafx.util.Pair;

public class Dec2016Day10Solver implements DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/10-input";

    @Override
    public int getDayNumber() {
        return 10;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        Pair<Map<Integer, BotValue>, Map<Integer, Bot>> allBots = loadAllBots(allFileLines);

        processBots(allBots.getValue());

        return findBotProcessingValues(allBots.getValue(), 17, 61);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allFileLines = getAllFileLines(INPUT_FILE);

        Pair<Map<Integer, BotValue>, Map<Integer, Bot>> allBots = loadAllBots(allFileLines);

        processBots(allBots.getValue());
        processOutputs(allBots.getKey(), allBots.getValue());

        Map<Integer, BotValue> allOutputs = allBots.getKey();

        return productOfOutputs(allOutputs, 0, 1, 2);
    }

    private Pair<Map<Integer, BotValue>, Map<Integer, Bot>> loadAllBots(List<String> allInstructions) {
        String loadRegex = "value (\\d+) goes to bot (\\d+)";
        String distributeRegex =
                "bot (\\d+) gives low to (bot|output) (\\d+) and high to (bot|output) (\\d+)";

        Pattern loadPattern = Pattern.compile(loadRegex);
        Pattern distributePattern = Pattern.compile(distributeRegex);

        Map<Integer, Bot> allBots = new HashMap<>();
        Map<Integer, BotValue> allOutputs = new HashMap<>();
        for (String instruction : allInstructions) {
            Matcher loadMatcher = loadPattern.matcher(instruction);
            Matcher distributeMatcher = distributePattern.matcher(instruction);

            if (loadMatcher.matches()) {
                Integer botId = Integer.valueOf(loadMatcher.group(2));
                Integer value = Integer.valueOf(loadMatcher.group(1));

                Bot currentBot = allBots.get(botId);
                if (currentBot == null || currentBot.valueOne == null) {
                    currentBot = new Bot();
                    currentBot.valueOne = new BotValue(value);
                } else {
                    currentBot.valueTwo = new BotValue(value);
                }

                allBots.put(botId, currentBot);
            } else if (distributeMatcher.matches()) {
                Integer botId = Integer.valueOf(distributeMatcher.group(1));

                String lowTarget = distributeMatcher.group(2);
                Integer lowTargetId = Integer.valueOf(distributeMatcher.group(3));

                if ("bot".equals(lowTarget)) {
                    allBots.put(lowTargetId, addBotValue(allBots, lowTargetId, botId, false));
                } else {
                    allOutputs.put(lowTargetId, new BotValue(botId, false));
                }

                String highTarget = distributeMatcher.group(4);
                Integer highTargetId = Integer.valueOf(distributeMatcher.group(5));
                if ("bot".equals(highTarget)) {
                    allBots.put(highTargetId, addBotValue(allBots, highTargetId, botId, true));
                } else {
                    allOutputs.put(highTargetId, new BotValue(botId, true));
                }
            } else {
                throw new RuntimeException("No match: " + instruction);
            }

        }

        return new Pair<>(allOutputs, allBots);
    }

    private Bot addBotValue(Map<Integer, Bot> allBots, Integer botId, Integer fromBotId, Boolean highValue) {
        Bot bot = allBots.get(botId);
        if (bot == null) {
            bot = new Bot();
        }

        if (bot.valueOne == null) {
            bot.valueOne = new BotValue(fromBotId, highValue);
        } else {
            bot.valueTwo = new BotValue(fromBotId, highValue);
        }
        return bot;
    }

    private void processBots(Map<Integer, Bot> allBots) {
        for (Integer botId : allBots.keySet()) {
            processBot(allBots, botId);
        }
    }

    private Bot processBot(Map<Integer, Bot> allBots, Integer botId) {
        Bot bot = allBots.get(botId);

        BotValue valueOne = bot.valueOne;
        if (valueOne != null) {
            valueOne.value = resolveValue(allBots, valueOne);
        } else {
            throw new RuntimeException("No first value");
        }

        BotValue valueTwo = bot.valueTwo;
        if (valueTwo != null) {
            valueTwo.value = resolveValue(allBots, valueTwo);
        } else {
            throw new RuntimeException("No second value");
        }

        return bot;
    }

    private Integer resolveValue(Map<Integer, Bot> allBots, BotValue value) {
        if (value.value != null) {
            return value.value;
        }

        Bot fromBot = processBot(allBots, value.fromBotId);
        Integer fromBotValueOne = fromBot.valueOne.value;
        Integer fromBotValueTwo = fromBot.valueTwo.value;

        if (value.highOutput) {
            return fromBotValueOne > fromBotValueTwo ? fromBotValueOne : fromBotValueTwo;
        } else {
            return fromBotValueOne < fromBotValueTwo ? fromBotValueOne : fromBotValueTwo;
        }
    }

    private Integer findBotProcessingValues(Map<Integer, Bot> allBots, Integer valueOne, Integer valueTwo) {
        for (Integer botId : allBots.keySet()) {
            Bot bot = allBots.get(botId);

            Integer botValueOne = bot.valueOne.value;
            Integer botValueTwo = bot.valueTwo.value;
            if ((valueOne.equals(botValueOne) && valueTwo.equals(botValueTwo))
                || (valueOne.equals(botValueTwo) && valueTwo.equals(botValueOne))) {
                return botId;
            }
        }

        return null;
    }

    private void processOutputs(Map<Integer, BotValue> outputs, Map<Integer, Bot> bots) {
        for (Integer outputId : outputs.keySet()) {
            BotValue outputValue = outputs.get(outputId);
            outputValue.value = resolveValue(bots, outputValue);
        }
    }

    private int productOfOutputs(Map<Integer, BotValue> outputs, Integer... outputIds) {
        int product = 1;
        for (Integer outputId : outputIds) {
            product *= outputs.get(outputId).value;
        }
        return product;
    }


    private class Bot {
        private BotValue valueOne = null;
        private BotValue valueTwo = null;
    }

    private class BotValue {
        private Integer value;
        private Integer fromBotId;
        private Boolean highOutput;

        BotValue(Integer value) {
            this.value = value;
        }

        BotValue(Integer fromBotId, Boolean highOutput) {
            this.fromBotId = fromBotId;
            this.highOutput = highOutput;
        }
    }
}
