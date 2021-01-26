# -*- encoding=utf-8 -*-

import socket

def server():
	#create socket
	s = socket.socket()
	host = "127.0.0.1"
	port = 6666
	#bind
	s.bind((host,port))

	#listen
	s.listen(5)

	while True:
		c, addr = s.accept()
		print('Connect Addr: ',addr)
		c.send(b'Welcome to my server.')
		c.close()

if __name__ == '__main__':
	server()
