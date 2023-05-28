from MauMau.mau_mau_player import start_mau_mau_game
from Skat.skat_player import start_skat
from Schnauzer.schnauzer_player import start_schnauzer
from Utilities.player import Player

import socket
import threading
import json

IP, PORT = "192.168.0.61", 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen()

def handle_player(player: Player):
    data = player.conn.recv(1024).decode()
    game = json.loads(data)
    if game["game"] == "mau_mau":
        global mau_mau_palyers
        mau_mau_palyers.append(player)
    elif game["game"] == "skat":
        global skat_players
        skat_players.append(player)
    elif game["game"] == "schnauzer":
        global schnauzer_players
        schnauzer_players.append(player)

def receive_new_players(server: socket.socket):
    player_count: int = 0
    while True:
        conn, adr = server.accept()
        print("new player connected")
        global player_buffer
        player_buffer.append(Player(str(player_count), adr, conn))
        player_count += 1



mau_mau_palyers = []
skat_players = []
schnauzer_players = []

player_buffer = []

receiver_thread = threading.Thread(target=receive_new_players, args=(server, ))
receiver_thread.start()

while True:
    if len(player_buffer) > 0:
        for i in range(len(player_buffer)):
            new_player = player_buffer.pop(0)
            player_handler = threading.Thread(target=handle_player, args=(new_player, ))
            player_handler.start()
    if len(mau_mau_palyers) > 2:
        players = [mau_mau_palyers.pop(0), mau_mau_palyers.pop(0), mau_mau_palyers.pop(0)]
        mau_mau_thread = threading.Thread(target=start_mau_mau_game, args=(players, ))
        mau_mau_thread.start()
    if len(skat_players) > 2:
        continue
    if len(schnauzer_players) > 1:
        continue


receiver_thread.join()