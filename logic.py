import operator
import random

DIRECTIONS = [(0, 1), (1, -1), (1, 0), (1, 1)]
STONES = ['B', 'W']


class Game:
    def __init__(self, board):
        self.board = board
        self.total_stones = 0
        self.playing = False
        self.win = False
        self.is_player_turn = bool(random.getrandbits(1))
        self.current_turn = 'W'
        self.turn = 1
        self.player_stone, self.computer_stone = '', ''
        self.winner = ''

    def __is_position_outside_of_the_board(self, position):
        row, col = position
        return row < 0 or col < 0 or row > self.board.BOARD_SIZE or col > self.board.BOARD_SIZE

    def is_valid_move(self, position):
        row, col = position
        return not self.__is_position_outside_of_the_board(position) and self.board.grid[row][col] == '-'

    def __put_stone(self, position, stone):
        row, col = position
        self.board.grid[row][col] = stone

    def __get_chain_length(self, position, direction, direction_operator):
        chain_length = 0

        current_position = tuple(map(direction_operator, position, direction))
        while not self.__is_position_outside_of_the_board(current_position):
            row, col = current_position
            current_stone = self.board.grid[row][col]
            if current_stone == self.current_turn:
                chain_length += 1
            else:
                return chain_length

            current_position = tuple(map(direction_operator, current_position, direction))

        return chain_length

    def __get_max_chain_length(self, position, direction):
        chain_length = 1
        chain_length += self.__get_chain_length(position, direction, operator.add)
        chain_length += self.__get_chain_length(position, direction, operator.sub)

        return chain_length

    def __check_five_in_a_row(self, position):
        for direction in DIRECTIONS:
            if self.__get_max_chain_length(position, direction) == 5:
                return True

        return False

    def check_winner(self):
        for i in range(self.board.BOARD_SIZE + 1):
            for j in range(self.board.BOARD_SIZE + 1):
                if self.board.grid[i][j] == self.current_turn:
                    if self.__check_five_in_a_row((i, j)):
                        return True

        return False

    def __computer_move(self, stone):
        i, j = random.randint(0, self.board.BOARD_SIZE), random.randint(0, self.board.BOARD_SIZE)

        while not self.is_valid_move((i, j)):
            i, j = random.randint(0, self.board.BOARD_SIZE), random.randint(0, self.board.BOARD_SIZE)

        self.__put_stone((i, j), stone)

    def switch_turn(self):
        if self.current_turn == 'B':
            self.current_turn = 'W'
        else:
            self.current_turn = 'B'

    def __first_turn_for_computer(self):
        self.__computer_move('B')
        self.__computer_move('W')
        self.__computer_move('B')

    def first_turn_for_player(self, position):
        if self.is_player_turn and self.total_stones < 3:
            if self.is_valid_move(position):
                row, col = position
                self.board.last_position = [row, col]
                if self.total_stones == 1:
                    self.__put_stone(position, 'W')
                else:
                    self.__put_stone(position, 'B')

                self.total_stones += 1
                if self.total_stones == 3:
                    self.turn = 2
                    self.is_player_turn = False
                    self.__second_turn_for_computer()

    def first_turn(self):
        if not self.is_player_turn:
            self.__first_turn_for_computer()
            self.total_stones = 3
            self.turn = 2
            self.is_player_turn = True

    def second_turn_for_player(self, position, mouse_position):
        if self.is_player_turn:

            if self.total_stones < 4:
                color = 'B' if self.board.mouse_in_black(mouse_position) else 'W' if self.board.mouse_in_white(
                    mouse_position) else ''

                if color == 'W':
                    self.player_stone = 'W'
                    self.computer_stone = 'B'
                elif color == 'B':
                    self.player_stone = 'B'
                    self.computer_stone = 'W'
                    self.computer_turn()

            if self.player_stone == '':
                if self.is_valid_move(position):
                    row, col = position
                    self.board.last_position = [row, col]

                    if self.total_stones == 3:
                        self.__put_stone(position, 'B')
                        self.total_stones += 1
                    else:
                        self.__put_stone(position, 'W')
                        self.total_stones += 1
                        self.turn = 3
                        self.is_player_turn = False
                        self.__third_turn_for_computer()
            else:
                self.turn = 4

    def __second_turn_for_computer(self):
        if not self.is_player_turn:
            choice = random.randint(1, 3)
            if choice == 1:
                self.player_stone = 'B'
                self.computer_stone = 'W'
                self.computer_turn()
            elif choice == 2:
                self.player_stone = 'W'
                self.computer_stone = 'B'
            else:
                self.__computer_move('B')
                self.__computer_move('W')

            if choice == 3:
                self.total_stones += 2
                self.turn = 3
            else:
                self.turn = 4

            self.is_player_turn = True

    def third_turn_for_player(self, mouse_position):
        if self.is_player_turn:

            color = 'B' if self.board.mouse_in_black(mouse_position) else 'W' if self.board.mouse_in_white(
                mouse_position) else ''
            if color == 'B':
                self.player_stone = 'B'
                self.computer_stone = 'W'
            elif color == 'W':
                self.player_stone = 'W'
                self.computer_stone = 'B'

            if color != '':
                self.turn = 4
                self.computer_turn()

    def __third_turn_for_computer(self):
        if not self.is_player_turn:
            random.shuffle(STONES)
            colour = STONES[0]

            if colour == 'B':
                self.player_stone = 'W'
                self.computer_stone = 'B'
            else:
                self.player_stone = 'B'
                self.computer_stone = 'W'
                self.computer_turn()

            self.turn = 4

    def computer_turn(self):
        if self.current_turn == self.computer_stone:
            self.__computer_move(self.computer_stone)

            if self.check_winner():
                self.game_over()
                self.winner = 'C'
            else:
                self.total_stones += 1
                if self.total_stones == self.board.BOARD_SIZE * self.board.BOARD_SIZE:
                    self.game_over()
                else:
                    self.switch_turn()

    def player_turn(self, position):
        if self.current_turn == self.player_stone:
            if self.is_valid_move(position):
                row, col = position
                self.board.last_position = [row, col]
                self.board.grid[row][col] = self.player_stone

                if self.check_winner():
                    self.game_over()
                    self.winner = 'P'
                else:
                    self.total_stones += 1
                    if self.total_stones == self.board.BOARD_SIZE * self.board.BOARD_SIZE:
                        self.win = True
                        self.playing = False
                    else:
                        self.switch_turn()
                        self.computer_turn()

    def reset(self):
        self.board.reset()
        self.total_stones = 0
        self.playing = True
        self.win = False
        self.is_player_turn = bool(random.getrandbits(1))
        self.turn = 1
        self.winner = ''
        self.player_stone, self.computer_stone = '', ''
        self.current_turn = 'W'

    def game_over(self):
        self.playing = False
        self.win = True
