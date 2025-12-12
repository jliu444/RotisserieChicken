import requests

class Poker:
    def __init__(self, player_chips):
        response = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
        )
        data = response.json()
        self.deck_id = data["deck_id"]
        self.board_cards = []
        self.hole_cards = []

        self.player_to_move = 0
        self.max_chips = player_chips
        self.player_stakes = [0, 0] # 0 <= player_stakes <= max_chips
        self.round_bets = [0, 0] # reset to [0, 0] every betting round

    def deal_hole(self):
        card_info = self.draw(4)["cards"]
        dealt_cards = [card_info[i]["code"] for i in range(len(card_info))]
        self.hole_cards.append(dealt_cards[0::2])
        self.hole_cards.append(dealt_cards[1::2])

    def burn_card(self):
        return self.draw(1)

    def deal_board(self):
        card_info = self.draw(1)["cards"]
        board_cards.append(card_info[0]["code"])

    def check_or_call(self):
        opp_bet = self.round_bets[self.next()]
        curr_bet = self.round_bets[self.player_to_move]
        to_bet = opp_bet - curr_bet

        # check
        if to_bet == 0:
            self.player_to_move = self.next()

        # call, within budget
        elif self.player_stakes[self.player_to_move] + to_bet <= self.max_chips:
            self.player_stakes[self.player_to_move] += to_bet
            self.round_bets[self.player_to_move] += to_bet
            self.player_to_move = self.next()

        # call, not within budget
        else:
            to_bet = 0 # fix





    def make_bet_or_raise_to(self):
        pass

    def fold(self):
        pass

    def draw(self, num: int):
        return requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count={num}"
        ).json()

    def next(self):
        if self.player_to_move == 0:
            return 1
        else:
            return 0


if __name__ == "__main__":
    game = Poker()
    print(game.deck_id)
    game.deal_hole()
    print(game.hole_cards)
