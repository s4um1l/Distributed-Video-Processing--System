import socket,thread
from Tkinter import *
from Tkconstants import *
import os
import time
import sys
from threading import Lock
import random
import subprocess
import getopt
from time import time
import shutil
import string
host=''
port=50007
s=socket.socket()
s.bind((host,port))
s.listen(5)
msg="1.Copy a file\n2.Append data in the file\n3.Trace the file \n4.exit"
def handleclient(conn):
    while True:
	conn.send(msg)
        data=conn.recv(1204)
        if not data:
            break
	if data=="1":
		conn.send("enter the file name with path: ")
		data=conn.recv(1204)
		file1=open(data,'r')
		file2=open(os.path.basename(data),'w')
		for line in file1.readlines():
			file2.writelines(line)
		file1.close()
		file2.close()
		conn.send("\n\nFile Copied...\n\n")
	elif data=="2":
		conn.send("Enter the data to be appended: ")
		data=conn.recv(1204)
		file2=open('server.txt','a')
		file2.writelines(data)
		file2.close()
		conn.send("\n\nData appended\n\n")
	elif data=="3":
		conn.send("Enter cursor position from where you want to trace the file: ")
		data=conn.recv(1204)
		d=int(data)
		file2=open('server.txt','r')
		z=1
		for z in range (0,d,1):
			ch=file2.read(1)
		file_stats = os.stat('server.txt')
		p=file_stats [stat.ST_SIZE]
		for z in range (d,p,1):
			ch+=file2.read(1)
		conn.send(ch)
	else :
		conn.close()
	
while True:
    conn,addr=s.accept()
    print "Server Initiliazation....................."
    
    print 'connected to ',addr
    thread.start_new_thread(handleclient,(conn,))


