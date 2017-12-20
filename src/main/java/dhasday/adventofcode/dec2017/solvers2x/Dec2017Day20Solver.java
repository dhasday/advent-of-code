package dhasday.adventofcode.dec2017.solvers2x;

import java.util.*;
import java.util.stream.Collectors;

import javafx.util.Pair;
import org.apache.commons.lang3.tuple.MutableTriple;
import org.apache.commons.lang3.tuple.Triple;

import dhasday.adventofcode.dec2017.Dec2017DaySolver;

public class Dec2017Day20Solver extends Dec2017DaySolver<Integer> {

    private static final String INPUT_FILE = "src/main/resources/dec2017/20-input";

    // Based on running both parts of this puzzle for a while, there isn't any relevant activity above this number.
    private static final Integer HIGH_ENOUGH_ITERATIONS = 400;

    @Override
    public int getDay() {
        return 20;
    }

    @Override
    public Integer solvePuzzleOne() {
        List<Particle> allParticles = loadAllParticles();

        for (int i = 0; i < HIGH_ENOUGH_ITERATIONS; i++) {
            moveParticles(allParticles);
        }

        return findClosest(allParticles);
    }

    @Override
    public Integer solvePuzzleTwo() {
        List<Particle> allParticles = loadAllParticles();

        for (int i = 0; i < HIGH_ENOUGH_ITERATIONS; i++) {
            moveParticles(allParticles);
            removeCollisions(allParticles);
        }

        return allParticles.size();
    }

    private List<Particle> loadAllParticles() {
        return getAllFileLines(INPUT_FILE).stream()
                .map(this::loadParticle)
                .collect(Collectors.toList());
    }

    private Particle loadParticle(String line) {
        String[] vectors = line.split(", ");

        // Extract the CSV blocks
        String[] posVector = parseVector(vectors[0]);
        String[] velVector = parseVector(vectors[1]);
        String[] accVector = parseVector(vectors[2]);

        return new Particle(
                new MutableTriple<>(Long.valueOf(posVector[0]), Long.valueOf(posVector[1]), Long.valueOf(posVector[2])),
                new MutableTriple<>(Long.valueOf(velVector[0]), Long.valueOf(velVector[1]), Long.valueOf(velVector[2])),
                new MutableTriple<>(Long.valueOf(accVector[0]), Long.valueOf(accVector[1]), Long.valueOf(accVector[2]))
        );
    }

    private String[] parseVector(String vector) {
        return vector.substring(3, vector.length() - 1).split(",");
    }

    private void moveParticles(List<Particle> allParticles) {
        for (Particle particle : allParticles) {
            particle.velocity.left += particle.acceleration.left;
            particle.velocity.middle += particle.acceleration.middle;
            particle.velocity.right += particle.acceleration.right;

            particle.position.left += particle.velocity.left;
            particle.position.middle += particle.velocity.middle;
            particle.position.right += particle.velocity.right;
        }
    }

    private void removeCollisions(List<Particle> allParticles) {
        Map<Triple<Long,Long,Long>, Set<Particle>> positionsToParticles = new HashMap<>();

        for (Particle particle : allParticles) {
            if (!positionsToParticles.containsKey(particle.position)) {
                positionsToParticles.put(particle.position, new HashSet<>());
            }
            positionsToParticles.get(particle.position).add(particle);
        }

        positionsToParticles.forEach((k, v) -> {
            if (v.size() > 1) {
                allParticles.removeAll(v);
            }
        });
    }

    private int findClosest(List<Particle> allParticles) {
        List<Pair<Integer, Long>> distances = new ArrayList<>();

        for (int i = 0; i < allParticles.size(); i++) {
            distances.add(new Pair<>(i, calculateDistanceFromOrigin(allParticles.get(i))));
        }

        distances.sort(Comparator.comparingLong(Pair::getValue));

        return distances.get(0).getKey();
    }

    private long calculateDistanceFromOrigin(Particle particle) {
        return Math.abs(particle.position.left)
                + Math.abs(particle.position.middle)
                + Math.abs(particle.position.right);
    }

    private class Particle {
        private MutableTriple<Long, Long, Long> position;
        private MutableTriple<Long, Long, Long> velocity;
        private MutableTriple<Long, Long, Long> acceleration;

        Particle(MutableTriple<Long, Long, Long> position,
                 MutableTriple<Long, Long, Long> velocity,
                 MutableTriple<Long, Long, Long> acceleration) {
            this.position = position;
            this.velocity = velocity;
            this.acceleration = acceleration;
        }
    }
}
