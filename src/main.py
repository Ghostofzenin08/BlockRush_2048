
import json
import math
import os
import platform
import random
import time
from array import array



import pygame



ACCENT = {
    "yellow": (255, 189, 0),
    "orange": (255, 84, 0),
    "purple": (57, 0, 153),
    "pink": (158, 0, 89),
    "cyan": (4, 199, 253),
}

THEMES = {
    "dark": {
        "bg": (0, 0, 0),
        "text": (255, 255, 255),
        "muted_text": (170, 170, 180),
        "card": (29, 30, 44),       # #1d1e2c per spec
        "board": (29, 30, 44),
        "empty_cell": (46, 47, 64),
    },
    "light": {
        "bg": (255, 255, 255),
        "text": (0, 0, 0),
        "muted_text": (95, 95, 105),
        "card": (29, 30, 44),       # buttons stay dark pills in light mode per spec
        "board": (230, 230, 236),
        "empty_cell": (213, 213, 222),
    },
}

TILE_COLORS = {
    2: ACCENT["yellow"],
    4: ACCENT["orange"],
    8: (156, 42, 77),
    16: ACCENT["purple"],
    32: ACCENT["yellow"],
    64: (255, 154, 0),
    128: (255, 119, 0),
    256: ACCENT["orange"],
    512: (207, 42, 45),
    1024: ACCENT["pink"],
    2048: (130, 0, 74),
    4096: ACCENT["cyan"],
    8192: (30, 99, 203),
}

WIDTH, HEIGHT = 600, 700
BOARD_X, BOARD_Y, BOARD_SIZE = 40, 140, 520
ROWS = COLS = 4
GAP = 12
CELL = (BOARD_SIZE - GAP * (COLS + 1)) // COLS
FPS = 60
MOVE_ANIM_TIME = 0.14
SPAWN_ANIM_TIME = 0.16
MERGE_POP_TIME = 0.12
UNDO_LIMIT = 20
SETTINGS_FILENAME = "settings.json"

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")
FONT_CANDIDATES = ["Instrument Sans", "Inria Sans", "Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"]


def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1 - pow(1 - t, 3)


def load_font(size, bold=False):
    filename = "InstrumentSans-Bold.ttf" if bold else "InstrumentSans-Regular.ttf"
    bundled_path = os.path.join(FONT_DIR, filename)
    if os.path.isfile(bundled_path):
        return pygame.font.Font(bundled_path, size)
    system_path = pygame.font.match_font(",".join(FONT_CANDIDATES), bold=bold)
    if system_path:
        return pygame.font.Font(system_path, size)
    return pygame.font.Font(None, size)


def get_app_data_dir(app_name="BlockRush2048"):
    system = platform.system()
    try:
        if system == "Windows":
            base = os.environ.get("APPDATA") or os.path.expanduser("~")
        elif system == "Darwin":
            base = os.path.expanduser("~/Library/Application Support")
        else:
            base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
        path = os.path.join(base, app_name)
        os.makedirs(path, exist_ok=True)
        return path
    except OSError:
        return os.path.dirname(os.path.abspath(__file__))


class SettingsStore:
    def __init__(self):
        self.path = os.path.join(get_app_data_dir(), SETTINGS_FILENAME)
        self.data = {"best_score": 0, "theme": "dark", "sound_on": True, "leaderboard": []}
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                loaded = json.load(file)
                for key in self.data:
                    if key in loaded:
                        self.data[key] = loaded[key]
        except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError):
            pass

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(self.data, file)
        except OSError:
            pass

    def submit_score(self, score):
        if score > self.data["best_score"]:
            self.data["best_score"] = score
        board = self.data["leaderboard"]
        board.append({"score": score, "date": time.strftime("%Y-%m-%d %H:%M")})
        board.sort(key=lambda entry: entry["score"], reverse=True)
        self.data["leaderboard"] = board[:5]
        self.save()


class BoardEngine:

    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.score = 0

    def snapshot(self):
        return [row[:] for row in self.board], self.score

    def restore(self, snapshot):
        board, score = snapshot
        self.board = [row[:] for row in board]
        self.score = score

    def empty_cells(self):
        return [(r, c) for r in range(self.rows) for c in range(self.cols) if not self.board[r][c]]

    def add_random_tile(self, p_four=0.1):
        empty = self.empty_cells()
        if not empty:
            return None
        row, col = random.choice(empty)
        value = 4 if random.random() < p_four else 2
        self.board[row][col] = value
        return row, col, value

    def can_move(self):
        for row in range(self.rows):
            for col in range(self.cols):
                value = self.board[row][col]
                if not value:
                    return True
                if col < self.cols - 1 and value == self.board[row][col + 1]:
                    return True
                if row < self.rows - 1 and value == self.board[row + 1][col]:
                    return True
        return False

    @staticmethod
    def transform_line(line, positions):
        occupied = [(value, pos) for value, pos in zip(line, positions) if value]
        result, motions, gained, index = [], [], 0, 0
        while index < len(occupied):
            value, source = occupied[index]
            destination = positions[len(result)]
            if index + 1 < len(occupied) and occupied[index + 1][0] == value:
                new_value = value * 2
                result.append(new_value)
                motions.append((value, source, destination, True))
                motions.append((value, occupied[index + 1][1], destination, True))
                gained += new_value
                index += 2
            else:
                result.append(value)
                motions.append((value, source, destination, False))
                index += 1
        return result + [0] * (COLS - len(result)), gained, motions

    def move(self, direction):
        """Attempt a move. Board/score are only mutated if it actually moves."""
        old = [row[:] for row in self.board]
        new = [[0] * COLS for _ in range(ROWS)]
        motions, gained = [], 0
        for fixed in range(ROWS):
            if direction in ("left", "right"):
                cols = range(COLS) if direction == "left" else range(COLS - 1, -1, -1)
                positions = [(fixed, c) for c in cols]
            else:
                rows = range(ROWS) if direction == "up" else range(ROWS - 1, -1, -1)
                positions = [(r, fixed) for r in rows]
            values = [old[r][c] for r, c in positions]
            transformed, points, line_motions = self.transform_line(values, positions)
            gained += points
            motions.extend(line_motions)
            for value, (r, c) in zip(transformed, positions):
                new[r][c] = value
        moved = new != old
        if moved:
            self.board, self.score = new, self.score + gained
        return moved, gained, motions


class BlockRush2048:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BlockRush 2048")
        self.clock = pygame.time.Clock()

        self.mega_font = load_font(60, bold=True)
        self.title_font = load_font(44, bold=True)
        self.hero_font = load_font(32, bold=True)
        self.section_font = load_font(24, bold=True)
        self.button_font = load_font(20, bold=True)
        self.body_font = load_font(16)
        self.small_font = load_font(14)

        self.settings = SettingsStore()
        self.theme_name = self.settings.data.get("theme", "dark")
        self.sound_on = self.settings.data.get("sound_on", True)
        self.best_score = self.settings.data.get("best_score", 0)

        self.move_sound = self.make_tone(400, 0.045)
        self.merge_sound = self.make_tone(660, 0.08)

        self.state = "playing"  # start, playing, paused, won, lost, leaderboard
        self.previous_state_before_pause = "playing"
        self.undo_stack = []
        self.engine = BoardEngine()
        self.reset_round()

    @property
    def theme(self):
        return THEMES[self.theme_name]

    # ---- persistence-backed toggles ---------------------------------
    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.settings.data["theme"] = self.theme_name
        self.settings.save()

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.settings.data["sound_on"] = self.sound_on
        self.settings.save()

    # ---- audio ----------------------------------------------------------
    def make_tone(self, frequency, duration):
        if not pygame.mixer.get_init():
            return None
        rate = 22050
        samples = array("h", (int(6500 * math.sin(2 * math.pi * frequency * i / rate))
                              for i in range(int(rate * duration))))
        return pygame.mixer.Sound(buffer=samples)

    def play(self, sound):
        if sound and self.sound_on:
            sound.play()



    # ---- round lifecycle --------------------------------------------



    def reset_round(self):
        self.engine = BoardEngine()
        self.undo_stack.clear()
        self.animations = []
        self.animation_time = 0.0
        self.merge_cells = set()
        self.merge_time = 0.0
        self.spawn_cell = None
        self.spawn_time = 0.0
        self.won = False
        self.displayed_score = 0.0
        self.engine.add_random_tile()
        self.engine.add_random_tile()

    def start_game(self):
        self.reset_round()
        self.state = "playing"




    # ---- geometry -----------------------------------------------------


    def cell_rect(self, row, col):
        return pygame.Rect(BOARD_X + GAP + col * (CELL + GAP), BOARD_Y + GAP + row * (CELL + GAP), CELL, CELL)


    @staticmethod
    def tile_text_color(rgb):
        r, g, b = rgb
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return (20, 18, 30) if luminance > 165 else (255, 255, 255)



    def tile_color(self, value):
        return TILE_COLORS.get(value, (20, 18, 30))

    # ---- drawing helpers ------------------------------------------------


    def draw_text_center(self, text, font, center, color):
        rendered = font.render(text, True, color)
        self.screen.blit(rendered, rendered.get_rect(center=center))




    def draw_pill_button(self, rect, label, font=None):
        font = font or self.button_font
        mouse_inside = rect.collidepoint(pygame.mouse.get_pos())
        base = self.theme["card"]
        color = tuple(min(255, c + 22) for c in base) if mouse_inside else base
        pygame.draw.rect(self.screen, color, rect, border_radius=rect.height // 2)
        self.draw_text_center(label, font, rect.center, (255, 255, 255))






    def circle_icon_button(self, x, y, diameter=40):
        rect = pygame.Rect(x, y, diameter, diameter)
        mouse_inside = rect.collidepoint(pygame.mouse.get_pos())
        base = self.theme["card"]
        color = tuple(min(255, c + 22) for c in base) if mouse_inside else base
        pygame.draw.circle(self.screen, color, rect.center, diameter // 2)
        return rect





    def draw_moon_icon(self, rect):
        cx, cy = rect.center
        r = rect.width // 2 - 6
        pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), r)
        pygame.draw.circle(self.screen, self.theme["card"], (cx + r // 2, cy - r // 3), r)






    def draw_sun_icon(self, rect):
        cx, cy = rect.center
        r = rect.width // 2 - 10
        pygame.draw.circle(self.screen, ACCENT["yellow"], (cx, cy), r)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1, y1 = cx + math.cos(rad) * (r + 3), cy + math.sin(rad) * (r + 3)
            x2, y2 = cx + math.cos(rad) * (r + 8), cy + math.sin(rad) * (r + 8)
            pygame.draw.line(self.screen, ACCENT["yellow"], (x1, y1), (x2, y2), 2)





    def draw_speaker_icon(self, rect, muted):
        cx, cy = rect.center
        body = pygame.Rect(0, 0, 9, 13)
        body.center = (cx - 7, cy)
        pygame.draw.rect(self.screen, (255, 255, 255), body, border_radius=2)
        points = [(cx - 2, cy - 9), (cx + 7, cy - 15), (cx + 7, cy + 15), (cx - 2, cy + 9)]
        pygame.draw.polygon(self.screen, (255, 255, 255), points)
        if muted:
            pygame.draw.line(self.screen, ACCENT["orange"], (cx + 3, cy - 9), (cx + 15, cy + 9), 3)
        else:
            pygame.draw.arc(self.screen, (255, 255, 255), (cx + 9, cy - 9, 13, 18), -0.7, 0.7, 2)






    def draw_tile(self, value, row, col, scale=1.0, offset=(0, 0)):
        base_rect = self.cell_rect(row, col)
        rect = base_rect.move(offset)
        if scale != 1.0:
            rect = pygame.Rect(0, 0, max(1, int(base_rect.width * scale)), max(1, int(base_rect.height * scale)))
            rect.center = (base_rect.centerx + offset[0], base_rect.centery + offset[1])
        color = self.tile_color(value)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        size = 42 if value < 128 else 36 if value < 1024 else 30 if value < 10000 else 24
        self.draw_text_center(str(value), load_font(size, bold=True), rect.center, self.tile_text_color(color))






    def draw_board(self):
        theme = self.theme
        pygame.draw.rect(self.screen, theme["board"], (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE), border_radius=12)
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(self.screen, theme["empty_cell"], self.cell_rect(row, col), border_radius=8)

        if self.animation_time > 0:
            progress = ease_out_cubic(1 - self.animation_time / MOVE_ANIM_TIME)
            for value, source, destination, _merged in self.animations:
                sr, sc = source
                dr, dc = destination
                offset = ((sc - dc) * (CELL + GAP) * (1 - progress), (sr - dr) * (CELL + GAP) * (1 - progress))
                self.draw_tile(value, dr, dc, offset=offset)
            return


        for row in range(ROWS):
            for col in range(COLS):
                value = self.engine.board[row][col]
                if not value:
                    continue
                scale = 1.0
                if self.spawn_cell == (row, col) and self.spawn_time > 0:
                    scale = 0.6 + 0.4 * ease_out_cubic(1 - self.spawn_time / SPAWN_ANIM_TIME)
                elif (row, col) in self.merge_cells and self.merge_time > 0:
                    t = 1 - self.merge_time / MERGE_POP_TIME
                    scale = 1.0 + 0.18 * math.sin(t * math.pi)
                self.draw_tile(value, row, col, scale)




    def draw_header(self):
        theme = self.theme
        self.draw_text_center("BlockRush 2048", self.section_font, (WIDTH // 2, 34), theme["text"])

        self.theme_button = self.circle_icon_button(20, 70, 40)
        (self.draw_moon_icon if self.theme_name == "dark" else self.draw_sun_icon)(self.theme_button)

        self.sound_button = self.circle_icon_button(70, 70, 40)
        self.draw_speaker_icon(self.sound_button, muted=not self.sound_on)

        self.undo_button = pygame.Rect(120, 74, 80, 36)
        can_undo = bool(self.undo_stack)
        pygame.draw.rect(self.screen, theme["card"] if can_undo else theme["empty_cell"],
                          self.undo_button, border_radius=18)
        self.draw_text_center("Undo", self.small_font, self.undo_button.center,
                               (255, 255, 255) if can_undo else theme["muted_text"])

        self.restart_button = pygame.Rect(210, 74, 110, 36)
        self.draw_pill_button(self.restart_button, "Restart", self.small_font)

        score_box = pygame.Rect(330, 64, 110, 56)
        best_box = pygame.Rect(450, 64, 110, 56)
        for rect, label, value in ((score_box, "SCORE", int(self.displayed_score)),
                                    (best_box, "BEST", self.best_score)):
            pygame.draw.rect(self.screen, theme["card"], rect, border_radius=10)
            self.draw_text_center(label, self.small_font, (rect.centerx, rect.y + 15), (200, 200, 210))
            self.draw_text_center(str(value), self.body_font, (rect.centerx, rect.y + 38), (255, 255, 255))





    def draw_overlay(self, heading, message, button_label):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((*self.theme["bg"], 210))
        self.screen.blit(overlay, (0, 0))
        cy = HEIGHT // 2
        self.draw_text_center(heading, self.title_font, (WIDTH // 2, cy - 70), self.theme["text"])
        self.draw_text_center(message, self.body_font, (WIDTH // 2, cy - 20), self.theme["text"])
        self.action_button = pygame.Rect(WIDTH // 2 - 100, cy + 10, 200, 52)
        self.draw_pill_button(self.action_button, button_label)



    def draw_start(self):
        theme = self.theme
        self.screen.fill(theme["bg"])
        self.draw_text_center("BlockRush", self.mega_font, (WIDTH // 2, 200), theme["text"])
        self.draw_text_center("2048", self.hero_font, (WIDTH // 2, 250), ACCENT["yellow"])
        self.draw_text_center("Slide tiles. Match numbers. Beat your best.",
                               self.body_font, (WIDTH // 2, 300), theme["muted_text"])

        self.action_button = pygame.Rect(WIDTH // 2 - 110, 340, 220, 54)
        self.draw_pill_button(self.action_button, "Start Game", self.button_font)
        self.leaderboard_button = pygame.Rect(WIDTH // 2 - 110, 408, 220, 46)
        self.draw_pill_button(self.leaderboard_button, "Leaderboard", self.button_font)

        self.theme_button = self.circle_icon_button(WIDTH - 60, 20, 40)
        (self.draw_moon_icon if self.theme_name == "dark" else self.draw_sun_icon)(self.theme_button)
        self.sound_button = self.circle_icon_button(WIDTH - 110, 20, 40)
        self.draw_speaker_icon(self.sound_button, muted=not self.sound_on)

        self.draw_text_center("Arrows / WASD to move  ·  U to undo  ·  Esc to pause",
                               self.small_font, (WIDTH // 2, 600), theme["muted_text"])



    def draw_leaderboard(self):
        theme = self.theme
        self.screen.fill(theme["bg"])
        self.draw_text_center("Leaderboard", self.hero_font, (WIDTH // 2, 70), theme["text"])
        entries = self.settings.data.get("leaderboard", [])
        if not entries:
            self.draw_text_center("No games finished yet — go set a record.",
                                   self.body_font, (WIDTH // 2, 200), theme["muted_text"])
        for i, entry in enumerate(entries[:5]):
            row_rect = pygame.Rect(WIDTH // 2 - 200, 130 + i * 60, 400, 48)
            pygame.draw.rect(self.screen, theme["card"], row_rect, border_radius=10)
            self.draw_text_center(f"#{i + 1}", self.body_font, (row_rect.x + 30, row_rect.centery), ACCENT["yellow"])
            self.draw_text_center(str(entry["score"]), self.body_font, (row_rect.centerx, row_rect.centery), (255, 255, 255))
            self.draw_text_center(entry["date"], self.small_font, (row_rect.right - 70, row_rect.centery), (200, 200, 210))
        self.back_button = pygame.Rect(WIDTH // 2 - 90, 460, 180, 48)
        self.draw_pill_button(self.back_button, "Back")



    def draw(self):
        if self.state == "start":
            self.draw_start()
        elif self.state == "leaderboard":
            self.draw_leaderboard()
        else:
            self.screen.fill(self.theme["bg"])
            self.draw_header()
            self.draw_board()
            if self.state == "won":
                self.draw_overlay("You made 2048!", "A brilliant move — keep going for a higher score.", "Keep Playing")
            elif self.state == "lost":
                self.draw_overlay("Game Over", f"Final score: {self.engine.score}", "Play Again")
            elif self.state == "paused":
                self.draw_overlay("Paused", "Take a breather.", "Resume")
        pygame.display.flip()

    # ---- gameplay ---------------------------------------------------



    def move(self, direction):
        if self.animation_time > 0 or self.state not in ("playing", "won"):
            return
        self.undo_stack.append(self.engine.snapshot())
        moved, gained, motions = self.engine.move(direction)
        if not moved:
            self.undo_stack.pop()
            if not self.engine.can_move():
                self.state = "lost"
                self.settings.submit_score(self.engine.score)
                self.best_score = self.settings.data["best_score"]
            return
        self.animations = motions
        self.animation_time = MOVE_ANIM_TIME
        self.merge_cells = {dest for _, _, dest, merged in motions if merged}
        self.spawn_cell = None
        self.play(self.merge_sound if gained else self.move_sound)
        if len(self.undo_stack) > UNDO_LIMIT:
            self.undo_stack.pop(0)



    def undo(self):
        if not self.undo_stack or self.animation_time > 0:
            return
        self.engine.restore(self.undo_stack.pop())
        self.animations = []
        self.animation_time = 0.0
        self.merge_cells.clear()
        self.spawn_cell = None
        if self.state == "lost":
            self.state = "playing"



    def update(self, delta_time):
        if self.animation_time > 0:
            self.animation_time = max(0.0, self.animation_time - delta_time)
            if self.animation_time == 0:
                spawned = self.engine.add_random_tile()
                if spawned:
                    self.spawn_cell = (spawned[0], spawned[1])
                    self.spawn_time = SPAWN_ANIM_TIME
                self.merge_time = MERGE_POP_TIME
                if any(v >= 2048 for row in self.engine.board for v in row) and not self.won:
                    self.won, self.state = True, "won"
                elif not self.engine.can_move():
                    self.state = "lost"
                    self.settings.submit_score(self.engine.score)
                    self.best_score = self.settings.data["best_score"]

        self.spawn_time = max(0.0, self.spawn_time - delta_time)
        self.merge_time = max(0.0, self.merge_time - delta_time)
        if self.merge_time == 0:
            self.merge_cells.clear()

        if self.engine.score > self.best_score:
            self.best_score = self.engine.score
            self.settings.data["best_score"] = self.best_score
            self.settings.save()

        target = self.engine.score
        if self.displayed_score < target:
            step = max(1.0, (target - self.displayed_score) * 0.2)
            self.displayed_score = min(target, self.displayed_score + step)

    # ---- input ---------



    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.state == "start":
                if self.action_button.collidepoint(pos):
                    self.start_game()
                elif self.leaderboard_button.collidepoint(pos):
                    self.state = "leaderboard"
                elif self.theme_button.collidepoint(pos):
                    self.toggle_theme()
                elif self.sound_button.collidepoint(pos):
                    self.toggle_sound()
            elif self.state == "leaderboard":
                if self.back_button.collidepoint(pos):
                    self.state = "start"
            elif self.state == "paused":
                if self.action_button.collidepoint(pos):
                    self.state = self.previous_state_before_pause
            elif self.state in ("playing", "won", "lost"):
                if self.restart_button.collidepoint(pos):
                    self.start_game()
                elif self.undo_button.collidepoint(pos):
                    self.undo()
                elif self.theme_button.collidepoint(pos):
                    self.toggle_theme()
                elif self.sound_button.collidepoint(pos):
                    self.toggle_sound()
                elif self.state == "lost" and self.action_button.collidepoint(pos):
                    self.start_game()
                elif self.state == "won" and self.action_button.collidepoint(pos):
                    self.state = "playing"
            return True

        if event.type != pygame.KEYDOWN:
            return True

        if event.key == pygame.K_ESCAPE:
            if self.state == "playing":
                self.previous_state_before_pause = self.state
                self.state = "paused"
            elif self.state == "paused":
                self.state = self.previous_state_before_pause
            elif self.state == "start":
                return False
            else:
                self.state = "start"
            return True

        if self.state == "start" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.start_game()
        elif self.state == "leaderboard" and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_BACKSPACE):
            self.state = "playing"
        elif self.state == "paused" and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_p):
            self.state = self.previous_state_before_pause
        elif self.state == "lost" and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
            self.start_game()
        elif self.state == "won" and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.state = "playing"
        elif self.state in ("playing", "won"):
            if event.key == pygame.K_r:
                self.start_game()
            elif event.key == pygame.K_p:
                self.previous_state_before_pause = self.state
                self.state = "paused"
            elif event.key in (pygame.K_u, pygame.K_z):
                self.undo()
            elif event.key == pygame.K_t:
                self.toggle_theme()
            elif event.key == pygame.K_m:
                self.toggle_sound()
            else:
                directions = {
                    pygame.K_LEFT: "left", pygame.K_a: "left",
                    pygame.K_RIGHT: "right", pygame.K_d: "right",
                    pygame.K_UP: "up", pygame.K_w: "up",
                    pygame.K_DOWN: "down", pygame.K_s: "down",
                }
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
    BlockRush2048().run()
