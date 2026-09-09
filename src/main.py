"""    Run with: main.py
"""

import json
import math
import os
import random
from array import array

import pygame


WIDTH, HEIGHT = 600, 720
BOARD_X, BOARD_Y, BOARD_SIZE = 40, 160, 520
ROWS = COLS = 4
GAP = 12
CELL = (BOARD_SIZE - GAP * (COLS + 1)) // COLS
FPS = 60
SAVE_FILE = "2048_best_score.json"

BACKGROUND = (250, 248, 239)
BOARD = (187, 173, 160)
EMPTY = (205, 193, 180)
DARK = (119, 110, 101)
LIGHT = (249, 246, 242)
ACCENT = (237, 194, 46)
TILE_COLORS = {
    2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
    16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59),
    128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80),
    1024: (237, 197, 63), 2048: (237, 194, 46), 4096: (60, 58, 50),
    8192: (45, 42, 37),
}


class Game2048:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 72)
        self.score_font = pygame.font.Font(None, 26)
        self.ui_font = pygame.font.Font(None, 30)
        self.large_font = pygame.font.Font(None, 58)
        self.best_score = self.load_best_score()
        self.move_sound = self.make_tone(400, 0.045)
        self.merge_sound = self.make_tone(660, 0.08)
        self.state = "start"
        self.reset()

    def load_best_score(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_FILE)
        try:
            with open(path, "r", encoding="utf-8") as file:
                return int(json.load(file).get("best_score", 0))
        except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError):
            return 0

    def save_best_score(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_FILE)
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump({"best_score": self.best_score}, file)
        except OSError:
            pass

    def make_tone(self, frequency, duration):
        if not pygame.mixer.get_init():
            return None
        rate = 22050
        samples = array("h", (int(6500 * math.sin(2 * math.pi * frequency * i / rate))
                              for i in range(int(rate * duration))))
        return pygame.mixer.Sound(buffer=samples)

    @staticmethod
    def play(sound):
        if sound:
            sound.play()

    def reset(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.score = 0
        self.animations = []
        self.animation_time = 0.0
        self.spawn_cell = None
        self.spawn_time = 0.0
        self.won = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(ROWS) for c in range(COLS) if not self.board[r][c]]
        if not empty:
            return
        row, col = random.choice(empty)
        self.board[row][col] = 4 if random.random() < 0.1 else 2
        self.spawn_cell, self.spawn_time = (row, col), 0.14

    def cell_rect(self, row, col):
        return pygame.Rect(BOARD_X + GAP + col * (CELL + GAP), BOARD_Y + GAP + row * (CELL + GAP), CELL, CELL)

    def tile_color(self, value):
        return TILE_COLORS.get(value, (45, 42, 37))

    def draw_text_center(self, text, font, center, color):
        rendered = font.render(text, True, color)
        self.screen.blit(rendered, rendered.get_rect(center=center))

    def draw_button(self, rect, label):
        mouse_inside = rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(self.screen, (143, 122, 102) if mouse_inside else DARK, rect, border_radius=8)
        self.draw_text_center(label, self.ui_font, rect.center, LIGHT)

    def draw_tile(self, value, row, col, scale=1.0, offset=(0, 0)):
        rect = self.cell_rect(row, col).move(offset)
        if scale != 1:
            rect = pygame.Rect(0, 0, max(1, int(rect.width * scale)), max(1, int(rect.height * scale)))
            rect.center = (self.cell_rect(row, col).centerx + offset[0], self.cell_rect(row, col).centery + offset[1])
        pygame.draw.rect(self.screen, self.tile_color(value), rect, border_radius=7)
        size = 52 if value < 128 else 46 if value < 1024 else 38 if value < 10000 else 31
        font = pygame.font.Font(None, size)
        color = DARK if value in (2, 4) else LIGHT
        self.draw_text_center(str(value), font, rect.center, color)

    def draw_board(self):
        pygame.draw.rect(self.screen, BOARD, (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE), border_radius=10)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(self.screen, EMPTY, self.cell_rect(row, col), border_radius=7)
        if self.animation_time > 0:
            progress = 1 - self.animation_time / 0.12
            for value, source, destination in self.animations:
                sr, sc = source
                dr, dc = destination
                offset = ((sc - dc) * (CELL + GAP) * (1 - progress), (sr - dr) * (CELL + GAP) * (1 - progress))
                self.draw_tile(value, dr, dc, offset=offset)
            return
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col]:
                    scale = 1.0
                    if self.spawn_cell == (row, col) and self.spawn_time > 0:
                        scale = 0.65 + 0.35 * (1 - self.spawn_time / 0.14)
                    self.draw_tile(self.board[row][col], row, col, scale)

    def draw_header(self):
        self.draw_text_center("2048", self.title_font, (120, 58), DARK)
        self.draw_text_center("Join the numbers", self.ui_font, (125, 104), DARK)
        score_box = pygame.Rect(320, 30, 105, 70)
        best_box = pygame.Rect(435, 30, 125, 70)
        for rect, label, value in ((score_box, "SCORE", self.score), (best_box, "BEST", self.best_score)):
            pygame.draw.rect(self.screen, BOARD, rect, border_radius=7)
            self.draw_text_center(label, self.score_font, (rect.centerx, rect.y + 16), LIGHT)
            self.draw_text_center(str(value), self.score_font, (rect.centerx, rect.y + 47), LIGHT)
        self.restart_button = pygame.Rect(440, 105, 120, 36)
        self.draw_button(self.restart_button, "Restart")

    def draw_overlay(self, heading, message, button_label):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((238, 228, 218, 205))
        self.screen.blit(overlay, (0, 0))
        self.draw_text_center(heading, self.large_font, (WIDTH // 2, 300), DARK)
        self.draw_text_center(message, self.ui_font, (WIDTH // 2, 350), DARK)
        self.action_button = pygame.Rect(WIDTH // 2 - 95, 390, 190, 52)
        self.draw_button(self.action_button, button_label)

    def draw(self):
        self.screen.fill(BACKGROUND)
        if self.state == "start":
            self.draw_text_center("2048", self.title_font, (WIDTH // 2, 200), DARK)
            self.draw_text_center("Slide tiles. Match numbers. Reach 2048.", self.ui_font, (WIDTH // 2, 270), DARK)
            self.action_button = pygame.Rect(WIDTH // 2 - 100, 330, 200, 54)
            self.draw_button(self.action_button, "Start Game")
            self.draw_text_center("Use arrow keys to move", self.score_font, (WIDTH // 2, 425), DARK)
        else:
            self.draw_header()
            self.draw_board()
            if self.state == "won":
                self.draw_overlay("You made 2048!", "A brilliant move.", "Keep Playing")
            elif self.state == "lost":
                self.draw_overlay("Game Over", f"Score: {self.score}", "Play Again")
        pygame.display.flip()

    def transform_line(self, line, positions):
        """Compress and merge one row/column; return values, point gain, and moves."""
        occupied = [(value, pos) for value, pos in zip(line, positions) if value]
        result, motions, gained, index = [], [], 0, 0
        while index < len(occupied):
            value, source = occupied[index]
            destination = positions[len(result)]
            if index + 1 < len(occupied) and occupied[index + 1][0] == value:
                new_value = value * 2
                result.append(new_value)
                motions.extend([(value, source, destination), (value, occupied[index + 1][1], destination)])
                gained += new_value
                index += 2
            else:
                result.append(value)
                motions.append((value, source, destination))
                index += 1
        return result + [0] * (COLS - len(result)), gained, motions

    def move(self, direction):
        if self.animation_time > 0 or self.state not in ("playing", "won"):
            return
        old = [row[:] for row in self.board]
        new = [[0] * COLS for _ in range(ROWS)]
        animations, gained = [], 0
        for fixed in range(ROWS):
            if direction in ("left", "right"):
                positions = [(fixed, col) for col in (range(COLS) if direction == "left" else range(COLS - 1, -1, -1))]
            else:
                positions = [(row, fixed) for row in (range(ROWS) if direction == "up" else range(ROWS - 1, -1, -1))]
            values = [old[row][col] for row, col in positions]
            transformed, points, motions = self.transform_line(values, positions)
            gained += points
            animations.extend(motions)
            for value, (row, col) in zip(transformed, positions):
                new[row][col] = value
        if new == old:
            if not self.can_move():
                self.state = "lost"
            return
        self.board, self.score = new, self.score + gained
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()
        self.animations, self.animation_time = animations, 0.12
        self.spawn_cell = None
        self.play(self.merge_sound if gained else self.move_sound)

    def can_move(self):
        for row in range(ROWS):
            for col in range(COLS):
                value = self.board[row][col]
                if not value:
                    return True
                if col < COLS - 1 and value == self.board[row][col + 1]:
                    return True
                if row < ROWS - 1 and value == self.board[row + 1][col]:
                    return True
        return False

    def update(self, delta_time):
        if self.animation_time > 0:
            self.animation_time = max(0, self.animation_time - delta_time)
            if self.animation_time == 0:
                self.add_random_tile()
                if any(value >= 2048 for row in self.board for value in row) and not self.won:
                    self.won, self.state = True, "won"
                elif not self.can_move():
                    self.state = "lost"
        self.spawn_time = max(0, self.spawn_time - delta_time)

    def start_game(self):
        self.reset()
        self.state = "playing"

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.state == "start" and self.action_button.collidepoint(event.pos):
                self.start_game()
            elif self.state in ("playing", "won", "lost") and self.restart_button.collidepoint(event.pos):
                self.start_game()
            elif self.state == "lost" and self.action_button.collidepoint(event.pos):
                self.start_game()
            elif self.state == "won" and self.action_button.collidepoint(event.pos):
                self.state = "playing"
            return True
        if event.type != pygame.KEYDOWN:
            return True
        if event.key == pygame.K_ESCAPE:
            return False
        if self.state == "start" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.start_game()
        elif self.state == "lost" and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
            self.start_game()
        elif self.state == "won" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.state = "playing"
        elif self.state in ("playing", "won"):
            if event.key == pygame.K_r:
                self.start_game()
            else:
                directions = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_UP: "up", pygame.K_DOWN: "down"}
                if event.key in directions:
                    self.move(directions[event.key])
        return True

    def run(self):
        running = True
        while running:
            delta_time = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                running = self.handle_event(event) and running
            self.update(delta_time)
            self.draw()
        pygame.quit()


if __name__ == "__main__":
    Game2048().run()
















