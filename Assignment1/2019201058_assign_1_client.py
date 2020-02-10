#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 00:11:53 2020
odt
@author: jeevesh
"""
import functions
import socket
import time
port = 9003
import pyDH
from Crypto.Cipher import DES3
from Crypto import Random
d1 = pyDH.DiffieHellman()
fileNameGloabal=''
sharedKeyGlobal=''
keyToDecrypt=''
cipher_decrypt=None
import pyDH
from Crypto.Cipher import DES3
from Crypto import Random


def sendmessage(message,serversocket):
    serversocket.send(bytes(message,"utf-8"))
    return 



def generateSharedKey(full_msg,clientsocket):
    global cipher_decrypt
    global keyToDecrypt
    
    serverPublicKey=int(full_msg[6:len(full_msg)])
    d1_sharedkey = d1.gen_shared_key(serverPublicKey)
    keyToDecrypt = d1_sharedkey[0:24]
    print('keyToDecrypt')
    print(keyToDecrypt)
    cipher_decrypt = DES3.new(keyToDecrypt, DES3.MODE_ECB)
    return d1_sharedkey



def generatePublicKey():
    
    d1_pubkey = d1.gen_public_key()
    return d1_pubkey
    

def keyExchangeProcess(serversocket):
    
    publicKey=generatePublicKey()
    pKey = createFileDataFrame(str(publicKey),str(10))
    sendmessage(pKey,serversocket)
    
    
    
    return




def loopForKeyAndData(serversocket):

    while True:
        full_msg=''
        msg = s.recv(1022)
        if len(msg) <=0:
            break
        full_msg += msg.decode("utf-8")
        print('msg received at client side')
        print(full_msg)
        
        splitMessage(full_msg,s)
        full_msg=''
    



def encryptedMessageToWrite(full_msg,serversocket):
    #first Data message came
    global fileNameGloabal
    global sharedKeyGlobal
    
    print(len(full_msg))
    print('full_msg')
    print(type(full_msg))
    print(full_msg)
    f = open(fileNameGloabal,'wb')
#    if len(full_msg) == 0:
#        f.close()
#        return
    lenOfMsgStr=full_msg[0:4]
    lenOfMsgStr=lenOfMsgStr.decode()
    lenOfMsg=int(lenOfMsgStr)
    plainText=cipher_decrypt.decrypt(full_msg[6:])
    print('after Decryption data is:')
    print(plainText)
    
    plainText=plainText[0:(lenOfMsg)]
#    plainText=plainText.encode()
#    print('plainText')
#    print(plainText)
#    print('cipher_decrypt.decrypt(plainText)')
#    print(cipher_decrypt.decrypt(plainText))
    f.write(plainText)
    print(plainText)
    
    while True:
        full_msg=''
        msg = s.recv(1022)
        if len(msg) <=0:
            break
        
#        full_msg += msg.decode("utf-8")
        full_msg = msg    
        lenOfMsgStr=full_msg[0:4]
        lenOfMsgStr=lenOfMsgStr.decode()
        lenOfMsg=int(lenOfMsgStr)
        
        lenOfMsgOp=full_msg[4:6]
        lenOfMsgOp=lenOfMsgOp.decode()
        op=int(lenOfMsgOp)
        
        if op == 50:
            f.close()
            print('Done with writing in file')
            return
        
#        lenOfMsgStr=full_msg[0:4]
#        lenOfMsgStr=lenOfMsgStr.decode()
#        lenOfMsg=int(lenOfMsgStr)

        plainText=cipher_decrypt.decrypt(full_msg[6:])
    
        plainText=plainText[0:(lenOfMsg)]
        f.write(plainText)
#        plainText=full_msg[6:6+(lenOfMsg)]
#        print('data received at client side')
#        print('plainText')
#        print(plainText)
#        print('cipher_decrypt.decrypt(plainText)')
#        print(cipher_decrypt.decrypt(plainText))
#        print(plainText)
        
#        f.write(cipher_decrypt.decrypt(plainText))
        
    f.close()   
        
    return


def opCodeAction(opCodeVerify,full_msg,serversocket):
    global sharedKeyGlobal
    if opCodeVerify == 10 :
        print("public key of server received")
        keyExchangeProcess(serversocket)
        sharedKey=generateSharedKey(full_msg,serversocket)
        print('shared key is')
        print(sharedKey)
        sharedKeyGlobal=sharedKey
    elif opCodeVerify == 99 :
        print(full_msg[6:len(full_msg)])
    elif opCodeVerify == 98 :
        print('file is found on server')
        print('now going to loop to wait for key exchange and data')
       # loopForKeyAndData(serversocket)
    elif opCodeVerify == 30 :
       # encryptedMessageToWrite(full_msg,serversocket)
        print('Encrypted msg going to come')
    
    return
    


def splitMessage(full_msg,s):
    #print(full_msg)
    opCodeVerify=int(full_msg[4:6])
    opCodeAction(opCodeVerify,full_msg,s)
    return 



def sendFilePath(fileNameDataFrame,s):
    s.send(bytes(fileNameDataFrame,"utf-8"))
    return 


def createFileDataFrame(file_path,op):
    dataFrame=''
    #print(type(file_path))
    filePathLen=len(file_path)
    length=f'{filePathLen:>4}'
    #print(type(f'{filePathLen > : 4}'))
    dataFrame += str(length)
    dataFrame += op
    #dataFrame += str(20)
    dataFrame += file_path
    
    #print(dataFrame)
    #print(len(dataFrame))
    return dataFrame


s=socket.socket()
s.connect(('127.0.0.1',port))
#print('waiting for iv')
#iv = s.recv(8)
#print('iv')
#print(iv)
full_msg = ''
file_path = input('Enter file path of file you need : ')
print(file_path)
#fileNameGloabal=file_path
fileNameGloabal="/home/jeevesh/Desktop/test111.odt"
fileNameDataFrame = createFileDataFrame(file_path,str(20))
sendFilePath(fileNameDataFrame,s)

while True:
    full_msg=''
    msg=''
    time.sleep(2)
    msg = s.recv(1022)
    if len(msg) <=0:
        break
    print(len(msg))
    print(type(msg))
    dat=msg[0:6]
    dat = dat.decode()
    print(dat)
    opstring=msg[4:6]
    opstring=opstring.decode()
    print(opstring)
    print(opstring)
    op=int(opstring)
    print(op)
    oplength=msg[0:4]
    oplength=oplength.decode()
    print(oplength)
    print(int(oplength))
    
    
    
    if op == 30:
        encryptedMessageToWrite(msg,s)
    else:    
        print(full_msg)    
        full_msg = msg.decode()
        print(full_msg)
        print(len(full_msg))
        splitMessage(full_msg,s)
        full_msg=''
        
