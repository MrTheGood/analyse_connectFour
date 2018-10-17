import pygame


def draw_board():
    return


COLUMN_COUNT = 7
ROW_COUNT = 6
CIRCLE_SIZE = 50
CIRCLE_MARGIN = 20
CIRCLE_COLOUR = (255, 255, 255)
POS_MULTIPLIER = CIRCLE_SIZE + CIRCLE_MARGIN

pygame.init()
screen = pygame.display.set_mode((POS_MULTIPLIER * COLUMN_COUNT, POS_MULTIPLIER * ROW_COUNT))
screen.fill((128, 0, 0))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()

    for x in range(0, COLUMN_COUNT):
        for y in range(0, ROW_COUNT):
            pygame.draw.circle(screen, CIRCLE_COLOUR,
                               (int(POS_MULTIPLIER * x + POS_MULTIPLIER / 2),
                                int(POS_MULTIPLIER * y + POS_MULTIPLIER / 2)),
                               int(CIRCLE_SIZE / 2)
                               )
