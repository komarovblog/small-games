# Сапер - игра с квадратным полем
# ■
# □
# ✸

import random
from random import *


# Класс - Поле
class Field():
    def __init__(self, size: int = 10, total_bomb: int = 10):
        self.size = size
        self.total_bomb = total_bomb
        self.where_bomb = {}
        self.field = []
        self.public_field = []

    # Метод - создает поле
    def create_field(self):
        """ Создает игровое поле по указанному размеру.
        """
        for row in range(self.size):
            self.field.append([])
            for col in range(self.size):
                 self.field[row].append("_")
                
    # Метод - создает публичное поле
    def create_public_field(self):
        """ Создает публичное игровое поле, которое видят игроки.
        """
        for row in range(self.size):
            self.public_field.append([])
            for col in range(self.size):
                 self.public_field[row].append("■")               

    # Метод - расставляет бомбы
    def place_bombs(self):
        """ Рандомно раставляет бомбы по полю.
        """
        for bomb in range(self.total_bomb):
            y = int(randint(0, self.total_bomb - 1))
            x = int(randint(0, self.total_bomb - 1))
            if self.field[y][x] != "✸":
                self.field[y][x] = "✸"

    # Метод - расставляет цифры
    def place_numbers(self):
        """ Проходит по ячейкам и считает кол-во бомб вокруг.
        """
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        for row in range(len(self.field)):
            for col in range(len(self.field[row])):
                count = 0   
                if self.field[row][col] =="✸":
                    continue

                for d in directions:
                    check_i = row + d[0]
                    check_z = col + d[1]

                    if check_i  >= self.size or check_i < 0:
                        continue
                    if check_z  >= self.size or check_z < 0:
                        continue
                    if self.field[check_i][check_z] == "✸":
                        count = count + 1           
                    
                self.field[row][col] = count

    # Метод показыавет публичную часть
    def show_public_field(self):
        """ Выводит публичную часть поля на экран.
        """
        for row in self.public_field:
            sep = "|"
            print([str(i) for i in row])

   # Метод показыавет скрую часть поля
    def show_field(self):
        """
        Метод показыавет скрую часть поля.
        """
        for row in self.field:
            sep = "|"
            print([str(i) for i in row])


# Класс - Ход и Проверка:
class MoveAndCheck():
    def __init__(self, obj_field: Field):
        self.obj_field = obj_field
    
    # Метод - Ход
    def move(self) -> dict:
        """ Делает ход
        """ 
        while True:
            try:
                row = int(input("Ведите номер строки:"))
                break
            except:
                print("Введи число:")
                continue

        while True:
            try:
                col = int(input("Ведите номер столбца:"))
                break
            except:
                print("Введи число:")
                continue
        return {"row": row, "col": col}

    # Метод - Не вышли ли за рамки поля
    def check_out_field(self, move) -> bool:
        """ Проверяет не вышли ли за рамки поля.
        """   
        row = move["row"]
        col = move["col"]
        if row < 0 or col < 0 or row >= self.obj_field.size or col >= self.obj_field.size:
            print("Вы вышли за пределы поля.")
            return False
        return True

    # Метод - Не было ли хода туда
    def check_move_was_made(self, move) -> bool:
        """ Проверяет не было ли хода туда
        """   
        row = move["row"]
        col = move["col"]
        if self.obj_field.public_field[row][col] != "■":
            print("Туда уже ходили, выберите другую точку")
            return False
        return True           

    # Метод - Если ход обычный, не стоит ли бомба
    def check_a_bomb(self, move) -> bool:
        """ Проверяет, если ход обычный, не стоит ли бомба
        """   
        row = move["row"]
        col = move["col"]
        if self.obj_field.field[row][col] == "✸":
            print("Вы нарвались на бомбу и проиграли")
            return False
        return True     

    # Метод - Отмечает ход в публичной части поля
    def move_value(self, move: dict):
        """ Отмечает ход в публичной части поля
        """        
        row = move["row"]
        col = move["col"]
        self.obj_field.public_field[row][col] = self.obj_field.field[row][col]

    # Метод - Если в клетке - 0, то тогда сразу становятся открытыми все клетки вокруг нее, если и в какой-нибудь из них ноль, то опять открываются, пока не останется нулей, вокруг которых есть закрытые клетки.
    def check_a_zero(self, move: dict):
        """ Открывает клетки врркруг, если в той что проверено стоит 0. Рекурсия.
        """
        row = move["row"]
        col = move["col"]
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        if self.obj_field.field[row][col] == 0:
            
            for d in directions:
                check_row = row + d[0]
                check_col = col + d[1]                 

                if check_row >= self.obj_field.size or check_col >= self.obj_field.size:
                    continue
                if check_row < 0 or check_col < 0:  
                    continue

                if self.obj_field.public_field[check_row][check_col] == "■":
                    self.obj_field.public_field[check_row][check_col] = self.obj_field.field[check_row][check_col]

                    if self.obj_field.field[check_row][check_col] == 0:
                        self.check_a_zero({"row": check_row, "col": check_col})

    # Метод - Проверяет не закончена ли игра (открыты все клетки кроме бомб)
    def check_the_winnings(self)  -> bool:
        """ Проверяет не закончена ли игра (открыты все клетки кроме бомб)
        """
        count = 0
        count_end = self.obj_field.size**2 - self.obj_field.total_bomb
        for i in range (len(self.obj_field.public_field)):
            for z in range (len(self.obj_field.public_field)):
                if self.obj_field.public_field[i][z] != "■":
                    count = count + 1
        
        if count == count_end:
            print("Вы выйграли")
            return False
        return True


# ИГРА

field = Field()
field.create_field()
field.create_public_field()
field.place_bombs()
field.place_numbers()

play = MoveAndCheck(field)

while True:
    new_muve = play.move()
    if not play.check_out_field(new_muve):
        continue
    if not play.check_move_was_made(new_muve):
        continue       
    if not play.check_a_bomb(new_muve):
        break
    play.move_value(new_muve)
    play.check_a_zero(new_muve)
    if not play.check_the_winnings():
        field.show_field()
        break
    field.show_public_field()