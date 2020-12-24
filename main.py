import pygame_gui

from board import *
from logic import *
from menu import Menu

DEFAULT_BOARD_SIZE = 19
RESOLUTION = 600, 660

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Gomoku')

    screen = pygame.display.set_mode(RESOLUTION, pygame.HWSURFACE | pygame.DOUBLEBUF)

    manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
    game_gui = Menu(screen, manager, RESOLUTION)
    board = Board(screen, DEFAULT_BOARD_SIZE)
    game = Game(board, game_gui.computer_selected_option)
    running = True
    clock = pygame.time.Clock()

    while running:
        time_delta = clock.tick(60) / 1000.0
        board.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == game_gui.new_game_button:
                        game.reset()
                        game.first_turn()
                    if event.ui_element == game_gui.options_button:
                        game_gui.open_options_panel()
                    if event.ui_element == game_gui.confirm_changes_button:
                        game_gui.confirm_changes()
                        game_gui.close_options_panel()
                        board = Board(screen, int(game_gui.board_size_changer_selected_option.split()[0]))
                        game = Game(board, game_gui.computer_selected_option)
                    if event.ui_element == game_gui.cancel_changes_button:
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
                    if game.board.mouse_in_button(pos):
                        if not game.playing:
                            game.reset()
                            game.first_turn()
                        else:
                            game.winner = 'C'
                            game.game_over()

                    elif game.playing:
                        row = (pos[1] - int(game.board.OFFSET_HEIGHT) + WIDTH // 2) // (WIDTH + MARGIN)
                        col = (pos[0] - int(game.board.OFFSET_WIDTH) + WIDTH // 2) // (WIDTH + MARGIN)
                        position = (row, col)

                        if game.turn == 1:
                            game.first_turn_for_player(position)
                        elif game.turn == 2:
                            game.second_turn_for_player(position, pos)
                        elif game.turn == 3:
                            game.third_turn_for_player(pos)
                        else:
                            game.player_turn(position)

            manager.process_events(event)
        manager.update(time_delta)
        game.board.on_render(
            {'playing': game.playing, 'winner': game.winner, 'stone': game.player_stone, 'turn': game.turn,
             'is_player_turn': game.is_player_turn, 'total_stones': game.total_stones})
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()
