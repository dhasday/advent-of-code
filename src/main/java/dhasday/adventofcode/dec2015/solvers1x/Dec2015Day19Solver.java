package dhasday.adventofcode.dec2015.solvers1x;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import dhasday.adventofcode.common.DaySolver;

public class Dec2015Day19Solver extends DaySolver<Integer> {

    private static final String SUBSTITUTIONS_FILE = "src/main/resources/dec2015/19-input-substitutions";
    private static final String SEQUENCE_FILE = "src/main/resources/dec2015/19-input-sequence";

    private static final String SUBSTITUTION_REGEX = "([A-Za-z0-9]+) .* ([A-Za-z0-9]+)";

    private static final Pattern SUBSTITUTION_PATTERN = Pattern.compile(SUBSTITUTION_REGEX);

    @Override
    public int getDayNumber() {
        return 19;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Substitution> allSubstitutions = loadSubstitutions(getAllFileLines(SUBSTITUTIONS_FILE));
        String sequence = getOnlyFileLine(SEQUENCE_FILE);

        Set<String> allUniqueReplacements = getAllUniqueReplacements(allSubstitutions, sequence);

        return allUniqueReplacements.size();
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Substitution> allSubstitutions = loadSubstitutions(getAllFileLines(SUBSTITUTIONS_FILE));
        String sequence = getOnlyFileLine(SEQUENCE_FILE);

        return deconstructSequence(allSubstitutions, sequence, 0);
    }

    private List<Substitution> loadSubstitutions(List<String> inputLines) {
        return inputLines.stream()
                .map(line -> {
                    Matcher matcher = SUBSTITUTION_PATTERN.matcher(line);

                    if (!matcher.matches()) {
                        throw new RuntimeException("Unable to extract data from input: " + line);
                    }

                    return new Substitution(matcher.group(1), matcher.group(2));
                })
                .collect(Collectors.toList());
    }

    Set<String> getAllUniqueReplacements(List<Substitution> substitutions, String input) {
        Set<String> allReplacements = new HashSet<>();

        substitutions.forEach(substitution -> allReplacements.addAll(getAllReplacements(substitution, input)));

        return allReplacements;
    }

    private Set<String> getAllReplacements(Substitution substitution, String input) {
        Set<String> allReplacements = new HashSet<>();
        int currentIndex = -1;

        do {
            currentIndex = input.indexOf(substitution.original, currentIndex + 1);


            if (currentIndex >= 0) {
                allReplacements.add(processSubstitution(substitution, input, currentIndex));
            }
        } while (currentIndex >= 0);

        return allReplacements;
    }

    Integer deconstructSequence(List<Substitution> substitutions, String sequence, Integer moveCount) {
        if ("e".equals(sequence)) {
            return moveCount;
        }

        for (Substitution substitution : substitutions) {
            int currentIndex = -1;
            do {
                currentIndex = sequence.indexOf(substitution.replacement, currentIndex + 1);

                if (currentIndex >= 0) {
                    String newSequence = unprocessSubstitution(substitution, sequence, currentIndex);

                    Integer newMoveCount = deconstructSequence(substitutions, newSequence, moveCount + 1);

                    if (newMoveCount != null) { // There's only one solution, so stop when we find it
                        return newMoveCount;
                    }
                }
            } while (currentIndex >= 0);
        }

        return null;
    }

    private String processSubstitution(Substitution substitution, String input, int matchStartIndex) {
        return input.substring(0, matchStartIndex)
                + input.substring(matchStartIndex).replaceFirst(substitution.original, substitution.replacement);
    }

    private String unprocessSubstitution(Substitution substitution, String input, int matchStartIndex) {
        return input.substring(0, matchStartIndex)
                + input.substring(matchStartIndex).replaceFirst(substitution.replacement, substitution.original);
    }

    public static class Substitution {
        private final String original;
        private final String replacement;

        public Substitution(String original, String replacement) {
            this.original = original;
            this.replacement = replacement;
        }
    }
}
