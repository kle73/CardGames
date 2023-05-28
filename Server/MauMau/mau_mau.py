from Utilities.deck import Deck
from Utilities.card import Card
from Utilities.player import Player

class MauMau:

    def __init__(self, players: list):
        if len(players) < 2:
            raise "RuntimeError"
        self.players = players
        self.current_player = players[0]
        self.deck = Deck()
        self.deck.shuffle()
        self.current_card = None
        self.stapel = []
        self.number_of_seven = 0
        self.last_player = None
        self.color_to_serve = None

    def cards_equal(self, card_one: Card, card_two: Card) -> bool:
        if card_one.value == card_two.value and card_one.color == card_two.color:
            return True
        return False

    def remove_card_from_hand(self, card: Card) -> bool:
        for c in self.current_player.hand:
            if self.cards_equal(c, card):
                self.current_player.hand.remove(c)
                return True
        return False
    
    def valid_card(self, card: Card) -> bool:
        if self.current_card is None:
            return True
        if self.number_of_seven > 0:
            if not card.value == "7":
                return False
        if card.value == "U":
            return True
        elif self.current_card.value == card.value:
            return True
        elif self.current_card.color == card.color:
            return True
        return False



    def give(self) -> bool:
        hand_size = 26 // len(self.players) 
        if hand_size == 0:
            return False
        for player in self.players:
            for i in range(hand_size):
                player.hand.append(self.deck.get_card())
        self.current_card = self.deck.get_card()

        if self.current_card.value == "7":
            self.number_of_seven += 1
        elif self.current_card.value == "A":
            self.current_player = self.players[1]
        n: int = len(self.deck.deck)
        for i in range(n):
            self.stapel.append(self.deck.get_card())
        return True
    
    def pull_new_card(self, amount: int) -> list:

        if self.number_of_seven > 0:
            if amount < self.number_of_seven*2:
                raise RuntimeError
            else:
                self.number_of_seven = 0

        result = []
        for i in range(amount):
            try:
                card: Card = self.stapel.pop(0)
                result.append(card)
                self.current_player.hand.append(card)
            except:
                break
        current_player_index = self.players.index(self.current_player) 
        self.current_player = self.players[(current_player_index+1)%len(self.players)]
        return result
        
                
    # returns json object with game info to caller 
    def set(self, card: Card) -> dict:
        info = {
            "winner": 0,
            "error": None,
            "end": 0,
            "prompt": None
        }

        if not self.remove_card_from_hand(card) or not self.valid_card(card):
            info["error"] = "invalid_card"
            return info
        
        if self.current_card:
            self.stapel.append(self.current_card)
        self.current_card = card

        #check if was 7:
        if card.value == "7":
            self.number_of_seven += 1
        elif card.value == "U":
            info["prompt"] = "choose_color"

        # determine next player
        next_player_offset: int = 1
        if self.current_card.value == "A":
            next_player_offset = 2
        current_player_index = self.players.index(self.current_player)
        next_player = self.players[(current_player_index + next_player_offset) % len(self.players)]

        # determine if a player has won
        if len(self.current_player.hand) == 0:
            info["winner"] = 1
            self.players.remove(self.current_player)
            if len(self.players) == 1:
                info["end"] == 1

        
        # update next player
        self.current_player = next_player
        return info
 


    