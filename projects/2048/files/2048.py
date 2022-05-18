import os
import pygame
import random
import sys
from math import *
import text
from pygame.locals import *

pygame.init()

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 30
ICON = pygame.image.load('icon.png').convert_alpha()
ICON = pygame.transform.scale(ICON, (32, 32))

pygame.display.set_icon(ICON)
pygame.display.set_caption('2048')

####------Colours------####
TILECOLOUR = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (236, 141, 84),
    32: (246, 124, 95),
    64: (234, 89, 55),
    128: (243, 216, 107),
    256: (241, 208, 75),
    512: (238, 202, 82),
    1024: (226, 186, 19),
    2048: (236, 196, 0)
}

TEXTLIGHT = (255, 247, 247)
TEXTDARK = (119, 110, 101)

BACKGROUND = (250, 248, 239)
BOARDBACK = (187, 173, 160)
TILEBACK = (204, 192, 180)
####-------------------####

# Define variables for the game workings
# These are defined up here so they can be used in other functions

tiles = 0

pressed = [0, 0, 0, 0]
mouse_down = False
won = False

score = 0

# Creates a list with all the different possible values a tile can have
values = [2 ** x for x in range(1, 12)]

# Generate text to display on tiles
tile_text = [text.Text(text=str(value), size=35, colour=TEXTLIGHT, font='Helvetica Neue', anchor='center')
             for value in values]

# Read the current highscore from a file
with open('High Score.txt', 'r') as f:
    highscore = int(f.read())


def draw_rounded_rect(rect, radius, colour, surface=SCREEN):
    """
    Can draw a rectangle with corners that are rounded to a given radius
    :param (int, int, int, int) rect: The coordinates of the shape (x, y, width, height)
    :param int radius: The radius of the corners
    :param (int, int, int) colour: The colour of the shape
    :param Surface surface: The surface to draw the shape to
    :return: None
    """
    pointlist = ((rect[0] + radius, rect[1]), (rect[0] + rect[2] - radius, rect[1]), (rect[0] + rect[2], rect[1] + radius),
                 (rect[0] + rect[2], rect[1] + rect[3] - radius), (rect[0] + rect[2] - radius, rect[1] + rect[3]),
                 (rect[0] + radius, rect[1] + rect[3]), (rect[0], rect[1] + rect[3] - radius), (rect[0], rect[1] + radius))
    pygame.draw.polygon(surface, colour, pointlist)

    for point in ((rect[0] + radius, rect[1] + radius), (rect[0] + rect[2] - radius, rect[1] + radius),
                  (rect[0] + rect[2] - radius, rect[1] + rect[3] - radius),
                  (rect[0] + radius, rect[1] + rect[3] - radius)):
        pygame.draw.circle(surface, colour, point, radius)


def transpose(array):
    """
    Transposes an array
    :param array: The array to be transposed
    :return: Transposed array
    """
    new_array = []
    for _ in array[0]:
        new_array.append([])

    for row in array:
        for i, item in enumerate(row):
            new_array[i].append(item)

    return new_array


def add_tile():
    # Choose whether new tile will be a 2 (80% chance) or a 4 (20% chance)
    if random.random() <= 0.8:
        value = 2
    else:
        value = 4

    # Tests to see if there are any spaces to put a new tile in    
    has_zero = False
    for row in tiles:
        for item in row:
            if item == 0:
                has_zero = True

    if not has_zero:
        return

    # If there are available spaces then place a tile in one
    while True:
        # Chooses a random position on the board
        pos = [random.randint(0, 3) for i in range(2)]

        # If the position is empty then place a new tile
        if tiles[pos[1]][pos[0]] == 0:
            tiles[pos[1]][pos[0]] = value
            break

        else:
            continue


def slide():
    global tiles, pressed, score
    keys = pygame.key.get_pressed()
    moved = False

    if (keys[K_a] or keys[K_LEFT]) and not pressed[0]:
        pressed[0] = 1

        for i, row in enumerate(tiles):
            new_row = tiles[i].copy()
            position = 0
            for value in row:
                if value != 0:
                    if position != 0:
                        if new_row[position] == new_row[position - 1]:
                            new_row[position - 1] *= 2
                            new_row[position] = 0

                            new_row.append(new_row.pop(position))

                            score += new_row[position - 1]

                    position += 1

                else:
                    new_row.append(new_row.pop(position))

            if new_row != tiles[i]:
                tiles[i] = new_row
                moved = True

    elif (keys[K_d] or keys[K_RIGHT]) and not pressed[1]:
        pressed[1] = 1

        for i, row in enumerate(tiles):
            new_row = tiles[i].copy()
            position = 3
            for value in row[::-1]:
                if value != 0:
                    if position != 3:
                        if new_row[position] == new_row[position + 1]:
                            new_row[position + 1] *= 2
                            new_row[position] = 0

                            new_row.insert(0, new_row.pop(position))

                            score += new_row[position + 1]

                    position -= 1

                else:
                    new_row.insert(0, new_row.pop(position))

            if new_row != tiles[i]:
                tiles[i] = new_row
                moved = True

    elif (keys[K_w] or keys[K_UP]) and not pressed[2]:
        pressed[2] = 1

        vtiles = transpose(tiles)

        for i, row in enumerate(vtiles):
            new_row = vtiles[i].copy()
            position = 0
            for value in row:
                if value != 0:
                    if position != 0:
                        if new_row[position] == new_row[position - 1]:
                            new_row[position - 1] *= 2
                            new_row[position] = 0

                            new_row.append(new_row.pop(position))

                            score += new_row[position - 1]

                    position += 1

                else:
                    new_row.append(new_row.pop(position))

            if new_row != vtiles[i]:
                vtiles[i] = new_row
                moved = True

        tiles = transpose(vtiles)

    elif (keys[K_s] or keys[K_DOWN]) and not pressed[3]:
        pressed[3] = 1

        vtiles = transpose(tiles)

        for i, row in enumerate(vtiles):
            new_row = vtiles[i].copy()
            position = 3
            for value in row[::-1]:
                if value != 0:
                    if position != 3:
                        if new_row[position] == new_row[position + 1]:
                            new_row[position + 1] *= 2
                            new_row[position] = 0

                            new_row.insert(0, new_row.pop(position))

                            score += new_row[position + 1]

                    position -= 1

                else:
                    new_row.insert(0, new_row.pop(position))

            if new_row != vtiles[i]:
                vtiles[i] = new_row
                moved = True

        tiles = transpose(vtiles)

    pressed = [(keys[K_a] or keys[K_LEFT]), (keys[K_d] or keys[K_RIGHT]), (keys[K_w] or keys[K_UP]),
               (keys[K_s] or keys[K_DOWN])]

    return moved


def check_win():
    for row in tiles:
        for item in row:
            if item == 2048:
                return True

    return False


def draw_background():
    # Add the background colour
    SCREEN.fill(BACKGROUND)

    # Draw the 2048 logo
    tile_text[10].update_settings(size=75, position=(125, 150))

    draw_rounded_rect((25, 50, 200, 200), 10, TILECOLOUR[2048])
    tile_text[10].render(SCREEN)

    tile_text[10].update_settings(size=35)


def new_game():
    global score, tiles, won
    # Reset variables to their defaults
    score = 0
    won = False

    tiles = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    # Add two new tiles
    for i in range(2): add_tile()


def are_you_sure():
    '''Generates an 'Are You Sure' textbox'''
    # Generates pop-up text
    sure_text = text.Text((400, 270), 'ARE YOU SURE?', TEXTDARK, 40, 'Helvetica Neue', 'center')
    yes_text = text.Text((300, 340), 'YES', TEXTLIGHT, 30, 'Helvetica Neue', 'center')
    no_text = text.Text((500, 340), 'NO', TEXTLIGHT, 30, 'Helvetica Neue', 'center')

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Draws pop-up background
        draw_rounded_rect((200, 200, 400, 200), 20, TILECOLOUR[8])
        draw_rounded_rect((210, 210, 380, 180), 10, TILECOLOUR[4])

        # Draws buttons and text on pop-up
        sure_text.render(SCREEN)

        if 250 < mouse_pos[0] < 350 and 311 < mouse_pos[1] < 371:
            draw_rounded_rect((250, 311, 100, 60), 7, TILECOLOUR[8])

            if mouse_pressed[0] and not mouse_down:
                return True

        else:
            draw_rounded_rect((250, 311, 100, 60), 7, TILECOLOUR[16])

        if 450 < mouse_pos[0] < 550 and 311 < mouse_pos[1] < 371:
            draw_rounded_rect((450, 311, 100, 60), 7, TILECOLOUR[8])

            if mouse_pressed[0] and not mouse_down:
                return False

        else:
            draw_rounded_rect((450, 311, 100, 60), 7, TILECOLOUR[16])

        mouse_down = mouse_pressed[0]

        yes_text.render()
        no_text.render()

        # Exits the environment
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(FPS)


def main():
    global highscore, tiles, won

    # Change the settings for each of the different tile texts
    for i in range(2):
        tile_text[i].update_settings(size=70, colour=TEXTDARK)

    tile_text[2].update_settings(size=70)

    for i in range(3, 6):
        tile_text[i].update_settings(size=60)

    for i in range(6, 9):
        tile_text[i].update_settings(size=45)

    # Generate menu text
    score_text = [text.Text(position, text_str, colour, size, 'Helvetica Neue', 'center') for
                  text_str, position, size, colour in
                  [('SCORE', (70, 295), 20, TILECOLOUR[2]), (str(score), (70, 323), 30, TEXTLIGHT)]]
    best_text = [text.Text(position, text_str, colour, size, 'Helvetica Neue', 'center') for
                 text_str, position, size, colour in
                 [('BEST', (180, 295), 20, TILECOLOUR[2]), (str(highscore), (180, 323), 30, TEXTLIGHT)]]
    new_game_text = text.Text((125, 384), 'NEW GAME', TEXTLIGHT, 18, 'Helvetica Neue', 'center')
    reset_text = text.Text((125, 424), 'RESET HIGH SCORE', TEXTLIGHT, 18, 'Helvetica Neue', 'center')
    win_text = text.Text((525, 240), 'WELL DONE', TEXTLIGHT, 35, 'Helvetica Neue', 'center')

    new_game()
    draw_background()

    while True:
        render = True
        reset_highscore = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if not won:
            # Draw menu icons
            draw_rounded_rect((25, 275, 90, 70), 7, TILEBACK)
            draw_rounded_rect((135, 275, 90, 70), 7, TILEBACK)

            if 25 < mouse_pos[0] < 225:
                if 370 < mouse_pos[1] < 400:
                    draw_rounded_rect((25, 370, 200, 30), 7, TILECOLOUR[8])

                    if mouse_pressed[0] and not mouse_down:
                        # Render text on the menu icons so they show with pop-up
                        draw_rounded_rect((25, 370, 200, 30), 7, TILECOLOUR[16])

                        score_text[1].set_text(str(score))
                        for text_obj in score_text:
                            text_obj.render()

                        best_text[1].set_text(str(highscore))
                        for text_obj in best_text:
                            text_obj.render()

                        new_game_text.render((125, 384))

                        # Create pop-up
                        if are_you_sure():
                            new_game()

                        draw_background()

                        render = False
                        mouse_down = True

                else:
                    draw_rounded_rect((25, 370, 200, 30), 7, TILECOLOUR[16])

                if 410 < mouse_pos[1] < 440:
                    draw_rounded_rect((25, 410, 200, 30), 7, TILECOLOUR[8])

                    if mouse_pressed[0] and not mouse_down:
                        # Render text on the menu icons so they show with pop-up
                        draw_rounded_rect((25, 410, 200, 30), 7, TILECOLOUR[16])

                        score_text[1].set_text(str(score))
                        for text_obj in score_text:
                            text_obj.render()

                        best_text[1].set_text(str(highscore))
                        for text_obj in best_text:
                            text_obj.render()

                        new_game_text.render()
                        reset_text.render()

                        # Create pop-up
                        if are_you_sure():
                            reset_highscore = True

                        draw_background()

                        render = False
                        mouse_down = True

                else:
                    draw_rounded_rect((25, 410, 200, 30), 7, TILECOLOUR[16])

            else:
                draw_rounded_rect((25, 370, 200, 30), 7, TILECOLOUR[16])
                draw_rounded_rect((25, 410, 200, 30), 7, TILECOLOUR[16])

            # Draw game board
            draw_rounded_rect((250, 50, 500, 500), 10, BOARDBACK)

            for y in range(50 + 16, 550 - 16, 105 + 16):
                for x in range(250 + 16, 750 - 16, 105 + 16):
                    draw_rounded_rect((x, y, 105, 105), 7, TILEBACK)

            # Allows the user to make a move, and adds a new tile if a move is made
            if slide(): add_tile()

            # Draw tiles
            for y, row in enumerate(tiles):
                for x, value in enumerate(row):
                    if value != 0:
                        draw_rounded_rect((266 + 121 * x, 66 + 121 * y, 105, 105), 7, TILECOLOUR[value])

                        tile_text[int(log(value, 2) - 1)].update_settings(position=(319 + 121 * x, 117 + 121 * y))
                        tile_text[int(log(value, 2) - 1)].render(SCREEN)

            # Render text on the menu icons
            score_text[1].set_text(str(score))
            for text_obj in score_text:
                text_obj.render(SCREEN)

            best_text[1].set_text(str(highscore))
            for text_obj in best_text:
                text_obj.render(SCREEN)

            new_game_text.render(SCREEN)
            reset_text.render(SCREEN)

            # Updates the highscore and writes to file
            if score > highscore or reset_highscore:
                highscore = score

                try:
                    f = open('High Score.txt', 'w')
                    f.write(str(highscore))

                finally:
                    f.close()

            # Change size of score text so it can still fit in the box
            score_text[1].update_settings(size=30 - 2 * len(str(score)))
            best_text[1].update_settings(size=30 - 2 * len(str(highscore)))

        # Tests for win condition
        if check_win():
            if not won:
                for i in range(30):
                    pygame.display.update()
                    CLOCK.tick(FPS)

                won = True

            SCREEN.fill(BACKGROUND)

            # Draw logo    
            draw_rounded_rect((125, 200, 200, 200), 10, TILECOLOUR[2048])

            tile_text[10].update_settings(size=75)
            tile_text[10].render((225, 300))

            # Draw well done text
            draw_rounded_rect((375, 200, 300, 120), 10, TILEBACK)
            win_text.render()

            # Draw the score text
            score_text[0].update_settings((460, 285), size=35)
            score_text[1].update_settings((610, 285), size=35)
            for text_obj in score_text:
                text_obj.render()

            # Return the score text to its original position
            score_text[0].update_settings((70, 295), True, 20)
            score_text[1].update_settings((70, 323), True, 30)

            # Draw new game button
            if 375 < mouse_pos[0] < 675 and 340 < mouse_pos[1] < 400:
                draw_rounded_rect((375, 340, 300, 60), 10, TILECOLOUR[8])

                if mouse_pressed[0] and not mouse_down:
                    new_game()
                    draw_background()

                    mouse_down = True
            else:
                draw_rounded_rect((375, 340, 300, 60), 10, TILECOLOUR[16])

            # Draw the new game text
            new_game_text.update_settings(size=35)
            new_game_text.render((525, 370))

            # Return the new game text to its original size
            new_game_text.update_settings(size=18)

        mouse_down = mouse_pressed[0]

        # Exits the environment
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        if render:
            pygame.display.update()
            CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
