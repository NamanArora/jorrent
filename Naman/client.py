from threading import Thread
import Queue
import socket
import time
queue=Queue.Queue()
IP=socket.gethostname()
port=50001
threads=2
sockt=socket.socket()
sockt.settimeout(30)

def receiver(c,size):
        t=queue.get()
        tempdest=dest+str(t)
        f=open(tempdest,"wb")
        byte= c.recv(size)
        print 'Thread: ', len(byte)
        f.write(byte)
        queue.task_done()
        f.close()


sockt.connect((IP,port))
dest=raw_input("Save as: ")
size=int(sockt.recv(8).decode())

print 'Sending file of size: ', size

for i in range(threads):
            queue.put(i)
            t=Thread(target=receiver,args=(sockt,size))
            t.setDaemon(True)
            t.start()
            time.sleep(3)

queue.join()
print "All threads died"



