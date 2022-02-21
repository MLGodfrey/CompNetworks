import socket

IP = socket.gethostbyname(socket.gethostname()) #set server ip to hostname

SIZE = 1000

#FORMAT = "UTF-8"

def main():

    inPORT = input("Set server port #:")
    PORT = int(inPORT)
    print(f"IP address: {IP} Port #: {PORT}")

    ADDR = (IP, PORT)

    print ("Server booting up")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #init server

    server.bind(ADDR) #bind server to ip and port

    server.listen() #set server to listen for connections

    print("Server listening.")

    
    while True:
        try:
            conn, addr = server.accept()

            print(f'{addr} connected.')

            filename = conn.recv(SIZE).decode()

            print(f"[RECV] Receiving the filename.")

            
            if filename.split()[1] != None:
                try:
                    with open(filename, "rb") as f:
                        while 1:
                            contents = f.read(SIZE)
                            if not contents:
                                conn.send("End of file".encode())
                                break
                            conn.sendall(contents)
                            print(f"{filename} sent.")
                    f.close()
                except:
                    conn.send('File not found'.encode())
            else:
                conn.send('Invalid request'.encode())

            # Closing the connection from the client. 
            conn.close()
            print(f"[DISCONNECTED] {addr} disconnected.")
        except:
            ("Connection closed.")
if __name__ == "__main__":
    main()