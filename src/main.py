import math
import random

import pygame

pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
GAME_OVER_COLOR = (119, 110, 101)
GAME_OVER_TEXT_COLOR = (249, 246, 242)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 80, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


class Tile:
    COLORS = {
        2: (237, 229, 218),
        4: (238, 225, 201),
        8: (243, 178, 122),
        16: (246, 150, 101),
        32: (247, 124, 95),
        64: (247, 95, 59),
        128: (237, 208, 115),
        256: (237, 204, 99),
        512: (237, 202, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
    }

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        return self.COLORS.get(self.value, (60, 58, 50))

    def draw(self, window):
        pygame.draw.rect(window, self.get_color(), (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))
        text = FONT.render(str(self.value), True, FONT_COLOR)
        window.blit(text, (self.x + (RECT_WIDTH - text.get_width()) // 2,
                           self.y + (RECT_HEIGHT - text.get_height()) // 2))

    def set_pos(self, use_ceil=False):
        if use_ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        pygame.draw.line(window, OUTLINE_COLOR, (0, row * RECT_HEIGHT), (WIDTH, row * RECT_HEIGHT), OUTLINE_THICKNESS)
    for col in range(1, COLS):
        pygame.draw.line(window, OUTLINE_COLOR, (col * RECT_WIDTH, 0), (col * RECT_WIDTH, HEIGHT), OUTLINE_THICKNESS)
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles, lost=False):
    window.fill(BACKGROUND_COLOR)
    for tile in tiles.values():
        tile.draw(window)
    draw_grid(window)
    if lost:
        draw_game_over(window)
    pygame.display.update()


def draw_game_over(window):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((*GAME_OVER_COLOR, 150))
    window.blit(overlay, (0, 0))
    text = GAME_OVER_FONT.render("Game Over", True, GAME_OVER_TEXT_COLOR)
    window.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))


def get_random_pos(tiles):
    while True:
        row, col = random.randrange(ROWS), random.randrange(COLS)
        if (row, col) not in tiles:
            return row, col


def can_merge(tiles):
    for row in range(ROWS):
        for col in range(COLS):
            tile = tiles.get((row, col))
            if not tile:
                return True
            right_tile = tiles.get((row, col + 1))
            down_tile = tiles.get((row + 1, col))
            if right_tile and tile.value == right_tile.value:
                return True
            if down_tile and tile.value == down_tile.value:
                return True
    return False


def is_game_over(tiles):
    return len(tiles) == ROWS * COLS and not can_merge(tiles)


def get_board_state(tiles):
    return {position: tile.value for position, tile in tiles.items()}


def move_tiles(window, direction, tiles, clock):
    previous_state = get_board_state(tiles)
    updated, merged_tiles = True, set()
    if direction == "left":
        sort_func, reverse, delta, boundary_check = lambda tile: tile.col, False, (-MOVE_VEL, 0), lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get((tile.row, tile.col - 1))
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check, use_ceil = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL, True
    elif direction == "right":
        sort_func, reverse, delta, boundary_check = lambda tile: tile.col, True, (MOVE_VEL, 0), lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get((tile.row, tile.col + 1))
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check, use_ceil = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x, False
    elif direction == "up":
        sort_func, reverse, delta, boundary_check = lambda tile: tile.row, False, (0, -MOVE_VEL), lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get((tile.row - 1, tile.col))
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check, use_ceil = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL, True
    elif direction == "down":
        sort_func, reverse, delta, boundary_check = lambda tile: tile.row, True, (0, MOVE_VEL), lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get((tile.row + 1, tile.col))
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check, use_ceil = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y, False
    else:
        return "continue"

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)
        for index, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue
            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value == next_tile.value and tile not in merged_tiles and next_tile not in merged_tiles:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(index)
                    merged_tiles.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue
            tile.set_pos(use_ceil)
            updated = True
        update_tiles(window, tiles, sorted_tiles)
    if get_board_state(tiles) == previous_state:
        return "lost" if is_game_over(tiles) else "continue"
    return end_move(tiles)


def end_move(tiles):
    if is_game_over(tiles):
        return "lost"
    row, col = get_random_pos(tiles)
    tiles[(row, col)] = Tile(random.choice([2, 4]), row, col)
    return "lost" if is_game_over(tiles) else "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[(tile.row, tile.col)] = tile
    draw(window, tiles)


def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[(row, col)] = Tile(2, row, col)
    return tiles


def main(window):
    clock = pygame.time.Clock()
    run, lost, tiles = True, False, generate_tiles()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN and not lost:
                directions = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_UP: "up", pygame.K_DOWN: "down"}
                if event.key in directions:
                    lost = move_tiles(window, directions[event.key], tiles, clock) == "lost"
        draw(window, tiles, lost)
    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
