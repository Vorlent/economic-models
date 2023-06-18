import itertools
import math

class Product:
    def __init__(self, type):
        self.type = type
        self.amount = 0

class ConsumptionBehavior:
    def __init__(self, daily_water, daily_food):
        self.daily_water = daily_water
        self.daily_food = daily_food

    def consume(self, person):
        goods = ["WATER", "FOOD"]
        for good in goods:
            desired = person.consumption_behavior.desired(good)
            if not person.inventory.has(good, desired):
                # dehydrating or starving
                person.health -= 1
            else:
                person.inventory.remove(good, desired)
                person.health = min(20, person.health + 1)

    def desired(self, good_type):
        if good_type == "WATER":
            return self.daily_water
        if good_type == "FOOD":
           return self.daily_food
        return 0

class Inventory:
    def __init__(self, goods):
        self.goods_by_type = {}
        for good in goods:
            self.add(good)

    def add(self, good):
        if good.type in self.goods_by_type:
            self.goods_by_type[good.type].amount += good.amount
        else:
            self.goods_by_type[good.type] = good

    def has(self, good_type, amount):
        return good_type in self.goods_by_type and self.goods_by_type[good_type].amount >= amount

    def amount(self, good_type):
        if good_type in self.goods_by_type:
            return self.goods_by_type[good_type].amount
        return 0

    def remove(self, good_type, amount):
        if good_type in self.goods_by_type:
            self.goods_by_type[good_type].amount = max(0, self.goods_by_type[good_type].amount - amount)

class Person:
    def __init__(self, tp):
        self.productivityMultiplier = 1
        self.hoursPerDay = 8
        self.cash = 10
        self.inventory = [
            Product("WATER", 10),
            Product("FOOD", 10)
        ]
        self.health = 100
        self.time_preference = tp
        self.consumption_behavior = ConsumptionBehavior(3, 3)

class MarketOffer:
    def __init__(self, person, good_type, quantity, price):
        self.person = person
        self.good_type = good_type
        self.quantity = quantity
        self.price = price


def utility_function_water(person, quantity):
    if quantity < 3:
        return 0
    b = 6
    x = person.health
    return 0.5-(b/2)/(x-b)

def utility_function_food(person, quantity):
    if quantity < 3:
        return 0
    b = 6
    c = 20
    x = person.health
    return 0.5 - (b/2)/(x-c)

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
        self.prices = {"WATER": 1, "FOOD": 1}

    def produce(self):
        price = 1
        for person in self.people:
            goods = ["WATER", "FOOD"]
            predicted_cash = 0

            # todo implement utility based consumption allocation function with limited budget
            for good in goods:
                predicted_cash += person.consumption_behavior.desired(good) * self.prices[good]

            # todo implement production allocation function

            # excess cash and products reduce the need for production in this period
            max_production = ((predicted_cash - person.cash) / price) - person.products
            max_hours = min(person.hoursPerDay, max_production / person.productivityMultiplier)
            person.products += person.productivityMultiplier * max_hours

    def trade(self):
        # simulate market for each good individually
        goods = ["WATER", "FOOD"]

        for good in goods:
            sell_offers = []
            buy_offers = []

            for person in self.people:
                price = 1
                # TODO adjust consumption to stay within the budget
                difference = person.inventory.amount(good) - person.consumption_behavior.desired(good)
                if difference > 0:
                    # sell excess product
                    sell_offers.add(MarketOffer(person, good, difference, price))
                if difference < 0:
                    # buy shortage product
                    buy_offers.add(MarketOffer(person, good, -difference, price))

            # total_supply = sum([offer.quantity for offer in sell_offers])
            # total_demand = sum([offer.quantity for offer in buy_offers])
            # net_balance = total_supply - total_demand

            buy_offers_asc = buy_offers.sort(key=lambda x: x.price, reverse=True)
            sell_offers_desc = sell_offers.sort(key=lambda x: x.price)

            i = 0
            j = 0

            while buy_offers_asc and sell_offers_desc:
                b_offer = buy_offers_asc[i]
                s_offer = sell_offers_desc[j]
                if b_offer.price >= s_offer.price:
                    amount = min(b_offer.quantity, s_offer)
                    b_offer.quantity -= amount
                    s_offer.quantity -= amount
                    fair_price = (b_offer.price + s_offer.price)/2
                    b_offer.person.cash -= fair_price * amount
                    s_offer.person.cash += fair_price * amount

                    if b_offer.quantity <= 0:
                        i += 1
                    if s_offer.quantity <= 0:
                        j += 1
                else:
                    break
        # repeat pricing rounds


        # how do individuals choose prices for products?
        # the logical conclusion should be that
        # the price should differentiate the between the utilities of products
        # this means something that generates twice the utility
        # should be twice as valuable
        # or in other words, the marginal utility of any marginal dollar should be identical across products

        # there are no prices yet, because clearing the market
        # has not been implemented yet
        # all we did was generate buy and sell offers
        # depending on whether there is not enough food or water,
        # one of them will be more valuable than the other

        # te

    def consumption(self):
       for person in self.people:
           person.consumption_behavior.consume(person)

    def round(self):
        self.produce()
        self.trade()
        self.consumption()