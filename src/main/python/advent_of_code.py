import dec2015
import dec2016
import dec2017
import dec2018

dec2015_solvers = [
    dec2015.Day01Solver(), dec2015.Day02Solver(), dec2015.Day03Solver(), dec2015.Day04Solver(), dec2015.Day05Solver(),
    dec2015.Day06Solver(), dec2015.Day07Solver(), dec2015.Day08Solver(), dec2015.Day09Solver(), dec2015.Day10Solver(),
]
dec2016_solvers = [
]
dec2017_solvers = [
]
dec2018_solvers = [
    dec2018.Day01Solver(), dec2018.Day02Solver(), dec2018.Day03Solver(), dec2018.Day04Solver(), dec2018.Day05Solver(),
    dec2018.Day06Solver(), dec2018.Day07Solver(), dec2018.Day08Solver(), dec2018.Day09Solver(),
]

all_solvers = []
all_solvers.extend(dec2015_solvers)
all_solvers.extend(dec2018_solvers)

for solver in all_solvers:
    solver.print_results()
