import pygame 
import sys
import os
import math
import random
hangman_status = 0
# set display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

#button variables
RADIUS = 20
GAP = 15 
letters = []
startx = round( (WIDTH - (RADIUS*2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x,y, chr(A + i), True])

#fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)


#load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

#game variabless
words = ["HOUSE", "PRESIDNET", "DAWN", "AVOCADO", "SUNSET", "TREEHOUSE", "MEAT", "COMPILER"]
word = random.choice(words)
guessed = []

#compile
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#setup game loop
FPS = 60   #speed of the games (frames per second)
clock = pygame.time.Clock()   #counts the time


def draw():
    win.fill(WHITE)
    #draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_" + " "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    #draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1 , BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    win.blit(images[hangman_status], (150,100))
    pygame.display.update()

def disaply_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE) 
    text = WORD_FONT.render(message, 1 ,BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def start_message():
    win.fill(WHITE)
    text = WORD_FONT.render("Click On Screen to Start", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    while True:
        # clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

def continue_message():
    win.fill(WHITE)
    text = WORD_FONT.render("Play Again?", 1, BLACK)
    POSTION_X, POSTION_Y= (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2)
    win.blit(text, (POSTION_X, POSTION_Y))

    pygame.draw.circle(win, BLACK, (int(POSTION_X+20),int(POSTION_X+100) ), 50, 6)
    text = LETTER_FONT.render("Yes", 1 , BLACK)
    POSTION_X1, POSTION_Y1 =  (int(POSTION_X+20) - text.get_width() / 2, int(POSTION_X+100) - text.get_height() / 2)
    win.blit(text,(POSTION_X1, POSTION_Y1))

    pygame.draw.circle(win, BLACK, (int(POSTION_X+220),int(POSTION_X+100)), 50, 6)
    text = LETTER_FONT.render("No", 1 , BLACK)
    POSTION_X2, POSTION_Y2 =  (int(POSTION_X1+220) - text.get_width() / 2, int(POSTION_X1+100) - text.get_height() / 2)
    win.blit(text,(POSTION_X2, POSTION_Y2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                dis_yes = math.sqrt((POSTION_X1 - m_x)**2 + (POSTION_Y1 - m_y)**2)
                if(dis_yes < 50):
                    return
                dis_no = math.sqrt((POSTION_X2 - m_x)**2 + (POSTION_Y2 - m_y)**2)
                if(dis_no < 50):
                   return 1
        

def main():
    #initalize parameters
    global hangman_status
    global guessed
    global word
    hangman_status = 0
    guessed = []
    word = random.choice(words)
    for ltr in letters:
        ltr[3] = True
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y , ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if(dis < RADIUS):
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw()
        
        won = True
        for letter in word:
            if letter not in guessed: 
                won = False
                break
        if won:
            disaply_message("You WON!")
            break

        if hangman_status == 6:
            disaply_message("You Lost")
            break
while True:
    start_message()
    main()
    ret = continue_message()
    if ret == 1:
        pygame.quit()
        sys.exit()