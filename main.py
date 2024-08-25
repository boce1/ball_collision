import pygame
from ball import Ball, pi
from random import randint

pygame.init()

window_width = 600
window_height = window_width
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60

pygame.display.set_caption("ball collision")
window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

balls = set()

def draw_scene(win, balls):
    win.fill(WHITE)
    for ball in balls:
        ball.draw(win)

    pygame.display.update()

def add_ball(event, mouse_x, mouse_y):
    global balls
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            add_flag = True
            ball_temp = Ball(mouse_x, mouse_y, randint(1, 10), (randint(0, 255),randint(0, 255),randint(0, 255)), randint(1, 10), randint(1, 10) * pi / randint(1, 6))
            for ball in balls:
                if ball.is_colliding(ball_temp):
                    add_flag = False
                    break
            
            if add_flag:
                balls.add(ball_temp)

def move_balls(win, balls):
    for ball in balls:
        ball.move()
        ball.wall_collision(win)

def collide_balls(balls):
    ball_list = list(balls)
    n = len(ball_list)
    for i in range(n):
        for j in range(i + 1, n):
            ball_list[i].ball_collision(ball_list[j])

running = True
clock = pygame.time.Clock()
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clock.tick(FPS)
    draw_scene(window, balls)
    move_balls(window, balls)
    collide_balls(balls)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        add_ball(event, mouse_x, mouse_y)
pygame.quit()
