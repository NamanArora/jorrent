from threading import Thread
import Queue
import socket
import time

threadcon=Queue.Queue()
threadrcv=Queue.Queue()

IP=socket.gethostname()
port=50001
threads=2
sockt=socket.socket()
sockt.settimeout(30)

def receiver(c):
        #Get local thread id
        t=threadcon.get()

        #Get remote thread id
        remote=c.recv(1024)

        #Connected to corresponding thread
        if t==int(remote):
            c.send(str(t))
            print 'Thread: ',t,'connected to: ', remote
            threadcon.task_done()

        #if data has been received
        threadrcv.task_done()

try:
    sockt.connect((IP,port))
    for i in range(threads):
                threadcon.put(i)
                threadrcv.put(0)
                t=Thread(target=receiver,args=(sockt,))
                t.setDaemon(True)
                t.start()
                #Wait for threads to connect
                threadcon.join()

    threadrcv.join()
    print 'Data transfer complete'
    sockt.shutdown(socket.SHUT_RDWR)
    sockt.close()
except socket.error:
    print 'Could not connect to server'


