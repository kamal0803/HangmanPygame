import re
import random
import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
width, height = 800, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman")
font = pygame.font.Font('freesansbold.ttf', 32)

# Set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (167, 237, 231)
PINK = (243, 21, 89)

# Set up the circle parameters
radius = 20

x1 = (200, 400)  # (x, y) coordinates of the starting point
y1 = (225, 400)  # (x, y) coordinates of the ending point

words = ["elephant", "sunshine", "rainbow", "guitar", "pizza", "galaxy", "chocolate", "fame", "mountain",
         "butterfly", "adventure"]

x = 25
actual_word = random.choice(words).upper()
word_len = len(actual_word)
step = 25
is_game_over = you_won = False
coordinates = [x1] + [(x1[0] + (i * step), x1[1]) for i in range(1, 2*word_len)]

alphabets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z"]

hangman_pics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'),
                pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'),
                pygame.image.load('hangman6.png')]


chances_left = 6
guessed_letters = []
center = []

x = 0
for k in range(len(alphabets)):
    if k < 13:
        x_coordinate = x + 30
        center.append((x_coordinate, 100))
    elif k == 13:
        x = 0
        x_coordinate = x + 30
        center.append((x_coordinate, 150))
    else:
        x_coordinate = x + 30
        center.append((x_coordinate, 150))
    x = x + 60

blits_sequence = []
font_size = 58
font = pygame.font.Font(None, font_size)

text_width = 28
text_height = 40

positions = []

guessed_letters = []
counter = ["-"]*word_len

# Game loop
running = True
while running:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black color
    screen.fill(GREEN)

    for i in range(0, len(coordinates), 2):
        pygame.draw.line(screen, (255, 0, 0), coordinates[i], coordinates[i+1], 5)

    for i in range(len(alphabets)):
        pygame.draw.circle(screen, BLUE, center[i], radius)
        text_surface = font.render(alphabets[i], True, BLACK)
        text_x = center[i][0] - text_width // 2
        text_y = center[i][1] - text_height // 2
        screen.blit(text_surface, (text_x, text_y))

    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()

        if pos not in positions:
            positions.append(pos)

        for c in range(len(center)):

            if abs(pos[0] - center[c][0]) <= 20 and abs(pos[1] - center[c][1]) <= 20:

                if alphabets[c] not in guessed_letters:
                    guessed_letters.append(alphabets[c])

                    if alphabets[c] not in actual_word:
                        chances_left = chances_left - 1

                    else:
                        for m in re.finditer(alphabets[c], actual_word):
                            idx = m.start()
                            counter[idx] = alphabets[c]
                            letter_text = font.render(alphabets[c], True, PINK)
                            blits_sequence.append((letter_text, (coordinates[idx*2][0], 360)))

    screen.blits(blits_sequence)
    b_img = pygame.transform.scale(hangman_pics[6 - chances_left], (200, 200))
    screen.blit(b_img, (300, 180))

    chances_display = font.render(f"Chances left: {chances_left}", True, WHITE)
    screen.blit(chances_display, (0, 0))

    guessed_word = ''.join(map(str, counter))

    if guessed_word == actual_word and chances_left >= 0:
        game_over_timer = pygame.time.get_ticks()
        you_won = is_game_over = True

    elif chances_left <= 0:
        game_over_timer = pygame.time.get_ticks()
        is_game_over = True
        you_won = False

    if is_game_over:

        screen.fill(GREEN)
        font = pygame.font.Font('freesansbold.ttf', 26)

        if you_won:
            winning_text = font.render(f"YOU WON!!", True, WHITE)
            screen.blit(winning_text, (100, 200))
        else:
            losing_text = font.render(f"YOU LOST!! The correct word is {actual_word}", True, WHITE)
            screen.blit(losing_text, (100, 200))

        if pygame.time.get_ticks() - game_over_timer > 10000:
            running = False

    pygame.display.update()

pygame.quit()
