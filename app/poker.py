import requests

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.value = self.get_value()
        self.hand = self.get_hand()

    def get_hand(self):
        strength = self.value // (10**10)
        if strength == 8:
            return "Straight Flush"
        if strength == 7:
            return "Four of a Kind"
        if strength == 6:
            return "Full House"
        if strength == 5:
            return "Flush"
        if strength == 4:
            return "Straight"
        if strength == 3:
            return "Three of a Kind"
        if strength == 2:
            return "Two Pair"
        if strength == 1:
            return "Pair"
        if strength == 0:
            return "High Card"
        return "Invalid"

    def get_value(self):
        '''
        Evalute the poker hand by finding the best 5-card combination
        and returns integer value representing the hand's strength.
        '''

        possible_hands = []
        self.generate_unique_combinations(self.cards, 5, possible_hands)

        value = 0
        for hand in possible_hands:
            hand_value = self._get_value(hand)
            value = max(value, hand_value)

        return value

    def _get_value(self, hand: list):
        '''
        Evaluate a 5-card hand and return its value

        Hand Strength key:
        - 0: high card
        - 1: one pair
        - 2: two pair
        - 3: three of a kind
        - 4: straight
        - 5: flush
        - 6: full house
        - 7: four of a kind
        - 8: straight flush

        returns: hand_strength * 10^10 + encoding
        '''

        def encode(values: list):
            result = 0
            for value in values:
                result = result * 15 + value # base-15 since max rank is 14
            return result

        def get_rank(code: str):
            rank = code[0]
            if rank.isnumeric():
                if rank == "0":
                    return 10
                return int(rank)
            elif rank == "J":
                return 11
            elif rank == "Q":
                return 12
            elif rank == "K":
                return 13
            elif rank == "A":
                return 14

        ranks = sorted([get_rank(card) for card in hand], reverse=True)

        suits = [card[1] for card in hand]

        counts = {}
        for r in ranks:
            counts[r] = counts.get(r, 0) + 1

        # sorting by count descending, then rank descending
        counts = sorted(counts.items(), key=lambda x: (-x[1], -x[0]))

        is_flush = len(set(suits)) == 1

        is_straight = False
        unique = sorted(set(ranks), reverse=True)
        straight_high = None

        if len(unique) == 5:
            if unique[0] - unique[4] == 4:
                is_straight = True
                straight_high = unique[0]
            # A-5 straight
            elif unique == [14, 5, 4, 3, 2]:
                is_straight = True
                straight_high = 5

        # straight flush
        if is_flush and is_straight:
            return 8 * 10**10 + encode([straight_high])

        # four of a kind
        if counts[0][1] == 4:
            quad = counts[0][0]
            kicker = counts[1][0]
            return 7 * 10**10 + encode([quad, kicker])

        # full house
        if counts[0][1] == 3 and counts[1][1] == 2:
            triple = counts[0][0]
            pair = counts[1][0]
            return 6 * 10**10 + encode([triple, pair])

        # flush
        if is_flush:
            return 5 * 10**10 + encode(ranks)

        # straight
        if is_straight:
            return 4 * 10**10 + encode([straight_high])

        # three of a kind
        if counts[0][1] == 3:
            triple = counts[0][0]
            kickers = [r for r in ranks if r != triple]
            return 3 * 10**10 + encode([triple] + kickers)

        # two pair
        if counts[0][1] == 2 and counts[1][1] == 2:
            high_pair = counts[0][0]
            low_pair = counts[1][0]
            kicker = counts[2][0]
            return 2 * 10**10 + encode([high_pair, low_pair, kicker])

        # one pair
        if counts[0][1] == 2:
            pair = counts[0][0]
            kickers = [r for r in ranks if r != pair]
            return 1 * 10 ** 10 + encode([pair] + kickers)

        # high card
        return encode(ranks)

    # generate all unique k-card combinations from the available cards
    def generate_unique_combinations(self, cards: list, k: int, combinations: list, combination=[], start=0):
        if len(combination) == k:
            combinations.append(combination.copy())
            return

        for i in range(start, len(cards)):
            combination.append(cards[i])
            self.generate_unique_combinations(cards, k, combinations, combination, i + 1)
            combination.pop()


class Poker:
    def __init__(self, player_chips: int):
        # Initialize deck
        response = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
        )
        data = response.json()
        self.deck_id = data["deck_id"]
        self.board_cards = []
        self.hole_cards = []

        # Constants
        self.PLAYER = 0
        self.OPPONENT = 1

        # Game state
        self.player_to_move = self.PLAYER
        self.max_chips = player_chips
        self.stakes = [0, 0] # 0 <= stakes <= max_chips
        self.round_bets = [0, 0] # reset to [0, 0] every betting round
        self.winner = None
        self.is_game_over = False
    
    def set_chips(self, num_chips: int):
        self.max_chips = num_chips

    def deal_hole(self):
        card_info = self.draw(4)["cards"]
        dealt_cards = [card_info[i] for i in range(len(card_info))]
        self.hole_cards.append(dealt_cards[0::2])
        self.hole_cards.append(dealt_cards[1::2])

    def burn_card(self):
        return self.draw(1)

    def deal_board(self, num: int):
        card_info = self.draw(num)["cards"]
        for i in range(len(card_info)):
            self.board_cards.append(card_info[i])

    def check_or_call(self):
        opp_bet = self.round_bets[self.next_player()]
        curr_bet = self.round_bets[self.player_to_move]
        to_bet = opp_bet - curr_bet

        # call, within budget (equivalent to check if to_bet == 0)
        if self.stakes[self.player_to_move] + to_bet <= self.max_chips:
            self.stakes[self.player_to_move] += to_bet
            self.round_bets[self.player_to_move] += to_bet

        # call, not within budget
        else:
            to_bet = self.max_chips - self.stakes[self.player_to_move]
            self.stakes[self.player_to_move] += to_bet
            self.round_bets[self.player_to_move] += to_bet

        self.player_to_move = self.next_player()
        return to_bet

    def make_bet_or_raise_to(self, amt: int):
        if amt <= max(self.round_bets):
            raise ValueError("Bet/Raise amount must be greater than opponent's bet.")

        curr_bet = self.round_bets[self.player_to_move]
        to_bet = amt - curr_bet

        if self.stakes[self.player_to_move] + to_bet > self.max_chips:
            raise ValueError("Bet/Raise amount exceeds player's chip count.")

        self.stakes[self.player_to_move] += to_bet
        self.round_bets[self.player_to_move] += to_bet
        self.player_to_move = self.next_player()

    def fold(self):
        winner = self.next_player()
        self.is_game_over = True

    def showdown(self):
        player_hand = Hand(
            [card["code"] for card in self.hole_cards[self.PLAYER]] + \
            [card["code"] for card in self.board_cards]
        )

        opponent_hand = Hand(
            [card["code"] for card in self.hole_cards[self.OPPONENT]] + \
            [card["code"] for card in self.board_cards]
        )

        self.winner = None

        player_value = player_hand.value
        opponent_value = opponent_hand.value

        if player_value > opponent_value:
            self.winner = self.PLAYER
        elif opponent_value > player_value:
            self.winner = self.OPPONENT

        self.is_game_over = True

    def reset_round_bets(self):
        self.round_bets = [0, 0]

    def draw(self, num: int):
        return requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/draw/?count={num}"
        ).json()

    def next_player(self):
        if self.player_to_move == self.PLAYER:
            return self.OPPONENT
        else:
            return self.PLAYER

    def get_winnings(self):
        if self.winner == self.PLAYER:
            return self.stakes[self.OPPONENT]
        elif self.winner == self.OPPONENT:
            return -self.stakes[self.PLAYER]
        return 0 # tie

    def reset_game(self, player_chips):
        requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/return/"
        )

        requests.get(
            f"https://deckofcardsapi.com/api/deck/{self.deck_id}/shuffle/"
        )

        self.board_cards = []
        self.hole_cards = []
        self.player_to_move = self.PLAYER
        self.max_chips = player_chips
        self.stakes = [0, 0]
        self.round_bets = [0, 0]
        self.winner = None
        self.is_game_over = False

if __name__ == "__main__":
    pass
