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

    def request_cards(self):
        return requests.get("https://tarotapi.dev/api/v1/cards/random").json() 

    def generate_deck(self, num_cards):
        allcards = request_cards()
        return allcards[0, num_cards]
        
    def display_info(self, card):
        card_content = self.deck    
    

    def __init__(self):
        self.deck = self.generate_deck()        

        

if __name__ == "__main__":
    game = Solitaire()        
