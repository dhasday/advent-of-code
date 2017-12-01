package dhasday.adventofcode;

import java.util.List;

public interface DaySolver {

    int getDayNumber();

    Integer solvePuzzleOne();

    Integer solvePuzzleTwo();

    default List<String> getAllFileLines(String filename) {
        FileUtils fileUtils = new FileUtils();
        return fileUtils.loadFileLines(filename);
    }

    default String getOnlyFileLine(String filename) {
        FileUtils fileUtils = new FileUtils();
        return fileUtils.loadFileContents(filename);
    }

}
