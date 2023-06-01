import threading
import socket
import json
import sys
import os

data_buffer = []

def listening(server: socket.socket):
    global data_buffer
    while True:
        message = server.recv(2048).decode()
        try:
            message_dict = json.loads(message)
        except:
            break
        data_buffer.append(message_dict)



def print_my_cards(cards: list):
    sys.stdout.write("your hand:\n")
    for i, card in enumerate(cards):
        if (i == len(cards)-1):
            sys.stdout.write("_______\n")
            break
        sys.stdout.write("____")

    for i, card in enumerate(cards):
        if (i == len(cards)-1):
            sys.stdout.write(f"|{card[0][0]}   {card[1]}|\n")
            break
        sys.stdout.write(f"|{card[0][0]}{(3-len(card[0][0]))*' '}")

    for k in range(3):
        for i, card in enumerate(cards):
            if (i == len(cards)-1):
                sys.stdout.write(f"|{(4+len(card[1]))*' '}|\n") 
                break
            sys.stdout.write("|   ")

    for i, card in enumerate(cards):
        if (i == len(cards)-1):
            sys.stdout.write(f"|{card[1]}   {card[0][0]}|\n")
            break
        sys.stdout.write(f"|{card[1]}{(3-len(card[1]))*' '}") 
    
    for i, card in enumerate(cards):
        if (i == len(cards)-1):
            sys.stdout.write("-------\n")
            break
        sys.stdout.write("----")



def print_screen(hand, current_card):
    os.system("clear")
    print_my_cards(hand)
    sys.stdout.write(f"current card: {current_card}\n")

def prompt(message: str) -> str:
    result: str = input(message)
    n: int = len(message) + len(result)
    sys.stdout.write("\033[F\r" + " "*n + "\r")
    return result


def start_mau_mau(server: socket.socket, name: str):

    which_game = json.dumps({"game": "mau_mau", "name": name})
    server.sendall(which_game.encode())

    listener_thread = threading.Thread(target=listening, args=(server,))
    listener_thread.start()


    my_cards = []
    while True:
        global data_buffer
        if len(data_buffer) > 0:
            data = data_buffer.pop(0)

            if 'initial_cards' in data.keys():
                for card in data["initial_cards"]:
                    my_cards.append(card)
                print_screen(my_cards, data["current_card"])

            elif 'turn' in data.keys():
                instr: str = None
                amt: int = 0
                input_color: str = None
                input_value: str = None
                while True:
                    input_command = prompt("[set|get]: ")
                    if input_command == "set":
                        input_color = prompt("set card color: ")
                        input_value = prompt("set card value: ")
                        instr = "play_card"
                    elif input_command == "get":
                        amt = int(prompt("how many: "))
                        instr = "pull_card"
                    else:
                        continue
                    to_send = json.dumps({
                        "instr": instr,
                        "color": input_color, 
                        'value': input_value,
                        'amount': amt,
                        'error': 0
                    })
                    server.sendall(to_send.encode())
                    break
            
            elif "prompt" in data.keys():
                if data["prompt"] == "choose_color":
                    color = prompt("choose your color: ")
                    to_send = json.dumps({"color": color})
                    server.sendall(to_send.encode())

            elif 'message' in data.keys():
                print_screen(data["current_hand"], data["current_card"])
                if data['winner']:
                    sys.stdout.write(f'{data["winner"]} won the game! \n')
                if data.get("new_color"):
                    sys.stdout.write(f"new color: {data['new_color']}\n") 
                if data.get("end") == 1:
                    sys.stdout.write(f"GAME IS OVER\n")
                    break
                if data.get("other_counts"):
                    for key in data["other_counts"].keys():
                        if key != name:
                            sys.stdout.write(f"{key} has {data['other_counts'][key]} cards\n")
                
            elif 'error' in data.keys():
                if data["error"] == "invalid_card":
                    sys.stdout.write("invalid card, try again or pull a new card!\n")
                elif data["error"] == "pull_more_cards":
                    sys.stdout.write(f"you have to pull at least {data['amount']} cards!\n")
            

    listener_thread.join()
    