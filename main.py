import pygame
from network import Network
from utils import Color, scale_image
import sys

player_id = sys.argv[1]
try:
    player_id = int(player_id)
except:
    print('Wrong id, QUITING.....')
    pygame.quit()
    
FRAME_RATE = 60

GRASS = scale_image(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK = scale_image(pygame.image.load('imgs/track.png'), 0.9)
TRACK_BORDER = scale_image(pygame.image.load('imgs/track-border.png'), 0.9)
FINISH = pygame.image.load('imgs/finish.png')
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
CARS = dict()
CARS[Color.GREEN] = scale_image(pygame.image.load('imgs/green-car.png'), 0.55)
CARS[Color.RED] = scale_image(pygame.image.load('imgs/red-car.png'), 0.55)
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Racing Game!')

def draw(win, images, player_cars):
    for img, pos in images:
        win.blit(img, pos)
    for car in player_cars:
        car.draw_car(win, CARS)
    pygame.display.update()

images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
n = Network(player_id)
player_car_main = n.player_car
player_car_opponent = n.send(player_car_main)
players = [player_car_main, player_car_opponent]
clock = pygame.time.Clock()
run = True
while run: 
    clock.tick(FRAME_RATE)

    draw(WIN, images, players)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_LEFT]: 
        players[0].rotate(left=True)
    if keys[pygame.K_RIGHT]: 
        players[0].rotate(right=True)
    if keys[pygame.K_s]:
        moved = True
        players[0].move_forward()
    if not moved:
        players[0].move_backward()
    players[0].detect_collison(TRACK_BORDER_MASK, CARS)
    players[1] = n.send(players[0])
    #Quit the game of current player if other player quits
    #Server returns string data if other player quits
    if type(players[1]) == str:
        run = False
pygame.quit()


