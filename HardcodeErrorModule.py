
def single_bit_error_hardcode(code_word):
    index = 3
    code_word_list = list(code_word)
    code_word_list[index] = '1' if code_word_list[index] == '0' else '1'
    code_word_with_error = ''.join(code_word_list)
    return code_word_with_error


def two_isolated_single_bit_hardcode(code_word):
    index1 = 13
    index2 = 29
    codeword_list = list(code_word)
    codeword_list[index1] = '1' if codeword_list[index1] == '0' else '1'
    codeword_list[index2] = '1' if codeword_list[index2] == '0' else '0'
    codeword_with_error = ''.join(codeword_list)
    return codeword_with_error


def burst_error_hardcode(code_word):
    # 1  0   1   0   1   0   0   1   1   0   1   1   1   0   0   1   1   0   1   0   1   0   0  0
    # 1  1   1   0   1   0   1   0   1   1   1   1   0   1   0   1   0   1   0   0   0   0   0   0
    # 0  1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22 23
    code_list = list(code_word)
    error_indices = [1, 6, 7, 9,12,13, 16, 17, 18, 20]
    for index in error_indices:
        code_list[index] = '1' if code_list[index] == '0' else '0'
    code_word_with_error = ''.join(code_list)
    return code_word_with_error
    # return ("11000000000000101"+"11000000000000101")[::-1].zfill(48)[::-1]
    # return ("100000100110000010001110110110111"+"100000100110000010001110110110111")[::-1].zfill(48)[::-1]


def odd_number_of_errors_hardcode(code_word):
    code_list = list(code_word)
    error_indices = [2, 5, 4, 9, 14]
    for index in error_indices:
        code_list[index] = '1' if code_list[index] == '0' else '0'
    code_word_with_error = ''.join(code_list)
    return code_word_with_error