import numpy as np

from pytswap import TSWAP, is_valid_amapf_solution, get_random_scenario


def test_DeadlockDetection():
    grid = np.array([[True, True, True, True]])
    starts = [(0, 0), (0, 3)]
    targets = [(0, 3), (0, 0)]

    # deadlock detection
    planner = TSWAP(grid, starts, targets)
    plan = [starts]
    for _ in range(3):
        plan.append(planner.step(plan[-1]))

    assert is_valid_amapf_solution(grid, starts, targets, plan)


def test_TSWAP():
    grid = np.full((20, 20), True)
    N = 50
    starts, targets = get_random_scenario(grid, N)
    planner = TSWAP(grid, starts, targets)
    plan = planner.solve()
    assert is_valid_amapf_solution(grid, starts, targets, plan)
