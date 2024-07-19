from __future__ import print_function
from optlang import Model, Variable, Constraint, Objective
import itertools

# this is essentially a discrete neoclassical model
# we have three agents

class Production:
    def __init__(self, batch_size, time_needed):
        self.id = -1
        self.batch_size = batch_size
        self.time_needed = time_needed
        self.trade_to_vars = {} # production specific agent to agent variable

class Agent:
    def __init__(self, id, max_time, production):
        self.id = id
        self.trade_to_vars = {} # agent to agent
        self.production = production
        self.production_by_id = {}
        for i in range(len(self.production)):
            self.production[i].id = i + 1
            self.production_by_id[i+1] = self.production[i]
        self.max_time = max_time
        self.prod_qty_to_vars = {}

    # make this agent aware of other agents
    def add_agent(self, other_agent):
        self.trade_to_vars[other_agent.id] = (Variable('t_{0}_{1}'.format(self.id, other_agent.id), lb=0, type='integer'))
        for prod in self.production:
            prod_var = Variable('prod_{0}_{1}_{2}'.format(self.id, prod.id, other_agent.id), lb=0, type='integer')
            prod.trade_to_vars[other_agent.id] = prod_var

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

agent1 = Agent(1, 30, [
    Production(8, 7),
    Production(7, 6),
    Production(3, 4)
])
agent2 = Agent(2, 30,[
    Production(5, 5),
    Production(2, 3),
    Production(11, 7)
])
agent3 = Agent(3, 30,[
    Production(4, 3),
    Production(1, 2),
    Production(3, 4)
])

agent_by_id = {
    1 : agent1,
    2 : agent2,
    3 : agent3
}

agents = agent_by_id.values()

for agent_id in agent_by_id:
    for other_id in agent_by_id:
        if agent_id != other_id:
            agent_by_id[agent_id].add_agent(agent_by_id[other_id])

# GDP maximization, aka all sales and all purchases
def objective_from_agents(agents):
    objective_vars = []
    for agent in agents:
        objective_vars.extend(agent.trade_to_vars.values())
    return Objective(sum(objective_vars), direction='max')

def global_constraints(agents):
    constraints = []
    # global equilibrium constraint
    # all sales by agent1 to agent2 and agent3
    # must be compensated by sales from agent2 to agent1
    # and agent3 to agent1
    for agent in agents:
        sales = []
        purchases = []
        for other_agent in agent.trade_to_vars:
            sales.append(agent.trade_to_vars[other_agent])
            purchases.append(agent_by_id[other_agent].trade_to_vars[agent.id])

        constraints.append(Constraint(sum(sales) - sum (purchases), lb=0, ub=0))
    return constraints

def barter_constraints(agents):
    constraints = []
    # find unique 2-agent pairs...
    # todo generalize for n-agent tuples
    agent_pairs = itertools.combinations(agents, 2)
    for pair in agent_pairs:
        agent1 = pair[0]
        agent2 = pair[1]
        var1 = agent1.trade_to_vars[agent2.id]
        var2 = agent2.trade_to_vars[agent1.id]
        constraints.append(Constraint(var1 - var2, lb=0, ub=0))
    return constraints

def time_constraints(agents):
    constraints = []
    for agent in agents:
        vars = []
        for prod in agent.production:
            for other_agent in prod.trade_to_vars:
                vars.append(prod.time_needed * prod.trade_to_vars[other_agent])
        constraints.append(Constraint(sum(vars), lb=0, ub=agent.max_time))
    return constraints

# there is an assumption here
# different batch sizes are considered different commodities
# people always buy non divisible batches
# this essentially allows us to have 1 qty = 1 price = 1 utility
# and more useful commodities are simply set to be bigger batches
def batch_constraints(agents):
    constraints = []
    for agent in agents:
        buyers = {}
        # init buyers
        for prod in agent.production:
            for other_agent in prod.trade_to_vars:
                if not (other_agent in buyers):
                    buyers[other_agent] = []

        for prod in agent.production:
            for other_agent in prod.trade_to_vars:
                buyers[other_agent].append(prod.batch_size * prod.trade_to_vars[other_agent])

        for other_agent in buyers:
            seller_var = agent.trade_to_vars[other_agent]
            # print(sum(buyers[other_agent]) - seller_var)
            constraints.append(Constraint(sum(buyers[other_agent]) - seller_var, lb=0, ub=0))
    return constraints

# expected solution:
# Effective GDP: 119.0
# Actor 1 Sales: 32.0, Purchases: 32.0, Time spent: 28.0
# Actor 2 Sales: 40.0, Purchases: 40.0, Time spent: 29.0
# Actor 3 Sales: 40.0, Purchases: 40.0, Time spent: 30.0
c_batch = batch_constraints(agents)

# production time constraint Z = 30
c_time = time_constraints(agents)

# Variables, constraints and objective are combined in a Model object, which can subsequently be optimized.
model = Model(name='Simple model')
model.objective = objective_from_agents(agents)
model.add(c_batch)
model.add(c_time)

# global equilibrium constraint
model.add(global_constraints(agents))

# barter equilibrium constraint
#model.add(barter_constraints(agents))

status = model.optimize()

t_1_2 = agent_by_id[1].trade_to_vars[2]
t_1_3 = agent_by_id[1].trade_to_vars[3]

t_2_1 = agent_by_id[2].trade_to_vars[1]
t_2_3 = agent_by_id[2].trade_to_vars[3]

t_3_1 = agent_by_id[3].trade_to_vars[1]
t_3_2 = agent_by_id[3].trade_to_vars[2]

time_spent_by_id = {}
for i in range(len(c_time)):
    time_spent_by_id[i+1] = c_time[i]

c_time_prod_1 = c_time[0]
c_time_prod_2 = c_time[1]
c_time_prod_3 = c_time[2]

print("----------")
for var_name, var in model.variables.iteritems():
    print(var_name, "=", var.primal)

print("status:", model.status)

print("Effective GDP:", model.objective.value)

for agent_id in agent_by_id:
    agent = agent_by_id[agent_id]
    sales = 0
    purchases = 0
    for other_agent in agent.trade_to_vars:
        sales += agent_by_id[agent_id].trade_to_vars[other_agent].primal
        purchases += agent_by_id[other_agent].trade_to_vars[agent_id].primal
    time_spent = time_spent_by_id[agent_id].primal

    print("Actor {3} Sales: {0}, Purchases: {1}, Time spent: {2}".format(
        sales,
        purchases,
        time_spent,
        agent_id))