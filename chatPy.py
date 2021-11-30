import client
import threading

t1 = threading.Thread(target=client.get_message, args=())
t2= threading.Thread(target=client.send_message, args=())


t1.start()
t2.start()