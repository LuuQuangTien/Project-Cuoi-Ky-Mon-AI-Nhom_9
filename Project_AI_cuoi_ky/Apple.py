import pygame
from pygame.math import Vector2
from random import randint

class Apple:
    def __init__(self, screen, tile_size, sprite_sheet, snake):
        self.screen = screen
        self.tile_size = tile_size
        self.snake = snake
        self.static_pos = [Vector2(10, 7), Vector2(4, 7), Vector2(16, 3), Vector2(18, 11),
                           Vector2(12, 7), Vector2(22, 7), Vector2(1, 13)]
        self.static_pos_index = 0
        self.position = None
        self.sprite_sheet = sprite_sheet

        rect = pygame.Rect(0 * 64, 3 * 64, 64, 64)
        apple_img = self.sprite_sheet.subsurface(rect).copy()
        self.apple_img = pygame.transform.smoothscale(apple_img, (self.tile_size, self.tile_size))

    def reset_position(self, mode=None):
        if(mode == "STATIC_APPLE"):
            self.static_pos_index = 0
            self.position = self.static_pos[self.static_pos_index]
        else:
            self.set_apple_random()

    def draw(self):
        apple_rect = pygame.Rect(self.position * self.tile_size, (self.tile_size, self.tile_size))
        self.screen.blit(self.apple_img, apple_rect)

    def set_apple_random(self):
        x = randint(0, (1200 // self.tile_size) - 1)
        y = randint(0, (750 // self.tile_size) - 1)
        
        self.position = Vector2(x, y)
        if(self.position in self.snake.snake or self.position in self.snake.wall_pos): self.set_apple_random()
        return self.position

    def apple_collision(self, menu = None):
        if(self.position == self.snake.snake[0]):
            self.snake.grow = True
            if(menu and menu.mode == "STATIC_APPLE"):
                self.static_pos_index += 1
                if (self.static_pos_index < len(self.static_pos)):
                    self.position = self.static_pos[self.static_pos_index]
                else: return "GAMEOVER"
            else: self.set_apple_random()

            if(menu): return menu.select_method(self.snake, self)
        return None