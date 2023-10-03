

import random
import threading
import ErrorModule as ERR
import Frame
import time
import socket
import json
import select
import crcModule as CRC
import checksumModule as Checksum
import channel


TIMEOUT = 4
ack_received = False

def recv_ack(client: socket.socket):
    global ack_received
    readable, _, _ = select.select([client], [], [], 0)
    ack_received = False
    if client in readable:
        ack = client.recv(1024).decode('utf-8')
        if len(ack) > 0:
            print(f"{ack}")
            ack_received = True


def stop_and_wait(client: socket.socket):
    global ack_received
    # functions = [ERR.no_error, ERR.single_bit_error]
    with open('./data.txt', 'r') as file:
        line = file.readline()
        line = line.strip()
        seq = 0
        i = 0
        data = line[i:368]
        while len(data) != 0:
            # callError = random.choice(functions)
            schema = input("Enter Schema type (1:CHECKSUM, 0:CRC)")
            if schema == "1":
                frame = Frame.framing(data, "CHECKSUM", seq, len(data))
            elif schema == "0":
                frame = Frame.framing(data, "CRC,", seq, len(data))
            else:
                print("**Invalid choice**")
            
            # modified_data = callError(data)
            serialized_frame = json.dumps({
                "header": frame.header.__dict__,
                "data": data,
                "tailer": frame.tailer.__dict__
            })
            client.send(serialized_frame.encode('utf-8'))
            print(f"Sending Frame: {seq}")
            start_time = time.time()
            ack_thread = threading.Timer(TIMEOUT, recv_ack, args=(client,))
            ack_thread.start()
            ack_thread.join()
            while not ack_received:
                if time.time() - start_time > TIMEOUT:
                    print(f"Resending Frame:{seq}")
                    serialized_frame = json.dumps({
                    "header": frame.header.__dict__,
                    "data": data,
                    "tailer": frame.tailer.__dict__
                     })
                    client.send(serialized_frame.encode('utf-8'))            
                    ack_thread = threading.Timer(TIMEOUT, recv_ack, args=(client,))
                    ack_thread.start()
                    ack_thread.join()
            seq += 1
            i += 368
            data = line[i:i + 368]
        client.close()



def recv(client:socket.socket):
    try:
        while True:
            serialized_frame = client.recv(4096).decode('utf-8')
            if not serialized_frame:
                # If the received data is empty, skip processing
                continue
                
            #print(serialized_frame)
            try:
                serialized_frame_data = json.loads(serialized_frame)
                frame_header = serialized_frame_data["header"]
                frame_tailer = serialized_frame_data["tailer"]
                data = serialized_frame_data["data"]
                header = Frame.Header(**frame_header)
                tailer = Frame.Tailer(**frame_tailer)
                print(f"Received Frame {header.seq}")
                modified_data = channel.channel(data)
                codeword = ""
                if tailer.schema == "CRC":
                    codeword = CRC.crc_generator(modified_data)
                else:
                    codeword = Checksum.generate(modified_data)

                if codeword == tailer.frame_check_seq:
                    ack_message = "ACK:" + str(header.seq + 1)
                    client.send(ack_message.encode('utf-8'))
                else:
                    print("ERROR IN DATA")
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
    finally:
        client.close()
    





# import random
# import ErrorModule as ERR
# import Frame
# import time
# import socket
# import json
# import select

# TIMEOUT = 1

# def stop_and_wait(client: socket.socket):
#     functions = [ERR.no_error, ERR.single_bit_error]
#     with open('./data.txt', 'r') as file:
#         line = file.readline()
#         line = line.strip()
#         seq = 0
#         i = 0
#         data = line[i:368]
#         while len(data) != 0:
#             callError = random.choice(functions)
#             schema = input("Enter Schema type (1:CHECKSUM, 0:CRC)")
#             if schema == "1":
#                 frame = Frame.framing(data, "CHECKSUM", seq, len(data))
#             elif schema == "0":
#                 frame = Frame.framing(data, "CRC,", seq, len(data))
#             else:
#                 print("**Invalid choice**")

#             modified_data = callError(data)
#             serialized_frame = json.dumps({
#                 "header": frame.header.__dict__,
#                 "data": modified_data,
#                 "tailer": frame.tailer.__dict__
#             })
#             client.send(serialized_frame.encode('utf-8'))
#             print(f"Sending Frame: {seq}")
            
#             start_time = time.time()
#             ack_received = False
#             while not ack_received:
#                 if time.time() - start_time > TIMEOUT:
#                     print(f"Resending Frame:{seq}")
#                     modified_data = callError(data)
#                     serialized_frame = json.dumps({
#                         "header": frame.header.__dict__,
#                         "data": modified_data,
#                         "tailer": frame.tailer.__dict__
#                     })
#                     client.send(serialized_frame.encode('utf-8'))
#                     start_time = time.time()  # Reset the timer

#                 # Use select to check if the socket is ready to be read
#                 readable, _, _ = select.select([client], [], [], 0)
#                 if client in readable:
#                     ack = client.recv(1024).decode('utf-8')
#                     if len(ack) > 0:
#                         print(f"{ack}")
#                         ack_received = True

#             seq += 1
#             i += 368
#             data = line[i:i + 368]

# Rest of your code...


