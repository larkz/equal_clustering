from __future__ import print_function
from ortools.linear_solver import pywraplp
from equal_clustering_opt import *
import pickle as pkl

# https://developers.google.com/optimization/assignment/assignment_mip

def main():
  solver = pywraplp.Solver('SolveAssignmentProblemMIP',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

  cost = dist_mat.tolist()

  num_workers = len(cost)
  
  num_tasks = len(cost[1])
  x = {}

  for i in range(num_workers):
    for j in range(num_tasks):
      x[i, j] = solver.BoolVar('x[%i,%i]' % (i, j))

  # Objective
  solver.Minimize(solver.Sum([cost[i][j] * x[i,j] for i in range(num_workers)
                                                  for j in range(num_tasks)]))

  # Constraints

  # Each worker is assigned to at most 1 task.

  for i in range(num_workers):
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

  # Each task is assigned to exactly one worker.

  for j in range(num_tasks):
    solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == k)

  # Each team takes on two tasks.
  
  sol = solver.Solve()
  output_list = []

  print('Total cost = ', solver.Objective().Value())
  print()
  for i in range(num_workers):
    for j in range(num_tasks):
      if x[i, j].solution_value() > 0:
        print('Worker %d assigned to task %d.  Cost = %f' % (
              i,
              j,
              cost[i][j]))
        output_list.append([i, j])
  
  with open('or_tools_output/ass_mip.pkl', 'wb') as file_io:
    pkl.dump(output_list, file_io)

  print()
  print("Time = ", solver.WallTime(), " milliseconds")

if __name__ == '__main__':
  main()
