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
    def new_pile(self, deck_id, pile_name):
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/add/?cards=')

    def show_pile_cards(self, deck_id, pile_name):
        pile = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/list/').json()
        list_of_cards = []
        if pile['piles'][pile_name]['remaining'] != 0:
            for i in pile['piles'][pile_name]['cards']:
                list_of_cards.append([i["image"], i["value"], i["suit"], 'back'])
        return list_of_cards

    def populate_pile(self, deck_id, pile_name, amount):
        draw_from_deck = requests.get(f'https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count={amount}').json()
        card_list = ''
        for i in draw_from_deck["cards"]:
            card_list = card_list + i["code"] + ","
        card_list = card_list[:-1]
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/add/?cards={card_list}')

    def flip_top(self, pile):
        # only run if pile is not empty
        if self.card_dict[pile] != []:
            if self.card_dict[pile][0][3] == 'front':
                self.card_dict[pile][0][3] = 'back'
            else:
                self.card_dict[pile][0][3] = 'front'

    def isEmpty(self, pile):
        if self.card_dict[pile] == []:
            return True
        return False

    def endMove(self):
        self.active_card = []
        self.active_pile = ''
        self.active_card2 = []
        self.active_pile2 = ''

    def card_location(self, pile, card):
        if self.card_dict[pile] != []:
            return self.card_dict[pile].index(card)
        else:
            return 0

    def t_valid(self):
        #you can never move a card into a spot that isn't at the top of a tableau
        if self.card_location(self.active_pile2, self.active_card2) != 0:
            return False
        ac_color = self.getColor(self.active_card)
        ac_number = self.getNumber(self.active_card)
        if self.card_dict[self.active_pile2] == []:
            if ac_number == 13:
                return True
        else:
            ac_color2 = self.getColor(self.active_card2)
            ac_number2 = self.getNumber(self.active_card2)
            if ac_color != ac_color2 and ac_number == (ac_number2-1):
                return True
        return False

    def f_valid(self):
        if self.card_location(self.active_pile, self.active_card) != 0:
            return False
        ac_number = self.getNumber(self.active_card)
        if self.card_dict[self.active_pile2] == []:
            if ac_number == 1:
                return True
        else:
            ac_number2 = self.getNumber(self.active_card2)
            if (self.active_card[2] == self.active_card2[2]) and ac_number == (ac_number2+1):
                return True
        return False

    def getNumber(self, card):
        ac_number = 0
        if card[1] == 'JACK': ac_number = 11
        elif card[1] == 'QUEEN': ac_number = 12
        elif card[1] == 'KING': ac_number = 13
        elif card[1] == 'ACE': ac_number = 1
        else: ac_number = int(card[1])
        return ac_number

    def getColor(self, card):
        ac_color = ''
        if card[2] == 'DIAMONDS' or card[2] == 'HEARTS': ac_color = 'red'
        else: ac_color= 'black'
        return ac_color

    def play(self):
        #always have a pile and card selected
        if not self.active_pile or not self.active_card:
            self.endMove()
            return
        
        #cannot use empty tableau, waste, or empty foundation
        if self.active_pile == 'waste' or 'tableau' in self.active_pile or 'foundation' in self.active_pile:
            if self.card_dict[self.active_pile] == []:
                self.endMove()
                return

        # if active card is from STOCK, move it to WASTE
        if self.active_pile == 'stock':
            # restock stock pile if empty
            if self.isEmpty('stock'):
                self.flip_top('waste')
                while self.isEmpty('waste') == False:
                    self.card_dict['stock'].insert(0, self.card_dict['waste'].pop(0))
            # move next card to waste
            self.flip_top('waste')
            self.card_dict['waste'].insert(0, self.card_dict['stock'].pop(0))
            self.flip_top('waste')
            # no need for second decision
            self.endMove()
            return

        # if active card is from TABLEAU and is hidden, flip it
        if 'tableau' in self.active_pile and self.card_location(self.active_pile, self.active_card) == 0  and self.active_card[3] == 'back':
            self.flip_top(self.active_pile)
            self.endMove()
            return 

        # in all other cases, if card is still hidden, move cannot be made
        if self.active_card[3] == 'back':
            self.endMove()
            return

        else:
            # if target location is TABLEAU
            if 'tableau' in self.active_pile2:
                print('tableau seen')
                if self.t_valid():
                    print('tableau validated')
                    # need to add case for trying to move multiple cards from one tableau to another
                    for i in range (self.card_location(self.active_pile,self.active_card), -1, -1):
                        self.card_dict[self.active_pile2].insert(0, self.card_dict[self.active_pile].pop(i))
                self.endMove()
                return 
            if 'foundation' in self.active_pile2:
                print('foundation seen')
                if self.f_valid():
                    print('foundation validated')
                    self.card_dict[self.active_pile2].insert(0, self.card_dict[self.active_pile].pop(0))
                self.endMove()
                return

            # always make sure that even if active_card is taken from waste, next card is available for use
            if self.isEmpty('waste') == False:
                if self.card_dict['waste'][0][3] == 'back':
                    self.flip_top('waste')

    def __init__(self):
        # create the deck
        self.master_deck = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/').json()
        self.deck_id = ''
        self.active_card = []
        self.active_pile = ''
        self.active_card2 = []
        self.active_pile2 = ''
        self.card_dict = {}
        if self.master_deck["success"]:
            self.deck_id = self.master_deck["deck_id"]
            self.deck_size = self.master_deck["remaining"]

            # create all other piles
            self.new_pile(self.deck_id, 'stock')
            self.new_pile(self.deck_id, 'waste')
            self.new_pile(self.deck_id, 'foundation1')
            self.new_pile(self.deck_id, 'foundation2')
            self.new_pile(self.deck_id, 'foundation3')
            self.new_pile(self.deck_id, 'foundation4')
            self.new_pile(self.deck_id, 'tableau1')
            self.new_pile(self.deck_id, 'tableau2')
            self.new_pile(self.deck_id, 'tableau3')
            self.new_pile(self.deck_id, 'tableau4')
            self.new_pile(self.deck_id, 'tableau5')
            self.new_pile(self.deck_id, 'tableau6')
            self.new_pile(self.deck_id, 'tableau7')

            #populate tableaus
            self.populate_pile(self.deck_id, 'tableau1', 1)
            self.populate_pile(self.deck_id, 'tableau2', 2)
            self.populate_pile(self.deck_id, 'tableau3', 3)
            self.populate_pile(self.deck_id, 'tableau4', 4)
            self.populate_pile(self.deck_id, 'tableau5', 5)
            self.populate_pile(self.deck_id, 'tableau6', 6)
            self.populate_pile(self.deck_id, 'tableau7', 7)

            #populate stock
            self.populate_pile(self.deck_id, 'stock', 24)

            #populate dict
            self.card_dict["stock"] = self.show_pile_cards(self.deck_id, "stock")
            self.card_dict["waste"] = self.show_pile_cards(self.deck_id, "waste")
            self.card_dict["foundation1"] = self.show_pile_cards(self.deck_id, "foundation1")
            self.card_dict["foundation2"] = self.show_pile_cards(self.deck_id, "foundation2")
            self.card_dict["foundation3"] = self.show_pile_cards(self.deck_id, "foundation3")
            self.card_dict["foundation4"] = self.show_pile_cards(self.deck_id, "foundation4")
            self.card_dict["tableau1"] = self.show_pile_cards(self.deck_id, "tableau1")
            self.card_dict["tableau2"] = self.show_pile_cards(self.deck_id, "tableau2")
            self.card_dict["tableau3"] = self.show_pile_cards(self.deck_id, "tableau3")
            self.card_dict["tableau4"] = self.show_pile_cards(self.deck_id, "tableau4")
            self.card_dict["tableau5"] = self.show_pile_cards(self.deck_id, "tableau5")
            self.card_dict["tableau6"] = self.show_pile_cards(self.deck_id, "tableau6")
            self.card_dict["tableau7"] = self.show_pile_cards(self.deck_id, "tableau7")

            self.flip_top('tableau1')
            self.flip_top('tableau2')
            self.flip_top('tableau3')
            self.flip_top('tableau4')
            self.flip_top('tableau5')
            self.flip_top('tableau6')
            self.flip_top('tableau7')

        else:
            print ("deck creation failed")


if __name__ == "__main__":
    game = Solitaire()

    '''
    def move_cards(self, deck_id, init_pile_name, final_pile_name, amount):
        # move top card from the init_pile to deck
        for i in range(amount):
            requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{init_pile_name}/return/')
        # add all deck cards to final_pile
        requests.get(f'https://www.deckofcardsapi.com/api/deck/{deck_id}/return/')
        populate_pile(deck_id, final_pile_name, amount)

    def check_top(self, deck_id, pile):
        # figure out why pile is not updating asap. then remove the hard code
        pile = 'stock'
        card_list = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile}/list/').json()
        return [card_list['piles'][pile]['cards'][0]['value'], card_list['piles'][pile]['cards'][0]['suit']]

    def confirm_top(self, active_card, top_card):
        if active_card[0] == top_card[0] and active_card[1] == top_card[1]:
            return True
        else:
            return False

    def return_waste(self, deck_id):
        requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/pile/waste/return/')
    '''


    '''
    top_card = self.check_top(self.deck_id, self.active_pile)
    top = self.confirm_top(self.active_card, top_card)
    # if active card is in a stock
    if (self.active_pile == 'stock'):
        if top and self.card_dict['stock'][0][3] == 'back':
            self.card_dict['stock'][0][3] == 'front'
    # if active card is in a tableau
    if (self.active_pile == 'tableau1') or (self.active_pile == 'tableau2') or (self.active_pile == 'tableau3') or (self.active_pile == 'tableau4') or (self.active_pile == 'tableau5') or (self.active_pile == 'tableau6') or (self.active_pile == 'tableau7'):
        if self.active_card[0] == top_card[0] and self.active_card[1] == top_card[1]:
            # check if hidden, if hidden, un-hide it
            pass
    '''
