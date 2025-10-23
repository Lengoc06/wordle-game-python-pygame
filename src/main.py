import os
import random
import pygame
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.create_word_list()
        self.not_enough_letters_message = UIElement(75, 60, "Not Enough Letters", WHITE)
        self.not_found_word_message = UIElement(100, 60, "Word Not Found", WHITE)

    def create_word_list(self):
        curr_dir = os.path.dirname(__file__)
        answer_path = os.path.join(curr_dir, "assets", "answers.txt")
        allowed_path = os.path.join(curr_dir, "assets", "allowed.txt")
        with open(answer_path, "r") as file:
            answer = file.read().splitlines()
        with open(allowed_path, "r") as file:
            allowed = file.read().splitlines()
        
        self.ans_list = answer
        self.words_list = set(answer)
        self.words_list.update(set(allowed))

    def new(self):
        self.ans = random.choice(self.ans_list).upper()
        # self.ans = "CLOCK"
        # print(self.ans)
        self.text = ""
        self.curr_row = 0
        self.tiles = []
        self.create_tiles()
        self.flip = True
        self.not_enough_letters = False
        self.not_found_word = False
        self.timer = 0

    def create_tiles(self):
        for row in range(6):
            self.tiles.append([])
            for col in range(5):
                self.tiles[row].append(Tile((col * (TILESIZE + GAPSIZE)) + MARGIN_X, (row * (TILESIZE + GAPSIZE)) + MARGIN_Y))

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.add_letter()

    def add_letter(self):
        for tile in self.tiles[self.curr_row]:
            tile.letter = ""

        for i, letter in enumerate(self.text):
            self.tiles[self.curr_row][i].letter = letter
            self.tiles[self.curr_row][i].create_font()

    def draw_tiles(self):
        for row in self.tiles:
            for tile in row:
                tile.draw(self.screen)

    def draw(self):
        self.screen.fill(BGCOLOR)
        if self.not_enough_letters:
            self.timer += 1
            self.not_enough_letters_message.fade_in()
            if self.timer > 90:
                self.not_enough_letters = False
                self.timer = 0
        else:
            self.not_enough_letters_message.fade_out()

        if self.not_found_word:
            self.timer += 1
            self.not_found_word_message.fade_in()
            if self.timer > 90:
                self.not_found_word = False
                self.timer = 0
        else:
            self.not_found_word_message.fade_out()
            
        self.not_enough_letters_message.draw(self.screen)
        self.not_found_word_message.draw(self.screen)

        self.draw_tiles()

        pygame.display.flip()

    def row_animation(self):
        start_pos = self.tiles[0][0].x
        amount_move = 4
        move = 3
        screen_copy = self.screen.copy()
        screen_copy.fill(BGCOLOR)
        for row in self.tiles:
            for tile in row:
                if row != self.tiles[self.curr_row]:
                    tile.draw(screen_copy)

        while True:
            while self.tiles[self.curr_row][0].x < start_pos + amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.curr_row]:
                    tile.x += move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            while self.tiles[self.curr_row][0].x > start_pos - amount_move:
                self.screen.blit(screen_copy, (0, 0))
                for tile in self.tiles[self.curr_row]:
                    tile.x -= move
                    tile.draw(self.screen)
                self.clock.tick(FPS)
                pygame.display.flip()

            amount_move -= 2
            if amount_move < 0:
                break

    def box_animation(self):
        for tile in self.tiles[self.curr_row]:
            if tile.letter == "":
                screen_copy = self.screen.copy()
                for start, end, step in ((0, 6, 1), (0, -6, -1)):
                    for size in range(start, end, 2*step):
                        self.screen.blit(screen_copy, (0, 0))
                        tile.x -= size
                        tile.y -= size
                        tile.width += size * 2
                        tile.height += size * 2
                        surface = pygame.Surface((tile.width, tile.height))
                        surface.fill(BGCOLOR)
                        self.screen.blit(surface, (tile.x, tile.y))
                        tile.draw(self.screen)
                        pygame.display.flip()
                        self.clock.tick(FPS)
                    self.add_letter()
                break

    def reveal_animation(self, tile, color):
        screen_copy = self.screen.copy()

        while True:
            surface = pygame.Surface((tile.width + 5, tile.height + 5))
            surface.fill(BGCOLOR)
            screen_copy.blit(surface, (tile.x, tile.y))
            self.screen.blit(screen_copy, (0, 0))
            if self.flip:
                tile.y += 6
                tile.height -= 12
                tile.font_y += 4
                tile.font_height = max(tile.font_height - 8, 0)
            else:
                tile.color = color
                tile.y -= 6
                tile.height += 12
                tile.font_y -= 4
                tile.font_height = min(tile.font_height + 8, tile.font_size)
            if tile.font_height == 0:
                self.flip = False

            tile.draw(self.screen)
            pygame.display.update()
            self.clock.tick(FPS)

            if tile.font_height == tile.font_size:
                self.flip = True
                break

    def check_letters(self):
        copy_word = list(self.ans)
        color = [GREY] * 5
        for i in range(5):
            if self.text[i] == copy_word[i]:
                color[i] = GREEN
                copy_word[i] = ''

        for i in range(5):
            if color[i] == GREY:
                if self.text[i] in copy_word:
                    color[i] = YELLOW
                    idx = copy_word.index(self.text[i])
                    copy_word[idx] = ''
            
        for i in range(5):    
            self.reveal_animation(self.tiles[self.curr_row][i], color[i])


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.text) == 5:
                        if self.text.lower() in self.words_list:
                            self.check_letters()

                            if self.text == self.ans or self.curr_row + 1 == 6:
                                if self.text != self.ans:
                                    self.end_screen_text = UIElement(65, 40, f"THE WORD WAS: {self.ans}", WHITE)

                                else:
                                    self.end_screen_text = UIElement(80, 40, "YOU GUESSED RIGHT", WHITE)

                                self.playing = False
                                self.end_screen()
                                break

                            self.curr_row += 1
                            self.text = ""

                        else:
                            self.not_found_word = True
                            self.row_animation()

                    else:
                        self.not_enough_letters = True
                        self.row_animation()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 5 and event.unicode.isalpha():
                        self.text += event.unicode.upper()
                        self.box_animation()

    def end_screen(self):
        play_again = UIElement(12.5, 80, "PRESS ENTER TO PLAY AGAIN", WHITE)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.fill(BGCOLOR)
            self.draw_tiles()
            self.end_screen_text.fade_in()
            self.end_screen_text.draw(self.screen)
            play_again.fade_in()
            play_again.draw(self.screen)
            pygame.display.flip()

game = Game()
while True:
    game.new()
    game.run()
