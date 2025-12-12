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


    def __init__(self, balance):
        response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6")
        data = response.json()
        self.deck_id = data["deck_id"]
        self.game_active = False
        self.player_hand = []
        self.dealer_hand = []
        self.score = 0
        self.balance = balance


    def ui(self):

        
    def bet(self):


    def deal(self):
        return requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=2").json()["cards"]

    def start(self):
        self.game_active = True
        return self.deal

    def hit(self):
        return requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1").json()["cards"]

    def score(self):



    def blackjack(self):
        if self.player_hand["value"][]

    def stand(self):



    def end_game(self):
        self.game_active = False


if __name__ == "__main__":
    game = Blackjack()
