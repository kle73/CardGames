from .mau_mau import MauMau
from Utilities.card import Card


def convert_to_card(data: str) -> Card:
    pass

def convert_to_json(card: Card) -> str:
    pass


def start_mau_mau_game(players : list):
    game = MauMau(players)
"""
    #geben:
    for player in game.players:
        player.send(player.hand)

    #spielen:
    while True:

        try:
            game.current_player.send("play: ")
            data: str = game.current_player.rcv()
            card: Card = convert_to_card
            game.set(card)
            #distribute new gamestate
            for player in game.players:
                player.send(card)
            #..."""


