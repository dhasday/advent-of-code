import dec2015

dec2015_solvers = [
    dec2015.Day01Solver(), dec2015.Day02Solver(), dec2015.Day03Solver(), dec2015.Day04Solver(),
]

for solver in dec2015_solvers:
    solver.print_results()
