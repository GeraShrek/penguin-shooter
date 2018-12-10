# This module includes graphics and scenes of the game.
# There are 5 scenes: Menu, Information, Game Start, Game and Pause.

import sys
import time
import random

import pygame

from button import Button
from sounds import MenuSound, GameSound, SoundEffects, SoundMethods

# Sounds.
MS = MenuSound()
MS.play_menu()

class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.start()

    def start(self):
        done = True
        while done:

            self.screen.blit(menu_bg, (0, 0))

            # Buttons.
            start_game_button.update(self.screen)
            menu_exit_button.update(self.screen)
            info_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == MS.MUSIC_ENDED:
                    MS.event_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if start_game_button.on_click():
                        # Game Start.
                        done = False
                        GameStart(self.screen)

                    if info_button.on_click():
                        # Info.
                        done = False
                        Info(self.screen)

                    if menu_exit_button.on_click():
                        # Exit.
                        sys.exit()

            pygame.display.flip()

class Info:

    def __init__(self, screen):
        self.screen = screen
        self.FONT_SIZE = 20
        self.font_obj = pygame.font.SysFont('Tahoma', self.FONT_SIZE, bold=True)
        self.info = open('resources/info/info.txt', 'r').readlines()

        self.start()

    def information(self, pos):
        # Block of the information.
        # Takes position of the text.
        x, y = pos
        max_width = self.screen.get_size()[0] - x
        for line in self.info:
            for word in line.rstrip('\n'):
                word_surface = self.font_obj.render(word, 0, (255, 255, 255))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                self.screen.blit(word_surface, (x, y))
                x += word_width
            x = pos[0]
            y += word_height

    def start(self):
        done = True
        while done:

            self.screen.blit(info_bg, (0, 0))

            # Buttons.
            info_back_button.update(self.screen)

            self.information((32, 32))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == MS.MUSIC_ENDED:
                    MS.event_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if info_back_button.on_click():
                        # Menu.
                        Menu(self.screen)

            pygame.display.flip()

class GameStart:

    def __init__(self, screen):
        self.screen = screen
        sprite_sheet = pygame.image.load('resources/game_start/counter.png')

        # Counter.
        self.counter = []
        self.counter.append(sprite_sheet.subsurface(0, 0, 250, 250))
        self.counter.append(sprite_sheet.subsurface(250, 0, 250, 250))
        self.counter.append(sprite_sheet.subsurface(500, 0, 250, 250))

        self.start()

    def play_counter(self):
        for frame in self.counter:
            self.screen.blit(count_bg, (0, 0))
            self.screen.blit(frame, (387, 220))
            pygame.display.flip()
            time.sleep(1)

    def start(self):
        done = True

        # Sounds.
        SM = SoundMethods()

        while done:

            self.screen.blit(start_bg, (0, 0))

            # Buttons.
            start_button.update(self.screen)
            back_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == MS.MUSIC_ENDED:
                    MS.event_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.on_click():
                        # Game.
                        self.play_counter()
                        SM.stop_music()
                        Game(self.screen)

                    if back_button.on_click():
                        # Menu.
                        Menu(self.screen)

            pygame.display.flip()

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Score and level variables.
        self.score = 0
        self.level = 1
        self.LEVEL_SCORE_GAP = 10
        self.FONT_SIZE = 48

        self.font_obj = pygame.font.SysFont('Tahoma', self.FONT_SIZE, bold=True)

        self.pause = Pause(self.screen)
        self.SE = SoundEffects()

        self.start()

    def is_penguin_hit(self, current_peng_coordinates, current_peng_size):
        # Takes two args: tuple of coordinates and tuple of size.
        size = current_peng_size
        cord = current_peng_coordinates
        mp = pygame.mouse.get_pos()
        if cord[0] < mp[0] < cord[0] + size[0] and cord[1] < mp[1] < cord[1] + size[1]:
            return True
        else:
            return False

    def get_player_level(self):
        # Calculate player's level.
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            self.SE.play_level_up()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    def get_interval_by_level(self, initial_interval):
        # Calculate appearance interval from level.
        # NOTE: try to change const to 0.25 or 0.15 and check what will occur.
        const = 0.35
        new_interval = initial_interval - self.level * const
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    def get_random_penguin(self):
        # Just choose random penguin from penguins list.
        return random.choice(penguins)

    def restart_stats(self, SM):
        # Restart score and level.
        if self.pause.restart:
            self.score = 0
            self.level = 1
            self.pause.restart = False
        else:
            SM.unpause_music()

    def reset_stats(self):
        # Reset score and level after its max value.
        if self.score == 1000:
            self.score = 0
            self.level = 0

        if self.level > 99:
            self.score = 0
            self.level = 0

    def update_score(self):
        # Draws players score.
        # Format 1 to 001 and 13 to 013
        if self.score < 10:
            current_score_string = '00' + str(self.score)
        elif 10 <= self.score < 100:
            current_score_string = '0' + str(self.score)
        else:
            current_score_string = str(self.score)

        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.x = 464
        score_text_pos.y = 620
        self.screen.blit(score_text, score_text_pos)

    def update_level(self):
        # Draws players level.
        # Format 1 to 01
        if self.level < 10:
            current_level_string = 'LVL: ' + '0' + str(self.level)
        elif 10 <= self.level < 100:
            current_level_string = 'LVL: ' + str(self.level)
        else:
            current_level_string = 'LVL: ' + str(self.level)

        level_text = self.font_obj.render(current_level_string, True, (255, 0, 0))
        level_text_pos = level_text.get_rect()
        level_text_pos.x = 800
        level_text_pos.y = 620
        self.screen.blit(level_text, level_text_pos)

    def update_time(self, start_time):
        if start_time:
            time_since_enter = str(int(round((pygame.time.get_ticks() - start_time) / 1000, 0)))
            time_text = self.font_obj.render(time_since_enter, True, (255, 255, 255))
            time_text_pos = time_text.get_rect()
            time_text_pos.x = 24
            time_text_pos.y = 620
            self.screen.blit(time_text, time_text_pos)
            pygame.display.flip()

    def update(self):
        self.update_score()
        self.update_level()

    def start(self):
        self.score = 0
        self.level = 1

        # Control time variables.
        cycle_time = 0
        frame = -1
        is_down = False
        flag = False
        start_time = None
        interval = 0.1
        initial_interval = 1
        clock = pygame.time.Clock()

        done = True

        # Sounds.
        GS = GameSound()
        SM = SoundMethods()
        GS.play_game()

        while done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == GS.MUSIC_ENDED:
                    GS.event_game()

                if event.type == pygame.KEYDOWN:
                    # Count time.
                    if event.key == pygame.K_RETURN:
                        start_time = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_penguin_hit(penguin.coordinates, penguin.size) and frame > 0 and not flag:
                        # Penguin is hitted.
                        frame = 3
                        flag = True
                        is_down = False
                        interval = 0
                        self.score += 1
                        self.level = self.get_player_level()
                        self.screen.blit(hit, (pygame.mouse.get_pos()[0] - 24, pygame.mouse.get_pos()[1] - 24))
                        self.SE.play_hit()
                        self.update()
                        pygame.display.flip()
                    else:
                        # Penguin is missed.
                        self.SE.play_miss()

                    if pause_button.on_click():
                        # Pause.
                        SM.pause_music()
                        self.pause.start()

            if frame > 5:
                # Down animation.
                self.screen.blit(game_bg, (0, 0))
                pause_button.update(self.screen)
                frame = -1
                flag = False
                self.update()

            if frame == -1:
                # Up animation.
                self.screen.blit(game_bg, (0, 0))
                pause_button.update(self.screen)
                frame = 0
                is_down = False
                interval = 0.5
                penguin = self.get_random_penguin()
                self.update()

            mil = clock.tick(60)
            sec = mil / 1000.0
            cycle_time += sec

            if cycle_time > interval:
                # Control interval.
                self.screen.blit(game_bg, (0, 0))
                pause_button.update(self.screen)
                pic = penguin.penguin[frame]
                self.screen.blit(pic, penguin.coordinates)
                self.update()

                if is_down is False:
                    frame += 1
                else:
                    frame -= 1

                if frame == 4:
                    interval = 0.3

                elif frame == 3:
                    frame -= 1
                    is_down = True
                    interval = self.get_interval_by_level(initial_interval)
                else:
                    interval = 0.1

                cycle_time = 0

            # Buttons.
            pause_button.update(self.screen)

            # Updates time.
            self.update_time(start_time)

            # Pause restart and score reset.
            self.reset_stats()
            self.restart_stats(SM)

            pygame.display.flip()

class Pause:
    def __init__(self, screen):
        self.screen = screen
        self.restart = False
        self.done = False

    def start(self):
        self.done = True
        while self.done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if resume_button.on_click():
                        self.done = False

                    if restart_button.on_click():
                        self.restart = True

                    if menu_button.on_click():
                        # Menu.
                        self.done = False
                        MS.play_menu()
                        Menu(self.screen)

                    if pause_exit_button.on_click():
                        # Exit.
                        sys.exit()

            self.screen.blit(pause_bg, (0, 0))

            # Buttons.
            resume_button.update(self.screen)
            restart_button.update(self.screen)
            menu_button.update(self.screen)
            pause_exit_button.update(self.screen)

            pygame.display.flip()

# ---------------------------------------- RESOURCES ---------------------------------------- #

class Penguin:
    # Creates penguins frames from their frame sheets.
    # Takes 4 args; sprite_sheet (.png), size of every frame (example: (100, 100)),
    # step (one side of the frame, example: 100) and tuple of coordinates (x, y)
    def __init__(self, sprite_sheet, size, step, coordinates):

        self.size = size
        self.coordinates = coordinates

        self.penguin = []
        self.penguin.append(sprite_sheet.subsurface(0,        0, size[0], size[1]))
        self.penguin.append(sprite_sheet.subsurface(step,     0, size[0], size[1]))
        self.penguin.append(sprite_sheet.subsurface(step * 2, 0, size[0], size[1]))
        self.penguin.append(sprite_sheet.subsurface(step * 3, 0, size[0], size[1]))
        self.penguin.append(sprite_sheet.subsurface(step * 4, 0, size[0], size[1]))
        self.penguin.append(sprite_sheet.subsurface(step * 5, 0, size[0], size[1]))

# BACKGROUNDS
menu_bg = pygame.image.load('resources/menu/bg.jpg')

info_bg = pygame.image.load('resources/info/bg.jpg')

pause_bg = pygame.image.load('resources/pause/bg.jpg')

start_bg = pygame.image.load('resources/game_start/bg.jpg')

game_bg = pygame.image.load('resources/game/bg.png')

# BUTTONS
start_game_button = Button(301, 540, 'resources/menu/start_game_1.png', 'resources/menu/start_game_2.png')
menu_exit_button = Button(399, 610, 'resources/menu/exit_1.png', 'resources/menu/exit_2.png')
info_button = Button(945, 24, 'resources/menu/info_1.png', 'resources/menu/info_2.png')

info_back_button = Button(164, 566, 'resources/info/back_1.png', 'resources/info/back_2.png')

start_button = Button(342, 380, 'resources/game_start/start_1.png', 'resources/game_start/start_2.png')
back_button = Button(397, 493, 'resources/game_start/back_1.png', 'resources/game_start/back_2.png')

resume_button = Button(24, 24, 'resources/pause/resume_1.png', 'resources/pause/resume_2.png')
restart_button = Button(107, 24, 'resources/pause/restart_1.png', 'resources/pause/restart_2.png')
menu_button = Button(257, 527, 'resources/pause/menu_1.png', 'resources/pause/menu_2.png')
pause_exit_button = Button(399, 610, 'resources/pause/exit_1.png', 'resources/pause/exit_2.png')

pause_button = Button(24, 24, 'resources/game/pause_1.png', 'resources/game/pause_2.png')

# COUNTDOWN
count_bg = pygame.image.load('resources/game_start/count_bg.jpg')

# PENGUINS
penguin_1 = Penguin(pygame.image.load('resources/game/penguin_1.png'), (51, 51), 51, (174, 351))
penguin_2 = Penguin(pygame.image.load('resources/game/penguin_2.png'), (121, 121), 121, (295, 428))
penguin_3 = Penguin(pygame.image.load('resources/game/penguin_3.png'), (62, 62), 62, (538, 372))
penguin_4 = Penguin(pygame.image.load('resources/game/penguin_4.png'), (59, 59), 59, (654, 383))
penguin_5 = Penguin(pygame.image.load('resources/game/penguin_5.png'), (111, 111), 111, (875, 350))
penguin_6 = Penguin(pygame.image.load('resources/game/penguin_6.png'), (60, 60), 60, (618, 26))

penguins = [penguin_1, penguin_2, penguin_3, penguin_4, penguin_5, penguin_6]

# EFFECTS
hit = pygame.image.load('resources/game/hit.png')

# ---------------------------------------- START THE GAME ---------------------------------------- #

pygame.init()

class GameManager:
    # Starts the game.
    # Game starts every time from Menu scene.

    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 690))
        pygame.display.set_caption('PENGUIN SHOOTER')
        self.start_game()

    def start_game(self):
        Menu(self.screen)

StartGame = GameManager()