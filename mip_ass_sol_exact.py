from __future__ import print_function
from ortools.linear_solver import pywraplp
# from equal_clustering_opt import *
from equal_clustering_prep_elki import *
import pickle as pkl
import sys
from get_mse import *

# n_clus = 7
n_clus = sys.argv[1]
elki_result_obj = elki_cluster_obj_samp(int(n_clus))

k = elki_result_obj.k

solver = pywraplp.Solver('SolveAssignmentProblemMIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

cost = elki_result_obj.dist_mat.T.tolist()

num_depots = len(cost) # num_workers

num_wp = len(cost[1]) # num_tasks MUST
x = {}

for i in range(num_depots):
    for j in range(num_wp):
        x[i, j] = solver.BoolVar('x[%i,%i]' % (i, j))

# Objective
solver.Minimize(solver.Sum( [cost[i][j] * x[i,j] for i in range(num_depots) for j in range(num_wp)] ) )
# solver.Minimize(solver.Sum( [cost[i][j] for i in range(num_depots) for j in range(num_wp)] ) )
#  * x[i,j]

# Constraints

# Each wp is assigned to 1 depot.

for j in range(num_wp):
    solver.Add(solver.Sum([1 * x[i, j] for i in range(num_depots)]) == 1)

# Each depot is assigned to exactly k wp's.
# fac = 0.2
for i in range(num_depots):
    solver.Add(solver.Sum([1 * x[i, j] for j in range(num_wp)]) == k)


sol = solver.Solve()
print('Total cost = ', solver.Objective().Value())

output_list = []
for i in range(num_depots):
    for j in range(num_wp):
        if x[i, j].solution_value() > 0:
            print('depot %d assigned to wp %d.  Cost = %f' % (i, j, cost[i][j]))
            output_list.append([i, j])

with open('or_tools_output/ass_mip_elki_' + str(n_clus) + '.pkl', 'wb') as file_io:
    pkl.dump(output_list, file_io)

with open('or_tools_output/ass_mip_costs_elki_' + str(n_clus) + '.pkl', 'wb') as file_io:
    pkl.dump(cost, file_io)

print("Time = ", solver.WallTime(), " milliseconds")

