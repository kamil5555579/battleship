import socket

# Tworzenie gniazda klienta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adres i port serwera
server_address = ('localhost', 12346)

# Łączenie z serwerem
client_socket.connect(server_address)

try:
    # Odbieranie danych od serwera
    data = client_socket.recv(1024)
    print('Otrzymano:', data.decode())
    if data.decode()[-1] == '1':
        while True:
            # Najpierw wysyłanie wiadomości do serwera
            message = input('Wyślij cos do serwera: ')
            if message == 'exit':
                break
            client_socket.sendall(message.encode())
            print('Wysłano:', message)
            # Odbieranie danych od serwera
            message = client_socket.recv(1024)
            print('Otrzymano:', message.decode())


    elif data.decode()[-1] == '2':
        while True:
            # Najpierw odbieranie danych od serwera
            message = client_socket.recv(1024)
            print('Otrzymano:', message.decode())
            # Wysyłanie wiadomości do serwera
            message = input('Wyślij cos do serwera: ')
            if message == 'exit':
                break
            client_socket.sendall(message.encode())
            print('Wysłano:', message)


finally:
    # Zamykanie gniazda klienta
    client_socket.close()
