import socket
import signal
import sys
from game_engine import Game, Player, ConnectionErrorWithConn
# sendall - nakładka na send, która zapewnia, że wszystkie dane zostaną wysłane
import atexit
import threading

def close_socket(server_socket):
    server_socket.close()

def start_server():
    # Tworzenie gniazda serwera
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Adres i port serwera
    server_address = ('localhost', 12345)

    # Bindowanie gniazda do adresu i portu
    server_socket.bind(server_address)

    # Nasłuchiwanie na połączenia
    server_socket.listen()

    print('Server listens on port', server_address[1])

    return server_socket

def handle_clients(server_socket, conn_list = []):

    while len(conn_list) < 2:
        # Akceptowanie połączenia
        print('Waiting for connection...')
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

def disconnect_clients(conn_list):
    message = 'exit'
    for conn in conn_list:
        conn.sendall(message.encode())
        conn.close()
        print('Client disconnected')

def init_board(player):
    try:
        player.init_board()
    except ConnectionErrorWithConn as e:
        print('Error. Closing connection')

if __name__ == '__main__':
    server_socket = start_server()
    atexit.register(close_socket, server_socket)
    conn_list = []

    while True:
        conn_list = handle_clients(server_socket, conn_list)
        player1 = Player(conn_list[0])
        player2 = Player(conn_list[1])
        init_success = 0
        thread1 = threading.Thread(target=init_board, args=(player1,))
        thread2 = threading.Thread(target=init_board, args=(player2,))
        thread1.start()
        thread2.start() 
        thread1.join()
        thread2.join()
        for player in [player1, player2]:
            if player.players_board is None:
                player.conn.close()
                conn_list.remove(player.conn)
                print(conn_list)
                if len(conn_list) == 1:
                    conn_list[0].sendall('Opponent disconnected, waiting for new player'.encode())
            else:
                init_success += 1

        if init_success == 2:
            try:
                game = Game(player1, player2)
                game.start()
            except ConnectionErrorWithConn as e:
                print('Error. Closing connection')
                conn_list.remove(e.conn)
                e.conn.close()
                conn_list[0].sendall('Opponent disconnected, waiting for new player'.encode())
            else:
                print('Game finished')
                disconnect_clients(conn_list)
                conn_list = []

    server_socket.close()