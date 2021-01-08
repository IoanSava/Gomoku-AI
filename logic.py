import operator
import random
import sys

DIRECTIONS = [(0, 1), (1, -1), (1, 0), (1, 1)]
STONES = ['B', 'W']
INF = sys.maxsize
EASY_DIFFICULTY = 'AI Easy'
MEDIUM_DIFFICULTY = 'AI Medium'


class Game:
    def __init__(self, board, difficulty, hints):
        self.board = board
        self.difficulty = difficulty
        self.total_stones = 0
        self.playing = False
        self.win = False
        self.is_player_turn = bool(random.getrandbits(1))
        self.current_turn = 'W'
        self.turn = 1
        self.player_stone, self.computer_stone = '', ''
        self.winner = ''
        self.hints = hints

    def __is_position_outside_of_the_board(self, position):
        row, col = position
        return row < 0 or col < 0 or row > self.board.BOARD_SIZE or col > self.board.BOARD_SIZE

    def is_valid_move(self, position):
        row, col = position
        return not self.__is_position_outside_of_the_board(position) and self.board.grid[row][col] == '-'

    def __put_stone(self, position, stone):
        row, col = position
        self.board.grid[row][col] = stone

    def __get_chain_length(self, position, direction, direction_operator, stone):
        chain_length = 0

        last_position = position
        current_position = tuple(map(direction_operator, position, direction))
        while not self.__is_position_outside_of_the_board(current_position):
            row, col = current_position
            current_stone = self.board.grid[row][col]
            if current_stone == stone:
                chain_length += 1
            else:
                return chain_length, last_position

            last_position = current_position
            current_position = tuple(map(direction_operator, current_position, direction))

        return chain_length, last_position

    def __get_max_chain_length(self, position, direction, stone):
        chain_length = 1
        chain_length += self.__get_chain_length(position, direction, operator.add, stone)[0]
        chain_length += self.__get_chain_length(position, direction, operator.sub, stone)[0]

        return chain_length

    def __check_five_in_a_row(self, position, stone):
        for direction in DIRECTIONS:
            if self.__get_max_chain_length(position, direction, stone) == 5:
                return True

        return False

    def __check_if_exists_one_open_row_with_n_stones(self, n, stone, both_ends=True):
        for i in range(self.board.BOARD_SIZE + 1):
            for j in range(self.board.BOARD_SIZE + 1):
                if self.board.grid[i][j] == stone:
                    for direction in DIRECTIONS:
                        if self.__get_max_chain_length((i, j), direction, stone) == n:
                            position_1 = self.__get_chain_length((i, j), direction, operator.add, stone)[1]
                            position_1 = tuple(map(operator.add, position_1, direction))

                            position_2 = self.__get_chain_length((i, j), direction, operator.sub, stone)[1]
                            position_2 = tuple(map(operator.sub, position_2, direction))

                            if not self.__is_position_outside_of_the_board(position_1) and \
                                    not self.__is_position_outside_of_the_board(position_2):
                                tile1 = self.board.grid[position_1[0]][position_1[1]]
                                tile2 = self.board.grid[position_2[0]][position_2[1]]
                                if both_ends:
                                    if tile1 == '-' and tile2 == '-':
                                        return True
                                else:
                                    if tile1 == '-' or tile2 == '-':
                                        return True
        return False

    def __check_if_move_forms_two_open_rows_of_three_stones(self, position, stone):
        for direction in DIRECTIONS:
            if self.__get_max_chain_length(position, direction, stone) == 3:
                position1 = self.__get_chain_length(position, direction, operator.add, stone)[1]
                position1 = tuple(map(operator.add, position1, direction))

                position2 = self.__get_chain_length(position, direction, operator.sub, stone)[1]
                position2 = tuple(map(operator.sub, position2, direction))

                if not self.__is_position_outside_of_the_board(position1) and \
                        not self.__is_position_outside_of_the_board(position2):
                    tile1 = self.board.grid[position1[0]][position1[1]]
                    tile2 = self.board.grid[position2[0]][position2[1]]
                    if tile1 == '-' and tile2 == '-':
                        return self.__check_if_exists_one_open_row_with_n_stones(3, stone)

        return False

    def __check_if_exists_one_row_with_four_stones(self, stone):
        for i in range(self.board.BOARD_SIZE + 1):
            for j in range(self.board.BOARD_SIZE + 1):
                if self.board.grid[i][j] == stone:
                    for direction in DIRECTIONS:
                        if self.__get_max_chain_length((i, j), direction, stone) == 4:
                            return True

        return False

    def __check_if_move_forms_two_rows_of_four_stones(self, position, stone):
        for direction in DIRECTIONS:
            if self.__get_max_chain_length(position, direction, stone) == 4:
                return self.__check_if_exists_one_row_with_four_stones(stone)

        return False

    def __check_winner(self, stone):
        for i in range(self.board.BOARD_SIZE + 1):
            for j in range(self.board.BOARD_SIZE + 1):
                if self.board.grid[i][j] == stone:
                    if self.__check_five_in_a_row((i, j), stone):
                        return True

        return False

    def __generate_possible_moves(self, stone):
        moves = []
        for i in range(0, self.board.BOARD_SIZE + 1):
            for j in range(0, self.board.BOARD_SIZE + 1):
                if self.board.grid[i][j] == '-':
                    if not self.__check_if_move_forms_two_open_rows_of_three_stones((i, j), stone) and \
                            not self.__check_if_move_forms_two_rows_of_four_stones((i, j), stone):
                        moves.append((i, j))

        return moves

    def __heuristic(self, stone):
        score = 0
        if self.__check_winner(stone):
            score += 150_000
        if self.__check_if_exists_one_open_row_with_n_stones(4, stone):
            score += 15_000
        if self.__check_if_exists_one_open_row_with_n_stones(4, stone, False):
            score += 10_000
        if self.__check_if_exists_one_open_row_with_n_stones(4, 'B' if stone != 'B' else 'W'):
            score -= 100_000
        if self.__check_if_exists_one_open_row_with_n_stones(4, 'B' if stone != 'B' else 'W', False):
            score -= 50_000
        if self.__check_if_exists_one_open_row_with_n_stones(3, stone):
            score += 10_000
        if self.__check_if_exists_one_open_row_with_n_stones(3, 'B' if stone != 'B' else 'W'):
            score -= 12_000
        if self.__check_if_exists_one_open_row_with_n_stones(2, stone):
            score += 1_000

        return score

    def __max_value(self, alfa, beta, current_depth, max_depth):
        if current_depth >= max_depth or self.__check_winner(self.player_stone):
            return [], self.__heuristic(self.player_stone)

        val_max = -INF
        optimal_move = []
        moves = self.__generate_possible_moves(self.computer_stone)
        for move in moves:
            self.board.grid[move[0]][move[1]] = self.computer_stone
            new_move, move_value = self.__min_value(alfa, beta, current_depth + 1, max_depth)
            self.board.grid[move[0]][move[1]] = '-'

            if val_max < move_value:
                val_max = move_value
                optimal_move = move

            if val_max >= beta:
                return optimal_move, val_max

            alfa = max(val_max, alfa)

        return optimal_move, val_max

    def __min_value(self, alfa, beta, current_depth, max_depth):
        if current_depth >= max_depth or self.__check_winner(self.computer_stone):
            return [], self.__heuristic(self.computer_stone)

        val_min = INF
        optimal_move = []
        moves = self.__generate_possible_moves(self.player_stone)
        for move in moves:
            self.board.grid[move[0]][move[1]] = self.player_stone
            new_move, move_value = self.__max_value(alfa, beta, current_depth + 1, max_depth)
            self.board.grid[move[0]][move[1]] = '-'

            if val_min > move_value:
                val_min = move_value
                optimal_move = move

            if alfa >= val_min:
                return optimal_move, val_min

            beta = min(val_min, beta)

        return optimal_move, val_min

    def __minimax_alfa_beta(self, max_depth):
        move, _ = self.__max_value(-INF, INF, 0, max_depth)
        return move

    def __bfs(self, stone):
        moves = []
        for i in range(0, self.board.BOARD_SIZE + 1):
            for j in range(0, self.board.BOARD_SIZE + 1):
                if self.board.grid[i][j] == stone:
                    for direction in DIRECTIONS:
                        new_i, new_j = i + direction[0], j + direction[1]
                        if self.is_valid_move((new_i, new_j)) and \
                                not self.__check_if_move_forms_two_open_rows_of_three_stones((new_i, new_j), stone) and \
                                not self.__check_if_move_forms_two_rows_of_four_stones((new_i, new_j), stone):
                            moves.append((new_i, new_j))

                        new_i, new_j = i - direction[0], j - direction[1]
                        if self.is_valid_move((new_i, new_j)) and \
                                not self.__check_if_move_forms_two_open_rows_of_three_stones((new_i, new_j), stone) and \
                                not self.__check_if_move_forms_two_rows_of_four_stones((new_i, new_j), stone):
                            moves.append((new_i, new_j))

        return moves

    def __best_bfs_move(self, stone):
        moves = self.__bfs(stone)
        if len(moves) == 0:
            return random.randint(0, self.board.BOARD_SIZE), random.randint(0, self.board.BOARD_SIZE)

        best_score = -INF
        best_move = ()
        for move in moves:
            self.board.grid[move[0]][move[1]] = stone
            score = self.__heuristic(stone)
            if score > best_score:
                best_score = score
                best_move = move
            self.board.grid[move[0]][move[1]] = '-'

        return best_move

    def __computer_move(self, stone):
        if self.difficulty == EASY_DIFFICULTY or self.turn < 4:
            i, j = random.randint(0, self.board.BOARD_SIZE), random.randint(0, self.board.BOARD_SIZE)
        elif self.difficulty == MEDIUM_DIFFICULTY:
            i, j = self.__best_bfs_move(stone)
        else:
            i, j = self.__minimax_alfa_beta(1)

        while not self.is_valid_move((i, j)) or \
                self.__check_if_move_forms_two_open_rows_of_three_stones((i, j), self.computer_stone) or \
                self.__check_if_move_forms_two_rows_of_four_stones((i, j), self.computer_stone):
            if self.difficulty == EASY_DIFFICULTY or self.turn < 4:
                i, j = random.randint(0, self.board.BOARD_SIZE), random.randint(0, self.board.BOARD_SIZE)
            elif self.difficulty == MEDIUM_DIFFICULTY:
                i, j = self.__best_bfs_move(stone)
            else:
                i, j = self.__minimax_alfa_beta(1)

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

            if self.__check_winner(self.computer_stone):
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
            if self.is_valid_move(position) and not self.__check_if_move_forms_two_open_rows_of_three_stones(
                    position, self.player_stone) and \
                    not self.__check_if_move_forms_two_rows_of_four_stones(position, self.player_stone):
                row, col = position
                self.board.last_position = [row, col]
                self.board.grid[row][col] = self.player_stone

                if self.__check_winner(self.player_stone):
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

    def get_hints(self):
        if self.hints and self.turn > 3:
            move_score_dict = {}
            moves = self.__generate_possible_moves(self.player_stone)
            for move in moves:
                self.board.grid[move[0]][move[1]] = self.player_stone
                score = self.__heuristic(self.player_stone)
                self.board.grid[move[0]][move[1]] = '-'
                move_score_dict[move] = score
            sorted_dict = dict(
                sorted(move_score_dict.items(), key=lambda item: (item[1], item[0][0], item[0][1]), reverse=True))
            first_5_items_dict = []
            for i in range(min(5, len(sorted_dict))):
                first_5_items_dict.append(list(sorted_dict.items())[i])
            return [value[0] for value in first_5_items_dict]
        else:
            return []

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
