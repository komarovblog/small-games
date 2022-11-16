# Black Jack - карточная игра

# Есть дилер компьтер и игрок человек и колода 52 карты.
# У игрока есть фишки, он делает ставки.
# Далее идет игра, в начале у всех по 2 карты, у компьютера 1 карта закрыта, у игрока обе открыты.
# Каждая карта имеет свои очки, цель приблизится к 21, но нельзя перебирать.
# Можно взять карту из колоды или остаться при текущих.
# Если игрок берет карту или остается при своих картах, далее шагает дилер.
# Если у игрока перебор, то игрок проиграл.
# Дилер обязан брать карты если у енго меньше 17.
# Если у дилера больше чем у игрока то дилер выйграл.
# Если 21 то ничья.
# Все очки по своим, картинки по 10, а туз это 11 или 1, как захочет игрок.
import random


# класс Колода
class CardDeck():
    cards_in_deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    points_for_the_card = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

    def __init__(self):
        self.deck = []

    # Колода обновляется
    def new_deck(self):
        self.deck = []
        for card in self.cards_in_deck:
            for i in range(4):
                self.deck.append(card)


# класс Игрок
class Player():
    def __init__ (self, money = 500, go_home = 1000):
        self.money = money
        self.go_home = go_home
        self.cards_in_line = []
        self.point_in_line = []
        self.name = "Игрок"

    # Делает ставку
    def make_a_bet(self) -> int:
        """Проверяе кошелек и говорит сколько можно поставить, если ставка не число и если оно меньше кошелька, то повторяет вопрос. Возвращает ставку.
        """
        while True:
            try:
                result =  int(input(f"Сделайте ставку не более {self.money} рублей."))
                if result > self.money:
                    print("Крупье: У вас столько нет.")
                    continue
                else:
                    print("Крупье: Вашу ставку приняли.")
                    return result
            except:
                print("Введите число, а не текст.")

    # Берет карту или говорит стоп
    def take_card_or_say_stop(self) -> bool:
        """Игрок берет карту или говорит стоп, возвращает bool.
        """
        go = True
        while go:
            result = input("Хотите взять еще карту? Введите 'Да' или 'Нет'.")
            if result != "Да" and result != "Нет":
                print("Только 'Да' или 'Нет'")
                continue
            if result == "Да":
                go = True
                return True
            else:
                go = False
                return False

    # Ищет туз при переборе
    def check_ace_if_bust(self) -> bool:
        """Если игроку сообщили что у него перебор, он ищет туза в своих картах и меняет 11 на 1. Если не находит возвращает True
        """
        print(f"Карты у {self.name} - {self.cards_in_line}, очки {self.point_in_line} сумма очков {sum(self.point_in_line)}.")

        for index, point in enumerate(self.point_in_line):
            if point == 11:
                self.point_in_line[index] = 1
                print("Игрок: Так просто не сдаюсь, меняю туза на единицу.")
                print(f"Карты у {self.name} - {self.cards_in_line}, очки {self.point_in_line} сумма очков {sum(self.point_in_line)}.")
                return False
            
        print("Игрок: Реально перебор.")
        return True

    # Проверяет не пора ли домой
    def check_go_home(self) -> bool:
        """Если кошелек полон, то заканчивает игру
        """
        if self.money >= self.go_home or self.money == 0:
            print("Игрок: Я домой!")
            return True


# класс Крупье
class Croupier():
    def __init__(self, player: Player):
        self.player = player
        self.money = 1000000
        self.cards_in_line = []
        self.point_in_line = []
        self.name = "Крупье"

    # Открывает свои карты
    def show_croupie_cart(self):
         print(f"Карты крупье {self.cards_in_line}, очки {self.point_in_line}.")

    # Сравнивает очки и решает брать ли карту
    def compare_points(self):
        """Сравнивает свои очки с очками игрока и решает брать или не брать карту
        """
        if sum(self.point_in_line) < 17:
            print("Крупье: Меньше 17, беру еще карту")
            return True
        elif sum(self.player.point_in_line) > sum(self.point_in_line) and sum(self.point_in_line) < 21:
            print("Крупье: Беру еще карту")
            return True
        else:
            return False

    # Ищет туз при переборе
    def check_ace_if_bust(self) -> bool:
        """Если крупье видит что у него перебор, он ищет туза в своих картах и меняет 11 на 1.
        """
        print(f"Карты у {self.name} - {self.cards_in_line}, очки {self.point_in_line} сумма очков {sum(self.point_in_line)}.")
        for index, point in enumerate(self.point_in_line):
            if point == 11:
                self.point_in_line[index] = 1
                print("Крупье: Меняю туза на единицу.")
                print(f"Карты у {self.name} - {self.cards_in_line}, очки {self.point_in_line} сумма очков {sum(self.point_in_line)}.")
                return False

        print("Крупье: Реально перебор")
        return True


# класс Казино
class BlackJack():

    def __init__(self, player: Player, croupier: Croupier, cart_deck: CardDeck):
        self.player = player
        self.croupier = croupier
        self.cart_deck = cart_deck

    # Формирует банк      
    def bank_for_line(self, bet: int) -> int:
        """Принимает ставку игрока, уменьшает его кошелек и возвращает банк, ставку x 2.
        """
        self.player.money = self.player.money - bet
        bank = bet * 2
        return bank     

    # Создает новый кон
    def create_new_line(self) -> list:
        """Обнуляем карты и создаем новую колоду со всеми картаим и возвращаем список карт, который будет меняться
        """
        self.player.point_in_line = []
        self.croupier.point_in_line = []
        self.player.cards_in_line = []
        self.croupier.cards_in_line = []

        self.cart_deck.new_deck()
    
    # Раздать карты и показать все у игрока и одну у крупье
    def hand_out_cards(self):
        """Раздает карты и показывает, и меняет колоду карт.
        """
        for i in range(2):
            random_index = random.randint(0,len(self.cart_deck.deck)-1)
            self.player.cards_in_line.append(self.cart_deck.deck[random_index])
            self.player.point_in_line.append(self.cart_deck.points_for_the_card[self.cart_deck.deck[random_index]])
            self.cart_deck.deck.pop(random_index)
            # print(len(self.cart_deck.deck))

            random_index = random.randint(0,len(self.cart_deck.deck)-1)
            self.croupier.cards_in_line.append(self.cart_deck.deck[random_index])
            self.croupier.point_in_line.append(self.cart_deck.points_for_the_card[self.cart_deck.deck[random_index]])         
            self.cart_deck.deck.pop(random_index)
            # print(len(self.cart_deck.deck))

        print(f"Карты игрока {self.player.cards_in_line}, очки {self.player.point_in_line}.")
        print(f"Карты крупье {self.croupier.cards_in_line[0]}, вторая скрыта.")
        
    # Выдать еще одну карту
    def give_card(self, obj):
        """Выдает карту, и обновляет колоду, на вход получает объект
        """
        random_index = random.randint(0,len(self.cart_deck.deck)-1)
        obj.cards_in_line.append(self.cart_deck.deck[random_index])
        obj.point_in_line.append(self.cart_deck.points_for_the_card[self.cart_deck.deck[random_index]])
        self.cart_deck.deck.pop(random_index)
   
        print(f"Карты у {obj.name} - {obj.cards_in_line}, очки {obj.point_in_line} сумма очков {sum(obj.point_in_line)}.")

    # Проверка на перебор
    def check_a_bust(self, obj) -> bool:
        if sum(obj.point_in_line) > 21:
            print("У Вас перебор, больше 21")
            return True

    # Проверка на выйгрыш
    def check_a_win(self, bank) -> bool:
        """После того как карты сданы и игроки перестали набирать, проверяет кто выйграл
        """
        if self.player.point_in_line == self.croupier.point_in_line:
            self.player.money = self.player.money + bank/2
            self.croupier.money = self.croupier.money + bank/2
            print("Крупье: Ничья")
            return False
        elif self.player.point_in_line < self.croupier.point_in_line:
            self.croupier.money = self.croupier.money + bank
            print(f"Крупье: Казино выйграло, мой счет {self.croupier.money}")
            return False
        elif self.player.point_in_line > self.croupier.point_in_line:
            self.player.money = self.player.money + bank
            print(f"Крупье: Вы выйграли, ваш счет {self.player.money}")
            return False

    # Перечисляет банк кому либо
    def bank_win(self, obj, bank):
        """Перечесляет деньги на счет победителя
        """
        obj.money = obj.money + bank



# ИГРА

obj_carddeck = CardDeck()
obj_player = Player()
obj_croupier = Croupier(obj_player)
obj_game = BlackJack(obj_player, obj_croupier, obj_carddeck)

# Начинаем кон
stop_lev_1 = False
while stop_lev_1 == False:

   bet = obj_player.make_a_bet()
   bank = obj_game.bank_for_line(bet)
   obj_game.create_new_line()
   obj_game.hand_out_cards()

   stop_lev_2 = False

   # Игрок набирает карты
   while obj_player.take_card_or_say_stop():
      obj_game.give_card(obj_player)
      
      if obj_game.check_a_bust(obj_player):
         if obj_game.player.check_ace_if_bust():
            # Перечисление денег
            obj_game.bank_win(obj_croupier, bank)
            print(f"Крупье: Казино выйграло, мой счет {obj_game.croupier.money}")            
            stop_lev_2 = True

            # Если у игрока кончились деньги или он набрал много
            if obj_player.check_go_home():
               stop_lev_1 = True
            break
         else:
            continue
      
   if stop_lev_2:
      continue

   # Крупье набирает карты, сначала показывает вторую
   obj_game.croupier.show_croupie_cart()        
   while obj_game.croupier.compare_points():
      obj_game.give_card(obj_croupier)
      if obj_game.check_a_bust(obj_croupier):
         if obj_game.croupier.check_ace_if_bust():
            # Перечисление денег
            obj_game.bank_win(obj_player, bank) 
            print(f"Крупье: Вы выйграли, ваш счет {obj_game.player.money}")           
            stop_lev_2 = True

            # Если у игрока кончились деньги или он набрал много
            if obj_player.check_go_home():
               stop_lev_1 = True
            break
         else:
            continue

      
   if stop_lev_2:
      continue
   else:
      # Проверяем кто выйграл
      obj_game.check_a_win(bank)

      # Если у игрока кончились деньги или он набрал много
      if obj_player.check_go_home():
         stop_lev_1 = True
   





