
def crc_generator(n):
    if n == 8:
        return "111010101"
    if n == 10:
        return "11000110011"
    if n == 16:
        return "11000000000000101"
    if n == 32:
        return "100000100110000010001110110110111"


def crc_helper(data_word, n):
    divisor = crc_generator(n)
    codeword = [int(bit) for bit in data_word]
    integer_divisor = [int(bit) for bit in divisor]
    for i in range(0, len(integer_divisor) - 1):
        codeword.append(0)
    for i in range(0, len(data_word)):
        if codeword[i] == 1:
            for j in range(0, len(integer_divisor)):
                codeword[i + j] ^= integer_divisor[j]
    remainder = ''.join(str(bit) for bit in codeword)[-(len(divisor) - 1):]
    return remainder, data_word


def generate(data_word, n):
    remainder, chunk_bin = crc_helper(data_word, n)
    ##codeword = chunk_bin + remainder
    return remainder


def crc_validate(codeword, n):
    codeword_int = [int(bit) for bit in codeword]
    divisor = crc_generator(n)
    divisor_int = [int(bit) for bit in divisor]
    # Perform division
    for i in range(len(codeword) - len(divisor) + 1):
        if codeword_int[i] == 1:
            for j in range(len(divisor)):
                codeword_int[i + j] ^= divisor_int[j]

    # Check if remainder is all zeros
    remainder = ''.join(str(bit) for bit in codeword_int)[-len(divisor) + 1:]
    if remainder == "0" * (len(divisor) - 1):
        return True
    else:
        return False


