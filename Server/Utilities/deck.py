from .card import Card
import random

class Deck:

    def __init__(self):
        self.deck = []
        self.colors = ["schellen", "herzen", "gruene", "eicheln"]
        self.values = ["7", "8", "9", "10", "O", "U", "K", "A"]
        self.shuffle()
    
    # puts all cards back into deck 
    def shuffle(self) -> None:
        self.deck = []
        for color in self.colors:
            for value in self.values:
                self.deck.append(Card(color, value))
    
    # gets a random card out of deck and removes it
    def get_card(self) -> Card:
        i: int = random.randint(0, len(self.deck)-1)
        card: Card = self.deck.pop(i)
        return card


    
