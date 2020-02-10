#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 00:11:23 2020

@author: jeevesh
"""
port = 9003

import socket
import os
import functions
import pyDH
import time
from Crypto.Cipher import DES3
from Crypto import Random
d1 = pyDH.DiffieHellman()
import pyDH
from Crypto.Cipher import DES3
from Crypto import Random
import threading

#sharedKeyGlobal=''
#fileNameGloabal=''
#keyToEncrypt=''
#cipher_encrypt=None
#


def splitMessage(full_msg,clientsocket):
    #print(full_msg)
    opCodeVerify=int(full_msg[4:6])
    opCodeAction(opCodeVerify,full_msg,s)
    return 



def generateSharedKey(full_msg,clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt):
#    global cipher_encrypt
#    global keyToEncrypt
    clientPublicKey=int(full_msg[6:len(full_msg)])
    d1_sharedkey = d1.gen_shared_key(clientPublicKey)
    keyToEncrypt.append(d1_sharedkey[0:24])
#    keyToEncrypt = d1_sharedkey[0:24]
    print('keyToEncrypt')
    print(keyToEncrypt[0])
    cipher_encrypt.append(DES3.new(keyToEncrypt[0], DES3.MODE_ECB))
#    cipher_encrypt = DES3.new(keyToEncrypt[0], DES3.MODE_ECB)
    return d1_sharedkey

def generatePublicKey():
   
    d1_pubkey = d1.gen_public_key()
    return d1_pubkey
    

def keyExchangeProcess(clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt):
    
    print('entered inside key exchange process')
    publicKey=generatePublicKey()
    pKey = createFileDataFrame(str(publicKey),str(10))
    print('public key at serrver side')
    print(pKey)
    sendmessage(pKey,clientsocket)
    print('public key send')
    
    
    
    return



def sendmessage(message,clientsocket):
    clientsocket.send(bytes(message,"utf-8"))
    return 



def createFileDataFrame(message,op):
    dataFrame=''
    print(type(message))
    filePathLen=len(message)
    length=f'{filePathLen:>4}'
    #print(type(f'{filePathLen > : 4}'))
    dataFrame += str(length)
    dataFrame += op
    #dataFrame += str(99)
    dataFrame += message
    
    #print(dataFrame)
    #print(len(dataFrame))
    return dataFrame





def splitFilePath(full_msg,clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt):
#    global fileNameGloabal
    file_path=full_msg[6:len(full_msg)]
    dataFrame=''
    try:
        f = open(file_path,'rb')
        
        fileNameGloabal.append(file_path)
#        fileNameGloabal=file_path
        print('fileNameGloabal inside splitFilePath')
        print(fileNameGloabal[0])
        f.close()
        dataFrame = createFileDataFrame("File  Found",str(98))
    except:
        dataFrame = createFileDataFrame("File Not Found",str(99))
        print('dataFrame is executed in except')
        sendmessage(dataFrame,clientsocket)
        return
        
    print('sending msg about client that file is found')
    print(dataFrame)
    sendmessage(dataFrame,clientsocket)
    time.sleep(2)
    print("file path is correct now key sharing will be done")
    keyExchangeProcess(clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt)
    return     
        
        
def sendSetup(full_msg,clientsocket):
#    global sharedKeyGlobal
#    global fileNameGloabal
    f = open(fileNameGloabal,'rb')
    sendDataToClient()
    return


def  opCodeAction(opCodeVerify,full_msg,clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt):
#    global fileNameGloabal
#    global sharedKeyGlobal
    if opCodeVerify == 20 :
        splitFilePath(full_msg,clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt)
    elif opCodeVerify == 10 :
        print("public key of client received")
        sharedKey=generateSharedKey(full_msg,clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt)
        print('shared key is')
        print(sharedKey)
        print(fileNameGloabal[0])
        sharedKeyGlobal.append(sharedKey)

#        sharedKeyGlobal=sharedKey
        #sendSetup(full_msg,clientsocket)
        sendDataToClient(clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt)
    return    

def client_handle(clientsocket , address, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt):
    dataFrame = createFileDataFrame("Connection between client and server has been established",str(99))
    sendmessage(dataFrame,clientsocket)
    #clientsocket.send(bytes("Connection between client and server has been established","utf-8"))
    return 
    

def sendDataToClient(clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt):
#    global sharedKeyGlobal
#    global fileNameGloabal
    print(sharedKeyGlobal)
    print(fileNameGloabal[0])
    if True:
        print('file to open is:::file_path')
        print(fileNameGloabal[0])
        print(len(fileNameGloabal[0]))
        f = open(fileNameGloabal[0],'rb')
        print('file opened is:')
        print(fileNameGloabal[0])
        file_stats = os.stat(fileNameGloabal[0])

        print(file_stats)
        print(f'File Size in Bytes is {file_stats.st_size}')
        numberOfChunk = file_stats.st_size//1016
        lastChunk     = file_stats.st_size%1016
        print(numberOfChunk)
        print(lastChunk)
        
        while True:
            l=f.read(1016)
            if not l:
                dataFrame = createFileDataFrame("DISCONNECT",str(50))
                sendmessage(dataFrame,clientsocket)
                time.sleep(1)
                f.close()
                
                break
            print(l)
            print(type(l))
            length=len(l)
            old_length = (length)
           
            if((length%8)!=0):
                
                temp_msg=l
                s="0"
                j=s.encode()
                temp_msg = temp_msg.ljust(length+(8-(length%8)),j)
                print('after padding')
                print(temp_msg)
                l=temp_msg
            
            
#            if((length%8)!=0):
#                temp_msg=l.decode()
#                temp_msg = temp_msg.ljust(length+(8-(length%8))," ")
#                print('after padding')
#                print(temp_msg)
#                l=temp_msg.encode()
            length=len(l)
            print('after not multiple of 8')
            print(length)
            
            #msg=b''
            print('line1')
            
            msg= f'{old_length:>4}'.encode()
            print(msg)
            print('line2')
            msg += str(30).encode()
            print(msg)
            print('line3')
            print(msg)
            print(type(msg))
            print(type(msg))
            msg += cipher_encrypt[0].encrypt(l)
            print('l')
            print(l)
            print('data before encryption')
            print(l.decode)
            print('cipher_encrypt[0].encrypt(l)')
            print(cipher_encrypt[0].encrypt(l))
            print(type(msg))
            print('line4')
            print(msg)
            clientsocket.send(msg)
            time.sleep(2)
            
        

    
    return;



def clientFunction(clientsocket):
    sharedKeyGlobal=[]
    fileNameGloabal=[]
    keyToEncrypt=[]
    cipher_encrypt=[]
       
    print(f"Connection from {address} has been established")
    client_handle(clientsocket , address, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt)
    while True:
        full_msg=''
        msg = clientsocket.recv(1022)
        if len(msg) <=0:
            break
        full_msg += msg.decode("utf-8")
        print(full_msg)
        opCodeVerify=int(full_msg[4:6])
        opCodeAction(opCodeVerify,full_msg,clientsocket, sharedKeyGlobal,fileNameGloabal, keyToEncrypt,cipher_encrypt)
        print(opCodeVerify)

    
    
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('', port))
s.listen(5)

while True:
    clientsocket , address = s.accept()
    x=threading.Thread(target=clientFunction,args=(clientsocket,))
    x.start()
#    clientFunction(clientsocket)
   