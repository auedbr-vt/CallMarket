import random

players = []

class Player:
    def __init__(self, bidp, bidq, askp, askq):
        self.bidp = bidp
        self.bidq = bidq
        self.askp = askp
        self.askq = askq
        self.stock = 5
        self.cash = 20
        self.purchases = 0
        self.sales = 0
        global players
        players = players + [self]

        if bidp >= askp:       #Removing selfsatisfying bids
            self.net_askq = self.askq - abs(self.askq - self.bidq)
            self.net_bidq = self.bidq - abs(self.askq - self.bidq)
        else:
            self.net_askq = self.askq
            self.net_bidq = self.bidq

        self.supply = [self.askp] * self.net_askq
        self.demand = [self.bidp] * self.net_bidq

    def buy_one(self, market_price):
        self.stock = self.stock + 1
        self.cash = self.cash - market_price
        self.purchases = self.purchases + 1

    def sell_one(self, market_price):
        self.stock = self.stock - 1
        self.cash = self.cash + market_price
        self.sales = self.sales + 1


P1 = Player(0,0,8,3)
P2 = Player(4,3,7,3)
P3 = Player(7,5,4,2)

supply = []
demand = []
for i in [P1,P2,P3]:
    supply = sorted(supply + i.supply)
    demand = sorted(demand + i.demand, reverse=True)

i = 0
while demand[i] >= supply[i]:
    i += 1
volume = i
market_price = supply[volume]


j = 0
l = []
m = []
n = []
while j < volume:
    for k in [P1,P2,P3]:
        if k.purchases < k.net_bidq:
            l = l + [k.bidp]
    for k in [P1,P2,P3]:
        if k.bidp == max(l):
            m = m + [k.purchases]
    for k in [P1,P2,P3]:
        if k.bidp == max(l) and k.purchases == min(m) and k.purchases < k.net_bidq:
            n = n + [k]
    Player.buy_one(random.choice(n), market_price)

    j += 1

j = 0
l = []
m = []
n = []
while j < volume:
    for k in [P1,P2,P3]:
        if k.sales < k.net_askq:
            l = l + [k.askp]
    for k in [P1,P2,P3]:
        if k.askp == min(l):
            m = m + [k.sales]
    for k in [P1,P2,P3]:
        if k.askp == min(l) and k.sales == min(m) and k.sales < k.net_askq:
            n = n + [k]
    Player.sell_one(random.choice(n), market_price)

    j += 1

