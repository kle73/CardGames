import threading
import socket
import json

from mau_mau_client import start_mau_mau


HOST = '127.0.0.1'
PORT = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
print(type(server))


def least_edit_distance(word: str):
    # TODO
    return "maumau"

def main():
    while True:
        game_to_play = input("what game do you want to play [maumau|skat|schnauzer]: ")
        while True:
            if game_to_play == "maumau":
                start_mau_mau(server)
                break
            elif game_to_play == "skat":
                break
            elif game_to_play == "schnauzer":
                break
            else:
                game_to_play = least_edit_distance(game_to_play)
                continue

            


main()

