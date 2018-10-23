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

SIZE = SCREENWIDTH, SCREENHEIGHT = 600, 400
BACKGROUND_COLOR = (125, 125, 255)
FPS = 4


class Tile(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y):
        super().__init__(*groups)
        self.images = [
            pygame.image.load("assets/sprites/white.png"),
            pygame.image.load("assets/sprites/red.png"),
            pygame.image.load("assets/sprites/yellow.png")
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def set_player(self, p):
        if p in range(0, len(pygame.image)):
            self.index = p
            self.image = self.images[self.index]
        else:
            raise ValueError("Unexpected value type: " + type(p))

    def update(self, *args):
        super().update(*args)


def init_game_board():
    global GAME_BOARD
    column_count = 7
    row_count = 6
    circle_size = 50
    circle_margin = 15

    pos_multiplier = circle_size + circle_margin

    GAME_BOARD = pygame.sprite.Group(
        Tile(x=int(pos_multiplier * x + pos_multiplier / 2),
             y=int(pos_multiplier * y + pos_multiplier / 2))
        for x in range(0, column_count) for y in range(0, row_count)
    )


def main():
    global SCREEN, FPS_CLOCK
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode(SIZE)
    done = False
    init_game_board()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()

        SCREEN.fill(BACKGROUND_COLOR)
        GAME_BOARD.draw(SCREEN)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
