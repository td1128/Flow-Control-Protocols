import socket as sk
import Frame 
import threading
import stopandwait as STOP_AND_WAIT
import go_back_n as GO_BACK_N
import selective_repeat as SELECTIVE_REPEAT_ARQ


def send():
    server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server.bind(('localhost', 8500))
    server.listen()
    while True:
        client, addr = server.accept()
        print(f"connected with{client}")
        # GO_BACK_N.go_back_n(client)
        SELECTIVE_REPEAT_ARQ.selective_repeatARQ(client)
        break
    
send()
  



