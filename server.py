import socket
from game_engine import Game, Player, ConnectionErrorWithConn
import atexit
import threading

def close_socket(server_socket):
    server_socket.close()

def start_server() -> socket.socket:
    """
    Creates and starts a server socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen()
    print('Server listens on port', server_address[1])

    return server_socket

def handle_clients(server_socket: socket.socket, conn_list: list[socket.socket]) -> list[socket.socket]:
    """
    Accepts incoming client connections and manages the connection list.
    """
    while len(conn_list) < 2:
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

def disconnect_clients(conn_list: list[socket.socket]) -> None:
    """
    Disconnects all clients.
    """
    message = 'exit'
    for conn in conn_list:
        conn.sendall(message.encode())
        conn.close()
        print('Client disconnected')

def thread_board_init(player1: Player, player2: Player):
    """
    Initializes boards for both players in separate threads.
    """
    thread1 = threading.Thread(target=player1.init_board, args=())
    thread2 = threading.Thread(target=player2.init_board, args=())
    thread1.start()
    thread2.start() 
    thread1.join()
    thread2.join()

if __name__ == '__main__':
    server_socket = start_server()
    atexit.register(close_socket, server_socket)
    conn_list = []

    while True:
        conn_list = handle_clients(server_socket, conn_list)
        player1 = Player(conn_list[0])
        player2 = Player(conn_list[1])
        thread_board_init(player1, player2)
        init_success = 0
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