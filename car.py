import math
import pygame
from utils import blit_rotate_center
class player_car:
    def __init__(self, max_vel, rot_vel, start_pos, color):
        self.max_vel = max_vel
        self.vel = 0
        self.angle = 180
        self.rot_vel = rot_vel
        self.color = color
        self.x, self.y = start_pos
        self.acceleration = 0.1
        self.decceleration = 0.05
        
    def rotate(self, left = False, right = False):
        if left:
            self.angle = (self.angle + self.rot_vel)%360
        if right:
            self.angle = (self.angle - self.rot_vel)%360

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.decceleration, 0)
        self.move()

    def move(self):
        self.x = self.x - self.vel*math.sin(math.radians(self.angle))
        self.y = self.y - self.vel*math.cos(math.radians(self.angle))

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def detect_collison(self, CALLING_MASK, car_images):
        car_mask = pygame.mask.from_surface(car_images[self.color])
        point = CALLING_MASK.overlap(car_mask, (self.x, self.y))
        if point:
            self.bounce()

    def draw_car(self, win, car_images):
        blit_rotate_center(win, car_images[self.color], (self.x, self.y), self.angle)