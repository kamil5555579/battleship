import socket

# Tworzenie gniazda serwera
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adres i port serwera
server_address = ('localhost', 12345)

# Bindowanie gniazda do adresu i portu
server_socket.bind(server_address)

# Nasłuchiwanie na połączenia
server_socket.listen(1)

print('Serwer nasłuchuje na porcie', server_address[1])

# Akceptowanie połączenia
connection, client_address = server_socket.accept()

try:
    print('Połączenie z', client_address)

    # Odbieranie danych od klienta
    while True:
        data = connection.recv(1024)
        if data:
            print('Otrzymano:', data.decode())
        else:
            print('Brak danych od klienta')
            break

finally:
    # Zamykanie połączenia
    connection.close()
