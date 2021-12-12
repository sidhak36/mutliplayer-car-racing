import socket
from _thread import *
import pickle
from car import player_car
from utils import  Color


port = 5555
server = "192.168.29.171"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(e)

#Listen for max 2 clients
s.listen(2)
player_cars = [player_car(2, 2, (155, 200), Color.RED),
player_car(2, 2, (180, 200), Color.GREEN)]

players = [{
    'name': 'Sidhak',
    'age': 25,
    'connection': 1,
    'connected': False
}, 
{
    'name': 'Pratyush',
    'age': 22,
    'connection': 0,
    'connected': False
}]

def both_connected(players):
    for player in players:
        if player['connected'] == False:
            return False
    return True

def threaded_client(conn, player_cars):
    id = pickle.loads(conn.recv(2048))
    players[id]['connected'] = True
    while not both_connected(players):
        pass
    conn.send(pickle.dumps(player_cars[id]))
    
    while True:

        try:
            player_cars[id] = pickle.loads(conn.recv(2048))
            if not both_connected(players):
                players[id]['connected'] = False
                conn.sendall(pickle.dumps('Disconnected!'))
                break
            conn.sendall(pickle.dumps(player_cars[players[id]['connection']]))
        except :
            players[id]['connected'] = False
            break
    
    print('Disconnected from Client')
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to: ', addr)
    start_new_thread(threaded_client, (conn, player_cars))