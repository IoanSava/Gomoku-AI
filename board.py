import pygame

WIDTH = 20
MARGIN = 1
PADDING = 20
DOT = 4

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (133, 42, 44)
TILE_COLOR = (208, 176, 144)
GREEN = (26, 81, 79)
PLAYER = False


def player_turn(color):
    if color == BLACK:
        return "BLACK turn"
    else:
        return "WHITE turn"


class Gomoku:
    def __init__(self, display_surf, board_size):
        self.initialize(display_surf, board_size)

    def initialize(self, display_surf, board_size):
        self.BOARD_SIZE = board_size
        self.BOARD = (WIDTH + MARGIN) * self.BOARD_SIZE + MARGIN
        self.GAME_WIDTH = self.BOARD + PADDING * 2
        self.GAME_HEIGHT = self.GAME_WIDTH + 100

        self.grid = [[0 for _ in range(self.BOARD_SIZE + 1)] for _ in range(self.BOARD_SIZE + 1)]

        self._display_surf = display_surf

        self.playing = False
        self._win = False
        self.lastPosition = [-1, -1]

        self.OFFSET_WIDTH = self._display_surf.get_width() / self.BOARD * PADDING + \
                            self._display_surf.get_width() / self.BOARD_SIZE * 2.4
        self.OFFSET_HEIGHT = self._display_surf.get_height() / self.BOARD * PADDING + \
                             self._display_surf.get_height() / self.BOARD_SIZE * 2

    def on_render(self):
        self.render_gomoku_stone()
        self.render_last_position()
        self.render_game_info()
        self.render_button()

    def start(self):
        self.playing = True
        self.grid = [[0 for _ in range(self.BOARD_SIZE + 1)] for _ in range(self.BOARD_SIZE + 1)]
        self.lastPosition = [-1, -1]
        self._win = False

    def surrender(self):
        self.playing = False
        self._win = True

    def draw_points(self):
        # Five dots
        # points = [(3, 3), , (9, 9), (3, 9), (9, 3), (15, 15), (3, 15), (15, 3), (9, 15), (15, 9)]
        points = [(int(self.BOARD_SIZE / 6), int(self.BOARD_SIZE / 6)),
                  (int(self.BOARD_SIZE / 2), int(self.BOARD_SIZE / 2)),
                  (int(self.BOARD_SIZE / 6), int(self.BOARD_SIZE / 2)),
                  (int(self.BOARD_SIZE / 2), int(self.BOARD_SIZE / 6)),
                  (self.BOARD_SIZE - int(self.BOARD_SIZE / 6), self.BOARD_SIZE - int(self.BOARD_SIZE / 6)),
                  (int(self.BOARD_SIZE / 6), self.BOARD_SIZE - int(self.BOARD_SIZE / 6)),
                  (self.BOARD_SIZE - int(self.BOARD_SIZE / 6), int(self.BOARD_SIZE / 6)),
                  (int(self.BOARD_SIZE / 2), self.BOARD_SIZE - int(self.BOARD_SIZE / 6)),
                  (self.BOARD_SIZE - int(self.BOARD_SIZE / 6), int(self.BOARD_SIZE / 2))]

        for point in points:
            pygame.draw.rect(self._display_surf, BLACK,
                             (self.OFFSET_WIDTH + point[0] * (MARGIN + WIDTH) - DOT // 2,
                              self.OFFSET_HEIGHT + point[1] * (MARGIN + WIDTH) - DOT // 2,
                              DOT,
                              DOT), 0)

    def gomoku_board_init(self):
        self._display_surf.fill(TILE_COLOR)
        # Draw background rect for game area
        pygame.draw.rect(self._display_surf, BLACK,
                         [self.OFFSET_WIDTH,
                          self.OFFSET_HEIGHT,
                          self.BOARD,
                          self.BOARD])

        # Draw the grid
        for row in range(self.BOARD_SIZE + 1):
            for column in range(self.BOARD_SIZE + 1):
                pygame.draw.rect(self._display_surf, TILE_COLOR,
                                 [(MARGIN + WIDTH) * column + MARGIN + self.OFFSET_WIDTH,
                                  (MARGIN + WIDTH) * row + MARGIN + self.OFFSET_HEIGHT,
                                  WIDTH,
                                  WIDTH])

        self.draw_points()

    def render_button(self):
        color = GREEN if not self.playing else RED
        info = "Start" if not self.playing else "Surrender"

        pygame.draw.rect(self._display_surf, color,
                         (self._display_surf.get_width() // 2 - 50, self._display_surf.get_height() - 110, 100, 30))

        info_font = pygame.font.SysFont('Helvetica', 18)
        text = info_font.render(info, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = self._display_surf.get_width() // 2
        text_rect.centery = self._display_surf.get_height() - 95
        self._display_surf.blit(text, text_rect)

    def render_game_info(self):
        # current player color
        color = BLACK if not PLAYER else WHITE
        center = (self._display_surf.get_width() // 2 - 60, self._display_surf.get_height() - 130)
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
        for r in range(self.BOARD_SIZE + 1):
            for c in range(self.BOARD_SIZE + 1):
                center = ((MARGIN + WIDTH) * c + MARGIN + self.OFFSET_WIDTH,
                          (MARGIN + WIDTH) * r + MARGIN + self.OFFSET_HEIGHT)

                if self.grid[r][c] > 0:
                    color = BLACK if self.grid[r][c] == 2 else WHITE
                    pygame.draw.circle(self._display_surf, color,
                                       center,
                                       WIDTH // 2 - MARGIN, 0)

    def render_last_position(self):
        if self.lastPosition[0] >= 0 and self.lastPosition[1] >= 0:
            pygame.draw.rect(self._display_surf, RED,
                             ((MARGIN + WIDTH) * self.lastPosition[1] + self.OFFSET_WIDTH - (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH) * self.lastPosition[0] + self.OFFSET_HEIGHT - (MARGIN + WIDTH) // 2,
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
                while 0 <= p[0] <= self.BOARD_SIZE and 0 <= p[1] <= self.BOARD_SIZE:
                    if self.grid[p[0]][p[1]] == target:
                        continue_game += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]
            if continue_game >= 6:
                return True
        return False

    def mouse_in_button(self, pos):
        if self._display_surf.get_width() // 2 - 50 <= pos[0] <= self._display_surf.get_width() // 2 + 50 and \
                self._display_surf.get_height() - 110 <= pos[1] <= self._display_surf.get_height() - 80:
            return True
        return False
