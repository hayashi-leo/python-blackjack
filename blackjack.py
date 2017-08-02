#!/usr/bin/env python

from random import shuffle
from random import randint
import time

hearts_cards = [{"key":"HA", "value":1},
                {"key":"H2", "value":2},
                {"key":"H3", "value":3},
                {"key":"H4", "value":4},
                {"key":"H5", "value":5},
                {"key":"H6", "value":6},
                {"key":"H7", "value":7},
                {"key":"H8", "value":8},
                {"key":"H9", "value":9},
                {"key":"H10", "value":10},
                {"key":"HJ", "value":10},
                {"key":"HQ", "value":10},
                {"key":"HK", "value":10}]

spades_cards = [{"key":"SA", "value":1},
                {"key":"S2", "value":2},
                {"key":"S3", "value":3},
                {"key":"S4", "value":4},
                {"key":"S5", "value":5},
                {"key":"S6", "value":6},
                {"key":"S7", "value":7},
                {"key":"S8", "value":8},
                {"key":"S9", "value":9},
                {"key":"S10", "value":10},
                {"key":"SJ", "value":10},
                {"key":"SQ", "value":10},
                {"key":"SK", "value":10}]

diamonds_cards = [{"key":"DA", "value":1},
                  {"key":"D2", "value":2},
                  {"key":"D3", "value":3},
                  {"key":"D4", "value":4},
                  {"key":"D5", "value":5},
                  {"key":"D6", "value":6},
                  {"key":"D7", "value":7},
                  {"key":"D8", "value":8},
                  {"key":"D9", "value":9},
                  {"key":"D10", "value":10},
                  {"key":"DJ", "value":10},
                  {"key":"DQ", "value":10},
                  {"key":"DK", "value":10}]

clubs_cards = [{"key":"CA", "value":1},
               {"key":"C2", "value":2},
               {"key":"C3", "value":3},
               {"key":"C4", "value":4},
               {"key":"C5", "value":5},
               {"key":"C6", "value":6},
               {"key":"C7", "value":7},
               {"key":"C8", "value":8},
               {"key":"C9", "value":9},
               {"key":"C10", "value":10},
               {"key":"CJ", "value":10},
               {"key":"CQ", "value":10},
               {"key":"CK", "value":10}]


deck_cards = hearts_cards + spades_cards + diamonds_cards + clubs_cards


shuffle(deck_cards)

for card in deck_cards:
    print("card %s:%d" % (card["key"], card["value"]))
    

class Player:

    def __init__(self, cash_amount):
        self.cards = []
        self.cash_amount = cash_amount
        self.bet_amount = 0

    def Win(self):
        self.cash_amount += self.bet_amount
        self.ClearBet()

    def Loose(self):
        self.bet_amount = 0
        self.ClearBet()
        
    def Bet(self, bet_amount):
        self.bet_amount = bet_amount
        if (self.bet_amount > self.cash_amount):
            self.bet_amount = self.cash_amount
        self.cash_amount -= self.bet_amount

    def ClearBet(self):
        self.cash_amount += self.bet_amount
        self.bet_amount = 0
        
    def CalcOutcome(self):
        outcome = 0
        ace_card = False
        for card in self.cards:
            outcome += card["value"]
            if (card["value"] == 1):
                ace_card = True

        if (ace_card == True and outcome + 10 < 22):
            outcome += 10
            
        if (outcome > 21):
            self.busted = True
            # lost bet
            self.bet_amount = 0
            
        return outcome

    def StartNewPlay(self):
        self.cards = []
        self.busted = False

    def IsBusted(self):
        return self.busted
        
    def HitWithCard(self, card):
        self.cards.append(card)

    def PrintCards(self):
        for card in self.cards:
            print(card["key"])

    def PrintCashAmount(self):
        print("Cash $%d" % self.cash_amount)

    def GetCashAmount(self):
        return self.cash_amount
        
class Dealer:

    def __init__(self):
        self.cards = []

    def CalcOutcome(self):
        outcome = 0
        ace_card = False
        for card in self.cards:
            outcome += card["value"]
            if (card["value"] == 1):
                ace_card = True

        if (ace_card == True and outcome + 10 < 22):
            outcome += 10
            
        if (outcome > 21):
            self.busted = True
            
        return outcome

    def StartNewPlay(self):
        self.cards = []
        self.busted = False

    def IsBusted(self):
        return self.busted
        
    def HitWithCard(self, card):
        self.cards.append(card)

    def GetCards(self):
        return self.cards
    
    def PrintCards(self):
        for card in self.cards:
            print(card["key"])

# number of draws before re-shuffling
nr_draws = randint(2, len(deck_cards) - 10)
nr_plays = 2000
nr_busted = 0
nr_win = 0
nr_loose = 0
nr_push = 0
play_count = 0

player = Player(1000)
dealer = Dealer()

print("")

while (nr_plays > 0 and player.GetCashAmount() > 0):

    try:
        # update play count
        nr_plays -= 1
        play_count += 1

        if (nr_draws < 0):
            deck_cards = hearts_cards + spades_cards + diamonds_cards + clubs_cards
            nr_draws = randint(2, len(deck_cards) - 10)
            print("-- shuffling --")
            shuffle(deck_cards)
            
     
        print("nr draws %d" % nr_draws)
            
        player.StartNewPlay()

        dealer.StartNewPlay()
        
        player.Bet(5)
        
        # draw
        player.HitWithCard(deck_cards.pop())
        dealer.HitWithCard(deck_cards.pop())
 
        player.HitWithCard(deck_cards.pop())
        dealer.HitWithCard(deck_cards.pop())
        nr_draws -= 4

        stand = False
        while (stand == False and player.IsBusted() == False):
            outcome = player.CalcOutcome()
            dealer_card = dealer.GetCards()[0]
            
            if (outcome < 13):
                player.HitWithCard(deck_cards.pop())
                nr_draws -= 1
            elif (outcome < 16):
                                 # @17 wins ~
                                 # @18 wins ~ 
                                 # @19 wins ~ 38%, loose ~ 52%
                                 # to hit 18, 19, 20, 21 -> chances are 50/50
                if (dealer_card["value"] == 1 or dealer_card["value"] + 10 > outcome):
                    player.HitWithCard(deck_cards.pop())
                    nr_draws -= 1
                else:
                    stand = True
            else:
                stand = True
            
        # check results
        if (player.IsBusted() == True):
            print("BUSTED!")
            nr_busted += 1
        else:
            while (dealer.CalcOutcome() < 17 and dealer.IsBusted() == False):
                dealer.HitWithCard(deck_cards.pop())
                nr_draws -= 1

            if (dealer.IsBusted() == True or dealer.CalcOutcome() < player.CalcOutcome()):
                print("Player Wins!!")
                nr_win += 1
                player.Win()
            elif (dealer.CalcOutcome() == player.CalcOutcome()):
                print("PUSH!!")
                nr_push += 1
                player.ClearBet()
            else:
                nr_loose += 1
                print("DEALER WINS!!")
                player.Loose()
                
        print("Player Totals = %d, Dealer Totals = %d" % (player.CalcOutcome(), dealer.CalcOutcome()))
        print("number wins   = %d/%d" % (nr_win, play_count))
        print("number push   = %d/%d" % (nr_push, play_count))
        print("number loose  = %d/%d" % (nr_loose, play_count))
        print("number busted = %d/%d" % (nr_busted, play_count))
              
        print("--PlayerCards--")
        player.PrintCards()
        print("--DealerCards--")
        dealer.PrintCards()
        print("---")
        player.PrintCashAmount()
        print("---")
        print("")
        # time.sleep(2)

    except KeyboardInterrupt:
        print '\nPausing...  (Hit ENTER to continue, type quit to exit.)'
        try:
            response = raw_input()
            if response == 'quit':
                break
            print 'Resuming...'
        except KeyboardInterrupt:
            print 'Resuming...'
            continue
    

    
