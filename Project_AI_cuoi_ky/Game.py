import pygame
from pygame import Vector2

from Snake import Snake
from Apple import Apple
from Menu import Menu

pygame.init()
#__________________________Game definition___________________________

#Clolor
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (173, 204, 96)
LIGHT_BLUE = (173, 216, 230)

#Display
screen_size = (1200, 750)
tile_size = 50
fps = 60

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
sprite_sheet = pygame.image.load("img/snake_img.png").convert_alpha()
"""font = pygame.font.Font(None, 50)"""
SNAKE_MOVE = pygame.USEREVENT + 1
pygame.time.set_timer(SNAKE_MOVE, 50)
state = "MENU"
gameover_screen = None
solution = None
running = True

menu = Menu(screen, tile_size, sprite_sheet)
snake = Snake(screen, tile_size, sprite_sheet)
apple = Apple(screen, tile_size, sprite_sheet, snake)
apple.reset_position()

#________________________________Game Loop____________________________

def menu_state(menu, state, events):
    global running
    if state == "MENU":
        menu.draw_start()
    elif state == "GAMEOVER":
        menu.draw_gameover(gameover_screen)
    elif state == "COMPUTER":
        menu.draw_computer()

    inp = menu.input(state, events, apple)
    if inp == "QUIT":
        running = False
    elif inp in ["MENU", "PLAY", "COMPUTER", "SIMULATE"]:
        state = inp

    return state

def game_loop(snake, apple, events, state):
    global running, gameover_screen, solution
    clock.tick(fps)
    menu.draw_game_grid(tile_size, snake)

    snake.draw()
    apple.draw()
    draw_solution_path(screen, solution, tile_size)

    if(state == "PLAY"):
        key = pygame.key.get_pressed()
        if (key[pygame.K_LEFT] and snake.direction != (1, 0)):
            snake.next_dir = (-1, 0)
        elif (key[pygame.K_RIGHT] and snake.direction != (-1, 0)):
            snake.next_dir = (1, 0)
        elif (key[pygame.K_UP] and snake.direction != (0, 1)):
            snake.next_dir = (0, -1)
        elif (key[pygame.K_DOWN] and snake.direction != (0, -1)):
            snake.next_dir = (0, 1)
        for event in events:
            if (event.type == pygame.QUIT):
                running = False
            if (event.type == SNAKE_MOVE):
                snake.move()

    elif(state == "SIMULATE"):
        for event in events:
            if (event.type == pygame.QUIT):
                running = False
            if (event.type == SNAKE_MOVE):
                if(solution):
                    next_pos = Vector2(solution.popleft())
                    dir = next_pos - snake.snake[0]
                    snake.move(next_pos)
                    snake.next_dir = dir
                else:
                    solution = menu.select_method(snake, apple)
                    if (solution):
                        next_pos = Vector2(solution.popleft())
                        dir = next_pos - snake.snake[0]
                        snake.move(next_pos)
                        snake.next_dir = dir
                    else:
                        print("Cant find solution")
                        state = "GAMEOVER"
                        gameover_screen = screen.copy()

    if(snake.collision(screen_size[0] // tile_size, screen_size[1] // tile_size)):
        state = "GAMEOVER"
        gameover_screen = screen.copy()

    new_solution = apple.apple_collision(menu if state == "SIMULATE" else None)
    if(new_solution == "GAMEOVER"):
        state = "GAMEOVER"
        gameover_screen = screen.copy()
    elif(new_solution is not None): solution = new_solution
    return state

def draw_solution_path(screen, solution, tile_size):
    menu.highlight_dangerzone(snake)
    if(solution is not None):
        for pos in solution:
            rect = pygame.Rect(pos.x * tile_size, pos.y * tile_size, tile_size, tile_size)
            path = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            path.fill((253, 145, 145, 80))
            screen.blit(path, rect.topleft)

while(running):
    events = pygame.event.get()

    if(state in ["MENU", "GAMEOVER", "COMPUTER"]):
        state = menu_state(menu, state, events)
        if(state in ["PLAY", "SIMULATE"]):
            snake.reset()
            apple.reset_position(menu.mode)
    elif(state in ["PLAY", "SIMULATE"]):
        state = game_loop(snake, apple, events, state)

    pygame.display.flip()
pygame.quit()