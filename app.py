import argparse
from pathlib import Path

from pytswap import (
    TSWAP,
    get_grid,
    get_scenario,
    get_random_scenario,
    is_valid_amapf_solution,
    save_configs_for_visualizer,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--map-file",
        type=str,
        default=str(Path(__file__).parent / "assets/random-32-32-10.map"),
        required=True,
    )
    parser.add_argument(
        "-i",
        "--scen-file",
        type=str,
        default="",
    )
    parser.add_argument(
        "-N",
        "--num-agents",
        type=int,
        default=200,
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="output.txt",
    )
    parser.add_argument("-s", "--seed", type=int, default=0)
    args = parser.parse_args()

    # define problem instance
    grid = get_grid(args.map_file)
    if Path(args.scen_file).is_file():
        starts, targets = get_scenario(args.scen_file, args.num_agents)
    else:
        starts, targets = get_random_scenario(grid, args.num_agents, seed=args.seed)

    # solve unlabeled MAPF
    planner = TSWAP(grid, starts, targets)
    plan = planner.solve()

    # validation: True -> feasible solution
    print(
        f"solved: {is_valid_amapf_solution(grid, starts, targets, plan)},",
        f"makespan: {len(plan) - 1}",
    )

    # save result
    save_configs_for_visualizer(plan, args.output_file)
