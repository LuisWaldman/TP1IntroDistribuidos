from socket import socket, AF_INET, SOCK_DGRAM


SERVER_PORT = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("", SERVER_PORT))
print("El servidor está listo para recibir")
while True:
    message, clientAddress = server_socket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    server_socket.sendto(modifiedMessage.encode(), clientAddress)
