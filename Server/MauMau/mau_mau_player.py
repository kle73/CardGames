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
        return "to_many_players"

    for player in game.players:
        player_hand: list = [(card.color, card.value) for card in player.hand]
        cache_current_card = (game.current_card.color, game.current_card.value)
        player.send({"initial_cards": player_hand, "current_card": cache_current_card})

    # spielen:
    while True:

        if not game.current_player.send({"turn": game.current_player.name}):
            return "network_error"
            
        data: dict = game.current_player.receive()

        # {"instr": x, "color": str, "value": str, "amount": int, "error": bool}

        cache_player: Player = game.current_player
        end = 0

        if data["error"] == 1:
            return "error"    

        elif data["instr"] == "pull_card":
            amount: int = data["amount"]
            cards: list = []
            try:
                cards = game.pull_new_card(amount)
            except:
                cache_player.send({"error": "pull_more_cards", "amount": game.number_of_seven*2})
                continue
            for i in range(len(cards)):
                cards[i] = (cards[i].color, cards[i].value)
            cache_player.send({"new_card": cards})
            new_game_state: dict = {"message": "got_card", "amount": amount, "winner": None, "current_hand": []}

        elif data["instr"] == "play_card":
            card: Card = convert_to_card(data["color"], data["value"])
            winner = None
            info: dict = game.set(card)
            color: str = None

            if info["error"] == "invalid_card":
                # client has to try again, game state was not updated
                cache_player.send({"error": "invalid_card"})
                continue

            if info["winner"] == 1:
                winner = cache_player.name
                if info["end"] == 1:
                    end = 1

            if info["prompt"] == "choose_color":
                game.current_player.send({"prompt": "choose_color"})
                color_data = game.current_player.receive()
                if "color" in color_data.keys():
                    color = color_data["color"]

            new_game_state: dict = {
                "message": "card_set", 
                "color": card.color, 
                "value": card.value, 
                "next_player": game.current_player.name,  
                "winner": winner, 
                "end": end, 
                "current_card": (game.current_card.color, game.current_card.value), 
                "current_hand": [],
                "new_color": color
            }


        for player in game.players:
            new_game_state["current_hand"] = [(c.color, c.value) for c in player.hand]
            if not player.send(new_game_state):
                return "network_error"
        
        if end == 1:
            break
    
    return "end"
        
        


