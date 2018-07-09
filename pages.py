from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class NewRoundWaitPage(WaitPage):

    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        if self.round_number > 1:
            for p in players:
                p.stock = p.in_round(self.round_number - 1).stock
                p.cash = p.in_round(self.round_number - 1).cash


class BidPage(Page):
    form_model = 'player'
    form_fields = ['bidp','bidq','askp','askq']
    timeout_seconds = 60

    def vars_for_template(self):
        return {'cash': self.player.cash, 'stock': self.player.stock}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        group = self.group
        players=group.get_players()

        for p in players:
            if p.bidp >= p.askp and p.bidq > 0 and p.askq >0 :  # Removing selfsatisfying bids
                p.net_askq = p.askq - abs(p.askq - p.bidq)
                p.net_bidq = p.bidq - abs(p.askq - p.bidq)
            else:
                p.net_askq = p.askq
                p.net_bidq = p.bidq

            p.supply = [p.askp] * p.net_askq   # the error is near here as only supply is working properly
            p.demand = [p.bidp] * p.net_bidq

        self.group.run_market()

        j = 0
        l = []
        m = []
        n = []
        while j < self.group.volume:            # Begin selling
            for k in players:
                if k.sales < k.net_askq:
                    l = l + [k.askp]
            for k in players:
                if k.askp == min(l):
                    m = m + [k.sales]
            for k in players:
                if k.askp == min(l) and k.sales == min(m) and k.sales < k.net_askq:
                    n = n + [k]
            p = random.choice(n)
            p.stock = p.stock - 1
            p.cash = p.cash + self.group.market_price
            p.sales = p.sales + 1

            j += 1      # End Selling

        j = 0           # Begin buying
        l = []
        m = []
        n = []
        while j < self.group.volume:
            for k in players:
                if k.purchases < k.net_bidq:
                    l = l + [k.bidp]
            for k in players:
                if k.bidp == min(l):
                    m = m + [k.purchases]
            for k in players:
                if k.bidp == min(l) and k.purchases == min(m) and k.purchases < k.net_bidq:
                    n = n + [k]
            p = random.choice(n)
            p.stock = p.stock + 1
            p.cash = p.cash - self.group.market_price
            p.purchases = p.purchases + 1

            j += 1  # End Buying


class Results(Page):
    pass


page_sequence = [
    NewRoundWaitPage,
    BidPage,
    ResultsWaitPage,
    Results
]
