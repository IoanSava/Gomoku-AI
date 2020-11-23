import operator
import pprint
import sys
import random

DIRECTIONS = [(0, 1), (1, -1), (1, 0), (1, 1)]
STONES = ['B', 'W']


class Game:
    def __init__(self, board_size):
        self.__board_size = board_size
        self.__initialize_board(board_size)
        self.__current_turn = 'B'  # black has the first turn

    def __initialize_board(self, board_size):
        self.__board = [['-'] * board_size for _ in range(0, board_size)]

    def __is_position_outside_of_the_board(self, position):
        x, y = position
        return x < 0 or y < 0 or x > self.__board_size - 1 or y > self.__board_size - 1

    def __is_valid_move(self, position):
        x, y = position
        return not self.__is_position_outside_of_the_board(position) and self.__board[x][y] == '-'

    def __put_stone(self, position, stone):
        x, y = position
        self.__board[x][y] = stone

    def __get_chain_length(self, position, direction, direction_operator):
        chain_length = 0
        
        current_position = tuple(map(direction_operator, position, direction))
        while not self.__is_position_outside_of_the_board(current_position):
            x, y = current_position
            current_stone = self.__board[x][y]
            if current_stone == self.__current_turn:
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

    def __check_winner(self):
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                if self.__board[i][j] == self.__current_turn:
                    if self.__check_five_in_a_row((i, j)):
                        return True

        return False

    def __player_move(self, stone):
        print('Player move -', stone, ': ', end='')
        i, j = [int(element) for element in input().split()]

        while not self.__is_valid_move((i, j)):
            print('Invalid move. Try again: ', end='')
            i, j = [int(element) for element in input().split()]

        self.__put_stone((i, j), stone)

    def __computer_move(self, stone):
        print('Computer move -', stone)
        i, j = random.randint(0, self.__board_size - 1), random.randint(0, self.__board_size - 1)

        while not self.__is_valid_move((i, j)):
            i, j = random.randint(0, self.__board_size - 1), random.randint(0, self.__board_size - 1)

        self.__put_stone((i, j), stone)

    def __print_stones(self):
        print('Player:', self.__player_stone, '| Computer:', self.__computer_stone)

    def __switch_turn(self):
        if self.__current_turn == 'B':
            self.__current_turn = 'W'
        else:
            self.__current_turn = 'B'

    def __print_winner(self):
        if self.__current_turn == self.__player_stone:
            print('Player won')
        else:
            print('Computer won')

    def __first_turn_for_player(self):
        pprint.pprint(self.__board)
        self.__player_move('B')
        pprint.pprint(self.__board)
        self.__player_move('W')
        pprint.pprint(self.__board)
        self.__player_move('B')
        pprint.pprint(self.__board)

    def __first_turn_for_computer(self):
        self.__computer_move('B')
        self.__computer_move('W')
        self.__computer_move('B')
        pprint.pprint(self.__board)

    def __first_turn(self, is_player_turn):
        if is_player_turn:
            self.__first_turn_for_player()
        else:
            self.__first_turn_for_computer()

    def __print_second_turn_options(self):
        print('1. Choose white and put the 4th stone')
        print('2. Swap and control the black stones')
        print(
            '3. Put two more stones (one black and one white stone) and pass the opportunity to choose colour to the opponent')

    def __get_second_turn_player_choice(self):
        print('Your choice (1-3): ', end='')
        choice = int(input())

        while choice < 1 or choice > 3:
            print('Invalid choice. Choose again (1-3): ', end='')
            choice = int(input())

        return choice

    def __second_turn_for_player(self):
        print('Choose your action:')
        self.__print_second_turn_options()

        choice = self.__get_second_turn_player_choice()
        if choice == 1:
            self.__player_stone = 'W'
            self.__computer_stone = 'B'
        elif choice == 2:
            self.__player_stone = 'B'
            self.__computer_stone = 'W'
        else:
            self.__player_move('B')
            pprint.pprint(self.__board)
            self.__player_move('W')
            pprint.pprint(self.__board)

        return choice

    def __second_turn_for_computer(self):
        choice = random.randint(1, 3)
        if choice == 1:
            self.__player_stone = 'B'
            self.__computer_stone = 'W'
        elif choice == 2:
            self.__player_stone = 'W'
            self.__computer_stone = 'B'
        else:
            self.__computer_move('B')
            self.__computer_move('W')
            pprint.pprint(self.__board)

        return choice

    def __second_turn(self, is_player_turn):
        if is_player_turn:
            return self.__second_turn_for_player()
        else:
            return self.__second_turn_for_computer()

    def __third_turn_for_player(self):
        print('Choose colour (B or W): ', end='')
        colour = input()
        while colour not in STONES:
            print('Invalid colour. Try again (B or W): ', end='')
            colour = input()

        if colour == 'B':
            self.__player_stone = 'B'
            self.__computer_stone = 'W'
        else:
            self.__player_stone = 'W'
            self.__computer_stone = 'B'

    def __third_turn_for_computer(self):
        random.shuffle(STONES)
        colour = STONES[0]

        if colour == 'B':
            self.__player_stone = 'W'
            self.__computer_stone = 'B'
        else:
            self.__player_stone = 'B'
            self.__computer_stone = 'W'

    def __third_turn(self, is_player_turn):
        if is_player_turn:
            self.__third_turn_for_player()
        else:
            self.__third_turn_for_computer()

    def play(self):
        is_player_turn = bool(random.getrandbits(1))
        self.__first_turn(is_player_turn)
        total_stones = 3

        second_turn_choice = self.__second_turn(not is_player_turn)
        if second_turn_choice == 3:
            total_stones += 2
            self.__third_turn(is_player_turn)

        self.__current_turn = 'W'

        self.__print_stones()
        pprint.pprint(self.__board)

        while True:
            if self.__current_turn == self.__player_stone:
                self.__player_move(self.__player_stone)
            else:
                self.__computer_move(self.__computer_stone)

            self.__print_stones()
            pprint.pprint(self.__board)

            if self.__check_winner():
                self.__print_winner()
                break

            total_stones += 1
            if total_stones == self.__board_size * self.__board_size:
                print('Draw')
                break

            self.__switch_turn()


if __name__ == '__main__':
    n = int(sys.argv[1])
    game = Game(n)
    game.play()
