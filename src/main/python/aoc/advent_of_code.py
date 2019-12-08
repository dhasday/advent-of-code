from aoc import dec2015, dec2016, dec2017, dec2018, dec2019

dec2015_solvers = [
    dec2015.Day01Solver, dec2015.Day02Solver, dec2015.Day03Solver, dec2015.Day04Solver, dec2015.Day05Solver,
    dec2015.Day06Solver, dec2015.Day07Solver, dec2015.Day08Solver, dec2015.Day09Solver, dec2015.Day10Solver,
    dec2015.Day11Solver,
]
dec2016_solvers = [
]
dec2017_solvers = [
]
dec2018_solvers = [
    dec2018.Day01Solver, dec2018.Day02Solver, dec2018.Day03Solver, dec2018.Day04Solver, dec2018.Day05Solver,
    dec2018.Day06Solver, dec2018.Day07Solver, dec2018.Day08Solver, dec2018.Day09Solver, dec2018.Day10Solver,
    dec2018.Day11Solver, dec2018.Day12Solver, dec2018.Day13Solver, dec2018.Day14Solver, dec2018.Day15Solver,
    dec2018.Day16Solver, dec2018.Day17Solver, dec2018.Day18Solver, dec2018.Day19Solver, dec2018.Day20Solver,
    dec2018.Day21Solver, dec2018.Day22Solver, dec2018.Day23Solver, dec2018.Day24Solver, dec2018.Day25Solver,
]
dec2019_solvers = [
    dec2019.Day01Solver, dec2019.Day02Solver, dec2019.Day03Solver, dec2019.Day04Solver, dec2019.Day05Solver,
    dec2019.Day06Solver, dec2019.Day07Solver, dec2019.Day08Solver, dec2019.Day09Solver,
]

all_solvers = []
all_solvers.extend(dec2015_solvers)
all_solvers.extend(dec2018_solvers)
all_solvers.extend(dec2019_solvers)

# Slow Days (>5000 ms)
#   2015
#       Day  4  ~ 8500 ms
#       Day  6  ~ 7500 ms
#       Day 10  ~ 5000 ms
#   2016
#   2017
#   2018
#       Day 14  ~15000 ms
#   2019

for solver in all_solvers:
    solver().print_results()
