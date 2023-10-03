
        
import socket as sk
import stopandwait as STOP_AND_WAIT
import go_back_n as GO_BACK_N 
import selective_repeat as SELECTIVE_REPEAT_ARQ

client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
client.connect(('localhost', 8500))
# GO_BACK_N.recv(client)
SELECTIVE_REPEAT_ARQ.recv(client)
client.close()



   