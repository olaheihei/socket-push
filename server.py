#coding=utf-8
import socket
import threading
import time
import struct
import re
import os

def filep(filepath):
	filepath = filepath.decode('utf-8').replace('D:', os.path.abspath(os.curdir)).replace('\\', '/')
	if '.' in filepath:
		return filepath
	if not os.path.exists(filepath):
		os.mkdir(str(filepath))
		print('mkdir:%s' %filepath)
	return filepath


def function(newsock, address): 
	FILEINFO_SIZE = struct.calcsize('128sI')
	fhead = newsock.recv(FILEINFO_SIZE)
	filename, filesize = struct.unpack('128sI', fhead) 
	filename = filename.strip(b'\00')
	file = filep(filename)
	if os.path.isdir(file):
		pass
	else:
		fp = open(file,'wb')
		restsize = filesize 
		while True:
			if restsize > 1024:
				filedata = newsock.recv(1024)
			else:
				filedata = newsock.recv(restsize)
				fp.write(filedata)  
				break
			if not filedata:
				break
			fp.write(filedata)
			restsize = restsize - len(filedata)
			if restsize <= 0:  
				break
		fp.close()
		print("recv succeeded !!File named:",filename)



sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('',8888))
sock.listen(1)
print( 'Serving HTTP on port 8888 ...' )

while True:  
	newsock, address = sock.accept()
	tmpThread = threading.Thread(target=function,args=(newsock,address))
	tmpThread.start()
	time.sleep(0.5)
	print( '\nawait another connection..................... ')
	time.sleep(0.5)


