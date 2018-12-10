import pygame

# This module includes class Button which help to create and interact with your game buttons.

class Button:

    def __init__(self, x, y, filename1, filename2=False):
        # Describes a button.
        # Takes two coordinates x, y; and one or two images of the button.
        # Filename1 - inactive, Filename2 - active state.
        self.image = pygame.image.load(filename1)
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.filename1 = filename1
        self.filename2 = filename2

    def mouse_on_button(self):
        # Changes inactive state on active if mouse on the button.
        # Works only if there are two images.
        mp = pygame.mouse.get_pos()
        if self.filename2:
            if self.rect[0] < mp[0] < self.rect[0] + self.rect[2] and self.rect[1] < mp[1] < self.rect[1] + self.rect[3]:
                self.image = pygame.image.load(self.filename2)
            else:
                self.image = pygame.image.load(self.filename1)

    def on_click(self):
        # Checks if the button is pressed.
        mp = pygame.mouse.get_pos()
        if self.rect[0] < mp[0] < self.rect[0] + self.rect[2] and self.rect[1] < mp[1] < self.rect[1] + self.rect[3]:
            return True
        else:
            return False

    def update(self, screen):
        # Method which we call to draw the button and update it.
        self.mouse_on_button()
        self.on_click()
        screen.blit(self.image, self.rect)