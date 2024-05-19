import socket

def connect_to_server() -> socket.socket:
    """
    Connects to the server and returns the client socket.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    return client_socket

def wait_for_msg(client_socket: socket.socket) -> None:
    """
    Waits for messages from the server and sends responses.
    """
    while True:
        data = client_socket.recv(1024)
        msg = data.decode()
        match msg:
            case '1':
                print('Waiting for second player...')
            case '2':
                print('We have two players. Game starts!')
            case 'carrier' | 'battleship' | 'cruiser' | 'submarine' | 'destroyer':
                input_str = 'Place your ' + msg + ' (5 fields)\n Starting index (A-J and 1-10): '
                index = input(input_str)
                client_socket.sendall(index.encode())
            case 'rotation':
                rotation = input('Choose rotation (v/h): ')
                client_socket.sendall(rotation.encode())
            case 'shoot':
                shot = input('Shoot! (A-J and 1-10): ')
                client_socket.sendall(shot.encode())
                print('Shot sent. Wait for response...')
            case 'error':
                print('Error. Try again.')
            case 'exit':
                print('Exiting')
                break
            case _:
                print(msg)

if __name__ == '__main__':

    client_socket = connect_to_server()
    wait_for_msg(client_socket)
    client_socket.close()