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
import math

import pygame

BACKGROUND_COLOR = (27, 109, 167)
FPS = 4
CURRENT_PLAYER = 1


def num_input(text, min, max):
    print(text)
    inp = input()
    while not inp.isdigit() or int(inp) < min or int(inp) > max:
        print("Invalid input! Should be a number with a min value of", min, "and max", max)
        print(text)
        inp = input()
    return int(inp)


def bool_input(text, true, false):
    print(text)
    inp = input()
    while not (inp == true or inp == false):
        print("Invalid input! Possible options: ", true, false)
        print(text)
        inp = input()
    return inp == true


COLUMN_COUNT = num_input("How many columns? (default 7)", 2, 20)
ROW_COUNT = num_input("How many rows? (default 6)", 2, 20)
SIZE = SCREENWIDTH, SCREENHEIGHT = 60 + 65 * COLUMN_COUNT, 60 + 65 * ROW_COUNT

WIN_CONDITION = num_input("How many in a row to win? (default 4)", 1,
                          COLUMN_COUNT if (COLUMN_COUNT > ROW_COUNT) else ROW_COUNT)
PLAYER_COUNT = num_input("How many players? (default 2)", 2, 7)
PLAYERS = []


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
            pygame.image.load("assets/sprites/yellow.png"),
            pygame.image.load("assets/sprites/green.png"),
            pygame.image.load("assets/sprites/cyan.png"),
            pygame.image.load("assets/sprites/orange.png"),
            pygame.image.load("assets/sprites/pink.png"),
            pygame.image.load("assets/sprites/purple.png")
        ]
        self.player = 0
        self.image = self.images[self.player]
        self.rect = self.image.get_rect()
        self.rect.move_ip(
            pos_multiplier * x + pos_multiplier / 2,
            pos_multiplier * y + pos_multiplier / 2
        )

    def set_player(self, p):
        global CURRENT_PLAYER, PLAYERS
        if p in range(0, len(self.images)):
            self.player = p
            self.image = self.images[self.player]
            check_win(self)
            CURRENT_PLAYER = (CURRENT_PLAYER % PLAYER_COUNT) + 1
            print("Next turn: Player ", CURRENT_PLAYER)
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
                break


class Player:
    def __init__(self, p):
        self.p = p

    def move(self):
        """Default Player implementation does nothing. Moving is handled by the on click events."""
        return


class HumanPlayer(Player):
    """Uses default implementations"""

    def move(self):
        print(".")


MINIMAX_LOOK_AHEAD = 6


class MinimaxAIPlayer(Player):

    def __init__(self, p):
        global GAME_BOARD
        super().__init__(p)
        self.board = [{"x": t.x, "y": t.y, "player": t.player} for t in GAME_BOARD]

    def move(self):
        """Uses a Minimax Search algorithm to decide HOW TO BEST OVERTHROW STUPID INFERIOR HUMANS IN THE ULTIMATE GAME OF CONNECTFOUR"""
        global GAME_BOARD, MINIMAX_LOOK_AHEAD
        tile = [t for t in GAME_BOARD if t.y == (self.minimax(MINIMAX_LOOK_AHEAD, self.p)[1])][0]
        print("Computer", self.p, "chose tile", tile.y)
        tile.on_click()

    def minimax(self, look_ahead, player):
        global PLAYER_COUNT
        next_moves = self.generate_moves()

        best_score = -math.inf if player == self.p else math.inf
        best_x = -1

        if not next_moves or look_ahead == 0:
            best_score = self.evaluate()
        else:
            for move in next_moves:
                self.find_tile(lambda t: t["x"] == move["x"] and t["y"] == move["y"])[
                    "player"] = player
                if player == self.p:
                    # maximizing player
                    current_score = self.minimax(look_ahead - 1, (player + 1) % PLAYER_COUNT)[0]
                    if current_score > best_score:
                        best_score = current_score
                        best_x = move["x"]
                else:
                    # minimizing player
                    current_score = self.minimax(look_ahead - 1, (player + 1) % PLAYER_COUNT)[0]
                    if current_score < best_score:
                        best_score = current_score
                        best_x = move["x"]
                # undo move
                self.find_tile(lambda t: t["x"] == move["x"] and t["y"] == move["y"])["player"] = 0
        return best_score, best_x

    def find_tile(self, cond):
        return [t for t in self.board if cond(t)][0]

    def generate_moves(self):
        global ROW_COUNT
        moves = []
        for y in range(ROW_COUNT - 1, -1, -1):
            moves.append(self.find_tile(
                lambda t: t["y"] == y and t["player"] == 0
            ))
            return moves

    def evaluate(self):
        global ROW_COUNT
        score = 0
        for tile in self.board:
            if tile["x"] == 0:
                score = score + self.evaluate_row([t for t in self.board if t["y"] == tile["y"]])
                score = score + self.evaluate_row(
                    [t for t in self.board if t["y"] + t["x"] == tile["y"] + tile["x"]])
                score = score + self.evaluate_row(
                    [t for t in self.board if t["y"] - t["x"] == tile["y"] - tile["x"]])
            elif tile["y"] == 0:
                score = score + self.evaluate_row([t for t in self.board if t["x"] == tile["x"]])
                score = score + self.evaluate_row(
                    [t for t in self.board if t["y"] + t["x"] == tile["y"] + tile["x"]])
            elif tile["y"] == ROW_COUNT - 1:
                score = score + self.evaluate_row(
                    [t for t in self.board if t["y"] - t["x"] == tile["y"] - tile["x"]])
        return score

    def evaluate_row(self, row):
        """Note that this evaluation could be greatly improved and is just a prototype for now"""
        # TODO: Improve evaluation to keep in mind blocking, multiple opponents win conditions, etc
        global WIN_CONDITION
        # Don't count rows that don't matter
        if len(row) < WIN_CONDITION:
            return 0
        score = 0
        for t in row:
            if t["player"] == self.p:
                score = score + 10
            elif t["player"] == 0:
                score = score
            else:
                score = score - 10
        return score


def check_win(from_tile):
    # \
    check_win_row([t for t in GAME_BOARD if t.x + t.y == from_tile.x + from_tile.y])
    # /
    check_win_row([t for t in GAME_BOARD if t.x - t.y == from_tile.x - from_tile.y])
    # |
    check_win_row([t for t in GAME_BOARD if t.x == from_tile.x])
    # -
    check_win_row([t for t in GAME_BOARD if t.y == from_tile.y])


def check_win_row(tiles):
    x = 0
    for t in tiles:
        if t.player == CURRENT_PLAYER:
            x = x + 1
            if x >= WIN_CONDITION:
                print("Player", CURRENT_PLAYER, "has won! Congrats!")
                pygame.quit()
                quit()
        else:
            x = 0


def init_game_board():
    global GAME_BOARD, COLUMN_COUNT, ROW_COUNT, PLAYERS
    GAME_BOARD = pygame.sprite.Group(
        Tile(x=x, y=y) for x in range(0, COLUMN_COUNT) for y in range(0, ROW_COUNT)
    )

    for i in range(0, PLAYER_COUNT):
        if bool_input("Is this player a computer or human?", "computer", "human"):
            PLAYERS.append(MinimaxAIPlayer(i))
        else:
            PLAYERS.append(HumanPlayer(i))

    print("First turn: Player 1")
    PLAYERS[0].move()


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
                if isinstance(PLAYERS[CURRENT_PLAYER - 1], HumanPlayer):
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
        PLAYERS[CURRENT_PLAYER - 1].move()


if __name__ == '__main__':
    main()
