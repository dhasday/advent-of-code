from aoc import dec2015, dec2016, dec2017, dec2018, dec2019, dec2020

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
    dec2019.Day06Solver, dec2019.Day07Solver, dec2019.Day08Solver, dec2019.Day09Solver, dec2019.Day10Solver,
    dec2019.Day11Solver, dec2019.Day12Solver, dec2019.Day13Solver, dec2019.Day14Solver, dec2019.Day15Solver,
    dec2019.Day16Solver, dec2019.Day17Solver, dec2019.Day18Solver, dec2019.Day19Solver, dec2019.Day20Solver,
    dec2019.Day21Solver, dec2019.Day22Solver, dec2019.Day23Solver, dec2019.Day24Solver, dec2019.Day25Solver,
]
dec2020_solvers = [
    dec2020.Day01Solver, dec2020.Day02Solver, dec2020.Day03Solver, dec2020.Day04Solver, dec2020.Day05Solver,
    dec2020.Day06Solver, dec2020.Day07Solver, dec2020.Day08Solver, dec2020.Day09Solver, dec2020.Day10Solver,
    dec2020.Day11Solver, dec2020.Day12Solver, dec2020.Day13Solver,
    # dec2020.Day14Solver,
    # dec2020.Day15Solver,
    # dec2020.Day16Solver,
    # dec2020.Day17Solver,
    # dec2020.Day18Solver,
    # dec2020.Day19Solver,
    # dec2020.Day10Solver,
    # dec2020.Day21Solver,
    # dec2020.Day22Solver,
    # dec2020.Day23Solver,
    # dec2020.Day24Solver,
    # dec2020.Day25Solver,
]

all_solvers = []
all_solvers.extend(dec2015_solvers)
all_solvers.extend(dec2016_solvers)
all_solvers.extend(dec2017_solvers)
all_solvers.extend(dec2018_solvers)
all_solvers.extend(dec2019_solvers)
all_solvers.extend(dec2020_solvers)

# Slow Days (>5000 ms)
#   2015
#       Day  4  ~  13000 ms
#       Day  6  ~  28000 ms
#       Day 10  ~  16500 ms
#   2016
#   2017
#   2018
#       Day  5  ~   6600 ms
#       Day  6  ~   7900 ms
#       Day  9  ~   6800 ms
#       Day 11  ~  20000 ms
#       Day 14  ~  58000 ms
#       Day 15  ~   9800 ms
#       Day 18  ~  17500 ms
#   2019
#       Day  9  ~   6300 mx
#       Day 12  ~  15000 ms
#       Day 13  ~  12500 ms
#       Day 16  ~  57000 ms
#       Day 17  ~   6300 ms
#       Day 18  ~ 710000 ms
#       Day 19  ~  12500 ms
#       Day 21  ~  11900 ms
#   2020
#       Day 11  ~   5900 ms

for solver in all_solvers:
    solver().print_results()
