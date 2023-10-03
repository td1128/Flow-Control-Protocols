def checksum_helper(data_word_bin):
    chunk_sum = 0
    for i in range(0, len(data_word_bin), 32):  
        chunk = data_word_bin[i:i + 32]
        chunk_sum += int(chunk, 2)

    while chunk_sum >> 32:
        chunk_sum = (chunk_sum & 0xFFFFFFFF) + (chunk_sum >> 32)
    checksum = 0xFFFFFFFF - chunk_sum  

    return checksum


def generate(data_word_bin):
    sum32 = checksum_helper(data_word_bin)  
    code_word  = format(sum32, '032b')
    return code_word  
    


def validate(code_word):
    sum32 = checksum_helper(code_word)  
    return sum32 == 0xFFFFFFFF  

def all_zero(data):
    for i in range(0, len(data)):
        if data[i] == '1':
            return False
    return True
