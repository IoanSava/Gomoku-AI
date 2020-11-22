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
        self.__assign_stones()
        self.__current_turn = 'B'  # black has the first turn

    def __initialize_board(self, board_size):
        self.__board = [['-'] * board_size for _ in range(0, board_size)]

    def __assign_stones(self):
        random.shuffle(STONES)
        self.__player_stone, self.__computer_stone = STONES

    def __is_position_outside_of_the_board(self, position):
        x, y = position
        return x < 0 or y < 0 or x > self.__board_size - 1 or y > self.__board_size - 1

    def __is_valid_move(self, position):
        if self.__is_position_outside_of_the_board(position):
            return False

        x, y = position
        if self.__board[x][y] != '-':
            return False

        return True

    def __put_stone(self, position, stone):
        x, y = position
        self.__board[x][y] = stone

    def __get_max_chain_length(self, position, direction):
        chain_length = 1

        current_position = tuple(map(operator.add, position, direction))
        while not self.__is_position_outside_of_the_board(current_position):
            x, y = current_position
            current_stone = self.__board[x][y]
            if current_stone == self.__current_turn:
                chain_length += 1
            else:
                break

            current_position = tuple(map(operator.add, current_position, direction))

        current_position = tuple(map(operator.sub, position, direction))
        while not self.__is_position_outside_of_the_board(current_position):
            x, y = current_position
            current_stone = self.__board[x][y]
            if current_stone == self.__current_turn:
                chain_length += 1
            else:
                break

            current_position = tuple(map(operator.sub, current_position, direction))

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

    def __player_move(self):
        print('Player move: ', end='')
        i, j = [int(element) for element in input().split()]

        while not self.__is_valid_move((i, j)):
            print('Invalid move. Try again: ', end='')
            i, j = [int(element) for element in input().split()]

        self.__put_stone((i, j), self.__player_stone)

    def __computer_move(self):
        print('Computer move')
        i, j = random.randint(0, self.__board_size - 1), random.randint(0, self.__board_size - 1)

        while not self.__is_valid_move((i, j)):
            i, j = random.randint(0, self.__board_size - 1), random.randint(0, self.__board_size - 1)

        self.__put_stone((i, j), self.__computer_stone)

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

    def play(self):
        total_stones = 0
        self.__print_stones()
        pprint.pprint(self.__board)

        while True:
            if self.__current_turn == self.__player_stone:
                self.__player_move()
            else:
                self.__computer_move()

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
