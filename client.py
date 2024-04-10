import socket

# Tworzenie gniazda klienta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adres i port serwera
server_address = ('localhost', 12345)

# Łączenie z serwerem
client_socket.connect(server_address)

try:
    # Wysyłanie wiadomości do serwera
    message = 'Cześć, to klient!'
    client_socket.sendall(message.encode())

finally:
    # Zamykanie gniazda klienta
    client_socket.close()