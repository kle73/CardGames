import threading
import socket
import json
import sys

data_buffer = []

def listening(server: socket.socket):
    global data_buffer
    while True:
        message = server.recv(2048).decode()
        message_dict = json.loads(message)
        data_buffer.append(message_dict)

def print_card(color, value):
    sys.stdout.write(f' {color} {value} |')

def print_my_cards(cards: list):
    sys.stdout.write("your hand:\n")
    for card in cards:
        print_card(card[0], card[1])
    sys.stdout.write("\n")

def prompt(message: str, ) -> str:
    result: str = input(message)
    n: int = len(message) + len(result)
    sys.stdout.write("\033[F\r" + " "*n + "\r")
    return result


def start_mau_mau(server: socket.socket):

    which_game = json.dumps({"game": "mau_mau"})
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
                print_my_cards(my_cards)
                sys.stdout.write(f'{data["current_card"]}\n')

            elif 'turn' in data.keys():
                instr: str = None
                amt: int = 0
                input_color: str = None
                input_value: str = None
                input_command = prompt("[set|get]: ")
                if input_command == "set":
                    input_color = prompt("set card color: ")
                    input_value = prompt("set card value: ")
                    instr = "play_card"
                elif input_command == "get":
                    amt = int(prompt("how many: "))
                    instr = "pull_card"
                to_send = json.dumps({
                    "instr": instr,
                    "color": input_color, 
                    'value': input_value,
                    'amount': amt,
                    'error': 0
                })
                server.sendall(to_send.encode())
            
            elif "prompt" in data.keys():
                if data["prompt"] == "choose_color":
                    color = prompt("choose your color: ")
                    to_send = json.dumps({"color": color})
                    server.sendall(to_send.encode())

            elif 'message' in data.keys():
                if data["message"] == "card_set":
                    sys.stdout.write(f'{data["current_card"]}\n')
                if data['winner']:
                    sys.stdout.write(f'{data["winner"]} has won\n')
                print_my_cards(data["current_hand"])

            elif "new_card" in data.keys():
                print(data["new_card"])
                
            elif 'error' in data.keys():
                if data["error"] == "invalid_card":
                    sys.stdout.write("invalid card, try again or pull a new card!\n")
                elif data["error"] == "pull_more_cards":
                    sys.stdout.write(f"you have to pull at least {data['amount']} cards!\n")
            

    listener_thread.join()
    