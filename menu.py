import pygame
import pygame_gui


class Menu:
    def __init__(self, window, manager, resolution, params_list):
        self.window = window
        self.manager = manager
        self.resolution = resolution
        self.params_list = params_list

        self.icon = pygame.image.load('data/images/gomoku-logo.png').convert()
        pygame.display.set_icon(self.icon)

        self.change_params_button = None
        self.options_button = None

        self.options_panel = None
        self.params_panel = None

        self.computer_label = None
        self.computer_options = None
        self.computer_selected_option = None

        self.player_label = None
        self.player_options = None
        self.player_selected_option = None

        self.board_size_label = None
        self.board_size_changer = None
        self.board_size_changer_selected_option = None

        self.hints_label = None
        self.hints_button = None
        self.hints_enabled = None

        self.confirm_changes_button = None
        self.cancel_changes_button = None

        self.confirm_params_button = None
        self.cancel_params_button = None

        self.params_panel_label = None

        self.param_labels_list = []
        self.param_fields_list = []
        self.add_ui()

    def add_ui(self):
        self.manager.set_window_resolution(self.resolution)
        self.manager.clear_and_reset()

        self.change_params_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 15, 100, 30),
            text='Parameters', manager=self.manager)

        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(120, 15, 100, 30),
            text='Options', manager=self.manager)

        self.options_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(10, 45, 500, 250), starting_layer_height=3,
            manager=self.manager)

        self.params_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(10, 45, 250, 550), starting_layer_height=3,
            manager=self.manager)

        self.confirm_changes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(400, 195, 40, 40),
                                                                   text='\u2713', manager=self.manager,
                                                                   container=self.options_panel)

        self.cancel_changes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(445, 195, 40, 40),
                                                                  text='X', manager=self.manager,
                                                                  container=self.options_panel)

        self.confirm_params_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(160, 505, 35, 35),
                                                                  text='\u2713', manager=self.manager,
                                                                  container=self.params_panel)

        self.cancel_params_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(205, 505, 35, 35),
                                                                 text='X', manager=self.manager,
                                                                 container=self.params_panel)

        self.params_panel_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 15, 220, 20),
                                                              text='Change Heuristic Rewards', manager=self.manager,
                                                              container=self.params_panel)

        self.computer_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(55, 50, 80, 20), text='Computer',
                                                          manager=self.manager, container=self.options_panel)

        self.player_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(355, 50, 80, 20), text='Player',
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
        self.build_params_fields()
        self.options_panel.hide()
        self.params_panel.hide()
        if self.computer_options.selected_option == 'AI Easy':
            self.change_params_button.disable()

    def build_option_setters(self, computer_starting_option='AI Easy',
                             player_starting_option='Human', board_changer_starting_option='19 by 19'):

        self.computer_options = pygame_gui.elements.UIDropDownMenu(
            options_list=['AI Easy', 'AI Medium', 'AI Hard'], starting_option=computer_starting_option,
            relative_rect=pygame.Rect(40, 70, 110, 30), manager=self.manager, container=self.options_panel)

        self.player_options = pygame_gui.elements.UIDropDownMenu(
            options_list=['Human'], starting_option=player_starting_option,
            relative_rect=pygame.Rect(340, 70, 110, 30), manager=self.manager, container=self.options_panel)

        self.board_size_changer = pygame_gui.elements.UIDropDownMenu(
            options_list=['11 by 11', '15 by 15', '19 by 19'], starting_option=board_changer_starting_option,
            relative_rect=pygame.Rect(195, 40, 100, 30), manager=self.manager, container=self.options_panel)

        self.computer_selected_option = self.computer_options.selected_option
        self.player_selected_option = self.player_options.selected_option
        self.board_size_changer_selected_option = self.board_size_changer.selected_option

    def reset_options_panel_choices(self):
        if self.hints_enabled:
            self.hints_label.set_text('Hints Enabled')
            self.hints_button.set_text('Disable')
        else:
            self.hints_label.set_text('Hints Disabled')
            self.hints_button.set_text('Enable')
        self.computer_options.kill()
        self.player_options.kill()
        self.board_size_changer.kill()
        self.build_option_setters(self.computer_selected_option,
                                  self.player_selected_option, self.board_size_changer_selected_option)

    def confirm_changes(self):
        self.computer_selected_option = self.computer_options.selected_option
        if self.computer_selected_option != 'AI Easy':
            self.change_params_button.enable()
        else:
            self.change_params_button.disable()
        self.player_selected_option = self.player_options.selected_option
        self.board_size_changer_selected_option = self.board_size_changer.selected_option
        self.hints_enabled = True if self.hints_button.text == 'Disable' else False
        self.computer_options.kill()
        self.player_options.kill()
        self.board_size_changer.kill()
        self.build_option_setters(self.computer_selected_option,
                                  self.player_selected_option,
                                  self.board_size_changer_selected_option)

    def cancel_changes(self):
        self.computer_options.kill()
        self.player_options.kill()
        self.board_size_changer.kill()
        self.reset_options_panel_choices()

    def build_params_fields(self):
        param_identifiers = ['5, computer', '4, computer, open-both', '4, computer, open', '4, player, open-both',
                             '4, player, open', '3, computer', '3, player', '2, computer']
        for i in range(0, 8):
            self.param_labels_list.append(pygame_gui.elements.UILabel(relative_rect=pygame.Rect(15, 55 + 55 * i,
                                                                                                220, 20),
                                                                      text=str(i+1) + ') ' + param_identifiers[i],
                                                                      manager=self.manager,
                                                                      container=self.params_panel))
            self.param_fields_list.append(pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(30, 80 + 55 * i,
                                                                                                        180, 20),
                                                                              manager=self.manager,
                                                                              container=self.params_panel))
            self.param_fields_list[i].set_text(str(self.params_list[i]))

    def confirm_params(self):
        params_are_correct = True
        erase_wrong_params = []
        new_params = []
        for i in range(0, 8):
            try:
                new_params.append(int(self.param_fields_list[i].get_text()))
            except ValueError:
                try:
                    new_params.append(float(self.param_fields_list[i].get_text()))
                except ValueError:
                    params_are_correct = False
                    erase_wrong_params.append(i)
        if params_are_correct:
            for i in range(0, 8):
                self.params_list[i] = new_params[i]
                self.param_fields_list[i].set_text(str(self.params_list[i]))
            return True
        else:
            for index in erase_wrong_params:
                self.param_fields_list[index].set_text("")
                self.param_fields_list[index].redraw()
            return False

    def cancel_params(self):
        for i in range(0, 8):
            self.param_fields_list[i].set_text(str(self.params_list[i]))
            self.param_fields_list[i].redraw()

    def open_options_panel(self):
        self.options_panel.show()
        self.change_params_button.disable()
        self.options_button.disable()

    def close_options_panel(self):
        if self.computer_selected_option != 'AI Easy':
            self.change_params_button.enable()
        self.options_button.enable()
        self.options_panel.hide()

    def open_params_panel(self):
        self.params_panel.show()
        self.change_params_button.disable()
        self.options_button.disable()

    def close_params_panel(self):
        self.change_params_button.enable()
        self.options_button.enable()
        self.params_panel.hide()
