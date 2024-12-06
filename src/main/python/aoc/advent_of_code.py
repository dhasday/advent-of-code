from time import time

from aoc import (
    dec2015, dec2016, dec2017, dec2018, dec2019,
    dec2020, dec2021, dec2022, dec2023, dec2024,
)


def load_solvers_for_year(year_package):
    solvers = []
    for i in range(1, 26):
        solver_name = 'Day{:02d}Solver'.format(i)
        if hasattr(year_package, solver_name):
            solvers.append(getattr(year_package, solver_name))
    return solvers


years = [
    # dec2015,
    # dec2016,
    # dec2017,
    # dec2018,
    # dec2019,
    # dec2020,
    # dec2021,
    # dec2022,
    # dec2023,
    dec2024,
]

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
#       Day 15  ~  14000 ms
#       Day 22  ~  12000 ms
#       Day 23  ~  10000 ms
#   2021
#       Day 19  ~   7000 ms
#       Day 23  ~ ?????? ms
#   2022
#       Day 15  ~   8700 ms
#       Day 19  ~  42000 ms
#   2023
#       Day 17  ~   7200 ms
#       Day 21  ~   7100 ms
#       Day 23  ~ ?????? ms
#       Day 25  ~ ?????? ms
#   2024
#       Day  6  ~   7000 ms

for year in years:
    start_timestamp = int(time() * 1000.0)
    year_solvers = load_solvers_for_year(year)

    for solver in year_solvers:
        solver().print_results()

    end_timestamp = int(time() * 1000.0)
    print(f'{year.__name__} Elapsed Time: {end_timestamp - start_timestamp} ms\n')
