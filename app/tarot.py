'''
Generate a list of random tarot cards, and double it
Paste them randomly in a grid, all with a back card cover image
Front cover image?
Cards that are flipped over display their information on the box on the right
Up to two cards can be flipped at once and show their information on the right
If two cards are flipped and they are equal, they are removed
If two cards are flipped and arent the same, nothing happens
if third card is flipped, it becomes the first card flipped
'''

import requests
import random

class Tarot:

    def __init__(self):
        self.deck = self.generate_deck(4)
        self.active_card_ids = [None, None]

    def request_cards(self):
        return requests.get("https://tarotapi.dev/api/v1/cards/random").json()
        
    def generate_deck(self, num_cards):
        allcards = self.request_cards()
        allcards = allcards["cards"][:num_cards] * 2
        random.shuffle(allcards)
        return allcards
        
    def display_info(self, card):
        if card == None:
            return ["", "", "", ""]

        name = card["name"]
        meaning = card["meaning_up"]
        descr_list = card["desc"].split(".")[:3]
        descr_words = descr_list[0]
        i = 1

        for line in descr_list[1:]:
            descr_words = descr_words + ". " + descr_list[i]
            i=i+1

        return [name, meaning, descr_words, None]
        
    def all_matched(self):
        return all(card.get("matched", False) for card in self.deck)
        

if __name__ == "__main__":
    game = Tarot()        
