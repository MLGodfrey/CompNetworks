from socket import *
import sys

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)
	
# The proxy server is listening at 8888 
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)

while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	## FILL IN HERE...
	tcpSerSock.listen()
	tcpCliSock, addr = tcpSerSock.accept()

	print('Received a connection from:', addr)

	message = tcpCliSock.recv(1024)
	print("Message received: \n")
	niceMessage = message.decode()
	
	print(niceMessage)
	# Extract the filename from the given message

	## FILL IN HERE...
	message = message.decode()
	siteName = (str(message).split('\n')[0].split(" ")[1][1:])
	print("Message decoded: ")
	##print(message.split()[1])
	print(siteName)
	fileName = message.split()[1].partition("/")[2]
	print("Filename extracted: ")
	print(fileName)

	fileExist = "false"

	filetouse = "/" + fileName
	print("File to use: ")
	print(filetouse)

	try:
		# Check wether the file exist in the cache

		## FILL IN HERE...
		if ".com" in fileName:
			f = open(filetouse[1:],"rb")
			outputdata= f.readlines()

			fileExist = "true"

			# ProxyServer finds a cache hit and generates a response message
					
			tcpCliSock.send(b"HTTP/1.0 200 OK\r\n")            
			tcpCliSock.send(b"Content-Type:text/html\r\n")
			for i in range(len(outputdata)):
				print("Reading file: ")
				tcpCliSock.send(outputdata[i])
				tcpCliSock.send(b'\r\n')
				print("Read from cache: ")
			else:
				continue
			## FILL IN HERE...
	except KeyboardInterrupt:
		print("Force closed.")
		exit()
			
			


	# Error handling for file not found in cache, need to talk to origin server and get the file
	except IOError:
		print("IO Error!")
		
		if fileExist == "false": 
			## FILL IN HERE...

			 # Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)
			hostn = fileName.replace("www.","",1)
			print("hostn link: {}".format(fileName))
			try:
				hostn = gethostbyname(hostn)
			except:
				continue
			print("hostn : {}".format(hostn))
			try:
                # Connect to the socket to port 80
				print('try to connect!')
				c.connect((hostn,80))
				get_req = b"GET "+b"http://www." + fileName.encode() + b"/ HTTP/1.0\r\n\r\n"
				print('sending get request!\t Request: {}'.format(get_req))
				c.sendall(get_req)
				content = c.recv(20480)
                #print("content: {}".format(content))
                # storing cache
				cache_file = open(fileName, 'wb+')
				cache_file.write(content)
				tcpCliSock.sendall(content)
				cache_file.close()
			except KeyboardInterrupt:
				print('Ctrl-c, goodbye!')
				exit()

			except:
				print("Illegal request")                                               
		else:
			# HTTP response message for file not found
			tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n")                            
			tcpCliSock.send("Content-Type:text/html\r\n")
			tcpCliSock.send("\r\n")
			pass

	# Close the client and the server sockets    
	tcpCliSock.close() 
tcpSerSock.close()
