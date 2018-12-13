import dec2015
import dec2016
import dec2017
import dec2018

dec2015_solvers = [
    dec2015.Day01Solver(), dec2015.Day02Solver(), dec2015.Day03Solver(), dec2015.Day04Solver(), dec2015.Day05Solver(),
    dec2015.Day06Solver(), dec2015.Day07Solver(), dec2015.Day08Solver(), dec2015.Day09Solver(), dec2015.Day10Solver(),
    dec2015.Day11Solver(),
]
dec2016_solvers = [
]
dec2017_solvers = [
]
dec2018_solvers = [
    dec2018.Day01Solver(), dec2018.Day02Solver(), dec2018.Day03Solver(), dec2018.Day04Solver(), dec2018.Day05Solver(),
    dec2018.Day06Solver(), dec2018.Day07Solver(), dec2018.Day08Solver(), dec2018.Day09Solver(), dec2018.Day10Solver(),
    dec2018.Day11Solver(), dec2018.Day12Solver(), dec2018.Day13Solver(),
]

all_solvers = []
all_solvers.extend(dec2015_solvers)
all_solvers.extend(dec2018_solvers)

# Slow Days
#   2015
#       Day  4  ~8000 ms
#       Day  6  ~7000 ms
#       Day 10  ~5000 ms
#       Day 11  ~1300 ms
#   2016
#   2017
#   2018
#       Day  5  ~2000 ms
#       Day  6  ~1500 ms
#       Day  9  ~3000 ms
#       Day 11  ~4000 ms

for solver in all_solvers:
    solver.print_results()
