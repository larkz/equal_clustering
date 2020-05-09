import numpy as np
import pandas as pd
from ortools.linear_solver import pywraplp
from ortools.graph import pywrapgraph
from equal_clustering_prep_elki import *
import pickle as pkl
import sys
from get_mse import *

n_clus = 7
elki_result_obj = elki_cluster_obj(int(n_clus))

k = elki_result_obj.k

# Take a dividible number

# cost = np.tile(elki_result_obj.dist_mat, (1, k)) # the repetition here is inefficient
# cost = elki_result_obj.dist_mat[0:1*n_clus, 0:1*n_clus]

cost = np.tile(elki_result_obj.dist_mat, (1, k)) # the repetition here is inefficient
# cost = np.tile(elki_result_obj.dist_mat, (1, 10))[0:50,]

wp_len = len(cost)
batch_len = len(cost[0])

assignment = pywrapgraph.LinearSumAssignment()

for wp in range(wp_len):
    for batch in range(batch_len):
        if cost[wp][batch]:
            assignment.AddArcWithCost(wp, batch, int(cost[wp][batch]))

solve_status = assignment.Solve()

solutions = np.zeros([wp_len, 2])

if solve_status == assignment.OPTIMAL:
    print('Total cost = ', assignment.OptimalCost())
    print()
    for i in range(0, assignment.NumNodes()):
        print('Worker %d assigned to task %d.  Cost = %d' % (
            i,
            assignment.RightMate(i),
            assignment.AssignmentCost(i)))
        solutions[i, 0] = i
        solutions[i, 1] = assignment.RightMate(i) % n_clus
elif solve_status == assignment.INFEASIBLE:
    print('No assignment is possible.')
elif solve_status == assignment.POSSIBLE_OVERFLOW:
    print('Some input costs are too large and may cause an integer overflow.')

with open('or_tools_output/hung_sol_' + str(n_clus) + '_.pkl', 'wb') as file_io:
    pkl.dump(solutions, file_io)



'''
elif solve_status == assignment.INFEASIBLE:
    print('No assignment is possible.')
    return False
elif solve_status == assignment.POSSIBLE_OVERFLOW:
    print('Some input costs are too large and may cause an integer overflow.')
    return False
'''


