import threading
import server

t1 = threading.Thread(target=server.send_message, args=())
t2 = threading.Thread(target=server.get_message, args=())

t1.start()
t2.start()