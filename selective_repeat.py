import threading
import socket
import json
import time
import Frame
import select
import crcModule as CRC
import checksumModule as Checksum
import channel

n=0


TIMEOUT = 6
ack_received = {}
frame_loss = False        
def recv_ack(client: socket.socket):
    global ack_received, frame_loss
    readable, _, _ = select.select([client], [], [], 0)
    if client in readable:
        try:
            ack = client.recv(1024).decode('utf-8')
            ack_messages = ack.split("\n")  # Split messages based on delimiter '\n'
            for ack_message in ack_messages:
                if ack_message:
                    if ack_message.startswith("ACK"):
                        frame_no = int(ack_message[4:])
                        ack_received[frame_no - 1] = True
                        print(f"ACK Frame: {frame_no - 1}")
                    elif ack_message.startswith("NCK"):
                        frame_no = int(ack_message[4:])
                        ack_received[frame_no] = False
                        frame_loss = True
                        print(f"NCK Frame: {frame_no}")
        except socket.timeout:
            return        

def selective_repeatARQ(client: socket.socket):
    global ack_received, last_acked_frame , frame_loss,n
    last_acked_frame = -1 
    n = int(input('Enter the window Size: '))
    schema = input("Enter Schema type (1:CHECKSUM, 0:CRC): ")
    fL = []
    with open('./data.txt', 'r') as file:
        line = file.readline()
        line = line.strip()
        seq = 0
        i = 0
        data = line[i:368]
        while len(data) != 0:
            if schema == "1":
                frame = Frame.framing(data, "CHECKSUM", seq, len(data))
            elif schema == "0":
                frame = Frame.framing(data, "CRC,", seq, len(data))
            else:
                print("**Invalid choice**")
            serialized_frame = json.dumps({
                "header": frame.header.__dict__,
                "data": data,
                "tailer": frame.tailer.__dict__
            })
            fL.append(serialized_frame)
            seq += 1
            i += 368
            data = line[i:i + 368]
    window_start = 0  
    while window_start < len(fL):
        for k in range(window_start, min(window_start+n,len(fL))):
            print(f"Sending Frame {k}")
            client.send(fL[k].encode('utf-8'))
            time.sleep(2)
        ack_threads = []
        #print("Here")
        for k in range(window_start, min(window_start+n,len(fL))):
            ack_received[k] = False
            ack_thread = threading.Timer(TIMEOUT,recv_ack, args=(client,))
            ack_threads.append(ack_thread)
            ack_thread.start()       
        for ack_thread in ack_threads:
            ack_thread.join()

        print(ack_received)

        while frame_loss:
            for k in range(window_start, min(window_start+n,len(fL))):
                if k in ack_received:
                    if not ack_received[k]:
                        print(f"Resending Frame:{k}")
                        client.send(fL[k].encode('utf-8'))
                        time.sleep(2)
            frame_loss = False
            for k in range(window_start, min(window_start+n,len(fL))):
                if k in ack_received:
                    if ack_received[k] == False:
                        ack_thread = threading.Timer(TIMEOUT,recv_ack, args=(client,))
                        ack_threads.append(ack_thread)
                        ack_thread.start()       
            for ack_thread in ack_threads:
                ack_thread.join()
            if not frame_loss:
                break
        window_start = window_start+n

        
      
    print("All frames sent successfully!")
    client.close()


def recv(client:socket.socket):
    n =4
    frame_buffer = []
    recved_frame ={}
    try:
        while True:
            for i in range (0,n):
                readable, _, _ = select.select([client], [], [], 0)
                if client in readable:
                    data = client.recv(4096).decode('utf-8')
                    if not data:
                        continue
                    frame_buffer.append(data)
            for frame in frame_buffer:
                try:
                    serialized_frame_data = json.loads(frame)
                    frame_header = serialized_frame_data["header"]
                    frame_tailer = serialized_frame_data["tailer"]
                    data = serialized_frame_data["data"]
                    header = Frame.Header(**frame_header)
                    tailer = Frame.Tailer(**frame_tailer)
                    if header.seq not in recved_frame:
                        print(f"Received Frame {header.seq}")
                        codeword = ""
                        modified_data = channel.channel(data)
                        if tailer.schema == "CRC":
                            codeword = CRC.crc_generator(modified_data)
                        else:
                            codeword = Checksum.generate(modified_data)

                        if codeword == tailer.frame_check_seq:
                            recved_frame[header.seq] = True
                            ack_message = "ACK:" + str(header.seq + 1)+"\n"
                            client.send(ack_message.encode('utf-8'))
                        else:
                            print(f"ERROR IN DATA : Frame{header.seq}")
                            ack_message = "NCK:" + str(header.seq)+"\n"
                            client.send(ack_message.encode('utf-8'))
                        
                    else:
                        pass
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")
            frame_buffer.clear()
    finally:
        client.close()



        
    
