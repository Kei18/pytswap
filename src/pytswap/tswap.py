import numpy as np
from .dist_table import DistTable
from .mapf_utils import Config, Configs, Coord, Grid, get_neighbors
from scipy.optimize import linear_sum_assignment
from copy import deepcopy


class TSWAP:
    def __init__(self, grid: Grid, starts: Config, targets: Config):
        self.grid = grid
        self.starts = starts
        self.targets = targets
        self.N = len(self.starts)

        # distance table
        self.dist_tables = [DistTable(grid, g) for g in targets]

        # assignment
        self.assigned_target_ind = np.arange(self.N)

        # cache
        self.NIL = self.N  # meaning \bot
        self.occupied_now = np.full(grid.shape, self.NIL, dtype=int)

    def assign_target(self):
        # Hungarian
        cost = np.full((self.N, self.N), np.inf)
        for i, s in enumerate(self.starts):
            for j in range(self.N):
                cost[i][j] = self.dist_tables[j].get(s)
        _, self.assigned_target_ind = linear_sum_assignment(cost)

    def next_vertex(self, i: int, v: Coord) -> Coord:
        D = self.dist_tables[self.assigned_target_ind[i]]
        return sorted(get_neighbors(self.grid, v), key=lambda u: D.get(u))[0]

    def step(self, Q_from: Config) -> Config:
        Q = deepcopy(Q_from)

        # update cache
        for i, v in enumerate(Q):
            self.occupied_now[v] = i

        for i in range(self.N):
            g_i_ind = self.assigned_target_ind[i]

            # stay on target
            if Q[i] == self.targets[g_i_ind]:
                continue
            u = self.next_vertex(i, Q[i])

            # move toward target
            j = self.occupied_now[u]
            if j == self.NIL:
                self.occupied_now[Q[i]] = self.NIL
                Q[i] = u
                self.occupied_now[u] = i
                continue

            # swap targets
            g_j_ind = self.assigned_target_ind[j]
            if Q[j] == self.targets[g_j_ind]:
                self.assigned_target_ind[i] = g_j_ind
                self.assigned_target_ind[j] = g_i_ind
                continue

            # deadlock resolution
            A = [i, j]
            while True:
                j = A[-1]
                if Q[j] == self.targets[self.assigned_target_ind[j]]:
                    break  # not deadlock
                v = self.next_vertex(j, Q[j])
                k = self.occupied_now[v]
                if k == self.NIL:
                    break  # not
                if k == i:
                    # rotate assginement
                    target_ind_last = self.assigned_target_ind[A[-1]]
                    for m in reversed(range(1, len(A))):
                        self.assigned_target_ind[A[m]] = self.assigned_target_ind[
                            A[m - 1]
                        ]
                    self.assigned_target_ind[A[0]] = target_ind_last
                    break
                if k in A:
                    break  # there is a deadlock without i
                A.append(k)

        # clean cache
        for i, v in enumerate(Q):
            self.occupied_now[v] = self.NIL

        return Q

    def solve(self) -> Configs:
        solution = [self.starts]
        targets_set = set(self.targets)

        # target assignment
        self.assign_target()

        # path planning
        while not set(solution[-1]) == targets_set:
            Q = self.step(solution[-1])
            solution.append(Q)

        return solution
