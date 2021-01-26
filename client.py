# -*- encoding=utf-8 -*-

import socket

def client():
	#create socket
	s = socket.socket()
	#connect
	s.connect(('127.0.0.1', 6666))

	print('Recv msg: %s, Client: %d' %(s.recv(1024), i))

	s.close()

if __name__ == '__main__':
	for i in range(10):
		client()