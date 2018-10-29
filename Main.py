#    Maarten de Goede  0966770
#    Copyright 2018 Maarten de Goede
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import pygame

SIZE = SCREENWIDTH, SCREENHEIGHT = 505, 440
BACKGROUND_COLOR = (27, 109, 167)
FPS = 4
CURRENT_PLAYER = 1
MAX_PLAYERS = 2


class Tile(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):

        circle_size = 50
        circle_margin = 15
        pos_multiplier = circle_size + circle_margin
        self.x = x
        self.y = y

        super().__init__(*groups)
        self.images = [
            pygame.image.load("assets/sprites/white.png"),
            pygame.image.load("assets/sprites/red.png"),
            pygame.image.load("assets/sprites/yellow.png")
        ]
        self.player = 0
        self.image = self.images[self.player]
        self.rect = self.image.get_rect()
        self.rect.move_ip(
            pos_multiplier * x + pos_multiplier / 2,
            pos_multiplier * y + pos_multiplier / 2
        )

    def set_player(self, p):
        if p in range(0, len(self.images)):
            self.player = p
            self.image = self.images[self.player]
        else:
            raise ValueError("Unexpected value type: " + type(p))

    def update(self, *args):
        super().update(*args)

    def on_click(self):
        global CURRENT_PLAYER, ROW_COUNT
        for y in range(ROW_COUNT - 1, -1, -1):
            tile = get_tile_by_pos(self.x, y)
            if tile.player == 0:
                tile.set_player(CURRENT_PLAYER)

                # \
                check_win([t for t in GAME_BOARD if t.x + t.y == tile.x + tile.y])
                # /
                check_win([t for t in GAME_BOARD if t.x - t.y == tile.x - tile.y])
                # |
                check_win([t for t in GAME_BOARD if t.x == tile.x])
                # -
                check_win([t for t in GAME_BOARD if t.y == tile.y])

                CURRENT_PLAYER = (CURRENT_PLAYER % MAX_PLAYERS) + 1
                print("Next turn: Player ", CURRENT_PLAYER)
                break


def check_win(tiles):
    x = 0
    for t in tiles:
        if t.player == CURRENT_PLAYER:
            x = x + 1
            if x >= 4:
                print("Player", CURRENT_PLAYER, "has won! Congrats!")
                pygame.quit()
                quit()
        else:
            x = 0


def init_game_board():
    global GAME_BOARD, COLUMN_COUNT, ROW_COUNT
    COLUMN_COUNT = 7
    ROW_COUNT = 6

    GAME_BOARD = pygame.sprite.Group(
        Tile(x=x, y=y) for x in range(0, COLUMN_COUNT) for y in range(0, ROW_COUNT)
    )
    print("First turn: Player 1")


def get_tile_by_x(x):
    return [tile for tile in GAME_BOARD if tile.x == x]


def get_tile_by_y(y):
    return [tile for tile in GAME_BOARD if tile.y == y]


def get_tile_by_pos(x, y):
    return [tile for tile in GAME_BOARD if tile.y == y and tile.x == x][0]


def main():
    global SCREEN, FPS_CLOCK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode(SIZE)
    init_game_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                [s.on_click() for s in GAME_BOARD if s.rect.collidepoint(pos)]
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break

        SCREEN.fill(BACKGROUND_COLOR)
        GAME_BOARD.draw(SCREEN)
        GAME_BOARD.update()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
