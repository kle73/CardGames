import threading
import socket
import json
import os

from mau_mau_client import start_mau_mau


SERVER, PORT = 'localhost', 5050


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((SERVER, PORT))


def least_edit_distance(word: str):
    # TODO
    return "maumau"

def main():
    while True:
        game_to_play = input("what game do you want to play [maumau|skat|schnauzer]: ")
        name = input("whats your name: ")
        while True:
            if game_to_play == "maumau":
                start_mau_mau(server, name)
                break
            elif game_to_play == "skat":
                break
            elif game_to_play == "schnauzer":
                break
            else:
                game_to_play = least_edit_distance(game_to_play)
                continue

            

os.system("clear")
main()

