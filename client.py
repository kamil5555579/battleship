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
        decoded = data.decode()

        if decoded == '1':
            print('Waiting for second player...')

        elif decoded == '2':
            print('We have two players. Game starts!')

        elif decoded == 'carrier' or decoded == 'battleship' or decoded == 'cruiser' or decoded == 'submarine' or decoded == 'destroyer':
            input_str = 'Place your ' + decoded + ' (5 fields)\n Starting index (A-Z and 1-10): '
            index = input(input_str)
            client_socket.sendall(index.encode())
            # print('Wysłano planszę. Czekaj na planszę przeciwnika')

        elif decoded == 'rotation':
            rotation = input('Choose rotation (v/h): ')
            client_socket.sendall(rotation.encode())

        elif decoded == 'shoot':
            shot = input('Shoot! (A-J and 1-10): ')
            client_socket.sendall(shot.encode())
            print('Shot sent. Wait for response...')

        elif decoded == 'error':
            print('Error. Try again.')
            
        else: # otrzymano strzał
            print('Otrzymano strzał:', decoded)

if __name__ == '__main__':

    client_socket = connect_to_server()
    wait_for_msg(client_socket)
    client_socket.close()