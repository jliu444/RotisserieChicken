import requests

class Poker:
    def __init__(self):
        response = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
        )
        data = response.json()
        self.deck_id = data["deck_id"]

    def deal(self):
        return requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count=1"
        ).json()["cards"]

if __name__ == "__main__":
    game = Poker()
    print(game.deck_id)
    print(game.deal())
