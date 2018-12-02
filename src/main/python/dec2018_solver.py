import dec2018

dec2018_solvers = [
    dec2018.Day01Solver(), dec2018.Day02Solver(), dec2018.Day03Solver(),
]

for solver in dec2018_solvers:
    solver.print_results()
