from __future__ import print_function
from optlang import Model, Variable, Constraint, Objective

# this is essentially a discrete neoclassical model
# we have three agents

# each agent can produce a certain quantity based on a certain cost
# Variables t_i_j type='integer'
# where i is the seller and j is the buyer

# each agent has a time constraint which can be used to produce things
# \sum_{j=0\land j \neq i}^{n} c(t_i_j) < Z

# each agent must buy and sell goods with exactly the same value
# sales_i = \sum_{j=0\land j \neq i}^{n} p_i * t_i_j
# purchases_i = \sum_{j=0\land j \neq i}^{n} p_i * t_j_i
# \sum_{j=0\land j \neq i}^{n} p_i * t_i_j = \sum_{j=0\land j \neq i}^{n} p_i * t_j_i

# Transaction variables where t_i_j stands for i selling x amount to j

# actors cannot buy their own products so t_i_i is not necessary

#t_1_1 = Variable('t_1_1', lb=0, type='integer')
t_1_2 = Variable('t_1_2', lb=0, type='integer')
t_1_3 = Variable('t_1_3', lb=0, type='integer')

t_2_1 = Variable('t_2_1', lb=0, type='integer')
#t_2_2 = Variable('t_2_2', lb=0, type='integer')
t_2_3 = Variable('t_2_3', lb=0, type='integer')

t_3_1 = Variable('t_3_1', lb=0, type='integer')
t_3_2 = Variable('t_3_2', lb=0, type='integer')
#t_3_3 = Variable('t_3_3', lb=0, type='integer')

# production variables for each actor

prod_1_1_1 = Variable('prod_1_1_1', lb=0, type='integer')
prod_1_2_1 = Variable('prod_1_2_1', lb=0, type='integer')
prod_1_3_1 = Variable('prod_1_3_1', lb=0, type='integer')
prod_1_1_2 = Variable('prod_1_1_2', lb=0, type='integer')
prod_1_2_2 = Variable('prod_1_2_2', lb=0, type='integer')
prod_1_3_2 = Variable('prod_1_3_2', lb=0, type='integer')

prod_2_1_1 = Variable('prod_2_1_1', lb=0, type='integer')
prod_2_2_1 = Variable('prod_2_2_1', lb=0, type='integer')
prod_2_3_1 = Variable('prod_2_3_1', lb=0, type='integer')
prod_2_1_2 = Variable('prod_2_1_2', lb=0, type='integer')
prod_2_2_2 = Variable('prod_2_2_2', lb=0, type='integer')
prod_2_3_2 = Variable('prod_2_3_2', lb=0, type='integer')

prod_3_1_1 = Variable('prod_3_1_1', lb=0, type='integer')
prod_3_2_1 = Variable('prod_3_2_1', lb=0, type='integer')
prod_3_3_1 = Variable('prod_3_3_1', lb=0, type='integer')
prod_3_1_2 = Variable('prod_3_1_2', lb=0, type='integer')
prod_3_2_2 = Variable('prod_3_2_2', lb=0, type='integer')
prod_3_3_2 = Variable('prod_3_3_2', lb=0, type='integer')

# production with minimum batch sizes
c_batch_prod_1_1 = Constraint(8 * prod_1_1_1 + 7 * prod_1_2_1 + 3 * prod_1_3_1 - t_1_2, lb=0, ub=0)
c_batch_prod_1_2 = Constraint(8 * prod_1_1_2 + 7 * prod_1_2_2 + 3 * prod_1_3_2 - t_1_3, lb=0, ub=0)

c_batch_prod_2_1 = Constraint(5 * prod_2_1_1 + 2 * prod_2_2_1 + 11 * prod_2_3_1 - t_2_1, lb=0, ub=0)
c_batch_prod_2_2 = Constraint(5 * prod_2_1_2 + 2 * prod_2_2_2 + 11 * prod_2_3_2 - t_2_3, lb=0, ub=0)

c_batch_prod_3_1 = Constraint(4 * prod_3_1_1 + 1 * prod_3_2_1 + 3 * prod_3_3_1 - t_3_1, lb=0, ub=0)
c_batch_prod_3_2 = Constraint(4 * prod_3_1_2 + 1 * prod_3_2_2 + 3 * prod_3_3_2 - t_3_2, lb=0, ub=0)

# production time constraint Z = 30
c_time_prod_1 = Constraint(7 * prod_1_1_1 + 7 * prod_1_1_2 + 6 * prod_1_2_1 + 6 * prod_1_2_2 + 4 * prod_1_3_1 + 4 * prod_1_3_2, lb=0, ub=30)
c_time_prod_2 = Constraint(5 * prod_2_1_1 + 5 * prod_2_1_2 + 3 * prod_2_2_1 + 3 * prod_2_2_2 + 7 * prod_2_3_1 + 7 * prod_2_3_2, lb=0, ub=30)
c_time_prod_3 = Constraint(3 * prod_3_1_1 + 3 * prod_3_1_2 + 2 * prod_3_2_1 + 2 * prod_3_2_2 + 4 * prod_3_3_1 + 4 * prod_3_3_2, lb=0, ub=30)

# global equilibrium constraint
c_equilibrium_1 = Constraint(t_1_2 + t_1_3 - t_2_1 - t_3_1, lb=0, ub=0)
c_equilibrium_2 = Constraint(t_2_1 + t_2_3 - t_1_2 - t_3_2, lb=0, ub=0)
c_equilibrium_3 = Constraint(t_3_1 + t_3_2 - t_1_3 - t_2_3, lb=0, ub=0)

# barter equilibrium constraint
b_equilibrium_1_2 = Constraint(t_1_2 - t_2_1, lb=0, ub=0)
b_equilibrium_1_3 = Constraint(t_1_3 - t_3_1, lb=0, ub=0)
b_equilibrium_2_3 = Constraint(t_2_3 - t_3_2, lb=0, ub=0)

# GDP maximization, aka all sales and all purchases
obj = Objective(t_1_2 + t_1_3 + t_2_1 + t_2_3 + t_3_1 + t_3_2, direction='max')

# Variables, constraints and objective are combined in a Model object, which can subsequently be optimized.
model = Model(name='Simple model')
model.objective = obj
model.add([
    c_batch_prod_1_1, c_batch_prod_2_1, c_batch_prod_3_1,
    c_batch_prod_1_2, c_batch_prod_2_2, c_batch_prod_3_2,
    c_time_prod_1, c_time_prod_2, c_time_prod_3
])
# model.add([c_equilibrium_1, c_equilibrium_2, c_equilibrium_3])
model.add([b_equilibrium_1_2, b_equilibrium_1_3, b_equilibrium_2_3])

status = model.optimize()

print("----------")
for var_name, var in model.variables.iteritems():
    print(var_name, "=", var.primal)

print("status:", model.status)

print("Effective GDP:", model.objective.value)

print("Actor 1 Sales: {0}, Purchases: {1}, Time spent: {2}".format(
    t_1_2.primal + t_1_3.primal,
    t_2_1.primal + t_3_1.primal,
    c_time_prod_1.primal))

print("Actor 2 Sales: {0}, Purchases: {1}, Time spent: {2}".format(
    t_2_1.primal + t_2_3.primal,
    t_1_2.primal + t_3_2.primal,
    c_time_prod_2.primal))

print("Actor 3 Sales: {0}, Purchases: {1}, Time spent: {2}".format(
    t_3_1.primal + t_3_2.primal,
    t_1_3.primal + t_2_3.primal,
    c_time_prod_3.primal))