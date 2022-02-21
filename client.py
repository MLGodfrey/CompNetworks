import socket
#HOSTIP = socket.gethostbyname(socket.gethostname())

#FORMAT = "utf-8"
SIZE = 1000

def main():
    IP = input('Enter IP address:')
    #IP = int(inIP)
    inPORT = input('Enter port #')
    PORT = int(inPORT)
    ADDR = (IP, PORT)

    # Start TCP socket.
    # Honestly not sure why I have to init socket in this exact manner
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    try:
    # Connecting to the server.
        client.connect(ADDR)
        print('Connected to server')
        while True:
            cmd = input("RFTCLi>")
            if "RETR" in cmd:
                client.send(cmd.encode())
                print("Request sent, waiting...")
                with open("log.txt",'a') as f:
                    while 1:
                     #append data to log
                        data = client.recv(1000).decode()
                        f.write(data)
                    if "End of file" in data:
                        print('End of file')
                        break
                    print('Closing socket')
                    f.close()
            elif "CLOSE" == cmd:
                print("Connection closing...")
                client.close()
                print("Connection closed")
                break
            else:
                print("Command not recognized. Try again")

    except:
        print("Connection closed")

    client.close()

if __name__ == "__main__":
    main()