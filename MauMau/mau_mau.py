from Utilities.deck import Deck
from Utilities.card import Card

class MauMau:

    def __init__(self, players: list):
        print("maumau started")
        if len(players) < 2:
            raise "RuntimeError"
        self.players = players
        self.current_player = players[0]
        self.deck = Deck()

    def set(card: Card):
        pass
    