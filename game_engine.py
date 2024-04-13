import numpy as np


boat_types = {
    "Carrier" : 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
}

def get_indexes_from_player(prompt: str):
    while(True):
        command = input(prompt)
        indexes = convert_to_index(command)
        if indexes != -1:
            break
        print('Wrong position! Use letter A-J and number 1-10')

    return indexes

def convert_to_index(in_str: str):
        # Number convertion
        # Safety for wrong input
        if len(in_str) > 3:
            return -1
        elif len(in_str) == 3:
            if in_str[1:] == '10':
                number = 10
        else:
            try:
                number = int(in_str[1:])
                if number == 0:
                    return -1
            except:
                return -1

        number -= 1

        # Letters to number plus getting rid of wrong ASCII 
        letter = in_str[0]
        letter = ord(letter)
        if letter >= 97 and letter <= 106:
            letter -= 97
        elif letter >= 65 and letter <= 74:
            letter -= 65
        else:
            return -1

        return(number, letter)


class Game:
    def __init__(self):
        self.amount_of_winning_hits = np.array(list(boat_types.values())).sum()
        self.active_player = False
        self.players = (Player(1), Player(2))
        

    def change_player(self):
        self.active_player = not self.active_player

    def show_shots(self):
        self.players[int(self.active_player)].show_shots()

    def shoot(self):
        indexes = get_indexes_from_player("Shoot: ")
        if self.players[int(not self.active_player)].check_hit(indexes) == 1:
            self.players[self.active_player].hit(indexes)
        else:
            self.players[self.active_player].miss(indexes)

    def did_player_won(self):
        print(self.players[self.active_player].get_amount_of_hits())
        print(self.amount_of_winning_hits)
        if self.players[self.active_player].get_amount_of_hits() \
            == self.amount_of_winning_hits:
            return True
        else:
            return False

    def start(self):
        while(True):
            print(f"Player {int(self.active_player) + 1} shoots")
            self.show_shots()
            self.shoot()
            self.show_shots()
            if self.did_player_won():
                print(f"Player {int(self.active_player) + 1} won !!1!1")
                break
            self.change_player()

class Player:
    def __init__(self, number):
        self.players_board = Ship_placement()
        self.players_shots = Shots()
        self.hit_counter = 0

    def show_shots(self):
        print(self.players_shots)

    def check_hit(self, indexes):
        return self.players_board.check_hit(indexes)

    def hit(self, indexes):
        self.hit_counter += 1
        self.players_shots.hit(indexes)

    def miss(self, indexes):
        self.players_shots.miss(indexes)

    def get_amount_of_hits(self):
        return self.hit_counter

class Ship_placement:
    def __init__(self, board=None):
        if board == None:
            # first index number(row) second letter column
            self.ship_placements = np.zeros([10,10])

            lst_of_boat_types = list(boat_types.keys())
            i = 0
            while(i<len(lst_of_boat_types)):
                print(f"Please place your: {lst_of_boat_types[i]} (size: {boat_types[lst_of_boat_types[i]]})")
                position = get_indexes_from_player('Staring index (A-Z and 1-10): ')
                rotation = input('Rotation (H - horizontal or V - vertical): ')
                if not (self.place_boat(lst_of_boat_types[i], position, rotation)==-1):
                    i+=1

        else:
            self.ship_placements = board


    def __str__(self):
        return f"{self.ship_placements}"

    def place_boat(self, boat_type: str, starting_indexes, rotation: str): # H - horizontal V - vertical
        length = boat_types[boat_type]
        x = starting_indexes[1]
        y = starting_indexes[0]

        if (y+length)>9 or (x+length)>9:
            print("Wrong ship placement")
            return -1 


        if rotation == "v" or rotation == "V":
            if np.any(self.ship_placements[ \
                x:x+length, \
                y] == 1):
                    print("Wrong ship placement")
                    return -1
            else:
                self.ship_placements[ \
                    x:x+length, \
                    y] = 1
        else:
            if np.any(self.ship_placements[ \
                x, \
                y:y+length] == 1):
                    print("Wrong ship placement")
                    return -1
            else:
                self.ship_placements[ \
                    x, \
                    y:y+length] = 1

    def check_hit(self, attacked_place):
        x = attacked_place[1]
        y = attacked_place[0]
        if (self.ship_placements[x,y]==1):
            return 1
        else:
            return 0

class Shots:
    def __init__(self):
        self.board = np.ones([10,10])*-1

    def __str__(self):
        return str(self.board)

    def hit(self, indexes):
        x = indexes[1]
        y = indexes[0]
        self.board[x,y] = 1

    def miss(self, indexes):
        x = indexes[1]
        y = indexes[0]
        self.board[x,y] = 0


# Main

game1 = Game()
game1.start()