import requests

class Poker:
    def __init__(self):
        response = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
        )
        data = response.json()
        self.deck_id = data["deck_id"]
        self.board = []
        self.hole_cards = []

    def deal_hole(self):
        card_info = requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=4"
        ).json()["cards"]
        dealt_cards = [card_info[i]["code"] for i in range(len(card_info))]
        print(dealt_cards)
        self.hole_cards.append(dealt_cards[0::2])
        self.hole_cards.append(dealt_cards[1::2])
        print(hole_cards)

if __name__ == "__main__":
    game = Poker()
    print(game.deck_id)
    print(game.deal_hole())
