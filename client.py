import socket

def connect_to_server():
    # Tworzenie gniazda klienta
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Adres i port serwera
    server_address = ('localhost', 12346)

    # Łączenie z serwerem
    client_socket.connect(server_address)

    return client_socket

def wait_for_msg(client_socket):

    while True:
        # Odbieranie danych od serwera
        data = client_socket.recv(1024)

        if data.decode() == '1':
            print('Oczekiwanie na drugiego gracza...')

        elif data.decode() == '2':
            print('Gra rozpoczyna się!')

        elif data.decode() == 'board':
            print('Ustaw swoje statki')
            # wysyłanie planszy
            fake_board = input("Podaj swoją planszę: ")
            client_socket.sendall(fake_board.encode())
            print('Wysłano planszę. Czekaj na planszę przeciwnika')

        elif data.decode() == 'shoot':
            print('Twój ruch')
            # strzał
            shot = input("Podaj współrzędne strzału: ")
            client_socket.sendall(shot.encode())
            print('Wysłano strzał. Czekaj na ruch przeciwnika')

        else: # otrzymano strzał
            print('Otrzymano strzał:', data.decode())

if __name__ == '__main__':

    client_socket = connect_to_server()
    wait_for_msg(client_socket)
    client_socket.close()