from .mau_mau import MauMau
from Utilities.card import Card
from Utilities.player import Player


def convert_to_card(color: str, value: str) -> Card:
    try:
        return Card(color, value)
    except:
        return None

def convert_to_json(card: Card) -> dict:
    return {"color": card.color, "value": card.value}


def start_mau_mau_game(players : list) -> str:
    game = MauMau(players)

    # geben:
    if not game.give():
        return "to many players"

    for player in game.players:
        player_hand: list = [(card.color, card.value) for card in player.hand]
        cache_current_card = (game.current_card.color, game.current_card.value)
        player.send({"initial_cards": player_hand, "current_card": cache_current_card})

    # spielen:
    while True:

        if not game.current_player.send({"turn": game.current_player.name}):
            print("error1")
            
        data: dict = game.current_player.receive()

        # {"instr": x, "color": str, "value": str, "amount": int, "error": bool}

        cache_player: Player = game.current_player
        end = 0

        if data["error"] == 1:
            print("error2")  
            break      

        elif data["instr"] == "pull_card":
            amount: int = data["amount"]
            cards: list = game.pull_new_card(amount)
            for i in range(len(cards)):
                cards[i] = (cards[i].color, cards[i].value)
            if cards == []:
                print("not enough cards")
            cache_player.send({"new_card": cards})
            new_game_state: dict = {"message": "got_card", "amount": amount}

        elif data["instr"] == "play_card":
            card: Card = convert_to_card(data["color"], data["value"])
            winner = None
            info: dict = game.set(card)
            if info["error"] == "invalid_card":
                # client has to try again, game state was not updated
                cache_player.send({"error": "invalid_card"})
                continue
            if info["winner"] == 1:
                winner = cache_player.name
                if info["end"] == 1:
                    end = 1
            new_game_state: dict = {
                "message": "card_set", 
                "color": card.color, 
                "value": card.value, 
                "next_player": game.current_player.name,  
                "winner": winner, 
                "end": end, 
                "current_card": (game.current_card.color, game.current_card.value) 
            }


        for player in game.players:
            if not player.send(new_game_state):
                print("sending_error")
        
        if end == 1:
            break
    
    return "played"
        
        


