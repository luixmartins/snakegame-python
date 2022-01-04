import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

pygame.mixer.music.set_volume(0.2)

background_music = pygame.mixer.music.load('audio/BoxCat Games - CPU Talk.mp3')
pygame.mixer.music.play(-1)

collision_sound = pygame.mixer.Sound('audio/mario-coin-sound-effect.mp3')

width, height = 640, 480

x_snake, y_snake = int(width / 2), int(height / 2)
speed = 10
x_control, y_control = speed, 0
x_apple, y_apple = random.randint(40, 600), random.randint(50, 430)

points = 0
font = pygame.font.SysFont('arial', 30, bold=True)

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


def snake_grows(snake_list):
    for dimension in snake_list:
        pygame.draw.rect(display, (0, 255, 0),
                        (dimension[0], dimension[1], 20, 20))

def restart_game():
    global points, initial_length, speed, x_snake, y_snake, snake_list, head_list, x_apple, y_apple, death
    points = 0
    initial_length = 5
    speed = 10
    x_snake, y_snake = int(width / 2), int(height / 2)
    snake_list, head_list = [], []
    x_apple, y_apple = random.randint(40, 600), random.randint(50, 430)
    death = False

snake_list = []
initial_length = 5

while True:
    clock.tick(30)
    display.fill((255, 255, 255))

    message = f'Points: {points}'
    formatted_text = font.render(message, True, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_control == speed:
                    pass
                else:
                    x_control = -speed
                    y_control = 0
            elif event.key == K_d:
                if x_control  == -speed:
                    pass
                else:
                    x_control = speed
                    y_control = 0
            elif event.key == K_w:
                if y_control == speed:
                    pass
                else:
                    x_control = 0
                    y_control = -speed
            elif event.key == K_s:
                if y_control == -speed:
                    pass
                else:
                    y_control = speed
                    x_control = 0
                    
    
    x_snake += x_control
    y_snake += y_control 

    snake = pygame.draw.rect(display, (0, 255, 0), (x_snake, y_snake, 20, 20))
    apple = pygame.draw.circle(display, (255, 0, 0), (x_apple, y_apple), 10)

    if snake.colliderect(apple):
        x_apple = random.randint(40, 600)
        y_apple = random.randint(50, 430)
        points += 1
        collision_sound.play()
        speed += 0.025

        initial_length += 1

    head_list = []
    head_list.append(x_snake)
    head_list.append(y_snake)

    snake_list.append(head_list)

    if snake_list.count(head_list) > 1:
        death = True
        restart_font = pygame.font.SysFont('arial', 20, bold=True)
        restart_message = 'Game Over! Press R to play again.'
        formatted_text = restart_font.render(restart_message, True, (0, 0, 0))
        ret_text = formatted_text.get_rect()

        while death: 
            display.fill((255, 255, 255))
            for event in pygame.event.get():
                if event == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        restart_game()

            ret_text.center = (width // 2, height // 2)
            display.blit(formatted_text, ret_text)
            pygame.display.update()
    
    if x_snake > width:
        x_snake = 0
    elif x_snake < 0:
        x_snake = width
    elif y_snake < 0:
        y_snake = height
    elif y_snake > height:
        y_snake = 0
    if len(snake_list) > initial_length:
        del snake_list[0]

    snake_grows(snake_list)

    display.blit(formatted_text, (450, 40))

    pygame.display.update()
