'''
  Jake Liu, Cindy Liu, Veronika Duvanova, Robert Chen
  RotisserieChicken
  SoftDev
  P01
  2025-12-20
  time spent: 2h
'''
# <!--Concept of this page:
#   make house
#   - if house value under 17, hit
#   - if house value over 17 stand
#   Game code
#   - if player value over 21 and house value under 21, player loses
#   - if card value is 2 and player value 21 then 2.5 * bet
#   - if player and house are standing and values are equal, player recives thier bet back
#   - if value over 21 and house value over 21, player gets thier bet back
#   - if player is standing and value under 21 and house value over 21, player gets 2 * bet
#   - if player is standing and value under 21, and player value > house value, player gets 2 * bet
#   stand/hit button
#   bet chips
# -->

import requests


class Blackjack:
    def __init__(self):
        response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6")
        data = response.json()
        self.deck_id = data["deck_id"]

        self.bet = 0 

        self.winner = 0 # 0 = tie, 1 = player, 2 = dealer 
        self.game_active = False
        self.hand = [1, 1]
        self.dealer_hand = [1, 1]
        self.player_turn = True
        self.game_over = False
    
    def set_bet(self, bet_amt: int):
        self.bet = bet_amt

    def deal(self):
        self.hand = requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=2"
        ).json()["cards"]
        self.dealer_hand = requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=2"
        ).json()["cards"]

    def hit(self):
        if self.player_turn:
            self.hand += requests.get(
                f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1"
            ).json()["cards"]
            if self.score('Player') > 21:
                self.game_over = True
                self.player_turn = False
                self.winner = 2 
        else:
            self.dealer_hand += requests.get(
                f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1"
            ).json()["cards"]
            if self.score('Dealer') > 21:
                self.game_over = True
                self.winner = 1 

    def dealer_move(self):
        if self.player_turn:
            raise Exception("Must be dealer's turn.")

        if self.score('Dealer') <= 16:
            self.hit()
        else:
            self.stand()

    def get_value(self, code: str):
        '''
        takes in card code and returns integer
        representing value of card
        '''
        rank = code[0]
        if rank.isnumeric():
            if rank == "0":
                return 10
            return int(rank)
        elif rank in ["J", "Q", "K"]:
            return 10
        elif rank == "A":
            return 1

    def score(self, who: str):
        '''
        who - a string ('Player' or 'Dealer')
        '''
        hand = []
        if who == 'Player':
            hand = [card['code'] for card in self.hand]
        elif who == 'Dealer':
            hand = [card['code'] for card in self.dealer_hand]
        else:
            raise ValueError("hand must be 'Player' or 'Dealer'")

        has_ace = False
        total_value = 0
        for code in hand:
            if code[0] == 'A':
                has_ace = True
            total_value += self.get_value(code)

        if total_value <= 11 and has_ace:
            total_value += 10

        return total_value

    def stand(self):
        if not self.player_turn:
            self.game_over = True

        else:
            self.player_turn = not self.player_turn
    
    def get_winner(self):
        if self.player_turn or not self.game_over:
            return 0 
        
        if self.winner != 0:
            return self.winner

        if self.score('Player') > self.score('Dealer'):
            return 1 
        elif self.score('Player') < self.score('Dealer'):
            return 2 
        return 0# draw
    
    def reset_game(self):
        requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/return/"
        )

        requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/shuffle/"
        )
        self.bet = 0 

        self.game_active = False
        self.hand = [1, 1]
        self.dealer_hand = [1, 1]
        self.player_turn = True
        self.winner = False
        self.game_over = False



if __name__ == "__main__":
    pass
