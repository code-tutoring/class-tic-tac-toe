import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))

font = pygame.font.Font("freesansbold.ttf", 50)
small_font = pygame.font.Font("freesansbold.ttf", 20)
text_x = font.render("X", True, (255, 255, 255))
text_o = font.render("O", True, (255, 255, 255))

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board:
    def __init__(self):
        self.board_values = [["0", "0", "0"],
                             ["0", "0", "0"],
                             ["0", "0", "0"]]
        self.current_move = "X"
        self.squares = [
                        # row 1
                        pygame.Rect(200, 200, 133, 133),
                        pygame.Rect(333, 200, 134, 133),
                        pygame.Rect(467, 200, 133, 133),

                        # row 2
                        pygame.Rect(200, 333, 133, 133),
                        pygame.Rect(333, 333, 134, 133),
                        pygame.Rect(467, 333, 133, 133),

                        # row 3
                        pygame.Rect(200, 467, 133, 133),
                        pygame.Rect(333, 467, 134, 133),
                        pygame.Rect(467, 467, 133, 133),

                        ]
        self.game_over = False

        self.alternate_computer_move_value = False
        self.generate_computer_moves = False

    def draw_board(self, surface):
        white = (255, 255, 255)
        pygame.draw.line(surface, white,
                         (200 + 133, 200), (200 + 133, 600))
        pygame.draw.line(surface, white,
                         (200 + 133 + 134, 200), (200 + 133 + 134, 600))
        pygame.draw.line(surface, white,
                         (200, 200 + 133), (600, 200 + 133))
        pygame.draw.line(surface, white,
                         (200, 200 + 133 + 134), (600, 200 + 133 + 134))

    def switch_move(self):
        if self.is_computer_opponent():
            if self.current_move == "X":
                self.current_move = "computer"
            else:
                self.current_move = "X"
        else:
            if self.current_move == "X":
                self.current_move = "O"
            else:
                self.current_move = "X"

    def is_empty_square(self, x, y):
        return self.board_values[x][y] == "0"

    def is_computer_opponent(self):
        # implement later
        return False

    def draw_value(self, surface, collided):
        rect = self.squares[collided]
        x, y = self.collided_to_xy(collided)

        if self.board_values[x][y] == "X":
            text_rect = text_x.get_rect()
            text_rect.center = (rect.x + rect.w // 2, rect.y + rect.h // 2)
            surface.blit(text_x, text_rect)
        elif self.board_values[x][y] == "O":
            text_rect = text_o.get_rect()
            text_rect.center = (rect.x + rect.w // 2, rect.y + rect.h // 2)
            surface.blit(text_o, text_rect)

    def collided_to_xy(self, collided):
        x = 0
        y = 0

        if collided == 0:
            x = 0
            y = 0
        elif collided == 1:
            x = 1
            y = 0
        elif collided == 2:
            x = 2
            y = 0
        elif collided == 3:
            x = 0
            y = 1
        elif collided == 4:
            x = 1
            y = 1
        elif collided == 5:
            x = 2
            y = 1
        elif collided == 6:
            x = 0
            y = 2
        elif collided == 7:
            x = 1
            y = 2
        elif collided == 8:
            x = 2
            y = 2

        return (x, y)

    def clicked_on_box(self, coordinate):
        if self.game_over:
            return

        mouse = pygame.Rect(coordinate.x, coordinate.y, 1, 1)
        collided = mouse.collidelist(self.squares)

        if collided == -1:
            return
        else:
            x, y = self.collided_to_xy(collided)

            if self.is_empty_square(x, y):
                self.place_marker(x, y)
            else:
                return

    def check_win(self):
        # diagonals first
        if self.board_values[0][0] != "0" and self.board_values[0][0] == self.board_values[1][1] \
            and self.board_values[1][1] == self.board_values[2][2]:
                self.game_over = True
                return self.board_values[0][0]
        elif self.board_values[2][0] != "0" and self.board_values[2][0] == self.board_values[1][1] \
            and self.board_values[1][1] == self.board_values[0][2]:
                self.game_over = True
                return self.board_values[2][0]
        # horizontal
        elif self.board_values[0][0] != "0" and self.board_values[0][0] == self.board_values[1][0] \
            and self.board_values[1][0] == self.board_values[2][0]:
                self.game_over = True
                return self.board_values[0][0]
        elif self.board_values[0][1] != "0" and self.board_values[0][1] == self.board_values[1][1] \
             and self.board_values[1][1] == self.board_values[2][1]:
            self.game_over = True
            return self.board_values[0][1]
        elif self.board_values[0][2] != "0" and self.board_values[0][2] == self.board_values[1][2] \
             and self.board_values[1][2] == self.board_values[2][2]:
            self.game_over = True
            return self.board_values[0][2]
        # vertical
        elif self.board_values[0][0] != "0" and self.board_values[0][0] == self.board_values[0][1] \
            and self.board_values[0][1] == self.board_values[0][2]:
            self.game_over = True
            return self.board_values[0][0]
        elif self.board_values[1][0] != "0" and self.board_values[1][0] == self.board_values[1][1] \
            and self.board_values[1][1] == self.board_values[1][2]:
            self.game_over = True
            return self.board_values[1][0]
        elif self.board_values[2][0] != "0" and self.board_values[2][0] == self.board_values[2][1] \
            and self.board_values[2][1] == self.board_values[2][2]:
            self.game_over = True
            return self.board_values[2][0]
        # determine if it is a tie
        else:
            available_space = False
            for i in range(3):
                for j in range(3):
                    if self.board_values[i][j] == "0":
                        available_space = True

            if not available_space:
                return "Tie"
            else:
                return None

    def clear_board(self):
        for i in range(len(self.board_values)):
            for j in range(len(self.board_values[0])):
                self.board_values[i][j] = "0"
        self.game_over = False

    def generate_computer_move(self):
        while True:
            random_square = random.randint(0, 8)
            x,y = self.collided_to_xy(random_square)
            is_available = self.is_empty_square(x, y)

            if is_available:
                self.place_marker(x, y)
                return

    def place_marker(self, x, y):
        self.board_values[x][y] = self.current_move
        self.switch_move()

        if self.alternate_computer_move_value:
            self.generate_computer_moves = not self.generate_computer_moves

BOARD = Board()

clear_button_rect = pygame.Rect(300, 50, 200, 75)
mode_button_rect = pygame.Rect(575, 50, 175, 75)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()

            x = mouse_position[0]
            y = mouse_position[1]

            BOARD.clicked_on_box(Coordinate(x, y))

            if clear_button_rect.collidepoint(x, y):
                BOARD.clear_board()
            elif mode_button_rect.collidepoint(x, y):
                BOARD.alternate_computer_move_value = not BOARD.alternate_computer_move_value

    screen.fill((0, 0, 0))

    BOARD.draw_board(screen)

    # reset board button
    clear_board_button = pygame.draw.rect(screen, (255, 0, 0), clear_button_rect)
    text_reset = font.render("Reset", True, (255, 255, 255))
    text_reset_rect = text_reset.get_rect()
    text_reset_rect.center = (400, 90)
    screen.blit(text_reset, text_reset_rect)

    # current move
    text_move = small_font.render(f"Current move: {BOARD.current_move}", True, (255, 255, 255))
    text_move_rect = text_move.get_rect()
    text_move_rect.center = (100, 100)
    screen.blit(text_move, text_move_rect)

    # button to change modes
    mode_change_button = pygame.draw.rect(screen, (0, 255, 0), mode_button_rect)
    text_change_mode = small_font.render("Change Mode", True, (255, 255, 255))
    text_change_mode_rect = text_change_mode.get_rect()
    text_change_mode_rect.center = ((575 + 575 + 175) // 2, (50 + 50 + 75) // 2)
    screen.blit(text_change_mode, text_change_mode_rect)


    # mode text
    status = ""
    if BOARD.alternate_computer_move_value:
        status = "Singleplayer"
    else:
        status = "Multiplayer"

    text_mode = small_font.render(f"Current Mode: {status}", True, (255, 255, 255))
    text_mode_rect = text_mode.get_rect()
    text_mode_rect.center = (400, 700)
    screen.blit(text_mode, text_mode_rect)

    if BOARD.generate_computer_moves:
        BOARD.generate_computer_move()

    for i in range(9):
        BOARD.draw_value(screen, i)

    winner = BOARD.check_win()

    # winner
    text_winner = small_font.render("Winner: ", True, (255, 255, 255))
    if winner is not None:
        text_winner = small_font.render(f"Winner: {winner}", True, (255, 255, 255))

    text_winner_rect = text_winner.get_rect()
    text_winner_rect.center = (100, 135)
    screen.blit(text_winner, text_winner_rect)


    pygame.display.update()