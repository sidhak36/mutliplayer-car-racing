import pickle
import socket

import pygame

from car import player_car
PORT:int
SERVER = ""
class Network:
    def __init__(self, player_id):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (SERVER, PORT)
        self.player_car = self.connect(player_id)

    def connect(self, player_id):
        try:
            self.client.connect(self.address)
            self.client.send(pickle.dumps(player_id))
            return pickle.loads(self.client.recv(2048))
        except:
            pass
    
    def send(self, data):
        self.client.send(pickle.dumps(data))
        player = pickle.loads(self.client.recv(2048))
        return player
