from .mau_mau import MauMau
from Utilities.card import Card
from Utilities.player import Player
from Exceptions.mau_mau_exceptions import NetworkError, PlayerOverflowError


def convert_to_card(color: str, value: str) -> Card:
    try:
        return Card(color, value)
    except:
        return None

def convert_to_tuple(card: Card) -> tuple:
    return (card.color, card.value)


def request_color(player: Player, game: MauMau) -> str:
    player.send({"prompt": "choose_color"})
    color_data = player.receive()
    if "color" in color_data.keys():
        color = color_data["color"]
        game.color_to_serve = color


def play(players : list):
    game = MauMau(players)

    # geben:
    if not game.give():
        raise PlayerOverflowError("to many players")

    

    for player in game.players:
        player_hand: list = [convert_to_tuple(card) for card in player.hand]
        cache_current_card = convert_to_tuple(game.current_card)
        if not player.send({"initial_cards": player_hand, "current_card": cache_current_card}):
            raise NetworkError("player unreachable")

    if game.color_to_serve != None:   
        request_color(game.current_player, game)

    # spielen:
    while True:

        if not game.current_player.send({"turn": game.current_player.name}):
            raise NetworkError("Could not send state to player.")
            
        data: dict = game.current_player.receive()

        # {"instr": x, "color": str, "value": str, "amount": int, "error": bool}

        cache_player: Player = game.current_player
        end = 0

        if data["error"] == 1:
            raise RuntimeError   

        elif data["instr"] == "pull_card":
            amount: int = data["amount"]
            cards: list = []
            try:
                cards = game.pull_new_card(amount)
            except ValueError:
                if not cache_player.send({"error": "pull_more_cards", "amount": game.number_of_seven*2}):
                    raise NetworkError("player unreachable")
                continue

            for i, card in enumerate(cards):
                cards[i] = convert_to_tuple(card)

            new_game_state: dict = {
                "message": "got_card", 
                "amount": amount, 
                "winner": None, 
                "current_hand": [],
                "current_card": convert_to_tuple(game.current_card),
                "other_counts": {}
                }

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
                if not cache_player.send({"message": "winner", "winner": "you", "current_hand": [], "current_card": convert_to_tuple(game.current_card)}):
                    raise NetworkError("player unreachable")

                if info["end"] == 1:
                    end = 1

            if info["prompt"] == "choose_color":
                request_color(game.last_player, game)

            new_game_state: dict = {
                "message": "card_set", 
                "color": card.color, 
                "value": card.value, 
                "next_player": game.current_player.name,  
                "winner": winner, 
                "end": end, 
                "current_card": convert_to_tuple(game.current_card), 
                "current_hand": [],
                "new_color": game.color_to_serve,
                "other_counts": {}
            }

        for player in game.players:
            new_game_state["other_counts"][player.name] = len(player.hand)

        for player in game.players:
            new_game_state["current_hand"] = [ convert_to_tuple(c) for c in player.hand]
            if not player.send(new_game_state):
                raise NetworkError("player unreachable")
        
        if end == 1:
            break
    


def start_mau_mau_game(players: list):
    try:
        play(players)
    except NetworkError:
        print("one player seems to be unreachable")
    except PlayerOverflowError:
        print("there are to many players for this game")
    except RuntimeError:
        print("error, game ended")



        
        


