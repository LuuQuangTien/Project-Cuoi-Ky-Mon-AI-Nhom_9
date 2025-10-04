import pygame


class Button():
    def __init__(self, screen, font, x, y, width, height, text, button_color, text_color):
        self.screen = screen
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.button_color = button_color
        self.text_color = text_color
        self.clicked = False
            
    def draw(self, events, mode = "normal"):
        pressed_color = tuple(int(color * 0.8) for color in self.button_color)
        pressed = False

        if(mode == "normal"):
            for event in events:
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    if (self.rect.collidepoint(pygame.mouse.get_pos())):
                        self.clicked = True
                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                    if (self.rect.collidepoint(pygame.mouse.get_pos())):
                        pressed = True
                    self.clicked = False
        if(mode == "press"):
            for event in events:
                if (event.type == pygame.MOUSEBUTTONUP and event.button == 1):
                    if (self.rect.collidepoint(pygame.mouse.get_pos())):
                        self.clicked = not self.clicked
            pressed = self.clicked

        btn_color = pressed_color if (self.clicked) else self.button_color
        pygame.draw.rect(self.screen, btn_color, self.rect)
        btn_txt = self.font.render(self.text, True, self.text_color)
        self.screen.blit(btn_txt, btn_txt.get_rect(center=self.rect.center))

        return pressed