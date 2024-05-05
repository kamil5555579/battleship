import socket
import signal
import sys
from game_engine import Game, Player
# sendall - nakładka na send, która zapewnia, że wszystkie dane zostaną wysłane

def start_server():
    # Tworzenie gniazda serwera
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Adres i port serwera
    server_address = ('localhost', 12346)

    # Bindowanie gniazda do adresu i portu
    server_socket.bind(server_address)

    # Nasłuchiwanie na połączenia
    server_socket.listen()

    print('Serwer nasłuchuje na porcie', server_address[1])

    return server_socket

def handle_clients(server_socket):

    conn_list = []

    while len(conn_list) < 2:
        # Akceptowanie połączenia
        conn, addr = server_socket.accept()

        if len(conn_list) == 0:
            print('Connection with client 1', addr, 'waiting for second player')
            message = '1'
            conn.sendall(message.encode())
            conn_list.append(conn)
        else:
            print('Connection with client 2', addr, 'game starts')
            message = '2'
            conn.sendall(message.encode())
            conn_list.append(conn)
            conn_list[0].sendall(message.encode()) # informacja dla pierwszego klienta, że gra się rozpoczyna

    return conn_list

if __name__ == '__main__':
    server_socket = start_server()
    conn_list = handle_clients(server_socket)
    player1 = Player(conn_list[0])
    player2 = Player(conn_list[1])
    game = Game(player1, player2)
    game.start()
    server_socket.close()