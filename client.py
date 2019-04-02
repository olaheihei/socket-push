#coding=utf-8
import socket  
import time  
import struct  
import os  

def sendfile(path):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
	sock.settimeout(2)  
	sock.connect(('your IP',8888))
	FILEINFO_SIZE = struct.calcsize('128sI')
	fhead = struct.pack('128sI',bytes(path.encode('utf-8')),os.stat(path).st_size)
	sock.send(fhead)
	if os.path.isdir(path):
		pass
	else:
		fp = open(path,'rb') 
		while 1:
			filedata = fp.read(1024)
			if not filedata:  
				break
			sock.send(filedata)
		fp.close() 

d = []
f = []
def filefly(path, name=None):
	if os.path.isdir(path):
		d.append(path)
		files = os.listdir(path)
		for file in files:
			filefly(path + '/' + file, file)
	else:
		f.append(path)

#获取所有目录、所有文件路径
filefly('D:/your path')
for path in d:
	time.sleep(1)
	sendfile(path)
for file in f:
	time.sleep(1)
	print(file)
	sendfile(file)

