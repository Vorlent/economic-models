class Person:
    def __init__(self, consumption_rate, max_saving, max_debt):
        self.income = 0
        self.consumed_income = 0
        self.saved_income = 0
        self.repayment_income = 0
        self.borrowed_income = 0
        self.wealth_change = 0
        self.consumption_rate = consumption_rate
        self.saving_rate = (1 - consumption_rate)
        self.max_saving = max_saving
        self.max_debt = max_debt
        self.savings = 0
        self.debt = 0
        self.productivity = 1
        self.next_income = 50

class Simulation:
    def __init__(self):
        self.people = [
            Person(0.6, 60, 0),
            Person(0.6, 0, 50),
            Person(0.6, 0, 50)
        ]

    def round(self):
        for p in self.people:
            p.income = p.next_income

        # spending allocation phase
        for p in self.people:
            p.saved_income = p.income * p.saving_rate
            p.consumed_income = p.income - p.saved_income
            p.repayment_income = 0
            p.wealth_change = 0

            # use saved_income to pay off debt
            if p.debt > p.max_debt:
                p.repayment_income = min(p.debt - p.max_debt, p.saved_income)
                p.debt -= p.repayment_income
                p.saved_income -= p.repayment_income
                p.wealth_change += p.repayment_income

            if p.savings < p.max_saving:
                p.saved_income = min(p.max_saving - p.savings, p.saved_income)
                p.consumed_income = p.income - p.saved_income - p.repayment_income
                p.wealth_change += p.saved_income
            else:
                p.consumed_income = p.income - p.repayment_income
                p.saved_income = 0

        # lending phase
        loanable_funds = 0
        for p in self.people:
            loanable_funds += p.saved_income

        # borrowing phase
        borrower_demand = 0
        for p in self.people:
            borrower_demand += max(0, p.max_debt - p.debt)

        # dissaving phase
        repayment_demand = 0
        for p in self.people:
            # lenders must accept all payments
            repayment_demand += p.savings

        # repaying phase
        repayment_supply = 0
        for p in self.people:
            repayment_supply += p.repayment_income

        print("Capital Market: loanable_funds {0} borrower_demand {1}".format(loanable_funds, borrower_demand))
        print("Capital Market: repayment_demand {0} repayment_supply {1}".format(repayment_demand, repayment_supply))

        # find equilibrium values
        borrowed_vs_desired = 1
        savings_vs_desired = 1
        if loanable_funds < borrower_demand:
            borrowed_vs_desired = loanable_funds / borrower_demand
        if loanable_funds > borrower_demand:
            savings_vs_desired = borrower_demand / loanable_funds

        print("Equilibrium: borrowed_vs_desired {0}, savings_vs_desired {1}".format(borrowed_vs_desired, savings_vs_desired))

        # clear lender/borrower market
        for p in self.people:
            # allocate debt according to propensity to borrow
            p.borrowed_income = borrowed_vs_desired * max(0, (p.max_debt - p.debt))
            if p.borrowed_income > 0:
                p.debt += p.borrowed_income
                # all debt adds to consumption
                p.consumed_income += p.borrowed_income

            p_saved_income = savings_vs_desired * p.saved_income
            if p_saved_income > 0:
                p.saved_income = p_saved_income
                p.savings += p.saved_income
                p.consumed_income = p.income - p.saved_income
            else:
                p.consumed_income += p.saved_income
                p.saved_income = 0

        # find equilibrium values
        if repayment_demand == 0:
            repayment_vs_demand = 0
        else:
            repayment_vs_demand = repayment_supply / repayment_demand

        print("Equilibrium: repayment_vs_demand {0}".format(repayment_vs_demand))

        # clear repayment
        for p in self.people:
            repayment_spending = repayment_vs_demand * p.savings
            p.consumed_income += repayment_spending
            p.savings -= repayment_spending

        # supply phase
        aggregate_supply = 0
        for p in self.people:
            aggregate_supply += p.productivity

        # demand phase
        aggregate_demand = 0
        for p in self.people:
            aggregate_demand += p.consumed_income

        # find equilibrium values
        price = aggregate_demand / aggregate_supply

        # clear supply and demand
        for p in self.people:
            p.next_income = p.productivity * price

    def report(self):
        # report state of economy
        for i in range(0, len(self.people)):
            person = self.people[i]
            data = [i, person.income, person.borrowed_income, person.consumed_income, person.saved_income, person.savings, person.max_saving, person.debt, person.max_debt]
            print("Person {0}: Total Income {1}, Borrowed Income {2}, Consumption {3}, Saving {4}, Savings {5} / Max Saving. {6}, Debt {7} / Max Debt {8}".format(*data))
        print("")

sim = Simulation()
sim.report()
for i in range(1, 10):
    print("Round {0}".format(i))
    sim.round()
    sim.report()
    if i == 5:
        for p in sim.people:
            p.max_debt = 0

# I have to say something. Although I got most of the code correct on first try
# There have been money leaks (not memory leaks), where money simply disappeared
# and did not materialize as income. The model always gave the same obvious answer.
# If you have a money leak, then aggregate income will shrink but this leakage
# does not reprice debt. So the bug leads to Irving Fisher's debt deflation.
# Where is the bug in the monetary system that leads to money leaks in the real world?