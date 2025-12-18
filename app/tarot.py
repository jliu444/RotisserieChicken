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

class Tarot:

    def __init__(self):
        self.deck = self.generate_deck(20)
        self.active_cards = [self.display_info(self.deck[1]), self.display_info(self.deck[2])]  



    def request_cards(self):
        return requests.get("https://tarotapi.dev/api/v1/cards/random").json()
        
        
    def generate_deck(self, num_cards):
        allcards = self.request_cards()
        return allcards["cards"][:num_cards]
        
    def display_info(self, card):
        name = card['name']
        meaning = card['meaning_up']
        description = card['desc'].split(".")[:3]
        return [name, meaning, description]
        
        

if __name__ == "__main__":
    game = Tarot()        
