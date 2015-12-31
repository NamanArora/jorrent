from threading import Thread
import Queue
import socket
import os
import time

queue=Queue.Queue()
IP=socket.gethostname()
port=50001
threads=2
sockt=socket.socket()
sockt.bind((IP,port))
sockt.listen(5)
sockt.settimeout(30)

def send(c,addr,byte):
        print 'Thread: ', len(byte)
        t=queue.get()
        c.send(byte)
        queue.task_done()


def getconn():
        c,addr=sockt.accept()
        print "Connected to",addr[0]

        src=raw_input("Enter name of file you want to send: ")
        f=open(src,"rb")
        size=os.path.getsize(src)/threads
        c.send(str(size).encode())
        print 'Sending file of size: ', size

        for i in range(threads):
            byte=f.read(size)
            queue.put(i)
            t=Thread(target=send,args=(c,addr,byte))
            t.setDaemon(True)
            t.start()
            time.sleep(3)

        queue.join()
        f.close()
        print "All threads died"
        c.shutdown(socket.SHUT_RDWR)
        c.close()

try:
    getconn()
except socket.timeout:
    print
