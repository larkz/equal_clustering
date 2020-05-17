from __future__ import print_function
from ortools.linear_solver import pywraplp
from equal_clustering_opt import *
import pickle as pkl

# https://developers.google.com/optimization/mip/mip_var_array

def create_data_model_ip():
  """Stores the data for the problem."""
  data = {}
  dm = dist_mat.transpose()
  x_cent = dm.shape[0]
  total_obs = dm.shape[1]
  dm = dist_mat.reshape(x_cent*total_obs)
  dm2 = np.tile((dm, -1*dm), 1 )
  cost_ip = np.tile(dm2, (k, 1))
  data['constraint_coeffs'] = cost_ip.tolist()

  consts = x_cent * np.ones(k)
  data['bounds'] = consts.tolist()

  data['obj_coeffs'] = (-1*dm).tolist()
  data['num_vars'] = dm.shape[0]
  data['num_constraints'] = k
  return data

def create_data_model():
  """Stores the data for the problem."""
  data = {}
  data['constraint_coeffs'] = [
      [5, 7, 9, 2, 1],
      [18, 4, -9, 10, 12],
      [4, 7, 3, 8, 5],
      [5, 13, 16, 3, -7],
  ]
  data['bounds'] = [250, 285, 211, 315]
  data['obj_coeffs'] = [7, 8, 2, 9, 6]
  data['num_vars'] = 5
  data['num_constraints'] = 4
  return data

def main():
  data = create_data_model()
  # Create the mip solver with the CBC backend.
  solver = pywraplp.Solver('simple_mip_program',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  infinity = solver.infinity()
  x = {}
  for j in range(data['num_vars']):
    x[j] = solver.BoolVar('x[%i]' % j )
  print('Number of variables =', solver.NumVariables())

  for i in range(data['num_constraints']):
    constraint = solver.RowConstraint(data['bounds'][i], data['bounds'][i], '')
    for j in range(data['num_vars']):
      constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])
  print('Number of constraints =', solver.NumConstraints())
  # In Python, you can also set the constraints as follows.
  # for i in range(data['num_constraints']):
  #  constraint_expr = \
  # [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
  #  solver.Add(sum(constraint_expr) <= data['bounds'][i])

  objective = solver.Objective()
  for j in range(data['num_vars']):
    objective.SetCoefficient(x[j], data['obj_coeffs'][j])
  objective.SetMaximization()
  # In Python, you can also set the objective as follows.
  # obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
  # solver.Maximize(solver.Sum(obj_expr))

  status = solver.Solve()
  output_list = []

  print(status)

  # if status == pywraplp.Solver.OPTIMAL:
  if 1:
    print('Objective value =', solver.Objective().Value())
    for j in range(data['num_vars']):
      print(x[j].name(), ' = ', x[j].solution_value())
      output_list.append(x[j].solution_value())
    print()
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
  else:
    print('The problem does not have an optimal solution.')
  
  with open('or_tools_output/objs.pkl', 'wb') as file_io:
    pkl.dump(output_list, file_io)


if __name__ == '__main__':
  main()
 