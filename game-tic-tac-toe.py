# Крестики Нолики - игра с произвольным размером поля

# Класс - Поле
class Field():
    def __init__(self, size: int, line_win: int):
        self.size = size
        self.line_win = line_win
        self.game_board = []

    def create_game_board(self) -> list:
        """ Создаетр игровое поле по указанному размеру.
        """ 
        for row in range(self.size):
            self.game_board.append([])
            for col in range(self.size):
                self.game_board[row].append(8)
        return self.game_board

    def show_game_board(self):
        """ Показывает поле.
        """ 
        count = 0
        for row in (self.game_board):
            print (f"{count} {row}")
            count = count + 1

    def check_a_move(self, coordinates: dict, symbol: str) -> bool:
        """ Проверяет, свободна ли координата.
        """ 
        if self.game_board[coordinates["y"]][coordinates["z"]] == 8:
            self.game_board[coordinates["y"]][coordinates["z"]] = symbol
            print("Ход принят")
            return True
        else:
            print("Там уже занято")
            return False

    def check_the_winnings(self, coordinates: dict, symbol: str) -> bool:
        """ После хода проверяет не выйграл ли игрок по одному из четырех напрвлений.
        """       
        vertikal = 0
        dott_ver = coordinates["z"]
        for i in range(self.size):
            if self.game_board[i][dott_ver] == symbol:
                vertikal = vertikal + 1
        print(vertikal)
        if vertikal == self.line_win:
            print("Игрок выйграл по ветикали.")
            return True


        gorizont = 0
        dott_gor = coordinates["y"]
        for i in range(self.size):
            if self.game_board[dott_gor][i] == symbol:
                gorizont = gorizont + 1
        print(gorizont)
        if gorizont == self.line_win:
            print("Игрок выйграл по горизонту.")
            return True


        # 1, -1  &  -1, 1
        diagonally_1 = 1
        offset_y = coordinates["y"]
        offset_z = coordinates["z"]       
        while offset_y < self.size - 1 and offset_z > 0:
            if self.game_board[offset_y + 1][offset_z - 1] == symbol:
                diagonally_1 = diagonally_1 + 1
            offset_y = offset_y + 1
            offset_z = offset_z - 1

        offset_y = coordinates["y"]
        offset_z = coordinates["z"]       
        while offset_y > 0 and offset_z < self.size - 1:
            if self.game_board[offset_y - 1][offset_z + 1] == symbol:
                diagonally_1 = diagonally_1 + 1
            offset_y = offset_y - 1
            offset_z = offset_z + 1

        if diagonally_1 == self.line_win:
            print("Игрок выйграл по первой горизонтали.")
            return True


        # 1, 1  &  -1, -1
        diagonally_2 = 1
        offset_y = coordinates["y"]
        offset_z = coordinates["z"]       
        while offset_y < self.size - 1 and offset_z < self.size - 1:
            if self.game_board[offset_y + 1][offset_z + 1] == symbol:
                diagonally_2 = diagonally_2 + 1
            offset_y = offset_y + 1
            offset_z = offset_z + 1

        offset_y = coordinates["y"]
        offset_z = coordinates["z"]       
        while offset_y > 0 and offset_z > 0:
            if self.game_board[offset_y - 1][offset_z - 1] == symbol:
                diagonally_2 = diagonally_2 + 1
            offset_y = offset_y - 1
            offset_z = offset_z - 1

        if diagonally_2 == self.line_win:
            print("Игрок выйграл по второй горизонтали.")
            return True
        
        return False

# Класс - Игрок
class Player():
    def __init__(self):
        self.player_code = None
        self.name = input ("Введите ваше имя")

    def select_symbol(self): 
        """ Присваивает игроку символ которым он будет играть
        """
        stop_while = False  
        while stop_while == False:
            self.player_code = input("Введите только X или O")

            if self.player_code != "X" and self.player_code != "O":
                pass
            elif self.player_code == "X" or self.player_code == "O":
                stop_while = True

    def make_a_move(self) -> dict:
        """ Делает ход по заданным пользователем координатам
        """
        y = input("Введите номер строки")
        z = input("Введите номер стотлбца")
        return {"y": int(y), "z": int(z)}


# ИГРА

field_obj = Field(2, 2)
field_obj.create_game_board()

player_1 = Player()
player_2 = Player()

player_1.select_symbol()
if player_1.player_code == "X":
        player_2.player_code = "O"
elif player_1.player_code == "O":
        player_2.player_code = "X"


stop_level_1 = False
while stop_level_1 == False:

    stop_level_2 = False
    while stop_level_2 == False:
        print (f"Ходит игрок {player_1.name} ваш символ - {player_1.player_code} ")
        move = player_1.make_a_move()
        stop_level_2 = field_obj.check_a_move(move, player_1.player_code)
        if stop_level_2 == True:
            field_obj.show_game_board()
            stop_level_1 = field_obj.check_the_winnings(move, player_1.player_code)
            if stop_level_1 == True:
                break
    if stop_level_1 == True: # Выход из вложенного цикла
        break


    stop_level_2 = False
    while stop_level_2 == False:
        print (f"Ходит игрок {player_2.name} ваш символ - {player_2.player_code} ")
        move = player_2.make_a_move()
        stop_level_2 = field_obj.check_a_move(move, player_2.player_code)
        if stop_level_2 == True:
            field_obj.show_game_board()
            stop_level_1 = field_obj.check_the_winnings(move, player_2.player_code)
            if stop_level_1 == True:
                break
    if stop_level_1 == True: # Выход из вложенного цикла
        break