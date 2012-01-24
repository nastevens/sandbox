from socket import socket, AF_INET, SOCK_STREAM

def echo_client(client_sock, addr):
	print('Got connection from', addr)
	print('Socket fd:', client_sock.fileno())
	print(type(client_sock))
	
	# Make text-mode file wrappers for read/write
	client_in = client_sock.makefile('r', encoding='latin-1')
	client_out = client_sock.makefile('w', encoding='latin-1')

	# This method doesn't work under Windows because the number returned by socket.fileno
	# is not a valid file descriptor (see http://docs.python.org/3/library/socket.html#socket.socket.fileno)
	#client_in = open(client_sock.fileno(), 'rt', encoding='latin-1', closefd=False)
	#client_out = open(client_sock.fileno(), 'wt', encoding='latin-1', closefd=False)
	
	# Echo lines back using file io
	for line in client_in:
		client_out.write(line)
		client_out.flush()
	client_sock.close()
	
def echo_server(address):
	with socket(AF_INET, SOCK_STREAM) as sock:
		sock.bind(address)
		sock.listen(1)
		while True:
			client, addr = sock.accept()
			echo_client(client, addr)
		
def main():
	echo_server(('localhost', 8000))
	
if __name__ == '__main__':
	main()