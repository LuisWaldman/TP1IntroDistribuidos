from socket import AF_INET, SOCK_DGRAM, socket


SERVER_NAME = "localhost"
SERVER_PORT = 12000
CLIENT_SOCKET = socket(AF_INET, SOCK_DGRAM)
MESSAGE = "mi frase miniscula"

CLIENT_SOCKET.sendto(MESSAGE.encode(), (SERVER_NAME, SERVER_PORT))
modified_message, serverAddress = CLIENT_SOCKET.recvfrom(2048)
print(modified_message.decode())
CLIENT_SOCKET.close()
