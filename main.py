import itertools
import math


class ConsumptionBehavior:
    def __init__(self, fixed, income_pct, networth_pct):
        self.fixed = fixed # mandatory bills
        self.income_pct = income_pct # discretionary spending
        self.networth_pct = networth_pct # based on wealth

    def desired_consumption(self, person):
        discretionary = (person.income - self.fixed) * self.income_pct
        wealth_spending = person.networth * self.networth_pct
        return self.fixed + discretionary + wealth_spending

    def possible_consumption(self, person):
        return min(person.cash, self.desired_consumption(person))

class Person:
    def __init__(self, tp):
        self.productivityMultiplier = 1
        self.hoursPerDay = 8
        self.lifetimeIncome = 0
        self.cash = 10
        self.products = 0
        self.minimum_standard_of_living = 6
        self.standard_of_living = 0
        self.health = 100
        self.time_preference = tp
        self.consumption_behavior = ConsumptionBehavior(6, 0.10, 0.03)
        self.held_bonds = [BondOffer()]

# assuming lump sum at the end of the contract
class DebtDemand:
    def __init__(self, tp):
        self.principal = 1000
        self.interest_rate = 0.05
        self.duration = 12

# assuming lump sum at the end of the contract
class BondOffer:
    def __init__(self, tp):
        self.principal = 1000
        self.interest_rate = 0.05
        self.due_date = 12

class Simulation:
    def __init__(self):
        self.people = [
            Person(0.10),
            Person(0.05),
            Person(0.07),
            Person(0.08),
            Person(0.02),
            Person(0.01),
            Person(0.07),
            Person(0.01),
            Person(0.04),
            Person(0.20)
        ]

        self.investments = [
            {'duration': 2000, 'productivity': 0.15},
            #{'duration': 3000, 'productivity': 0.25},
            #{'duration': 2000, 'productivity': 0.12},
            #{'duration': 1000, 'productivity': 0.16},
            #{'duration': 1000, 'productivity': 0.16},
            #{'duration': 1000, 'productivity': 0.16}
        ]
        self.available_borrowers = [] # borrowers looking for lenders
        self.bonds_supply = [] # lenders trying to sell bonds

    def work_and_earn(self, price):
        balance = 0
        for person in self.people:
            income = price * person.productivityMultiplier * person.hoursPerDay
            person.cash += income
            balance += income
        return balance

    def initial_consumption(self, price):
        balance = 0
        # consume minimum standard of living
        for person in self.people:
            spending = person.consumption_behavior.possible_consumption(person)
            person.consumption = spending
            person.cash -= spending
            balance -= spending
        return balance

    def consumption_vs_savings(self):
        # divide remaining cash balance into consumption or investment
        for person in self.people:

            d_cons = person.consumption_behavior.desired_consumption(person)
            p_cons = person.consumption_behavior.possible_consumption(person)

            if d_cons > p_cons:
                # sell held bonds first
                if person.held_bonds:
                    # pick the bond with the biggest difference between personal valuation and market valuation
                    # this is getting too complicated...


                # sell investment or borrow money if the interest rate is below time preference
                # which investments should be sold first?
                # this is where time preference can actually help us!
                # we can calculate the net present value of any investment
                # and look if the market price is above that present value
                # the problem is I don't know how to model
                # the investments...

            else:
                # buy

            person.investment = 0

    def round(self):
        # assume that the minimum wage is the same for everyone
        # this wage can only be improved by being more productive
        balance = 0

        # work and earn phase, every product gets sold
        price = 1
        balance += self.work_and_earn(price)

        # consume minimum standard of living
        balance -= self.initial_consumption(price)

        #self.consumption_vs_savings()

        # and we are about to allocate 20000 worth of savings with a yield of 4%, how much will any given person invest?
        #
        # The rule for whether a person will invest or not is that he will invest until the absolute investment returns
        # match his consumption spending.
        #
        # if savings * timePreference < income then
        # maxInvest = max(income, (income - savings * timePreference) / timePreference) - minConsumption
        # else
        # maxDisinvest = (savings * timePreference - income) / timePreference) - maxConsumption
        # end
        #
        # 7% return example:
        #
        # p1=10%
        # p2=5% Will invest
        # p3=7% Will invest
        # p4=8%
        # p5=2% Will invest
        # p6=1% Will invest
        # p7=7% Will invest
        # p8=1% Will invest
        # p9=4% Will invest
        # p10=20%
        #
        # Assuming an income of 8*10 = 80 and a minimum consumption of 40,
        # then total investment for that day would be
        #
        # maxInvest = max(80, (80 - 0 * timePreference) / timePreference - 40 = 80 / timePreference) - 40
        #
        # p2=5% = 1600 / 25886 = 0,0618
        # p3=7% = 1143 / 25886 = 0,0441
        # p5=2% = 4000 / 25886 = 0,1545
        # p6=1% = 8000 / 25886 = 0,3090
        # p7=7% = 1143 / 25886 = 0,0441
        # p8=1% = 8000 / 25886 = 0,3090
        # p9=4% = 2000 / 25886 = 0,0772

