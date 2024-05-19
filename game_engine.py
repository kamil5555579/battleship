import numpy as np
import time

boat_types = {
    # "carrier" : 5,
    # "battleship": 4,
    # "cruiser": 3,
    # "submarine": 3,
    "destroyer": 2
}

class ConnectionErrorWithConn(Exception):
    def __init__(self, conn, message="Connection error occurred"):
        super().__init__(message)
        self.conn = conn

def get_indexes_from_player(conn, prompt: str):
    while(True):
        try:
            response = send_prompt_and_get_response(conn, prompt)
        except:
            raise ConnectionError
        indexes = convert_to_index(response)
        print(indexes)
        if indexes != -1:
            break
        send_message(conn, 'error')
        time.sleep(0.1) # 100ms

    return indexes

def send_prompt_and_get_response(conn, prompt: str):
    try:
        conn.sendall(prompt.encode())
    except:
        raise ConnectionError
    data = conn.recv(1024)
    return data.decode()

def send_message(conn, message: str):
    conn.sendall(message.encode())

def convert_to_index(in_str: str):
        # Number convertion
        # Safety for wrong input
        if len(in_str) > 3:
            return -1
        elif len(in_str) >= 3:
            if in_str[1:] == '10':
                number = 10
            else:
                return -1
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
    def __init__(self, player1, player2):
        self.amount_of_winning_hits = np.array(list(boat_types.values())).sum()
        self.active_player = False
        self.players = (player1, player2)

    def change_player(self):
        self.active_player = not self.active_player

    def show_shots(self):
        send_message(self.players[self.active_player].conn , self.players[int(self.active_player)].show_shots())
    
    def show_board(self):
        send_message(self.players[self.active_player].conn , self.players[int(self.active_player)].show_board())

    def shoot(self):
        while(True):
            try:
                indexes = get_indexes_from_player(self.players[self.active_player].conn, "shoot")
            except:
                print("Error while getting response")
                raise ConnectionError
            if not self.players[self.active_player].is_already_shot(indexes):
                break
            else:
                send_message(self.conn, 'You did that shot already!\n')


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
            self.show_board()
            self.show_shots()
            time.sleep(0.1) # 100ms
            try:
                self.shoot()
            except:
                raise ConnectionErrorWithConn(self.players[self.active_player].conn)
            self.show_shots()
            if self.did_player_won():
                win_msg = f"Player {int(self.active_player) + 1} won !!1!1"
                send_message(self.players[self.active_player].conn,win_msg)
                send_message(self.players[not self.active_player].conn,win_msg)
                print(win_msg)
                time.sleep(0.1) # 100ms
                break
            self.change_player()

class Player:
    def __init__(self, conn):
        self.players_shots = Shots()
        self.hit_counter = 0
        self.conn = conn
        self.players_board = None

    def init_board(self):
        try:
            self.players_board = Ship_placement(self.conn)
        except:
            raise ConnectionErrorWithConn(self.conn)
        
    def show_shots(self):
        return str(self.players_shots)

    def show_board(self):
        return str(self.players_board)

    def check_hit(self, indexes):
        return self.players_board.check_hit(indexes)

    def hit(self, indexes):
        self.hit_counter += 1
        self.players_shots.hit(indexes)

    def miss(self, indexes):
        self.players_shots.miss(indexes)

    def get_amount_of_hits(self):
        return self.hit_counter

    def is_already_shot(self, indexes):
        return self.players_shots.is_already_shot(indexes)

class Ship_placement:
    def __init__(self, conn, board=None):
        self.conn = conn

        if board == None:
            # first index number(row) second letter column
            self.ship_placements = np.zeros([10,10])

            lst_of_boat_types = list(boat_types.keys())
            i = 0
            while(i<len(lst_of_boat_types)):
                # print(f"Please place your: {lst_of_boat_types[i]} (size: {boat_types[lst_of_boat_types[i]]})")
                # position = get_indexes_from_player('Staring index (A-Z and 1-10): ')
                try:
                    position = get_indexes_from_player(self.conn, lst_of_boat_types[i])
                except:
                    raise ConnectionError
                try:
                    rotation = send_prompt_and_get_response(self.conn, 'rotation')
                except:
                    raise ConnectionError
                if not (self.place_boat(lst_of_boat_types[i], position, rotation)==-1):
                    i+=1

            send_message(self.conn, 'Zakonczono rozstawianie')

        else:
            self.ship_placements = board


    def __str__(self):
        return board_to_str(self.ship_placements)

    def place_boat(self, boat_type: str, starting_indexes, rotation: str): # H - horizontal V - vertical
        length = boat_types[boat_type]
        x = starting_indexes[1]
        y = starting_indexes[0]

        #if (y+length)>9 or (x+length)>9:
         #   send_message(self.conn, 'error too long')
         #   time.sleep(0.1) # 100ms
         #   return -1 


        if rotation == "v" or rotation == "V":
            if (x+length-1)>9:
                send_message(self.conn, 'error too long')
                time.sleep(0.1) # 100ms
                return -1 
            elif np.any(self.ship_placements[ \
                x:x+length, \
                y] == 1):
                    send_message(self.conn, 'error')
                    time.sleep(0.1) # 100ms
                    return -1
            else:
                self.ship_placements[ \
                    x:x+length, \
                    y] = 1
        else:
            if(y+length-1)>9:
                send_message(self.conn, 'error too long')
                time.sleep(0.1) # 100ms
                return -1 
            if np.any(self.ship_placements[ \
                x, \
                y:y+length] == 1):
                    send_message(self.conn, 'error')
                    time.sleep(0.1) # 100ms
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
        return board_to_str(self.board)

    def is_already_shot(self, indexes):
        x = indexes[1]
        y = indexes[0]
        if self.board[x,y] == 0 or self.board[x,y] == 1:
            return True
        else:
            return False

    def hit(self, indexes):
        x = indexes[1]
        y = indexes[0]
        self.board[x,y] = 1

    def miss(self, indexes):
        x = indexes[1]
        y = indexes[0]
        self.board[x,y] = 0

def board_to_str(array):
    N = array.shape[0]
    output_str = ""

    for i in range(N+1):   
        for j in range(N+1):
            if i ==0 and j==0:
                output_str += ' '
            elif j == 0:
                output_str += chr(ord('A')+i-1)
            elif i == 0:
                output_str += str(j)
            else:
                match array[i-1,j-1]:

                    case -1:
                        output_str += chr(35) # #

                    case 0:
                        output_str += chr(79) # O

                    case 1:
                        output_str += chr(88) # X

            output_str += ' '

        output_str += '\n'
 
    return output_str


# Main
'''
test_array = np.array([[0,0,0],
                        [0,1,0],
                        [0,0,-1]])
print(board_to_str(test_array))
'''
# game1 = Game()
# game1.start()