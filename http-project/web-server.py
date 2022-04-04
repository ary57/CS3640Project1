from multiprocessing import connection
import socket
import sys 
import os

from black import out
 
# http://<server-ip-addr>:<server- port-number>/<file-name>
# http://172.17.90.134:12000/hi.html
# http://129.255.226.172:12000/hi.html

#Create a TCP server socket
# serverSocket = socket(AF_INET, SOCK_STREAM)  # added socket. infront of AF_INET and SOCK_STREAM
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Prepare the sever socket
#FillInStart
serverPort = 12000
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
#FillInEnd 

while True:
    print('Ready to serve...') 
    #Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    # print("address:", addr)

    #If an exception occurs during the execution of try clause
    #the rest of the clause is skipped
    #If the exception type matches the word after except
    #the except clause is executed
    try: 
        #Receive the request message from the client
        message = connectionSocket.recv(4096)#FillInStart #FillInEnd 
        # print("!MESSAGE: ", message)         #####
        
        #Extract the path of the requested object from the message
        #The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1] # This line was a source of error. Should we change it? 
        #Because the extracted path of the HTTP request includes 
        #a character '\', we read the path from the second character 
        f = open(filename[1:])
        #Store the entire content of the requested file in a buffer
        outputdata = f.read()
        # print("!OUTPUT DATA: ", outputdata)# <----
        # print("!FILENAME: ", filename)# <----
        
        
        #Send the HTTP response header line to the connection socket
        #FillInStart
        print("HTTP/1.1 200\r\n")
        connectionSocket.send("HTTP/1.1 200\r\n\r\n".encode())
        #FillInEnd

        #Send the content of the requested file to the client 
        for i in range(0, len(outputdata)):
            # print("!PACKET SENT")
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        #Send HTTP response message for file not found
        #FillInStart
        print("HTTP/1.1 404 FILE NOT FOUND\r\n")
        # connectionSocket.send("HTTP/1.1 404 FILE NOT FOUND".encode())
        connectionSocket.send("HTTP/1.1 404\r\n\r\n".encode())
        #FillInEnd
        
        #Close client socket
        connectionSocket.close()

#Terminate the program
serverSocket.close()
sys.exit()