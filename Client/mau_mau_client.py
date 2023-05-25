import threading
import socket
import json

data_buffer = []

def listening(server: socket.socket):
    global data_buffer
    while True:
        message = server.recv(2048).decode()
        message_dict = json.loads(message)
        data_buffer.append(message_dict)

def print_card(color, value):
    print(color, value)

def print_my_cards(cards: list):
    for card in cards:
        print_card(card[0], card[1])


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
                print(data["current_card"])
            elif 'turn' in data.keys():
                instr: str = None
                amt: int = 0
                input_color: str = None
                input_value: str = None
                input_command = input("[set|get]: ")
                if input_command == "set":
                    input_color = input("set card color: ")
                    input_value = input("set card value: ")
                    instr = "play_card"
                elif input_command == "get":
                    amt = int(input("how many: "))
                    instr = "pull_card"
                to_send = json.dumps({
                    "instr": instr,
                    "color": input_color, 
                    'value': input_value,
                    'amount': amt,
                    'error': 0
                })
                server.sendall(to_send.encode())
            elif 'message' in data.keys():
                if data["message"] == "card_set":
                    print(data["current_card"])
            elif "new_card" in data.keys():
                print(data["new_card"])
            elif 'error' in data.keys():
                if data["error"] == "invalid_card":
                    print("invalid card, try again or pull a new card!")
            

    listener_thread.join()
    