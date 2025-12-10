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
        response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6")
        data = response.json()
        self.deck_id = data["deck_id"]

    def deal(self):
        return requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=2")

    def hit(self)
        return requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1")

if __name__ == "__main__":
    game = Blackjack()
