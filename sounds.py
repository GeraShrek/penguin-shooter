# This module includes sound classes of the scenes and their methods.

import os
import random

import pygame

def load_music(path, empty_list):
    # Loads all sound files from your folder.
    # Takes two args: path and empty list which will be filled with sound paths.
    # NOTE: files must be in .ogg, but you can change the format on .wav.
    for filename in os.listdir(path):
        if filename.endswith('.ogg'):
            empty_list.append(os.path.join(path, filename))
    return empty_list

def create_random_sequence(list_of_tracks):
    # Creates random sequence to play every time.
    list_of_tracks = sorted(list_of_tracks, key=lambda A: random.random())
    return list_of_tracks

class SoundManager:
    def __init__(self):
        self.MENU_PATH = 'resources/sounds/menu'
        self.GAME_PATH = 'resources/sounds/game'
        self.EFFECTS_PATH = 'resources/sounds/effects'

        self.menuTracks = []
        self.gameTracks = []
        self.gameEffects = []

        load_music(self.MENU_PATH, self.menuTracks)
        load_music(self.GAME_PATH, self.gameTracks)
        load_music(self.EFFECTS_PATH, self.gameEffects)

        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)

SoundEffectsObj = SoundManager()

class MenuSound:
    # Sounds which play in Menu scene.

    def __init__(self):
        self.menuTracks = SoundEffectsObj.menuTracks
        self.MUSIC_ENDED = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.MUSIC_ENDED)
        self.song_index = 0

    def play_menu(self):
        self.menuTracks = create_random_sequence(self.menuTracks)
        self.song_index = 0
        pygame.mixer.music.load(self.menuTracks[self.song_index])
        pygame.mixer.music.play()
        self.song_index += 1

    def event_menu(self):
        # Method helps to play next song every time.
        self.song_index = (self.song_index + 1) % len(self.menuTracks)
        pygame.mixer.music.load(self.menuTracks[self.song_index])
        pygame.mixer.music.play()

class GameSound:
    # Sounds which play in Game scene.

    def __init__(self):
        self.gameTracks = SoundEffectsObj.gameTracks

        self.MUSIC_ENDED = pygame.USEREVENT
        pygame.mixer.music.set_endevent(self.MUSIC_ENDED)
        self.song_index = 0

    def play_game(self):
        self.gameTracks = create_random_sequence(self.gameTracks)
        self.song_index = 0
        pygame.mixer.music.load(self.gameTracks[self.song_index])
        pygame.mixer.music.play()
        self.song_index += 1

    def event_game(self):
        # Method helps to play next song every time.
        self.song_index = (self.song_index + 1) % len(self.gameTracks)
        pygame.mixer.music.load(self.gameTracks[self.song_index])
        pygame.mixer.music.play()

class SoundEffects:
    # Hit, miss and level up effects.

    def __init__(self):
        self.gameEffects = SoundEffectsObj.gameEffects

        self.misses = self.gameEffects[2:]
        self.hit = pygame.mixer.Sound(self.gameEffects[0])
        self.level_up = pygame.mixer.Sound(self.gameEffects[1])

        self.hit.set_volume(0.5)

    def play_hit(self):
        self.hit.play()

    def play_miss(self):
        miss = pygame.mixer.Sound(random.choice(self.misses))
        miss.set_volume(0.5)
        miss.play()

    def play_level_up(self):
        self.level_up.play()

class SoundMethods:
    # Methods which stop, pause and unpause all sounds in game.

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()