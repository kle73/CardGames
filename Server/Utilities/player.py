import socket
import json

class Player:

    def __init__(self, name: str, adr: tuple, conn: socket.socket):
        self.name = name
        self.conn = conn
        self.adr = adr
        self.hand = []
    
    def send(self, data: dict) -> bool:
        try:
            json_data = json.dumps(data)
            self.conn.sendall(json_data.encode())
        except:
            return False
        return True
    
    def receive(self) -> dict:
        try: 
            data_string = self.conn.recv(2048).decode()
            data = json.loads(data_string)
            data["error"] = 0
            return data
        except:
            return {"error": 1}

