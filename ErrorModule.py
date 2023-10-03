import random

def no_error(code_word):
    return code_word

def single_bit_error(code_word):
    index = random.randint(0, (len(code_word) - 1))
    code_word_list = list(code_word)
    code_word_list[index] = '1' if code_word_list[index] == '0' else '1'
    code_word_with_error = ''.join(code_word_list)
    return code_word_with_error


def two_isolated_single_bit(code_word):
    index1 = random.randint(0, (len(code_word) - 1))
    index2 = index1
    while index2 == index1:
        index2 = random.randint(0, len(code_word) - 1)
    codeword_list = list(code_word)
    codeword_list[index1] = '1' if codeword_list[index1] == '0' else '1'
    codeword_list[index2] = '1' if codeword_list[index2] == '0' else '0'
    codeword_with_error = ''.join(codeword_list)
    return codeword_with_error


def burst_error(code_word):
    number_of_error = random.randint(3, len(code_word) - 1)
    code_list = list(code_word)
    all_indices = list(range(len(code_word)))
    error_indices = random.sample(all_indices, number_of_error)
    for index in error_indices:
        code_list[index] = '1' if code_list[index] == '0' else '0'
    code_word_with_error = ''.join(code_list)
    return code_word_with_error


def odd_number_of_errors(code_word):
    max_errors = len(code_word) - 1
    code_list = list(code_word)
    even_number_of_error = random.randint(1, max_errors // 2) * 2
    number_of_error = even_number_of_error + 1
    all_indices = list(range(len(code_word)))
    error_indices = random.sample(all_indices, number_of_error)
    for index in error_indices:
        code_list[index] = '1' if code_list[index] == '0' else '0'
    code_word_with_error = ''.join(code_list)
    return code_word_with_error
