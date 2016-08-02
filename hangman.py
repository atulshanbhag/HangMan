try:
    import pygame
    from sys import exit
    from string import join
    from random import choice
    from os import chdir
    from pygame.locals import *
except ImportError:
    print 'Import Error!'
    exit()

try:
    chdir('data')
except OSError:
    print 'Data folder does not exist!'
    exit()

pygame.init()

FPS = 30
fps_clock = pygame.time.Clock()

WINDOWWIDTH = 640
WINDOWHEIGHT = 480


DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('HANGMAN')

try:
    ICON = pygame.image.load('hangman-icon.png')
except IOError:
    print 'Icon did not load!'
    pygame.quit()
    exit()

pygame.display.set_icon(ICON)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (83, 216, 255)
HIGHLIGHT = (30, 144, 255)
FONTSIZE = 60
WORDSIZE = 45

try:
    FONT_OBJ = pygame.font.Font('kanover.ttf', FONTSIZE)
except IOError:
    print 'Font did not load!'
    pygame.quit()
    exit()

TITLE = FONT_OBJ.render('Welcome to Hangman!', True, BLACK)
TITLE_RECT = TITLE.get_rect()
TITLE_RECT.center = (320, 50)

START = FONT_OBJ.render('Start', True, BLACK)
START_RECT = START.get_rect()
START_RECT.center = (200, 430)

EXIT = FONT_OBJ.render('Exit', True, BLACK)
EXIT_RECT = EXIT.get_rect()
EXIT_RECT.center = (440, 430)

try:
    HANG_IMG = pygame.image.load('hang.png')
    HANG_IMG_RECT = HANG_IMG.get_rect()
    HANG_IMG_RECT.center = (320, 240)
except IOError:
    print 'Hang image did not load!'
    pygame.quit()
    exit()

NUM_OF_IMAGES = 11
try:
    IMG = [pygame.image.load('%d.png' % (x,)) for x in xrange(NUM_OF_IMAGES)]
    IMG_RECT = [IMG[itr].get_rect() for itr in xrange(NUM_OF_IMAGES)]
    for itr in xrange(NUM_OF_IMAGES):
        IMG_RECT[itr].center = (320, 150)
except IOError:
    print 'Hang sequences did not load!'
    pygame.quit()
    exit()

KEY_MAP = {
    K_a: 'a', K_b: 'b', K_c: 'c',
    K_d: 'd', K_e: 'e', K_f: 'f',
    K_g: 'g', K_h: 'h', K_i: 'i',
    K_j: 'j', K_k: 'k', K_l: 'l',
    K_m: 'm', K_n: 'n', K_o: 'o',
    K_p: 'p', K_q: 'q', K_r: 'r',
    K_s: 's', K_t: 't', K_u: 'u',
    K_v: 'v', K_w: 'w', K_x: 'x',
    K_y: 'y', K_z: 'z', K_MINUS: '-'
}

try:
    GANGNAM = pygame.image.load('gangnam.png')
    GANGNAM_RECT = GANGNAM.get_rect()
    GANGNAM_RECT.center = (320, 148)
except IOError:
    print 'Gangnam image did not load!'
    pygame.quit()
    exit()

PLAY_AGAIN = FONT_OBJ.render('Play Again', True, BLACK)
PLAY_AGAIN_RECT = PLAY_AGAIN.get_rect()
PLAY_AGAIN_RECT.center = (200, 430)

EXIT_AGAIN = FONT_OBJ.render('Exit', True, BLACK)
EXIT_AGAIN_RECT = EXIT_AGAIN.get_rect()
EXIT_AGAIN_RECT.center = (480, 430)


class Word(object):
    def __init__(self, word):
        self.solved_string = word
        self.solved = list(word)
        self.length = len(word)
        self.solver = self.solved[:1] + ['_' for _ in xrange(1, self.length - 1)] + self.solved[-1:]
        self.solver_string = join(self.solver)
        self.guessed = 2
        self.errors = 0
        self.true_letters = []
        self.wrong_letters = []

    def update(self, letter):
        if letter not in self.true_letters and letter not in self.wrong_letters:
            found = False
            for itr in xrange(1, len(self.solved) - 1):
                if self.solved[itr] == letter:
                    found = True
                    self.solver[itr] = letter
                    self.guessed += 1
                    self.true_letters.append(letter)

            if not found:
                self.wrong_letters.append(letter)
                self.errors += 1

            self.solver_string = join(self.solver)
        else:
            ALRDY_MSG = self.WORD_FONT_OBJ.render('You\'ve already inputted that character!', True, BLACK)
            ALRDY_MSG_RECT = ALRDY_MSG.get_rect()
            ALRDY_MSG_RECT.center = (320, 380)

            DISPLAYSURF.blit(ALRDY_MSG, ALRDY_MSG_RECT)

            pygame.display.update()
            pygame.time.wait(1000)

    def render(self):
        try:
            self.WORD_FONT_OBJ = pygame.font.Font('kanover.ttf', WORDSIZE)
        except IOError:
            print 'Font did not load!'
            pygame.quit()
            exit()

        self.WORD = self.WORD_FONT_OBJ.render(self.solver_string, True, BLACK)
        self.WORD_RECT = self.WORD.get_rect()
        self.WORD_RECT.center = (320, 325)

        DISPLAYSURF.blit(self.WORD, self.WORD_RECT)

        self.ERROR = self.WORD_FONT_OBJ.render('Errors: %d/10' % (self.errors,), True, BLACK)
        self.ERROR_RECT = self.ERROR.get_rect()
        self.ERROR_RECT.center = (320, 440)

        DISPLAYSURF.blit(self.ERROR, self.ERROR_RECT)


def load_words():
    try:
        with open('dictionary.txt') as f:
            lines = f.readlines()
            lines = [word.strip() for word in lines]
        return lines
    except IOError:
        print 'Dictionary Not Found!'
        pygame.quit()
        exit()


def get_mouse_box(mouseX, mouseY, box1, box2):
    mouse_box = (None, None)

    if box1.collidepoint(mouseX, mouseY):
        mouse_box = box1
    elif box2.collidepoint(mouseX, mouseY):
        mouse_box = box2

    return mouse_box


def draw_highlight_box(mouse_box):
    if mouse_box != (None, None):
        pygame.draw.rect(DISPLAYSURF, HIGHLIGHT, mouse_box, 3)
        pygame.display.update()


def lose(word):
    DISPLAYSURF.blit(IMG[10], IMG_RECT[10])

    LOSE = FONT_OBJ.render('You Lose! Get Hanged!', True, BLACK)
    LOSE_RECT = LOSE.get_rect()
    LOSE_RECT.center = (320, 320)

    DISPLAYSURF.blit(LOSE, LOSE_RECT)

    LOSE_RES = word.WORD_FONT_OBJ.render('The word was %s!' % (word.solved_string, ), True, BLACK)
    LOSE_RES_RECT = LOSE_RES.get_rect()
    LOSE_RES_RECT.center = (320, 370)

    DISPLAYSURF.blit(LOSE_RES, LOSE_RES_RECT)


def win(word):
    DISPLAYSURF.blit(GANGNAM, GANGNAM_RECT)

    WIN = FONT_OBJ.render('You Win!', True, BLACK)
    WIN_RECT = WIN.get_rect()
    WIN_RECT.center = (320, 320)

    DISPLAYSURF.blit(WIN, WIN_RECT)

    WIN_RES = FONT_OBJ.render('Congratulations!', True, BLACK)
    WIN_RES_RECT = WIN_RES.get_rect()
    WIN_RES_RECT.center = (320, 370)

    DISPLAYSURF.blit(WIN_RES, WIN_RES_RECT)


def play():
    word = Word(choice(load_words()))
    while word.errors < 10 and word.guessed < word.length:
        DISPLAYSURF.fill(BACKGROUND)
        word.render()
        DISPLAYSURF.blit(IMG[word.errors], IMG_RECT[word.errors])

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                try:
                    word.update(KEY_MAP[event.key])
                except KeyError:
                    W_INP = word.WORD_FONT_OBJ.render('Wrong Key Input!', True, BLACK)
                    W_INP_RECT = W_INP.get_rect()
                    W_INP_RECT.center = (320, 380)

                    DISPLAYSURF.blit(W_INP, W_INP_RECT)
                    pygame.display.update()
                    pygame.time.wait(1000)

        pygame.display.update()
        fps_clock.tick(FPS)

    while True:
        DISPLAYSURF.fill(BACKGROUND)
        if word.errors == 10:
            lose(word)
        else:
            win(word)

        DISPLAYSURF.blit(PLAY_AGAIN, PLAY_AGAIN_RECT)
        DISPLAYSURF.blit(EXIT_AGAIN, EXIT_AGAIN_RECT)

        mouseX, mouseY = (0, 0)
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouse_clicked = True

        mouse_box = get_mouse_box(mouseX, mouseY, PLAY_AGAIN_RECT, EXIT_AGAIN_RECT)
        draw_highlight_box(mouse_box)

        if mouse_clicked:
            if mouse_box == PLAY_AGAIN_RECT:
                play()
            elif mouse_box == EXIT_AGAIN_RECT:
                pygame.quit()
                exit()
            mouse_clicked = False

        pygame.display.update()
        fps_clock.tick(FPS)


def start_menu():
    while True:
        DISPLAYSURF.fill(BACKGROUND)

        DISPLAYSURF.blit(TITLE, TITLE_RECT)
        DISPLAYSURF.blit(HANG_IMG, HANG_IMG_RECT)
        DISPLAYSURF.blit(START, START_RECT)
        DISPLAYSURF.blit(EXIT, EXIT_RECT)

        mouseX, mouseY = (0, 0)
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouse_clicked = True

        mouse_box = get_mouse_box(mouseX, mouseY, START_RECT, EXIT_RECT)
        draw_highlight_box(mouse_box)

        if mouse_clicked:
            if mouse_box == START_RECT:
                play()
            elif mouse_box == EXIT_RECT:
                pygame.quit()
                exit()
            mouse_clicked = False

        pygame.display.update()
        fps_clock.tick(FPS)


if __name__ == '__main__':
    start_menu()
