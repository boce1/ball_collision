import pygame
from math import pi, sin, cos, atan2, sqrt

class Ball:
    def __init__(self, x, y, mass, color, vel, theta):
        self.x = x
        self.y = y
        self.mass = mass # mass = 1, 2, 3 / radius for 1kg is 10
        self.color = color
        self.radius = self.get_radius()
        self.vel = vel
        self.theta = theta
        self.vel_x = self.vel * cos(self.theta)
        self.vel_y = self.vel * sin(self.theta)

    def get_radius(self):
        unit = 10
        return self.mass * unit

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius, 1)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def wall_collision(self, win):
        width = win.get_width()
        height = win.get_height()
        if self.x < self.radius:
            self.theta = pi - self.theta
            self.vel_x *= -1
            self.x = self.radius
        elif self.x > width - self.radius:
            self.theta = pi - self.theta
            self.vel_x *= -1
            self.x = width - self.radius
        if self.y < self.radius:
            self.theta = -self.theta
            self.vel_y *= -1
            self.y = self.radius
        elif self.y > height - self.radius:
            self.theta = -self.theta
            self.vel_y *= -1
            self.y = height - self.radius

    def is_colliding(self, other):
        return self.get_distance(other) < self.radius + other.radius

    def get_distance(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def get_overlap(self, other):
        return self.radius + other.radius - self.get_distance(other)

    def ball_collision(self, other):
        if self.is_colliding(other):
            phi = atan2((self.y - other.y), (self.x - other.x))

            v1_1component = (self.vel*cos(self.theta - phi)*(self.mass - other.mass) + 2*other.mass*other.vel*cos(other.theta - phi)) / (self.mass + other.mass)
            v1_2component = self.vel*sin(self.theta - phi)*cos(phi + pi / 2)

            v2_1component = (other.vel*cos(other.theta - phi)*(other.mass - self.mass) + 2*self.mass*self.vel*cos(self.theta - phi)) / (other.mass + self.mass)
            v2_2component = other.vel*sin(other.theta - phi)*cos(phi + pi / 2)

            self.vel_x = v1_1component * cos(phi) + v1_2component
            self.vel_y = v1_1component * sin(phi) + v1_2component
            self.theta = atan2(self.vel_y, self.vel_x)
            
            other.vel_x = v2_1component * cos(phi) + v2_2component
            other.vel_y = v2_1component * sin(phi) + v2_2component
            other.theta = atan2(other.vel_y, other.vel_x)
            
            overlap = self.get_overlap(other)
            gap_when_collided = 0.5 * overlap + overlap // abs(overlap) # overlap // abs(overlap) is one pixer
            self.x += gap_when_collided * cos(phi)
            self.y += gap_when_collided * sin(phi)
            other.x -= gap_when_collided * cos(phi)
            other.y -= gap_when_collided * sin(phi)