import pygame

WIDTH = 20
MARGIN = 1
PADDING = 20
DOT = 4

# rgb colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (170, 2, 2)
TILE_COLOR = (250, 217, 179)
GREEN = (2, 123, 2)


def get_game_info(info):
    if info['winner'] == 'C':
        return 'You lost'
    elif info['winner'] == 'P':
        return 'You won'

    if info['playing']:
        if info['turn'] < 4:
            if info['turn'] == 1:
                return 'Place 2 black stones and 1 white stone'
            elif info['turn'] == 2:
                return 'Choose your stone color or put two more stones'
            else:
                return 'Choose your color'

        if info['stone'] in ['B', 'W']:
            text = 'Your stone: '
            text += 'BLACK' if info['stone'] == 'B' else 'WHITE'
            return text


class Board:
    def __init__(self, display_surf, board_size):
        self.BOARD_SIZE = board_size
        self.BOARD = (WIDTH + MARGIN) * self.BOARD_SIZE + MARGIN
        self.GAME_WIDTH = self.BOARD + PADDING * 2
        self.GAME_HEIGHT = self.GAME_WIDTH + 100

        self.grid = [['-'] * (self.BOARD_SIZE + 1) for _ in range(0, self.BOARD_SIZE + 1)]

        self._display_surf = display_surf

        self.last_position = [-1, -1]

        self.OFFSET_WIDTH = self._display_surf.get_width() / self.BOARD * PADDING + self._display_surf.get_width() / self.BOARD_SIZE * 2.4
        self.OFFSET_HEIGHT = self._display_surf.get_height() / self.BOARD * PADDING + self._display_surf.get_height() / self.BOARD_SIZE * 2

    def on_render(self, info):
        self.render_stone()
        self.render_last_position()
        self.render_new_position()
        self.render_game_info(info)
        self.render_button(info['playing'])
        self.render_stones_in_order_to_choose_color(info)

    def reset(self):
        self.grid = [['-'] * (self.BOARD_SIZE + 1) for _ in range(0, self.BOARD_SIZE + 1)]
        self.last_position = [-1, -1]

    def draw_points(self):
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

    def init(self):
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

    def render_button(self, playing):
        color = GREEN if not playing else RED
        info = 'START' if not playing else 'SURRENDER'

        pygame.draw.rect(self._display_surf, color,
                         (self._display_surf.get_width() // 2 - 50, self._display_surf.get_height() - 110, 100, 30))

        info_font = pygame.font.SysFont('Comicsansms', 15)
        text = info_font.render(info, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = self._display_surf.get_width() // 2
        text_rect.centery = self._display_surf.get_height() - 95
        self._display_surf.blit(text, text_rect)

    def render_game_info(self, info_dict):
        info = get_game_info(info_dict)
        info_font = pygame.font.SysFont('Comicsansms', 25)
        text = info_font.render(info, True, BLACK)
        text_rect = text.get_rect()
        text_rect.centerx = self._display_surf.get_rect().centerx
        text_rect.centery = self._display_surf.get_height() - 130
        self._display_surf.blit(text, text_rect)

    def render_stone(self):
        for r in range(self.BOARD_SIZE + 1):
            for c in range(self.BOARD_SIZE + 1):
                center = ((MARGIN + WIDTH) * c + MARGIN + self.OFFSET_WIDTH,
                          (MARGIN + WIDTH) * r + MARGIN + self.OFFSET_HEIGHT)

                if self.grid[r][c] != '-':
                    color = BLACK if self.grid[r][c] == 'B' else WHITE
                    pygame.draw.circle(self._display_surf, color, center, WIDTH // 2 - MARGIN, 0)

    def render_last_position(self):
        if self.last_position[0] >= 0 and self.last_position[1] >= 0:
            pygame.draw.rect(self._display_surf, RED,
                             ((MARGIN + WIDTH) * self.last_position[1] + self.OFFSET_WIDTH - (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH) * self.last_position[0] + self.OFFSET_HEIGHT - (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH),
                              (MARGIN + WIDTH)), 1)

    def render_new_position(self):
        if self.last_position[0] >= 0 and self.last_position[1] >= 0:
            pygame.draw.rect(self._display_surf, RED,
                             (
                                 (MARGIN + WIDTH) * (self.last_position[1] - 1) + self.OFFSET_WIDTH - (
                                         MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH) * (self.last_position[0] - 1) + self.OFFSET_HEIGHT - (
                                         MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH - 10),
                                 (MARGIN + WIDTH - 10)), 1)
            pygame.draw.rect(self._display_surf, RED,
                             (
                                 (MARGIN + WIDTH) * (self.last_position[1] - 1) + self.OFFSET_WIDTH - (
                                         MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH) * (self.last_position[0] + 1) + self.OFFSET_HEIGHT - (
                                         MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH - 10),
                                 (MARGIN + WIDTH - 10)), 1)
            pygame.draw.rect(self._display_surf, RED,
                             (
                                 (MARGIN + WIDTH) * (self.last_position[1] + 1) + self.OFFSET_WIDTH - (
                                         MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH) * (self.last_position[0] - 1) + self.OFFSET_HEIGHT - (
                                         MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH - 10),
                                 (MARGIN + WIDTH - 10)), 1)
            pygame.draw.rect(self._display_surf, RED,
                             (
                                 (MARGIN + WIDTH) * (self.last_position[1] + 1) + self.OFFSET_WIDTH - (
                                             MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH) * (self.last_position[0] + 1) + self.OFFSET_HEIGHT - (
                                             MARGIN + WIDTH) // 4,
                                 (MARGIN + WIDTH - 10),
                                 (MARGIN + WIDTH - 10)), 1)

    def mouse_in_button(self, pos):
        return self._display_surf.get_width() // 2 - 50 <= pos[0] <= self._display_surf.get_width() // 2 + 50 and \
               self._display_surf.get_height() - 110 <= pos[1] <= self._display_surf.get_height() - 80

    def render_stones_in_order_to_choose_color(self, info):
        if info['turn'] in [2, 3] and info['is_player_turn'] and info['total_stones'] != 4:
            # white stone
            center = (self._display_surf.get_width() // 2 - 30, self._display_surf.get_height() - 30)
            radius = 15
            pygame.draw.circle(self._display_surf, WHITE, center, radius, 0)

            # black stone
            center = (self._display_surf.get_width() // 2 + 30, self._display_surf.get_height() - 30)
            pygame.draw.circle(self._display_surf, BLACK, center, radius, 0)
        else:
            # white stone
            center = (self._display_surf.get_width() // 2 - 30, self._display_surf.get_height() - 30)
            radius = 15
            pygame.draw.circle(self._display_surf, TILE_COLOR, center, radius, 0)

            # black stone
            center = (self._display_surf.get_width() // 2 + 30, self._display_surf.get_height() - 30)
            pygame.draw.circle(self._display_surf, TILE_COLOR, center, radius, 0)

    def mouse_in_white(self, position):
        center = (self._display_surf.get_width() // 2 - 30, self._display_surf.get_height() - 30)
        radius = 15

        return (position[0] - center[0]) ** 2 + (position[1] - center[1]) ** 2 < radius ** 2

    def mouse_in_black(self, position):
        center = (self._display_surf.get_width() // 2 + 30, self._display_surf.get_height() - 30)
        radius = 15

        return (position[0] - center[0]) ** 2 + (position[1] - center[1]) ** 2 < radius ** 2
