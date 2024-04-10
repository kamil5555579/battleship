import socket
import signal
import sys

# Funkcja obsługująca sygnał SIGINT (Ctrl+C)
def signal_handler(sig, frame):
    print('\nPrzerwano działanie serwera.')
    server_socket.close()
    sys.exit(0)

# Ustawienie obsługi sygnału SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Tworzenie gniazda serwera
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Adres i port serwera
server_address = ('localhost', 12346)

# Bindowanie gniazda do adresu i portu
server_socket.bind(server_address)

# Nasłuchiwanie na połączenia
server_socket.listen(1)

print('Serwer nasłuchuje na porcie', server_address[1])


while True:
    # Akceptowanie połączenia
    connection1, client_address1 = server_socket.accept()

    try:
        print('Połączenie z klientem 1', client_address1, 'czekam na drugiego klienta...')
        message = 'Cześć, to serwer! Jesteś klientem 1'
        connection1.sendall(message.encode()) # sendall - nakładka na send, która zapewnia, że wszystkie dane zostaną wysłane

        connection2, client_address2 = server_socket.accept()
        print('Połączenie z klientem 2', client_address2)
        message = 'Cześć, to serwer! Jesteś klientem 2'
        connection2.sendall(message.encode())

        # Odbieranie danych od klienta
        while True:
            data = connection1.recv(1024)
            if data:
                print('Otrzymano:', data.decode())
                connection2.sendall(data)

                data = connection2.recv(1024)
                if data:
                    print('Otrzymano:', data.decode())
                    connection1.sendall(data)
                else:
                    print('Brak danych od klienta')
                    break
            else:
                print('Brak danych od klienta')
                break

    finally:
        # Zamykanie połączenia
        connection1.close()
        connection2.close()
