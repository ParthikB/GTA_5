import win32api as wapi
import time



keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890,.'$/\\":
    keyList.append(char)

def input_key():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState((ord(key))):
            keys.append(key)
    return keys

keys = input_key()