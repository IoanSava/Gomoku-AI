from game_gui.game_gui import GameGUI
import pygame
import pygame_gui

if __name__ == '__main__':
    pygame.init()
    resolution = [700, 650]
    screen = pygame.display.set_mode(tuple(resolution), 0, 32)
    manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()))
    game_gui = GameGUI(screen, manager, resolution)

    running = True
    clock = pygame.time.Clock()
    while running:
        game_gui.window.blit(game_gui.background, (0, 0))
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == game_gui.new_game_button:
                        print('New Game')
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
                    if event.ui_element == game_gui.cancel_changes_button:
                        print('X')
                        game_gui.cancel_changes()
                        game_gui.close_options_panel()
                    if event.ui_element == game_gui.hints_button:
                        if game_gui.hints_button.text == 'Enable':
                            game_gui.hints_label.set_text('Hints Enabled')
                            game_gui.hints_button.set_text('Disable')
                        else:
                            game_gui.hints_label.set_text('Hints Disabled')
                            game_gui.hints_button.set_text('Enable')
            if event.type == pygame.MOUSEBUTTONDOWN and event.type != pygame.USEREVENT:
                if not game_gui.options_panel.visible:
                    print(pygame.mouse.get_pos())

            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()
