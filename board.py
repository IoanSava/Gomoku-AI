import pygame

WIDTH = 20
MARGIN = 1
PADDING = 20
DOT = 4
BOARD_SIZE = 18
BOARD = (WIDTH + MARGIN) * BOARD_SIZE + MARGIN
GAME_WIDTH = BOARD + PADDING * 2
GAME_HEIGHT = GAME_WIDTH + 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (133, 42, 44)
TILE_COLOR = (208, 176, 144)
GREEN = (26, 81, 79)
PLAYER = False


def on_cleanup():
    pygame.quit()


def mouse_in_button(pos):
    if GAME_WIDTH // 2 - 50 <= pos[0] <= GAME_WIDTH // 2 + 50 and GAME_HEIGHT - 50 <= pos[1] <= GAME_HEIGHT - 20:
        return True
    return False


def player_turn(color):
    if color == BLACK:
        return "BLACK turn"
    else:
        return "WHITE turn"


class Gomoku:
    def __init__(self):
        self.grid = [[0 for _ in range(BOARD_SIZE + 1)] for _ in range(BOARD_SIZE + 1)]
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)

        pygame.display.set_caption('Gomoku')

        self._running = True
        self._playing = False
        self._win = False
        self.lastPosition = [-1, -1]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            global PLAYER
            if mouse_in_button(pos):
                if not self._playing:
                    self.start()
                    if PLAYER:
                        PLAYER = not PLAYER
                else:
                    self.surrender()
                    PLAYER = not PLAYER

            elif self._playing:
                row = (pos[0] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)
                col = (pos[1] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)

                if 0 <= row <= BOARD_SIZE and 0 <= col <= BOARD_SIZE:
                    if self.grid[row][col] == 0:
                        self.lastPosition = [row, col]
                        self.grid[row][col] = 1 if PLAYER else 2

                        # check win
                        if self.check_win([row, col], PLAYER):
                            self._win = True
                            self._playing = False
                        else:
                            PLAYER = not PLAYER

    def on_render(self):
        self.render_gomoku_stone()
        self.render_last_position()
        self.render_game_info()
        self.render_button()
        pygame.display.update()

    def on_execute(self):
        while self._running:
            self.gomoku_board_init()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        on_cleanup()

    def start(self):
        self._playing = True
        self.grid = [[0 for _ in range(BOARD_SIZE + 1)] for _ in range(BOARD_SIZE + 1)]
        self.lastPosition = [-1, -1]
        self._win = False

    def surrender(self):
        self._playing = False
        self._win = True

    def draw_points(self):
        # Five dots
        # points = [(3, 3), , (9, 9), (3, 9), (9, 3), (15, 15), (3, 15), (15, 3), (9, 15), (15, 9)]
        points = [(int(BOARD_SIZE / 6), int(BOARD_SIZE / 6)), (int(BOARD_SIZE / 2), int(BOARD_SIZE / 2)),
                  (int(BOARD_SIZE / 6), int(BOARD_SIZE / 2)), (int(BOARD_SIZE / 2), int(BOARD_SIZE / 6)),
                  (BOARD_SIZE - int(BOARD_SIZE / 6), BOARD_SIZE - int(BOARD_SIZE / 6)),
                  (int(BOARD_SIZE / 6), BOARD_SIZE - int(BOARD_SIZE / 6)),
                  (BOARD_SIZE - int(BOARD_SIZE / 6), int(BOARD_SIZE / 6)),
                  (int(BOARD_SIZE / 2), BOARD_SIZE - int(BOARD_SIZE / 6)),
                  (BOARD_SIZE - int(BOARD_SIZE / 6), int(BOARD_SIZE / 2))]

        for point in points:
            pygame.draw.rect(self._display_surf, BLACK,
                             (PADDING + point[0] * (MARGIN + WIDTH) - DOT // 2,
                              PADDING + point[1] * (MARGIN + WIDTH) - DOT // 2,
                              DOT,
                              DOT), 0)

    def gomoku_board_init(self):
        self._display_surf.fill(TILE_COLOR)
        # Draw background rect for game area
        pygame.draw.rect(self._display_surf, BLACK,
                         [PADDING,
                          PADDING,
                          BOARD,
                          BOARD])

        # Draw the grid
        for row in range(BOARD_SIZE + 1):
            for column in range(BOARD_SIZE + 1):
                pygame.draw.rect(self._display_surf, TILE_COLOR,
                                 [(MARGIN + WIDTH) * column + MARGIN + PADDING,
                                  (MARGIN + WIDTH) * row + MARGIN + PADDING,
                                  WIDTH,
                                  WIDTH])

        self.draw_points()

    def render_button(self):
        color = GREEN if not self._playing else RED
        info = "Start" if not self._playing else "Surrender"

        pygame.draw.rect(self._display_surf, color,
                         (GAME_WIDTH // 2 - 50, GAME_HEIGHT - 50, 100, 30))

        info_font = pygame.font.SysFont('Helvetica', 18)
        text = info_font.render(info, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = GAME_WIDTH // 2
        text_rect.centery = GAME_HEIGHT - 35
        self._display_surf.blit(text, text_rect)

    def render_game_info(self):
        # current player color
        color = BLACK if not PLAYER else WHITE
        center = (GAME_WIDTH // 2 - 60, BOARD + 60)
        radius = 12
        pygame.draw.circle(self._display_surf, color, center, radius, 0)

        info = "You Win" if self._win else player_turn(color)
        info_font = pygame.font.SysFont('Helvetica', 25)
        text = info_font.render(info, True, BLACK)
        text_rect = text.get_rect()
        text_rect.centerx = self._display_surf.get_rect().centerx + 20
        text_rect.centery = center[1]
        self._display_surf.blit(text, text_rect)

    def render_gomoku_stone(self):
        for r in range(19):
            for c in range(19):
                center = ((MARGIN + WIDTH) * r + MARGIN + PADDING,
                          (MARGIN + WIDTH) * c + MARGIN + PADDING)
                if self.grid[r][c] > 0:
                    color = BLACK if self.grid[r][c] == 2 else WHITE
                    pygame.draw.circle(self._display_surf, color,
                                       center,
                                       WIDTH // 2 - MARGIN, 0)

    def render_last_position(self):
        if self.lastPosition[0] > 0 and self.lastPosition[1] > 0:
            pygame.draw.rect(self._display_surf, RED,
                             ((MARGIN + WIDTH) * self.lastPosition[0] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH) * self.lastPosition[1] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH),
                              (MARGIN + WIDTH)), 1)

    def check_win(self, position, player):
        target = 1 if player else 2
        if self.grid[position[0]][position[1]] != target:
            return False
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        for direction in directions:
            continue_game = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] <= BOARD_SIZE and 0 <= p[1] <= BOARD_SIZE:
                    if self.grid[p[0]][p[1]] == target:
                        continue_game += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]
            if continue_game >= 6:
                return True
        return False


if __name__ == "__main__":
    gomoku = Gomoku()
    gomoku.on_execute()
