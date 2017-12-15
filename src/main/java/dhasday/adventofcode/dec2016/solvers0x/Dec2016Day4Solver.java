package dhasday.adventofcode.dec2016.solvers0x;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import dhasday.adventofcode.common.DaySolver;

public class Dec2016Day4Solver extends DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2016/4-input";

    private static final String INPUT_REGEX = "([a-z-]+)-(\\d+)\\[([a-z]{5})]";

    private Pattern inputPattern = Pattern.compile(INPUT_REGEX);

    @Override
    public int getDayNumber() {
        return 4;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<String> allRooms = getAllFileLines(INPUT_FILE);

        return allRooms.stream()
                .map(this::loadRoom)
                .filter(this::isValidRoom)
                .mapToInt(room -> room.sector)
                .sum();
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<String> allRooms = getAllFileLines(INPUT_FILE);

        return allRooms.stream()
                .map(this::loadRoom)
                .filter(this::isValidRoom)
                .filter(this::isNorthPoleRoom)
                .mapToInt(room -> room.sector)
                .sum();
    }

    private Room loadRoom(String input) {
        Matcher matcher = inputPattern.matcher(input);

        if (!matcher.matches()) {
            throw new RuntimeException("Fix your matcher");
        }

        return new Room(matcher.group(1), Integer.valueOf(matcher.group(2)), matcher.group(3));
    }

    private boolean isValidRoom(Room room) {
        String checksum = calculateChecksum(room.encryptedName);
        return checksum.equals(room.checksum);
    }

    private String calculateChecksum(String roomName) {
        Map<Character, Integer> letterCount = new HashMap<>();

        for (int i = 0; i < roomName.length(); i++) {
            Character curChar = roomName.charAt(i);
            if (curChar == '-') {
                continue;
            }

            Integer curCount = letterCount.get(curChar);
            if (curCount == null) {
                curCount = 0;
            }

            letterCount.put(curChar, curCount + 1);
        }

        List<Character> checksumChars = letterCount.entrySet()
                .stream()
                .sorted((e1, e2) -> {
                    int charCountOne = e1.getValue();
                    int charCountTwo = e2.getValue();

                    if (charCountOne != charCountTwo) {
                        return Integer.compare(charCountTwo, charCountOne);
                    }

                    return e1.getKey().compareTo(e2.getKey());
                })
                .map(Map.Entry::getKey)
                .limit(5)
                .collect(Collectors.toList());

        String checksum = "";
        for (Character character : checksumChars) {
            checksum += character;
        }
        return checksum;
    }

    private boolean isNorthPoleRoom(Room room) {
        return "northpole object storage".equals(decodeRoomName(room));
    }

    private String decodeRoomName(Room room) {
        String decodedName = "";

        for (int i = 0; i < room.encryptedName.length(); i++) {
            decodedName += decodeLetter(room.encryptedName.charAt(i), room.sector);
        }

        return decodedName;
    }

    private char decodeLetter(char letter, int rotateNTimes) {
        if (letter == '-') {
            return ' ';
        }

        return (char) ((((letter - 'a') + rotateNTimes) % 26) + 'a');
    }

    private class Room {
        private final String encryptedName;
        private final Integer sector;
        private final String checksum;

        Room(String encryptedName, Integer sector, String checksum) {
            this.encryptedName = encryptedName;
            this.sector = sector;
            this.checksum = checksum;
        }
    }
}
