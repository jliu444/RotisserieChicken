'''
Concept:
- add a restart button
  - user selects 1 item from FOUNDATIONS, STOCK, WASTE, OR TABLEAU and calls the function
    -> if the one item is a hidden card at the top of a tableau, show the card
    -> if the one item is an ace at the top of a tableau, place it in foundation pile
    -> if the one item is a stock card, place it (not hidden) on top of the waste pile
    -> ELSE, record active card and reload page
      -> user selects an item from TOP OF FOUNDATIONS or TOP OF TABLEAU and calls the function
        -> if second item is a TABLEAU, check if tableau is empty
          -> if empty and active card is a King: move the King
          -> if empty and active card is not a King: INVALID MOVE
          -> is not empty and active card is (same color) OR (not next #): INVALID MOVE
          -> ELSE: move the item and all the cards beneath it
          -> AFTER ALL THESE IFS, IF ACTIVE CARD IS A FOUNDATION, SHOW THE NEXT FOUNDATION CARD
        -> if second item is a FOUNDATION:
          -> if foundation is empty, INVALID move
          -> if card on top of foundation is (different house) OR (not next #): INVALID move
          -> if active card is NOT top of pile: INVALID move
          -> ELSE: move card into foundation
'''
import requests

class Solitaire:
    def __init__(self):
        # create the deck
        master_deck = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/').json()
        deck_id = ''
        if master_deck["success"]:
            deck_id = master_deck["deck_id"]
            deck_size = master_deck["remaining"]
            abc = "id: " + deck_id + "deck size: " + str(deck_size)

            # create all other piles
            new_pile(deck_id, 'stock_deck')
            new_pile(deck_id, 'waste_deck')
            new_pile(deck_id, 'foundation_1')
            new_pile(deck_id, 'foundation_2')
            new_pile(deck_id, 'foundation_3')
            new_pile(deck_id, 'foundation_4')
            new_pile(deck_id, 'tableau_1')
            new_pile(deck_id, 'tableau_2')
            new_pile(deck_id, 'tableau_3')
            new_pile(deck_id, 'tableau_4')
            new_pile(deck_id, 'tableau_5')
            new_pile(deck_id, 'tableau_6')
            new_pile(deck_id, 'tableau_7')

            #populate tableaus
            populate_pile(deck_id, 'tableau_1', 1)
            populate_pile(deck_id, 'tableau_2', 2)
            populate_pile(deck_id, 'tableau_3', 3)
            populate_pile(deck_id, 'tableau_4', 4)
            populate_pile(deck_id, 'tableau_5', 5)
            populate_pile(deck_id, 'tableau_6', 6)
            populate_pile(deck_id, 'tableau_7', 7)

            #populate stock
            populate_pile(deck_id, 'stock_deck', 24)

        else:
            abc = 'deck creation failed'

        return abc

    def new_pile(deck_id, pile_name):
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/add/?cards=').json()

    def show_pile(deck_id, pile_name):
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/list/')

    def return_waste(deck_id):
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/waste/return/')

    def populate_pile(deck_id, pile_name, amount):
        draw_from_deck = requests.get(f'https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count={amount}').json()
        card_list = ''
        for i in draw_from_deck["cards"]:
            card_list = cardlist + i["code"] + ","
        card_list = card_list[:-1]
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{name}/add/?cards={card_list}')

    def move_cards(deck_id, init_pile_name, final_pile_name, amount):
        # discard a card from the init_pile
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{init_pile_name}/draw/')
        # add all discarded cards to target pile


    ''' reminder to self about piles
    player2": {
                "cards": [
                    {
                        "image": "https://deckofcardsapi.com/static/img/KH.png",
                        "value": "KING",
                        "suit": "HEARTS",
                        "code": "KH"
                    },
                    {
                        "image": "https://deckofcardsapi.com/static/img/8C.png",
                        "value": "8",
                        "suit": "CLUBS",
                        "code": "8C"
                    }
                ],
                "remaining": "2"
            }
    '''

if __name__ == "__main__":
    game = Solitaire()
