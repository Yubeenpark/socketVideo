import cv2, imutils, socket
import numpy as np
import time, os
import base64

import threading, wave, pyaudio,pickle,struct

from threading import *

# For details visit pyshine.com
BUFF_SIZE = 65536

BREAK = False
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9699
message = b'Hello'

client_socket.sendto(message,(host_ip,port))


vid = cv2.VideoCapture(1)
class chatThread(Thread):
    def __init__(self,con):
        Thread.__init__(self)
        self.con = con
    def run(self):
        name =current_thread().getName()
        while True:
            if name =='Sender':
                data= input('Server:')
                self.con.send(bytes(data,'utf-8'))
            elif name == 'Reciver':
                recdata = self.con.rect(1024).decode()
                print('Clinet',recdata)


def get_message():
	
    # TCP socket
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_address = (host_ip,port-1)
    print('server listening at',socket_address)
    client_socket.connect(socket_address) 
    print("CLIENT CONNECTED TO",socket_address)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024) # 4K
                if not packet: break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            print('',end='\n')
            print('SERVER TEXT RECEIVED:',frame,end='\n')
            print('CLIENT TEXT SENDING:')
        except:
            
            break

    client_socket.close()
    print('Audio closed')
    os._exit(1)


def send_message():

    # create socket
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_address = (host_ip,port-2)
    print('server listening at',socket_address)
    client_socket.connect(socket_address) 
    print("msg send CLIENT CONNECTED TO",socket_address)
    while True:
        if client_socket: 
            while (True):
                print('CLIENT TEXT SENDING:')
                data = input ()
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                
                    
            

def get_video():

    cv2.namedWindow('RECEIVING VIDEO')        
    cv2.moveWindow('RECEIVING VIDEO', 10,360) 
    fps,st,frames_to_count,cnt = (0,0,20,0)
    while True:
        packet,_ = client_socket.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet,' /')
        npdata = np.fromstring(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            client_socket.close()
            os._exit(1)
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st),1)
                st=time.time()
                cnt=0
            except:
                pass
        cnt+=1
        
    client_socket.close()
    cv2.destroyAllWindows() 

def getsome_message():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host_ip, (port-4)))
    #client.bind((host_ip, (port-4))
    receiver  = chatThread(client)
    receiver.setName('Receiver')

def sendsome_message():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host_ip, (port-5)))
    #client.bind((host_ip, (port-5)))
    sender = chatThread(client)
    sender.setName('seder')


t1 = threading.Thread(target=get_message, args=())
t2= threading.Thread(target=send_message, args=())


t1.start()
t2.start()

t3 = threading.Thread(target=get_video, args=())
#t4 = threading.Thread(target=sendsome_message, args=())
#t5 = threading.Thread(target=getsome_message, args=())

t3.start()
#t4.start()
#t5.start()