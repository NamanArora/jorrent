from threading import Thread
import Queue
import socket
import os
import time

#threadcon checks if threads are connected
#threadsent checks if data has been sent from each thread
threadsent=Queue.Queue()
threadcon=Queue.Queue()

IP=socket.gethostname()
port=50001
threads=2
sockt=socket.socket()
sockt.bind((IP,port))
sockt.listen(5)
sockt.settimeout(30)

def send(c,addr):
        #Set the socket to blocking mode 
        c.setblocking(1)

        #Get thread id
        t=threadcon.get()

        #Send thread id
        c.send(str(t))

        #Get remote thread id
        remote=c.recv(1024)

        #Check if connection succesful
        if int(remote)==t:
            threadcon.task_done()

        #if data has been sent
        threadsent.task_done()


def getconn():
        c,addr=sockt.accept()
        print "Connected to",addr[0]

        for i in range(threads):
            threadcon.put(i)
            threadsent.put(0)
            t=Thread(target=send,args=(c,addr))
            t.setDaemon(True)
            t.start()
            #Wait for threads to connect
            threadcon.join()

        threadsent.join()
        print "Data transfer complete"
        c.shutdown(socket.SHUT_RDWR)
        c.close()

try:
    getconn()
except socket.timeout:
    print 'Server timed out'
