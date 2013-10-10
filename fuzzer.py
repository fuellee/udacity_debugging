'''
File: fuzzer.py
Author: fuel
Description: Fuzz Testing input generator, function fuzzer generates a random string.
'''
import random

def fuzzer():
    string_length = int(random.random()*1024)
    out = ""
    for i in range(0,string_length):
        c = chr(int(random.random()*96 + 32))
        out += c
    return out

print fuzzer()
print fuzzer()

