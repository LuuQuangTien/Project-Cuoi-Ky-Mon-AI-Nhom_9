import pygame
from pygame.math import Vector2

GRAY = (100, 100, 100)

class Snake:   
    def __init__(self, screen, tile_size, sprite_sheet):
        self.screen = screen
        self.screen_with, self.screen_height = self.screen.get_size()
        self.screen_rows, self.screen_cols = self.screen_height // tile_size, self.screen_with // tile_size
        self.tile_size = tile_size
        self.sprite_sheet = sprite_sheet
        
        self.snake = [Vector2(8, 7), Vector2(7, 7), Vector2(6, 7)]
        self.current_dir = Vector2(1, 0)
        self.direction = [Vector2(1,0), Vector2(-1,0), Vector2(0,1), Vector2(0,-1)]
        self.next_dir = None
        self.grow = False

        self.snake_body_horizontal = self.get_sprite(1, 0)
        self.snake_body_vertical = self.get_sprite(2, 1)

        self.snake_head_right = self.get_sprite(4, 0)
        self.snake_head_left = self.get_sprite(3, 1)
        self.snake_head_down = self.get_sprite(4, 1)
        self.snake_head_up = self.get_sprite(3, 0)

        self.snake_upleft_corner = self.get_sprite(0, 0)
        self.snake_upright_corner = self.get_sprite(2, 0)
        self.snake_downleft_corner = self.get_sprite(0, 1)
        self.snake_downrtight_corner = self.get_sprite(2, 2)

        self.snake_tail_right = self.get_sprite(4, 2)
        self.snake_tail_left = self.get_sprite(3, 3)
        self.snake_tail_down = self.get_sprite(4, 3)
        self.snake_tail_up = self.get_sprite(3, 2)

        self.head_dictionary = {
            (1, 0): self.snake_head_right,
            (-1, 0): self.snake_head_left,
            (0, 1): self.snake_head_down,
            (0, -1): self.snake_head_up
        }

        self.tail_dictionary = {
            (1, 0): self.snake_tail_right,
            (-1, 0): self.snake_tail_left,
            (0, 1): self.snake_tail_down,
            (0, -1): self.snake_tail_up
        }

        self.corner_dictionary = {
            ((1, 0), (0, -1)): self.snake_upright_corner,
            ((0, -1), (1, 0)): self.snake_upright_corner,

            ((-1, 0), (0, -1)): self.snake_upleft_corner,
            ((0, -1), (-1, 0)): self.snake_upleft_corner,

            ((1, 0), (0, 1)): self.snake_downrtight_corner,
            ((0, 1), (1, 0)): self.snake_downrtight_corner,

            ((-1, 0), (0, 1)): self.snake_downleft_corner,
            ((0, 1), (-1, 0)): self.snake_downleft_corner,
        }

        self.wall_pos = [Vector2(5, 2), Vector2(6, 2), Vector2(7, 2), Vector2(8, 2), Vector2(9, 2),
                         Vector2(14, 2), Vector2(15, 2), Vector2(16, 2), Vector2(17, 2), Vector2(18, 2),
                         Vector2(3, 5), Vector2(3, 6), Vector2(3, 7), Vector2(3, 8), Vector2(3, 9),
                         Vector2(5, 12), Vector2(6, 12), Vector2(7, 12), Vector2(8, 12), Vector2(9, 12),
                         Vector2(14, 12), Vector2(15, 12), Vector2(16, 12), Vector2(17, 12), Vector2(18, 12),
                         Vector2(20, 5), Vector2(20, 6), Vector2(20, 7), Vector2(20, 8), Vector2(20, 9)]

        self.high_dangerzone = [(c, r) for r in range(self.screen_rows) for c in range(self.screen_cols)
                                if ((r == 0 or r == (self.screen_rows - 1)) or (c == 0 or c == (self.screen_cols - 1)))]

        self.med_dangerzone = set()
        for wall in self.wall_pos:
            for n in self.direction:
                tile = wall + n
                if((0 <= tile.x < self.screen_cols) and (0 <= tile.y < self.screen_rows)
                    and (tile not in self.high_dangerzone)):
                    self.med_dangerzone.add(((tile.x), tile.y))
        self.med_dangerzone = list(sorted(self.med_dangerzone))

        self.low_dangerzone = [(x, y) for x in range(8, 16) for y in range(5, 10)]

        self.verylow_dangerzone = list({(x, y) for x in range(24) for y in range(15)} - {(w.x, w.y) for w in self.wall_pos} -
                                       set(self.high_dangerzone) - set(self.med_dangerzone) - set(self.low_dangerzone))


    def get_sprite(self, x, y):
        rect = pygame.Rect(x * 64, y * 64, 64, 64)
        sprite = self.sprite_sheet.subsurface(rect).copy()
        sprite = pygame.transform.smoothscale(sprite, (self.tile_size, self.tile_size))
        return sprite
    
    def draw(self):
        for index, tile in enumerate(self.snake):
            x = int(tile.x * self.tile_size)
            y = int(tile.y * self.tile_size)
            rect = pygame.Rect(x, y, self.tile_size, self.tile_size)

            if(index == 0):
                head_direction = (int(tile.x - self.snake[1].x), int(tile.y - self.snake[1].y))
                sprite = self.head_dictionary.get(head_direction)
            elif(index == len(self.snake) - 1):
                tail_direction = (int(self.snake[index - 1].x - tile.x), int(self.snake[index - 1].y - tile.y))
                sprite = self.tail_dictionary.get(tail_direction)
            else:
                prev_tile = self.snake[index - 1]
                next_tile = self.snake[index + 1]
                prev_direction = (int(tile.x - prev_tile.x), int(tile.y - prev_tile.y))
                next_direction = (int(tile.x - next_tile.x), int(tile.y - next_tile.y))
                
                sprite = self.corner_dictionary.get((prev_direction, next_direction))
                if not (sprite):
                    if(prev_direction[0] == next_direction[0]):
                        sprite = self.snake_body_vertical
                    else:
                        sprite = self.snake_body_horizontal

            if(sprite): self.screen.blit(sprite, rect)
        
    def move(self, new_head = None):
        if(self.next_dir is not None):
            if(self.next_dir != (-self.current_dir[0], -self.current_dir[1])):self.current_dir = self.next_dir
            self.next_dir = None

        if(new_head == None): new_head = self.snake[0] + self.current_dir
        if(self.grow):
            self.snake = [new_head] + self.snake
            self.grow = False
        else:
            tail =  self.snake[-1]
            self.snake = [new_head] + self.snake[:-1]
        
    def collision(self, col, row):
        if(self.snake[0].x >= col or self.snake[0].y >= row or 
           self.snake[0].x < 0 or self.snake[0].y < 0):
            print("You hit the border. Game Over")
            print(self.snake)
            return True
    
        if(self.snake[0] in self.snake[1:]):
            print("You hit yourself. Game Over")
            print(self.snake)
            return True

        if(self.snake[0] in self.wall_pos):
            print("You hit a wall. Game Over")
            print(self.snake)
            return True

    def Is_safe(self, state):
        sub_state = []
        for i in self.direction:
            next_state = state + i
            if((next_state.x >= self.screen_cols) or
                (next_state.y >= self.screen_rows) or
                (next_state.x < 0) or (next_state.y < 0) or
                next_state in self.wall_pos): continue
            if(next_state in self.snake and next_state != self.snake[-1]): continue
            sub_state.append(next_state)
        return sub_state

    """def Is_safe_2(self, head, state, goal):
        sub_state = []
        body = state[:-1]
        for d in self.direction:
            new_head = (head[0] + d[0], head[1] + d[1])
            if(new_head[0] < 0 or new_head[0] >= self.screen_cols or
                    new_head[1] < 0 or new_head[1] >= self.screen_rows or
                    new_head in self.wall_pos):
                continue
            if(new_head in body): continue
            if(new_head == goal):
                new_state = (new_head,) + state
            else: new_state = (new_head,) + body
            sub_state.append(new_state)
        return sub_state"""


    def reset(self):
        self.snake = [Vector2(8, 7), Vector2(7, 7), Vector2(6, 7)]
        self.current_dir= Vector2(1, 0)
        self.grow = False