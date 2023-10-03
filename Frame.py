import crcModule as crc
import checksumModule as checksum

class Header:
    def __init__(self, seq, length, destination, source) -> None:
        self.destination = destination
        self.source = source
        self.seq = seq
        self.length = length
class Tailer:
    def __init__(self,frame_check_seq,schema) -> None:
        self.frame_check_seq = frame_check_seq
        self.schema = schema


class Frame:
    def __init__(self,data,seq,length,dst,src,codeword,schema) -> None:
        self.header = Header(seq,length,dst,src)
        self.data = data
        self.tailer = Tailer(codeword,schema)
        
        
def framing(data,schema,seq,lenght):
    if(schema=="CRC"):
        codeword = crc.generate(data,32)
    else:
        codeword = checksum.generate(data)
    
    frame = Frame(data,seq,lenght,"172.28.5.31","172.28.5.31",codeword,schema)
    return frame 
         

    

