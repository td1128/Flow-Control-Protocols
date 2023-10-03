import ErrorModule as ERR
import time
import random
# def increaseTime(data):
#     time.sleep(4)
#     return ""


def channel(data):
    functions = [ERR.no_error, ERR.single_bit_error]
    callError = random.choice(functions)
    modified_data = callError(data)
    return modified_data