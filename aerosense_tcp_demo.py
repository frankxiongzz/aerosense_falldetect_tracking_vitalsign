import socket
import sys
from struct import unpack
import threading

def bytes_to_float(raw):
    bdata = bytes(raw)
    return unpack('f', bdata)[0]

def bytes_to_int(raw):
    bdata = bytes(raw)
    return unpack('i', bdata)[0]


def get_tansmit_rate(client_socket):
    sendBuffer = [0xAA, 0xAA, 0x55, 0x55, 0x04, 0x00, 0x00, 0x22, 0x00, 0x00, 0x00, 0x00]
    client_socket.send(bytes(sendBuffer))

def handle_client(client_socket):

    get_tansmit_rate(client_socket)

    while True:
        readBuffer = client_socket.recv(1024)
        readLen = len(readBuffer)
        if readLen >= 12:
            header = readBuffer[0:4]
            if header[0] == 0xAA and header[1] == 0xAA and header[2] == 0x55 and header[3] == 0x55:
                tag = bytes_to_int(readBuffer[4:8])
                if tag == 0x00E1:
                    n = bytes_to_float(readBuffer[8:12])
                    x = bytes_to_float(readBuffer[12:16])
                    y = bytes_to_float(readBuffer[16:20])
                    z = bytes_to_float(readBuffer[20:24])
                    breathOut = bytes_to_float(readBuffer[44:48])
                    heartBeatOut = bytes_to_float(readBuffer[48:52])
                    breathBPM = bytes_to_float(readBuffer[44:48])
                    heartBeatBPM = bytes_to_float(readBuffer[44:48])
                    uuid = readBuffer[60:72]
                    print("----------------------------")
                    print(str(uuid))
                    print("n: %f, x: %f, y: %f, z: %f"%(n, x, y, z))
                    print("breathOut: %f, heartBeatOut %f, heartBeatOut %f, heartBeatBPM %f"%(breathOut, heartBeatOut, breathBPM, heartBeatBPM))
                elif tag == 0x0022:
                    
                    transmitRate = bytes_to_int(readBuffer[8:12])
                    print("Firmware transmit rate %f second"%(transmitRate / 10))
                else:
                    print(".....")

def start_localhost_server():
    bind_ip = "0.0.0.0"
    bind_port = 8899

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)

    print("[*] Listening on %s:%d" % (bind_ip, bind_port))

    while True:
        client, addr = server.accept()
        print("[*] client accepted")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


if __name__ == "__main__":
    start_localhost_server()
