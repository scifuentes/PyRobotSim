# Simple UDP based client server communication.
# Intended mainly for local comunication inside the same PC or local LAN
# by Santiago Cifuentes

import socket
import errno

class Client:
    def __init__(self,ip='127.0.0.1',port=1005):
        self.ip=ip
        self.port=port
        self.udpsock=socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # Internet, UDP
            
    def Send(self,msgOut):
        self.udpsock.sendto(msgOut,(self.ip,self.port))  #envio -como cadena-
        
    def Read(self):
        msgIn, addr = self.udpsock.recvfrom( 128 )
        return msgIn.split()

    def Request(self,msgOut):
        self.Send(msgOut)
        return self.Read()

class Server:
    def __init__(self,ReceivedMessageCB,ip='127.0.0.1',port=1005):
        self.ip=ip
        self.port=port
        self.AttendMessage=ReceivedMessageCB 
            #callback function for incomming messages
            # signature: ReceivedMessage(self,msgIn,addr):
        
        self.udpsock=socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # Internet, UDP
        self.udpsock.setblocking(False)
        self.udpsock.bind((self.ip,self.port))
        
    def CheckRequests(self,buffsize=128):
        #check if there are incomming messages
        # and attend them
        
        try:
            while True:
                msgIn, addr = self.udpsock.recvfrom( buffsize )
        
                #attend the request
                msgOut=self.AttendMessage(msgIn,addr)        
        
                #something to answer?
                if msgOut!='':
                    self.udpsock.sendto(msgOut,addr)
        
        #keep going if there is no request waiting
        except IOError as e:
            if e.errno == errno.EWOULDBLOCK:
                pass 