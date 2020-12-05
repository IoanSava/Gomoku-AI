import pygame
import pygame_gui


class GameGUI:
    def __init__(self, window, manager, resolution):
        self.window = window
        self.manager = manager
        self.resolution = resolution

        self.icon = pygame.image.load('data/images/gomoku-logo.png').convert()
        pygame.display.set_icon(self.icon)

        self.new_game_button = None
        self.options_button = None
        self.options_panel = None

        self.black_player_label = None
        self.black_player_options = None
        self.black_player_selected_option = None

        self.white_player_label = None
        self.white_player_options = None
        self.white_player_selected_option = None

        self.board_size_label = None
        self.board_size_changer = None
        self.board_size_changer_selected_option = None

        self.hints_label = None
        self.hints_button = None
        self.hints_enabled = None

        self.confirm_changes_button = None
        self.cancel_changes_button = None
        self.add_ui()

    def add_ui(self):
        self.manager.set_window_resolution(self.resolution)
        self.manager.clear_and_reset()
        # self.background = pygame.transform.scale(self.og_background, (self.resolution[0], self.resolution[1]))

        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 15, 100, 30),
            text='New Game', manager=self.manager)

        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(120, 15, 100, 30),
            text='Options', manager=self.manager)

        self.options_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(10, 45, 500, 250), starting_layer_height=3,
            manager=self.manager)

        self.confirm_changes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(400, 195, 40, 40),
                                                                   text='\u2713', manager=self.manager,
                                                                   container=self.options_panel)

        # '\u2714'

        self.cancel_changes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(445, 195, 40, 40),
                                                                  text='X', manager=self.manager,
                                                                  container=self.options_panel)

        # '\u2718'

        self.black_player_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(55, 50, 80, 20), text='Black',
                                                              manager=self.manager, container=self.options_panel)

        self.white_player_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(355, 50, 80, 20), text='White',
                                                              manager=self.manager, container=self.options_panel)

        self.board_size_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(195, 20, 100, 20),
                                                            text='Board Size',
                                                            manager=self.manager, container=self.options_panel)

        self.hints_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(185, 150, 120, 20),
                                                       text='Hints Disabled',
                                                       manager=self.manager, container=self.options_panel)

        self.hints_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(195, 170, 100, 30),
                                                         text='Enable',
                                                         manager=self.manager, container=self.options_panel)

        self.hints_enabled = False
        self.build_option_setters()
        self.options_panel.hide()

    def build_option_setters(self, black_player_starting_option='AI Medium',
                             white_player_starting_option='Human', board_changer_starting_option='19 by 19'):

        self.black_player_options = pygame_gui.elements.UIDropDownMenu(
            options_list=['Human', 'AI Easy', 'AI Medium', 'AI Hard'], starting_option=black_player_starting_option,
            relative_rect=pygame.Rect(40, 70, 110, 30), manager=self.manager, container=self.options_panel)

        self.white_player_options = pygame_gui.elements.UIDropDownMenu(
            options_list=['Human', 'AI Easy', 'AI Medium', 'AI Hard'], starting_option=white_player_starting_option,
            relative_rect=pygame.Rect(340, 70, 110, 30), manager=self.manager, container=self.options_panel)

        self.board_size_changer = pygame_gui.elements.UIDropDownMenu(
            options_list=['11 by 11', '15 by 15', '19 by 19'], starting_option=board_changer_starting_option,
            relative_rect=pygame.Rect(195, 40, 100, 30), manager=self.manager, container=self.options_panel)

        self.black_player_selected_option = self.black_player_options.selected_option
        self.white_player_selected_option = self.white_player_options.selected_option
        self.board_size_changer_selected_option = self.board_size_changer.selected_option

    def reset_options_panel_choices(self):
        if self.hints_enabled:
            self.hints_label.set_text('Hints Enabled')
            self.hints_button.set_text('Disable')
        else:
            self.hints_label.set_text('Hints Disabled')
            self.hints_button.set_text('Enable')
        self.black_player_options.kill()
        self.white_player_options.kill()
        self.board_size_changer.kill()
        self.build_option_setters(self.black_player_selected_option,
                                  self.white_player_selected_option, self.board_size_changer_selected_option)

    def confirm_changes(self):
        self.black_player_selected_option = self.black_player_options.selected_option
        self.white_player_selected_option = self.white_player_options.selected_option
        self.board_size_changer_selected_option = self.board_size_changer.selected_option
        self.hints_enabled = True if self.hints_button.text == 'Disable' else False
        self.black_player_options.kill()
        self.white_player_options.kill()
        self.board_size_changer.kill()
        self.build_option_setters(self.black_player_selected_option,
                                  self.white_player_selected_option,
                                  self.board_size_changer_selected_option)

    def cancel_changes(self):
        self.black_player_options.kill()
        self.white_player_options.kill()
        self.board_size_changer.kill()
        self.reset_options_panel_choices()

    def open_options_panel(self):
        self.options_panel.show()
        self.new_game_button.disable()
        self.options_button.disable()

    def close_options_panel(self):
        self.new_game_button.enable()
        self.options_button.enable()
        self.options_panel.hide()
