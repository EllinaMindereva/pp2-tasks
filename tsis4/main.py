import pygame as py
import sys
import json
import os
from config import *
from db import init_db, save_result, get_leaderboard, get_personal_best
from game import Game

SETTINGS_FILE = "settings.json"

class App:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((SIZE, SIZE))
        py.display.set_caption("Snake game")
        self.clock = py.time.Clock()
        self.font_main = py.font.SysFont("comicsansms", 40)
        self.font_small = py.font.SysFont("comicsansms", 20)
        self.settings = self.load_settings()

        self.state = "MENU" #app state
        self.username = ""
        self.personal_best = 0
        self.game = None
    
        init_db() #initializing database

    def save_settings(self):
        #saves the current self.settings dictionary to disk
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)

    def load_settings(self):
        #loads settings from json or returns defaults
        defaults = {
            "snake_color": [0, 255, 0], 
            "grid_overlay": True,
            "sound": True
        }
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return defaults
    
    def draw_text(self, text, pos, font=None, color=COLOR_TEXT, center=False):
        if font is None: font = self.font_main
        img = font.render(text, True, color)
        rect = img.get_rect(topleft=pos)
        if center: rect.center = pos
        self.screen.blit(img, rect)

    def menu_screen(self):
        self.screen.fill(COLOR_BG)
        self.draw_text("Snake", (SIZE//2, 150), center=True)
        self.draw_text(f"Player: {self.username}", (SIZE//2, 250), self.font_small, center=True)
        self.draw_text("Press ENTER to Play", (SIZE//2, 400), self.font_small, center=True)
        self.draw_text("L: Leaderboard | S: Settings | Q: Quit", (SIZE//2, 450), self.font_small, center=True)

        for event in py.event.get():
            if event.type == py.QUIT: py.quit(); sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN and self.username:
                    self.personal_best = get_personal_best(self.username)
                    self.game = Game(self.username, self.personal_best)
                    self.state = "GAME"
                if event.key == py.K_l: self.state = "LEADERBOARD"
                if event.key == py.K_s: self.state = "SETTINGS"
                if event.key == py.K_q: py.quit(); sys.exit()
                #username typing
                if event.key == py.K_BACKSPACE: self.username = self.username[:-1]
                elif len(self.username) < 10 and event.unicode.isalnum():
                    self.username += event.unicode

    def settings_screen(self):
        self.screen.fill(COLOR_BG)
        self.draw_text("SETTINGS", (SIZE//2, 100), center=True)

        #map booleans to UI text
        grid_txt = "ON" if self.settings["grid_overlay"] else "OFF"
        sound_txt = "ON" if self.settings["sound"] else "OFF"
        color_rgb = self.settings["snake_color"]

        #display options
        self.draw_text(f"[1] Grid Overlay: {grid_txt}", (SIZE//2, 250), self.font_small, center=True)
        self.draw_text(f"[2] Sound: {sound_txt}", (SIZE//2, 300), self.font_small, center=True)
        self.draw_text(f"[3] Snake Color: {color_rgb}", (SIZE//2, 350), self.font_small, center=True)
        
        self.draw_text("Press ESC to Save and Return", (SIZE//2, 600), self.font_small, center=True, color=(150, 150, 150))

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit(); sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_1:
                    self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                
                if event.key == py.K_2:
                    self.settings["sound"] = not self.settings["sound"]
                
                if event.key == py.K_3:
                    # Simple color cycler: Green -> Blue -> Red
                    color_palette = [[0, 255, 0], [0, 0, 255], [255, 0, 0]]
                    current_idx = color_palette.index(color_rgb) if color_rgb in color_palette else 0
                    self.settings["snake_color"] = color_palette[(current_idx + 1) % len(color_palette)]
                
                if event.key == py.K_ESCAPE:
                    self.save_settings() # Save changes to disk
                    self.state = "MENU"

    def leaderboard_screen(self):
        self.screen.fill(COLOR_BG)
        self.draw_text("TOP 10 SCORES", (SIZE//2, 80), center=True)
        
        data = get_leaderboard()
        y_offset = 180
        header = f"{'User':<12} {'Score':<8} {'Lvl':<5} {'Date'}"
        self.draw_text(header, (100, 150), self.font_small, (200, 200, 0))

        for row in data:
            date_str = row[3].strftime("%Y-%m-%d")
            entry = f"{row[0]:<12} {row[1]:<8} {row[2]:<5} {date_str}"
            self.draw_text(entry, (100, y_offset), self.font_small)
            y_offset += 35

        self.draw_text("Press ESC for Menu", (SIZE//2, 700), self.font_small, center=True)
        
        for event in py.event.get():
            if event.type == py.QUIT: py.quit(); sys.exit()
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                self.state = "MENU"

    def game_over_screen(self):
        self.screen.fill((50, 0, 0)) # Dark red background
        self.draw_text("GAME OVER", (SIZE//2, 200), center=True)
        self.draw_text(f"Score: {self.game.score}", (SIZE//2, 300), self.font_small, center=True)
        
        self.draw_text("Press ENTER to Save to Leaderboard", (SIZE//2, 500), self.font_small, center=True)
        self.draw_text("Press ESC to Discard", (SIZE//2, 550), self.font_small, center=True)

        for event in py.event.get():
            if event.type == py.QUIT: 
                py.quit(); sys.exit()
                
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    print(f"Attempting to save: {self.username}, {self.game.score}") # Debug line
                    save_result(self.username, self.game.score, self.game.level)
                    self.state = "LEADERBOARD"
                    
                if event.key == py.K_ESCAPE:
                    self.state = "MENU"

    def run(self):
        while True:
            if self.state == "MENU":
                self.menu_screen()
            elif self.state == "LEADERBOARD":
                self.leaderboard_screen()
            elif self.state == "SETTINGS": #new state
                self.settings_screen()
            elif self.state == "GAME":
                self.play_game()
            elif self.state == "GAME_OVER":
                self.game_over_screen()
            
            py.display.flip()
            self.clock.tick(FPS)

    def play_game(self): #gameloop
        for event in py.event.get():
            if event.type == py.QUIT: py.quit(); sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_UP and self.game.snake_dir != (0, CELL_SIZE):
                    self.game.snake_dir = (0, -CELL_SIZE)
                if event.key == py.K_DOWN and self.game.snake_dir != (0, -CELL_SIZE):
                    self.game.snake_dir = (0, CELL_SIZE)
                if event.key == py.K_LEFT and self.game.snake_dir != (CELL_SIZE, 0):
                    self.game.snake_dir = (-CELL_SIZE, 0)
                if event.key == py.K_RIGHT and self.game.snake_dir != (-CELL_SIZE, 0):
                    self.game.snake_dir = (CELL_SIZE, 0)

        self.game.update() #update screen
        if self.game.game_over:
            self.state = "GAME_OVER"

        self.screen.fill(COLOR_BG)
        
        if self.settings["grid_overlay"]: #grid
            for x in range(0, SIZE, CELL_SIZE):
                py.draw.line(self.screen, (40, 40, 40), (x, 0), (x, SIZE))
            for y in range(0, SIZE, CELL_SIZE):
                py.draw.line(self.screen, (40, 40, 40), (0, y), (SIZE, y))

        self.game.draw(self.screen, self.settings["snake_color"])
        
        #UI
        self.draw_text(f"Score: {self.game.score} | Lvl: {self.game.level}", (10, 10), self.font_small)
        self.draw_text(f"PB: {self.personal_best}", (SIZE - 100, 10), self.font_small)

if __name__ == "__main__":
    app = App()
    app.run()