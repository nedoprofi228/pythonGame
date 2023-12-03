import time
import os
import keyboard
from random import choice, randrange
from copy import deepcopy

my_map = None
num_my_map = 1
hero = None
items = None
player_inventary = None
player_sword = None
sword_in_stone = None
crafts = None
timer = 0
size_x = 60
size_y = 10
count_stones = 0 # -> o
count_woods = 0 # -> #
count_gems = 0 # -> *
count_items_player = 0
count_spawn_items = 15
inventary_size_x = 32
inventary_size_y = 12
in_wate_flag = False
have_sword_flag = False
in_inventary_flag = False


text_sword_in_stone_1= """
«Идя вдоль реки вы видите странное образование,
удалённо напопинающее могилу, за исключением одного,
вместо креста торчит старый ржавый меч...»
"""

text_sword_in_stone_2= """
Вы подобрали старый ржавый меч!
Кто знает какие ужасы вы будете с ним творить..."""

text_equip_queshion= 'достать - Q или проигнорировать - R'

def create_map(size_x: int = size_x, size_y: int= size_y, num_map: int = num_my_map) -> None:
    global my_map
    if num_map <= 1:
        my_map = [[(('_' if row % 3 ==0 else " ")if row !=0 and row != size_y-1 else '=') for col in range(size_x)] for row in range(size_y)]
    elif num_map >= 2:
        map2 = []  
        for y in range(size_y + 1):
            row = []
            for _ in range(size_x + 1):
                if y == 0 or y == size_y:
                    row.append('=')
                elif 0 < y < size_y // 3:
                    row.append(choice(['~', ' ']))
                else:
                    if y % 3 == 0:
                        row.append('_')
                    else:
                        row.append(' ')
            map2.append(row)
        my_map = map2
    

def draw_sword(place, x, y):
    place[y][x] = '|'
    place[y+1][x] = '!'
    place[y][x+1] = '_'
    place[y][x-1] = '_'
    place[y-1][x] = '|'
    place[y+2][x-2] = 'S'
    place[y+2][x-1] = 'w'
    place[y+2][x] = 'o'
    place[y+2][x+1] = 'r'
    place[y+2][x+2] = 'd'
    
def draw_shield(place, x, y):
    place[y][x] = '_'       #  _
    place[y][x-1] = ')'     # )_)
    place[y][x+1] = ')'     #
    place[y-1][x] = '_'     # 
    place[y+2][x-3] = 'S'   # text
    place[y+2][x-2] = 'h'   # text
    place[y+2][x-1] = 'i'   # text
    place[y+2][x] =   'e'   # text
    place[y+2][x+1] = 'l'   # text
    place[y+2][x+2] = 'd'   # text
    
def draw_bow(place, x, y):
    place[y][x] = ' '       # I -
    place[y][x-1] = '|'     # |  |
    place[y][x+1] = '|'     # I -
    place[y-1][x] = '-'  
    place[y+1][x] = '-'  
    place[y-1][x-1] = 'I'
    place[y+1][x-1] = 'I'
    place[y+2][x-1] = 'B'   # text    
    place[y+2][x] = 'o'     # text 
    place[y+2][x+1] = 'w'   # text 

def draw_fishing_rod(place, x, y):
    place[y][x] = '/'
    place[y+1][x-1] = '/'
    place[y-1][x+1] = '/'
    place[y][x+2] = '|'
    place[y+1][x+2] = '\''
    place[y-1][x+2] = '|'
    place[y+2][x-1] = 'R'
    place[y+2][x] = 'o'
    place[y+2][x+1] = 'd'
        
def show_map(my_map) -> None:
    for row in my_map:
        print(''.join(row))
  
def write_about_item(place, x, y):  
    match place[y][x]:
        case '*': print('gem - usually item \nNeed for crafts')
        case '#': print('wood - usually item \nNeed for crafts')
        case 'o': print('stone - usually item \nNeed for crafts')

def choose_x_place(place, slots_x ,y):
    for n, x in enumerate(range(slots_x-3, slots_x+4)):
        if place[y][x] == ' ' and n == 0 or place[y][x] == ' ' and n == 6:
            place[y][x] = '+'

def choose_y_all_x_place(place, choose_slot_x, slot_x, y, slot_y):
                if choose_slot_x == 1:
                    choose_x_place(place, slot_x[1-1], y)
                    # write_about_item(place, slot_x[1-1], slot_y)
                elif choose_slot_x == 2:
                    choose_x_place(place, slot_x[2-1], y)
                    # write_about_item(place, slot_x[2-1], slot_y)
                elif choose_slot_x == 3:
                    choose_x_place(place, slot_x[3-1], y)
                    # write_about_item(place, slot_x[3-1], slot_y)
                elif choose_slot_x == 4:
                    choose_x_place(place, slot_x[4-1], y)
                    # write_about_item(place, slot_x[4-1], slot_y)

create_map()


class Item:
    def __init__(self, simvol:str = "#") -> None:
        self.x = randrange(3, len(my_map[0])-2)
        self.y = randrange(2, len(my_map)-2)
        self.simvol = simvol
        self.check_flag = True
    def set_item(self):
        if self.check_flag:
            my_map[self.y][self.x] = self.simvol
    def items():
        return [Item(choice(['#', 'o', '*'])) for _ in range(count_spawn_items)]
    
class Sword_in_stone(Item):
    def __init__(self):
        self.x = randrange(5, size_x-5)
        self.y = randrange(3, size_y-3)
        self.check_flag = True
        self.simvol = '|'                 
    def set_item(self, map):
        if num_my_map >= 2:                                      
            map[self.y][self.x-1] = '-'
            map[self.y][self.x-2] = ' '
            map[self.y][self.x-3] = '('
            map[self.y][self.x+1] = '-'
            map[self.y][self.x+2] = ' '
            map[self.y][self.x+3] = ')'
            map[self.y+1][self.x] = ' '
            map[self.y+1][self.x+1] = '_'
            map[self.y+1][self.x+2] = ' '
            map[self.y+1][self.x+3] = '_'
            map[self.y+1][self.x+4] = ' '
            map[self.y+1][self.x+5] = ')'
            map[self.y+1][self.x-1] = '_'
            map[self.y+1][self.x-2] = ' '
            map[self.y+1][self.x-3] = '_'
            map[self.y+1][self.x-4] = ' '
            map[self.y+1][self.x-5] = '('
            if self.check_flag:
                map[self.y][self.x] = '|'
                map[self.y-1][self.x] = '|'
                map[self.y-2][self.x] = '|'
                map[self.y-2][self.x-1] = '_'
                map[self.y-2][self.x+1] = '_'
        
        
#     _|_
#      |
#   [ -|- ]
# [ _ _ _ _ ]
 
    
class Hero:     # main character
    def __init__(self, x: int= 2, y: int= int(len(my_map)/2)) -> None:
        self.x = x
        self.y = y
        self.hero_item = ''
    def set_hero(self):
        if not (num_my_map >= 2 and self.y < size_y // 3):
            my_map[self.y+1][self.x+1] = '\\' 
            my_map[self.y+1][self.x-1] = '/'
        my_map[self.y][self.x] = '|'
        my_map[self.y][self.x-1] = '/'          #  O 
        my_map[self.y][self.x+1] = '\\'         # /|\
        my_map[self.y-1][self.x] = 'o'          # / \
        if not self.hero_item == '' and not have_sword_flag:
            my_map[self.y][self.x+2] = self.hero_item
    def hero_move(self, move: str):
        global num_my_map
        match move.lower():
            case 's':
                if self.y+1 < len(my_map)-1:
                    self.y += 1
                else:
                    self.y = 1
            case 'w':
                if self.y < 0:
                    self.y = len(my_map)-2
                else:
                    self.y -= 1
            case 'd':
                if self.x+3 < len(my_map[0])-1 and not have_sword_flag:
                    self.x += 2
                elif self.x+4 < len(my_map[0])-1 and have_sword_flag:
                    self.x += 2
                else:   
                    num_my_map += 1
                    self.x = 2  
            case 'a':
                if self.x-3 < 0:
                    if not have_sword_flag:
                        self.x = len(my_map[0])-4
                    else:
                        self.x = len(my_map[0])-5
                    num_my_map -= 1
                else:
                    self.x -= 2
                    
    def check_item(self, item, inventary):
        global count_stones, count_woods, count_gems, count_items_player, player_sword, have_sword_flag
        if self.x == item.x and self.y+1 == item.y or self.x-1 == item.x and self.y+1 == item.y or self.x+1 == item.x and self.y+1 == item.y:
            if item.check_flag:
                if item.simvol != '|':
                    self.hero_item = item.simvol
                    inventary.add_item(item.simvol)
                    item.check_flag = False 
                    match item.simvol:
                        case "#":
                            print('u pick up wood!')
                            count_woods +=1
                            count_items_player += 1
                            print(f'woods: {count_woods}')
                        case "o":
                            print('u pick up stone!')
                            count_stones +=1
                            count_items_player += 1
                            print(f'stones : {count_stones}')
                        case '*':
                            print('u pick up gem!')
                            count_gems += 1
                            count_items_player += 1
                            print(f'gems: {count_gems}')
                        
                elif item.simvol == '|':
                    print(text_sword_in_stone_1)
                    time.sleep(3)
                    print(text_equip_queshion)
                    if keyboard.read_key().lower() == 'q':
                        self.hero_item = item.simvol
                        inventary.add_item(item.simvol)
                        item.check_flag = False 
                        have_sword_flag = True
                        os.system('cls||clear')
                        print(text_sword_in_stone_2)
                        input('Нажмите Enter чтобы продолжить\n\n\n\n\n\n\n')
                        
  
def settings(user):
    global size_x, size_y, count_spawn_items
    match user.lower():
        case 'z': print('клавиши: \nP - настройки карты \nO - настройки кол-ва предметов \nE - инвентарь \nR - крафты')
        case 'r': crafts.check_choose_slots()
        case 'p':
            try:
                size_x = int(input('введите ширину карты: '))
                size_y = int(input('введите высоту карты: '))
            except:
                print('вы ввели не число')
        case 'e': os.system('cls||clear'); player_inventary.check_slots_inventory()
        case 'o':
            user_input = input('введите кол-во предметов на карте: ')
            try:
                count_spawn_items = int(user_input)
            except:
                print('вы ввели не число')

class Sword:
    def __init__(self):
        self.x = None
        self.y = None
    
    def check_collect(self, hero):
        if have_sword_flag:
            self.x = hero.x+2
            self.y = hero.y
    def set_item(self, map):
        if have_sword_flag:
            map[self.y][self.x] = '!'
            map[self.y-1][self.x -1] = '_'  #   |
            map[self.y-1][self.x +1] = '_'  #   |
            map[self.y-2][self.x] = '|'     #  ___ 
            map[self.y-1][self.x] = '|'     #   |
        


def start_text():
    print('Добро пожаловать в мою игру\n В этой игре есть набор движений: \n w - вверх \n a - влево\n s - вниз\n d - вправо')
    print('для выхода введите stop')
    print('для получения информации о настройках нажмите: z')
    print('Приятной игры!')

def set_items(items):
    for item in items:
        item.set_item()

def check_items(hero, items, inventary):
    for elem in items:
        hero.check_item(elem, inventary)
        
# -----------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
def first_start(): 
    os.system('cls||clear')
    start_text()
    input('нажмите Enter для начала: ')
    os.system('cls')
    
    global items, hero, player_inventary, player_sword, sword_in_stone, crafts
    
    crafts = Crafts()
    create_map(size_x, size_y)
    sword_in_stone = Sword_in_stone()
    player_sword = Sword()
    sword_in_stone.set_item(my_map)
    items = Item.items()
    set_items(items)
    hero = Hero()
    hero.set_hero()
    show_map(my_map)
    player_inventary = Inventary()
    player_inventary.create_inventary()

def spawn_items():
    global timer, items
    if timer > 100:
        items = Item.items()
        timer = 0
    else:
        timer += 1
        
class Inventary:
    def __init__(self) -> None:
        self.inv = None
        self.slotes_y = (2, 6, 10)
        self.slotes_x = (4, 12, 20, 28)
        
        
    def create_inventary(self):
        inventar = []
        for y in range(inventary_size_y +1):
            row = []
            for x in range(inventary_size_x +1):
                if y == 0 or y == inventary_size_y:
                    row.append('-') # ------------------------------------
                elif 0< y <inventary_size_y and y % 4 == 0:
                    if x == 0 or x == inventary_size_x:
                        row.append('|')
                    else:
                        row.append('-')
                elif 0< y <inventary_size_y:
                    if x == 0 or x % 8 == 0:
                        row.append('|')
                    else:
                        row.append(' ') 
            inventar.append(row)
        self.inv = inventar
    
    def add_item(self, item):
        for y in self.slotes_y:
            for x in self.slotes_x:
                if self.inv[y][x] == item or self.inv[y][x] == ' ':
                    self.inv[y][x] = item
                    match item:
                        case '*':
                            if 0 < count_gems < 10:
                                self.inv[y+1][x+3] = str(count_gems+1)
                            elif 9 < count_gems < 100:
                                self.inv[y+1][x+3] = str(count_gems+1)
                                self.inv[y+1][x+2] = ''
                            self.inv[y+2][x-2] = 'g'
                            self.inv[y+2][x-1] = 'e'
                            self.inv[y+2][x] = 'm'
                            self.inv[y+2][x+1] = 's'
                        case '#':
                            if 0 < count_woods < 10:
                                self.inv[y+1][x+3] = str(count_woods+1)
                            elif 9 < count_woods < 100:
                                self.inv[y+1][x+3] = str(count_woods+1)
                                self.inv[y+1][x+2] = ''
                            self.inv[y+2][x-2] = 'w'
                            self.inv[y+2][x-1] = 'o'
                            self.inv[y+2][x] = 'o'
                            self.inv[y+2][x+1] = 'd'
                            self.inv[y+2][x+2] = 's'
                        case 'o':
                            if 0 < count_stones < 10:
                                self.inv[y+1][x+3] = str(count_stones+1)
                            elif 9 < count_stones < 100:
                                self.inv[y+1][x+3] = str(count_stones+1)
                                self.inv[y+1][x+2] = ''
                            self.inv[y+2][x-3] = 'S'
                            self.inv[y+2][x-2] = 't'
                            self.inv[y+2][x-1] = 'o'
                            self.inv[y+2][x] =   'n'
                            self.inv[y+2][x+1] = 'e'
                            self.inv[y+2][x+2] = 's'
                            
                        case '|':
                            draw_sword(self.inv, x, y)
                            # self.inv[y][x] = '|'
                            # self.inv[y+1][x] = '!'
                            # self.inv[y][x+1] = '_'
                            # self.inv[y][x-1] = '_'
                            # self.inv[y-1][x] = '|'
                    break

            break
                

    def show_inventory(self):
        for row in self.inv:
            print(''.join(row))
    
    def check_slots_inventory(self):
        input('нажмите Enter чтобы продолжить \n\n\n\n\n')
        choose_slot_x = 1
        choose_slot_y = 1
        inventory = deepcopy(self.inv)
        time.sleep(0.3)
        while True:
            self.inv = deepcopy(inventory)
            if choose_slot_y == 1:
                for y in range(self.slotes_y[1-1]-1, self.slotes_y[1-1]+2):
                    choose_y_all_x_place(self.inv, choose_slot_x, self.slotes_x, y, self.slotes_y[1-1])
            elif choose_slot_y == 2:
                for y in range(self.slotes_y[2-1]-1, self.slotes_y[2-1]+2):
                    choose_y_all_x_place(self.inv, choose_slot_x, self.slotes_x, y, self.slotes_y[2-1])
            elif choose_slot_y == 3:
                for y in range(self.slotes_y[3-1]-1, self.slotes_y[3-1]+2):
                    choose_y_all_x_place(self.inv, choose_slot_x, self.slotes_x, y, self.slotes_y[3-1])
            os.system('cls||clear') 
            self.show_inventory()
            user1 = keyboard.read_key()
            self.inv = deepcopy(inventory)
            match user1.lower():
                case 'e': break
                case 'd': choose_slot_x += 1 if choose_slot_x < 4 else 0
                case 'a': choose_slot_x -= 1 if choose_slot_x > 1 else 0
                case 'w': choose_slot_y -= 1 if choose_slot_y > 1 else 0
                case 's': choose_slot_y += 1 if choose_slot_y < 3 else 0
            time.sleep(0.2)
        print('нажмите Enter чтобы вернуться')
                
#                                 32
# --------------------------------- 0   
# |       |       |       |       |     |
# |   4   |  12   |  20   |  28   | 2  _|_
# |      7|     15|     23|     31| 3   !
# |-------------------------------| 4
# |       |       |       |       | 
# |       |       |       |       | 6
# |       |       |       |       | 7
# |-------------------------------| 8
# |       |       |       |       | 
# |       |       |       |       | 10
# |       |       |       |       | 11
# --------------------------------- 12




class Crafts:
    def __init__(self):
        self.size_x = 32
        self.size_y = 4
        self.craft_window = []
        self.slots_y = 2
        self.slots_x = (4, 12, 20, 28)
    def set_craft_window(self):
        col = []
        for y in range(self.size_y+1):
            row = []
            for x in range(self.size_x+1):
                if y == 0 or y == self.size_y:
                    row.append('-')
                elif x % 8 == 0:
                    row.append('|')
                else:
                    row.append(' ')
            col.append(row)
        self.craft_window = col
    def set_crafts(self):
        for y in (self.slots_y, ):
            for index, x in enumerate(self.slots_x):
                if index == 0:
                    draw_shield(self.craft_window, x, y)
                if index == 1:                              
                    draw_bow(self.craft_window, x, y)
                if index == 2:
                    draw_sword(self.craft_window, x, y)
                if index == 3:
                    draw_fishing_rod(self.craft_window, x, y)
                    
    def show_craft(self):
        for row in self.craft_window:
            print(''.join(row))
    
    def print_text_menu(self):
        os.system('cls||clear')
        print('Crafts: \n')
    
    def check_choose_slots(self):
        input('Нажмите Enter чтобы продолжить\n\n\n\n\n')
        choose_slot = 1
        while True:
            crafts.print_text_menu()
            crafts.set_craft_window()
            crafts.set_crafts()
            for y in range(self.slots_y-1, self.slots_y+2):
                choose_y_all_x_place(self.craft_window, choose_slot, self.slots_x, y, self.slots_y)
            crafts.show_craft()
            time.sleep(0.2)
            if choose_slot == 1:
                print('_'*45)
                print(f'Shield - very good item for armory set!')
                print('_'*45)
                print('Need: \n6 stones \n10 woods')
                print('_'*45)
            if choose_slot == 2:
                print('_'*45)
                print(f'Bow - very important items for archer!')
                print('_'*45)
                print('Need: \n10 woods \n10 stones')
                print('_'*45)
            if choose_slot == 3:
                print('_'*45)
                print(f'Sword - its usually sword for knight')
                print('_'*45)
                print('Need: \n15 stones \n10 woods')
                print('_'*45)
            if choose_slot == 4:
                print('_'*45)
                print(f'Fishing rod - u need\'nt this')
                print('_'*45)
                print('Need: \n10 woods \n1 stones')
                print('_'*45)
            print(f'U have: \n* - {count_gems} \n# - {count_woods} \no - {count_stones}')
            user1 = keyboard.read_key()
            match user1.lower():
                case 'r': break
                case 'd': choose_slot += 1 if choose_slot < 4 else 0
                case 'a': choose_slot -= 1 if choose_slot > 1 else 0
        print('нажмите Enter чтобы вернуться')
        
                        
                    
        
def game():
    first_start()
    while True:
        time.sleep(0.1)
        user = keyboard.read_key()
        if user.lower() not in 'wasd':
            settings(user)
        elif user.lower() == 'esc': break
        else:
            os.system('cls||clear') # clear consol
            hero.hero_move(user)
            spawn_items()
            create_map(size_x, size_y,  num_map=num_my_map)
            if num_my_map >=2:
                hero.check_item(sword_in_stone, player_inventary)
            sword_in_stone.set_item(my_map)
            player_sword.check_collect(hero)
            player_sword.set_item(my_map)
            set_items(items) # set items
            hero.set_hero()
            show_map(my_map)
            check_items(hero, items, player_inventary) # check items
            
            
if __name__ == '__main__':
    game()
    
