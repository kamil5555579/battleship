import socket
import signal
import sys
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
            print('Połączenie z klientem 1', addr, 'czekam na drugiego klienta...')
            message = '1'
            conn.sendall(message.encode())
            conn_list.append(conn)
        else:
            print('Połączenie z klientem 2', addr)
            message = '2'
            conn.sendall(message.encode())
            conn_list.append(conn)
            conn_list[0].sendall(message.encode()) # informacja dla pierwszego klienta, że gra się rozpoczyna

    return conn_list
    
def get_boards(conn_list):

    for conn in conn_list:
        start_message = 'board'
        conn.sendall(start_message.encode())

    for conn in conn_list:
        data = conn.recv(1024)
        print('Otrzymano planszę:', data.decode())
        # inicjalizacja planszy

def handle_game(conn_list):
        
    shooter = 0

    while True:
        message = 'shoot'
        conn_list[shooter].sendall(message.encode())
        data = conn_list[shooter].recv(1024)
        print('Otrzymano strzał:', data.decode())
        # to-do sprawdzenie czy strzał trafił
        conn_list[not shooter].sendall(data) # przekazanie strzału do drugiego klienta
        shooter = not shooter
        # to-do sprawdzenie czy ktoś wygrał
        # to-do zakończenie gry

if __name__ == '__main__':
    server_socket = start_server()
    conn_list = handle_clients(server_socket)
    get_boards(conn_list)
    handle_game(conn_list)