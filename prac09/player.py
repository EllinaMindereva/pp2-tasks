import pygame

class MusicPlayer:
    def __init__(self, playlist):
        pygame.mixer.init()
        self.playlist = playlist
        self.index = 0
        self.paused = False
    
    def load(self):
        pygame.mixer.music.load(self.playlist[self.index])

    def play(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            self.load()
            pygame.mixer.music.play()
            self.paused = False
    
    def stop(self):
        pygame.mixer.music.stop()
        self.paused = False

    def next(self):
        self.index = (self.index + 1) % len(self.playlist)
        self.load()
        pygame.mixer.music.play()

    def previous(self):
        self.index = (self.index - 1) % len(self.playlist)
        self.load()
        pygame.mixer.music.play()

    def get_curr(self):
        return self.playlist[self.index]