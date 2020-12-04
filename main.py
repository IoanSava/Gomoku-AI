import pygame_gui

from board import *
from game_gui.game_gui import GameGUI


if __name__ == "__main__":

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Gomoku')

    screen = pygame.display.set_mode((600, 660), pygame.HWSURFACE | pygame.DOUBLEBUF)

    gomoku = Gomoku(screen, 19)

    manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
    game_gui = GameGUI(screen, manager, [600, 660])
    running = True
    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(60) / 1000.0
        gomoku.gomoku_board_init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == game_gui.new_game_button:
                        print('New Game')
                        gomoku.start()
                    if event.ui_element == game_gui.options_button:
                        print('Options')
                        game_gui.open_options_panel()
                    if event.ui_element == game_gui.confirm_changes_button:
                        print('New Game')
                        game_gui.confirm_changes()
                        print([game_gui.black_player_selected_option,
                               game_gui.white_player_selected_option,
                               game_gui.board_size_changer_selected_option, game_gui.hints_enabled])
                        game_gui.close_options_panel()
                        gomoku.initialize(screen, int(game_gui.board_size_changer_selected_option.split()[0]))
                    if event.ui_element == game_gui.cancel_changes_button:
                        print('\u2718')
                        game_gui.cancel_changes()
                        game_gui.close_options_panel()
                    if event.ui_element == game_gui.hints_button:
                        if game_gui.hints_button.text == 'Enable':
                            game_gui.hints_label.set_text('Hints Enabled')
                            game_gui.hints_button.set_text('Disable')
                        else:
                            game_gui.hints_label.set_text('Hints Disabled')
                            game_gui.hints_button.set_text('Enable')

            if event.type == pygame.MOUSEBUTTONUP:
                if not game_gui.options_panel.visible:
                    pos = pygame.mouse.get_pos()
                    global PLAYER
                    if gomoku.mouse_in_button(pos):
                        if not gomoku.playing:
                            gomoku.start()
                            if PLAYER:
                                PLAYER = not PLAYER
                        else:
                            gomoku.surrender()
                            PLAYER = not PLAYER

                    elif gomoku.playing:
                        print(pos)
                        row = (pos[1] - int(gomoku.OFFSET_HEIGHT) + WIDTH // 2) // (WIDTH + MARGIN)
                        col = (pos[0] - int(gomoku.OFFSET_WIDTH) + WIDTH // 2) // (WIDTH + MARGIN)

                        if 0 <= row <= gomoku.BOARD_SIZE and 0 <= col <= gomoku.BOARD_SIZE:
                            if gomoku.grid[row][col] == 0:
                                gomoku.lastPosition = [row, col]
                                gomoku.grid[row][col] = 1 if PLAYER else 2

                                # check win
                                if gomoku.check_win([row, col], PLAYER):
                                    gomoku._win = True
                                    gomoku.playing = False
                                else:
                                    PLAYER = not PLAYER

            manager.process_events(event)
        manager.update(time_delta)
        gomoku.on_render()
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()
