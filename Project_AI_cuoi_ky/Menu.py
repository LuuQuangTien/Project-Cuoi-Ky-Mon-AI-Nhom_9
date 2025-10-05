import pygame
from Button import Button
from Pathfinding import BFS, DFS, UCS, Greedy, SIMULATED_ANEALING, BEAM
from collections import deque

#__________________________Game definition___________________________

#Clolor
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (173, 204, 96)
RED = (253, 145, 145)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GRAY = (211,211,211)
HIGHDANGER_RED = (197, 21, 21, 100)
MEDDANGER_ORANGE = (209, 110, 1, 100)
LOWDANGER_GREEN = (67, 143, 78, 100)

#Button
button_x = 475
button_y = 325
button_width = 250
button_height = 100
algorithm_button_width = 200
algorithm_button_height = 75
button_gap = 20

ALGORITHMS = {
    "BFS": "BFS",
    "DFS": "DFS",
    "UCS": "UCS",
    "GREEDY": "GREEDY",
    "BEAM": "BEAM",
    "SIM A": "SIMULATED_ANEALING",
    "NON DETR": "NONDETERMINISTIC",
    "PAR OBS": "PARTIALLY_OBSERVABLE",
    "FORWARD": "FORWARD_CHECKING",
    "AC3": "AC3",
}

METHOD_LAYOUT = [
    ["BFS", "DFS"],
    ["UCS", "GREEDY"],
    ["BEAM", "SIM A"],
    ["NON DETR", "PAR OBS"],
    ["FORWARD", "AC3"]
]


#_____________________________Game Class_____________________________
class Menu():
    def __init__(self, screen, tile_size, sprite_sheet):
        self.screen = screen
        self.screen_with, self.screen_height = self.screen.get_size()
        self.tile_size = tile_size
        self.screen_rows, self.screen_cols = self.screen_height // tile_size, self.screen_with // tile_size
        self.font = pygame.font.Font(None, 50)
        self.algorithm_font = pygame.font.Font(None, 40)
        self.sprite_sheet = sprite_sheet
        self.grass_sprite = self.get_sprite(3, 0, "img/Grass_img.png")
        self.stone_sprite = self.get_sprite(0, 1, "img/Stone_img.png")
        self.method = None
        self.algorithm_buttons = {}
        self.mode = None

        #___MENU___
        self.rect_play = Button(self.screen, self.font, button_x, button_y - 75, button_width, button_height, "PLAY", GREEN, BLACK)
        self.rect_computer = Button(self.screen, self.font, button_x, button_y + 75, button_width, button_height, "COMPUTER", GREEN, BLACK)
        #___GAMEOVER___
        self.rect_startmenu = Button(self.screen, self.font, button_x - (50), button_y + 75, button_width + 100, button_height, "RETURN", WHITE, BLACK)
        self.rect_replay = Button(self.screen, self.font, button_x, button_y - 75, button_width, button_height, "REPLAY", WHITE, BLACK)
        #___COMPUTER
        self.rect_return = Button(self.screen, self.font, (self.screen_with - (50 + button_width)),
                                  (self.screen_height - (50 + button_height)), button_width, button_height, "RETURN", GREEN, BLACK)
        self.rect_startplaying = Button(self.screen, self.font, 50, self.screen_height - (50 + button_height), button_width, button_height, "START", RED, BLACK)

        for col_i, col in enumerate(METHOD_LAYOUT):
            x = 20 + col_i * (algorithm_button_width + button_gap + 20)
            for row_i, button_text in enumerate(col):
                y = 100 + row_i * (algorithm_button_height + button_gap)
                method_name = ALGORITHMS[button_text]
                button = Button(
                    self.screen, self.algorithm_font, x, y,
                    algorithm_button_width, algorithm_button_height,
                    button_text, GREEN, BLACK
                )
                self.algorithm_buttons[method_name] = button


        self.rect_visualize_path = Button(self.screen, self.font, button_x - 50, button_y - 50, algorithm_button_width + 100, algorithm_button_height, "VISUALIZE PATH", GREEN, BLACK)

    def draw_game_grid(self, tile_size, snake):
        self.screen.fill(GREEN)

        for row in range(0, self.screen_height, self.tile_size):
            for col in range(0, self.screen_with, self.tile_size):
                self.screen.blit(self.grass_sprite, (col, row))

        for index, tile in enumerate(snake.wall_pos):
            x = int(tile.x * self.tile_size)
            y = int(tile.y * self.tile_size)
            self.screen.blit(self.stone_sprite, (x, y))

    def get_sprite(self, x, y, img):
        rect = pygame.Rect(x * 48, y * 48, 48, 48)
        grass_sprite_sheet = pygame.image.load(img).convert_alpha()
        sprite = grass_sprite_sheet.subsurface(rect).copy()
        sprite = pygame.transform.smoothscale(sprite, (self.tile_size, self.tile_size))
        return sprite


    def draw_start(self):
        pygame.display.set_caption("Start Menu")
        background = pygame.Surface((self.screen_with, self.screen_height))
        background.fill(GREEN)
        background.fill(LIGHT_BLUE, pygame.Rect(self.screen_with // 3, 0, self.screen_with // 3, 750))
        self.screen.blit(background, (0, 0))

    def draw_gameover(self, gameover_screen):
        pygame.display.set_caption("Game Over")
        background = pygame.Surface((self.screen_with, self.screen_height), pygame.SRCALPHA)
        background.fill(LIGHT_GRAY)
        background.set_alpha(128)
        self.screen.blit(gameover_screen, (0, 0))
        self.screen.blit(background, (0, 0))

    def draw_computer(self):
        pygame.display.set_caption("Computer pathfinding algorithm mode")
        background = pygame.Surface((self.screen_with, self.screen_height))
        background.fill(LIGHT_BLUE, pygame.Rect(0, 0, self.screen_with, self.screen_height // 2))
        background.fill(LIGHT_GRAY, pygame.Rect(0, self.screen_height // 2, self.screen_with, self.screen_height // 2))
        self.screen.blit(background, (0, 0))

    def use_method(self, method, select):
        if(method == select): return None
        else: return select

    def select_method(self, snake, apple):
        solution = None
        match(self.method):
            case("BFS"):
                bfs = BFS(snake, apple.position)
                solution = bfs.Solving()
                if not(solution):
                    bfs_tail = BFS(snake, snake.snake[-1])
                    solution = bfs_tail.Solving()
            case("DFS"):
                dfs = DFS(snake, apple.position)
                solution = dfs.Solving()
                if not(solution):
                    dfs_tail = DFS(snake, snake.snake[-1])
                    solution = dfs_tail.Solving()
            case("UCS"):
                ucs = UCS(self.screen, self.tile_size, snake, apple.position)
                solution = ucs.Solving()
                if not(solution):
                    ucs_tail = UCS(self.screen, self.tile_size, snake, snake.snake[-1])
                    solution = ucs_tail.Solving()
            case("GREEDY"):
                greedy = Greedy(snake, apple.position)
                solution = greedy.Solving()
                if not(solution):
                    greedy_tail = Greedy(snake, snake.snake[-1])
                    solution = greedy_tail.Solving()
            case("SIMULATED_ANEALING"):
                sa = SIMULATED_ANEALING(snake, apple.position, T = 1000, alpha = 0.9)
                solution = sa.Solving()
                if not(solution):
                    sa_tail = SIMULATED_ANEALING(snake, snake.snake[-1], T = 1000, alpha = 0.9)
                    solution = sa_tail.Solving()
            case("BEAM"):
                beam = BEAM(snake, apple.position, 3)
                solution = beam.Solving()
                if not(solution):
                    beam_tail = BEAM(snake, snake.snake[-1], 5)
                    solution = beam_tail.Solving()


        if(solution and len(solution) > 1):
            solution.popleft()
            return solution
        return None

    def update_start_button_color(self):
        new_color = GREEN if self.method is not None else RED
        self.rect_startplaying.button_color = new_color

    def highlight_dangerzone(self, snake):
        if(self.method == "UCS"):
            for x in range(self.screen_cols):
                for y in range(self.screen_rows):
                    pos = (x, y)
                    if(pos in snake.high_dangerzone): color = HIGHDANGER_RED
                    elif(pos in snake.med_dangerzone): color = MEDDANGER_ORANGE
                    elif(pos in snake.low_dangerzone): color = LOWDANGER_GREEN
                    elif(pos in snake.verylow_dangerzone): color = (173, 204, 96, 0)

                    rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    zone = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
                    zone.fill(color)
                    self.screen.blit(zone, rect.topleft)

    def input(self, state, events):
        for event in events:
            if(event.type == pygame.QUIT):
                return "QUIT"

        if(state == "MENU"):
            if(self.rect_play.draw(events, "normal")):
                print("clicked PLAY")
                state = "PLAY"
            elif(self.rect_computer.draw(events, "normal")):
                print("clicked COMPUTER")
                state = "COMPUTER"
        elif(state == "GAMEOVER"):
            if(self.rect_startmenu.draw(events, "normal")):
                print("clicked RETURN MENU")
                state = "MENU"
            elif(self.rect_replay.draw(events, "normal")):
                print("clicked REPLAY")
                if(self.method is None): state = "PLAY"
                else: state = "SIMULATE"
        elif(state == "COMPUTER"):
            for method_name, button in self.algorithm_buttons.items():
                if button.draw(events, "press"):
                    self.method = self.use_method(self.method, method_name)
            if (self.rect_startplaying.draw(events, "normal")):
                if(self.method is not None):
                    print("clicked STARTPLAY")
                    state = "SIMULATE"
            elif (self.rect_return.draw(events, "normal")):
                print("clicked RETURN")
                state = "MENU"
            """elif(self.rect_visualize_path.draw(events, "press")):
                self.mode = self.use_method(self.mode, "VISUALIZE")"""
        return state
        
