from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Austin Bradley'

doc = """
This app is a simple call market 
"""


class Constants(BaseConstants):
    name_in_url = 'call_market'
    players_per_group = 2
    num_rounds = 2
    initial_cash = c(100)
    initial_stock = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    market_price = models.FloatField(initial=0)
    volume = models.IntegerField(initial=0)

    def run_market (self):
        supply = [999]
        demand = [0]
        players = self.get_players()

        for i in players:
            supply = sorted(supply + i.supply)
            demand = sorted(demand + i.demand, reverse=True)

        print('total supply is', supply)
        print('total demand is', demand)
        i = 0

        while demand[i] >= supply[i]:
            i += 1

        self.volume = i
        self.market_price = supply[self.volume - 1]


class Player(BasePlayer):
    stock = models.IntegerField(initial= Constants.initial_stock)
    cash = models.CurrencyField(initial=Constants.initial_cash)
    bidp = models.FloatField(initial=0)
    bidq = models.IntegerField(initial=0)
    askp = models.FloatField(initial=0)
    askq = models.IntegerField(initial=0)
    purchases = models.IntegerField(initial=0)
    sales = models.IntegerField(initial=0)


    def buy_one(self, market_price):
        self.stock = self.stock + 1
        self.cash = self.cash - market_price
        self.purchases = self.purchases + 1

    def sell_one(self, market_price):
        self.stock = self.stock - 1
        self.cash = self.cash + market_price
        self.sales = self.sales + 1

    def reset_transactions (self):
        self.purchases = 0
        self.sales = 0