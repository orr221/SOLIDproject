import random


class InvalidMoveError(Exception):
    pass


class Board(object):
    def __init__(self):
        self.board = [[] for i in range(24)]

    def get_board(self):
        return self.board

    def start_board(self, sign1, sign2):
        self.board[0] = 2 * [sign1]
        self.board[5] = 5 * [sign2]
        self.board[7] = 3 * [sign2]
        self.board[11] = 5 * [sign1]
        self.board[12] = 5 * [sign2]
        self.board[16] = 3 * [sign1]
        self.board[18] = 5 * [sign1]
        self.board[23] = 2 * [sign2]

    def change_board(self, index_now, steps, sign):
        try:
            if (sign in self.board[index_now] and (
                    self.board[index_now + steps] == [] or sign in (self.board[index_now + steps]))):
                self.board[index_now] = self.board[index_now][:-1]
                self.board[index_now + steps].append(sign)
                return
            else:
                return InvalidMoveError('invalid move')
        except Exception as e:
            return e

    def change_board_level_2(self, index):
        # get valid input
        self.board[index] = self.board[index][:-1]


class Player(object):
    def __init__(self, sign, name):
        self.sign = sign
        self.name = name

    def get_sign(self):
        return self.sign

    def get_name(self):
        return self.name


class Game(object):
    def __init__(self, player1, player2, board):
        self.p1 = player1
        self.p2 = player2
        self.board = board
        self.count = -1
        self.val_cube = (0, 0)

    def player_now(self):
        self.count = self.count + 1
        if self.count % 2 == 0:
            return self.p1
        return self.p2

    def rolling_the_cubes(self):
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        self.val_cube = num1, num2
        return self.val_cube


class SpecificField(Game):
    pass

    def print_board(self):
        print_str_board(self.board.get_board())

    def turn_in_game(self, player):
        self.val_cube = self.rolling_the_cubes()
        self.print_board()
        print("cubes is: {val}. \n{name} please enter your move".format(name=player.get_name(), val=self.val_cube))
        self.make_move(player)

    def make_move(self, player):
        dict_cubes = dict_val_cubes(self.val_cube)
        while (sum(list(dict_cubes.values())) > 0):
            step = self.move_in_board(player, dict_cubes)
            dict_cubes = change_dict_val_cubes(dict_cubes, step)
            self.print_board()

    def get_move_from_user(self, player, dic_val_cubes):
        index = self.valid_index(player)
        step = self.legal_step(dic_val_cubes)
        return index, step

    def move_in_board(self, player, dic_val_cubes):
        b = " "
        while (b is not None):
            print(b)
            index, step = self.get_move_from_user(player, dic_val_cubes)
            b = self.board.change_board(index, step, player.get_sign())
        return step

    def valid_index(self, player):
        while (True):
            try:
                index = int(input("index: "))
                if (player.get_sign() in self.board.get_board()[index]):
                    return index
                else:
                    print("You don't have a player in this index")
            except Exception as e:
                print(e)

    def legal_step(self, dic_val_cubes):
        while (True):
            step = int(input("step: "))
            valid_step = check_steps(dic_val_cubes, step)
            if valid_step is False:
                print("The step is not possible")
            else:
                return step

    def game(self):
        while (True):
            player = self.player_now()
            self.turn_in_game(player)

    def level(self, player_now):
        if player_now is p1:
            if (p1.get_sign() not in self.board[:-6]):
                return 2  # level 2
            return 1  # level 1
        if (p2.get_sign() not in self.board[6:]):
            return 2
        return 1

    def play_level_2(self, index, step, player_now):
        step = step - 1
        if player_now is p2:
            if ((index == step and p2.get_sign() in self.board.get_board()[index]) or (
                    index < step and p2.get_sign() not in self.board.get_board()[index:6])):
                self.board.change_board_level_2(index)
                return True
            if index > step and p2.get_sign() in self.board.get_board()[index]:
                self.board.change_board(index, -(step + 1), player_now.get_sign())

        elif ((abs(index - 23) == step and p1.get_sign() in self.board.get_board()[index]) or (
                (abs(index - 23) + 1) < step and p1.get_sign() not in self.board.get_board()[18:index])):
            self.board.change_board_level_2(index)
            return True
        if abs(index - 23) > step and p1.get_sign() in self.board.get_board()[index]:
            self.board.change_board(index, (step + 1), p1.get_sign())
            return True

        return False


def change_dict_val_cubes(dict_cubes, step):
    if len(dict_cubes.keys()) > 1:
        try:
            dict_cubes[step]
            dict_cubes[step] = 0
        except KeyError:
            for i in list(dict_cubes.keys()):
                dict_cubes[i] = 0
    else:
        val = list(dict_cubes.keys())[0]
        dict_cubes[val] = dict_cubes[val] - int(step / val)
    return dict_cubes


def dict_val_cubes(val_cubes):
    if val_cubes[0] != val_cubes[1]:
        dict_cubes = {val_cubes[0]: 1, val_cubes[1]: 1}
    else:
        dict_cubes = {val_cubes[0]: 4}
    return dict_cubes


def check_steps_regular(dict_cubes, step):
    if ((step in dict_cubes and dict_cubes[step] != 0) or (
            step == sum(dict_cubes) and sum(list(dict_cubes.values())) == 2)):
        return True
    return False


def check_steps_when_double(dict_cubes, step):
    val = int(list(dict_cubes.keys())[0])
    if step == val and dict_cubes[step] != 0:
        return True
    if step % val == 0:
        n = int(step / val)
        if n in range(1, dict_cubes[val] + 1):
            return True
    return False


def check_steps(dic_val_cubes, step):
    if len(dic_val_cubes) > 1:
        return check_steps_regular(dic_val_cubes, step)
    return check_steps_when_double(dic_val_cubes, step)


def print_str_board(board):
    asterisk_arr = ['*' for i in range(26)]
    print(" ", end=" ")
    print(*asterisk_arr[:13])
    print_first_half_board(board[:12])
    print_second_half_board(board[12:])
    print(" ", end=" ")
    print(*asterisk_arr[13:])


def get_len(arr):
    max_l = len(arr[0])
    for i in arr[1:]:
        max_l = max(len(i), max_l)
    return max_l


def print_first_half_board(board):
    len_max = get_len(board)
    for j in range(len_max):
        print(" ", end=" ")
        for i in range(len(board)):
            if i == 6: print('|', end=" ")
            try:
                print(board[i][j], end=" ")
            except:
                print(" ", end=" ")
        print("\n")


def print_second_half_board(board):
    len_max = get_len(board)
    for j in range(len_max, -1, -1):
        for i in range(len(board), -1, -1):
            if i == 5: print('|', end=" ")
            try:
                print(board[i][j], end=" ")
            except:
                print(" ", end=" ")
        print("\n")


if __name__ == '__main__':
    b = Board()
    b.start_board("@", "#")
    p1 = Player("@", "Orr")
    p2 = Player("#", "Yohai")
    s = SpecificField(p1, p2, b)
    s.game()
