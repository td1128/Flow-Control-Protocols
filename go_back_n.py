
import threading
import socket
import json

import time
import Frame
import select
import crcModule as CRC
import checksumModule as Checksum
import channel

TIMEOUT = 4
frame_loss = False

ack_received = {}
def recv_ack(client: socket.socket):
    global ack_received, last_acked_frame , frame_loss
    readable, _, _ = select.select([client], [], [], 0)
    if client in readable:
        try:
            ack = client.recv(1024).decode('utf-8')
            ack_messages = ack.split("ACK:")
            for ack_message in ack_messages:
                if ack_message:
                    ack_frame = int(ack_message)
                    if(ack_frame==-1):
                        frame_loss = True
                    else:
                        print(f"Acknowledgment for Frame {ack_frame-1}")
                        ack_received[ack_frame-1] = True
        except socket.timeout:
            return
            


def go_back_n(client: socket.socket):
    global ack_received, last_acked_frame , frame_loss
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
    ##window_end = min(n, len(fL))  
    while window_start < len(fL):
        #last_acked_frame = window_start
        
        for k in range(window_start, min(window_start+n,len(fL))):
            print(f"Sending Frame {k}")
            client.send((fL[k]+"\n").encode('utf-8'))
            time.sleep(1)
        ack_threads = []
        
        for k in range(window_start, min(window_start+n,len(fL))):
            ack_received[k] = False
            ack_thread = threading.Timer(TIMEOUT,recv_ack, args=(client,))
            ack_threads.append(ack_thread)
            ack_thread.start()

       
        for ack_thread in ack_threads:
            ack_thread.join()
        
        
        if not frame_loss:
            sorted_items = sorted(ack_received.items())
            sorted_dict = dict(sorted_items)
            for l in range (window_start , min(window_start+n,len(fL))):
                if l in ack_received:
                    if l>last_acked_frame:
                        last_acked_frame = l
            window_start = last_acked_frame+1
        else:
            while frame_loss:
                for k in range(window_start, min(window_start+n,len(fL))):
                    print(f"resending Frame {k}")
                    client.send((fL[k]+"\n").encode('utf-8'))
                    time.sleep(1)
                frame_loss = False
                for k in range(window_start, min(window_start+n,len(fL))):
                    ack_received[k] = False
                    ack_thread = threading.Timer(TIMEOUT,recv_ack, args=(client,))
                    ack_threads.append(ack_thread)
                    ack_thread.start()
                for ack_thread in ack_threads:
                    ack_thread.join()
                if not frame_loss:
                    break
            sorted_items = sorted(ack_received.items())
            sorted_dict = dict(sorted_items)
            #print(sorted_dict)
            last_acked_frame = -1
            for l in range (window_start , min(window_start+n,len(fL))):
                    if l in sorted_dict:
                        last_acked_frame = l
            window_start = last_acked_frame+1
        
       
    print("All frames sent successfully!")
    client.close()
    


def recv(client: socket.socket):
    recved_frame ={}
    try:
        buffer = ""
        while True:
            data = client.recv(4096).decode('utf-8')
            if not data:
                # If the received data is empty, skip processing
                continue
            
            buffer += data
            frames = buffer.split('\n')
            buffer = frames[-1]  # Keep any incomplete frame in the buffer

            for frame in frames[:-1]:  # Process complete frames
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
                            ack_message = "ACK:" + str(header.seq + 1)
                            client.send(ack_message.encode('utf-8'))
                        else:
                            print(f"ERROR IN DATA : Frame{header.seq}")
                            ack_message = "ACK:" + str(-1)
                            client.send(ack_message.encode('utf-8'))
                    else:
                        print(f"Frame:{header.seq} Discarded")
                    

                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")
    finally:
        client.close()





