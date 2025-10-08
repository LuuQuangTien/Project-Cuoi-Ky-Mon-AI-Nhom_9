import pygame

GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

class SensorlessBoard:
    def __init__(self, screen, tile_size, cols, rows):
        self.screen = screen
        self.tile_size = tile_size
        self.cols = cols
        self.rows = rows

        # mặc định tất cả ô đều có thể chứa mục tiêu
        self.board = [[1 for _ in range(rows)] for _ in range(cols)]

    def reset(self):
        # reset toàn bộ bảng về có thể chứa mục tiêu
        for x in range(self.cols):
            for y in range(self.rows):
                self.board[x][y] = 1

    def block_cell(self, x, y):
        # đánh dấu ô (x, y) không thể đến
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.board[x][y] = 0

    def reveal_cell(self, x, y):
        # đánh dấu ô (x, y) có thể đến
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.board[x][y] = 2

    def draw(self):
        # vẽ bảng
        for x in range(self.cols):
            for y in range(self.rows):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if self.board[x][y] == 1:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)
                elif self.board[x][y] == 2:
                    pygame.draw.rect(self.screen, YELLOW, rect, 2)
                elif self.board[x][y] == 0:
                    pygame.draw.rect(self.screen, RED, rect, 1)