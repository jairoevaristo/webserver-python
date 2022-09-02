import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5
FILE_SERVER = 'www'

def http_header(code):
	if(code == 200):
		header = "HTTP/1.1 200 OK\n"
	elif(code == 404):
		header = "HTTP/1.1 404 Page not found\n"

	header += "Server: Afrar's Web Server\n"
	header += "Connection: Alive\n\n"

	return header

def handle_request(client_connection):
	request = client_connection.recv(1024)
	data = bytes.decode(request)
	print(data)

	method = data.split()[0]

	if(method == 'GET' or method == 'HEAD'):
		resource = data.split()[1]
		resource = resource.split('?')[0]

		if(resource == '/'): resource = '/index.html'

		resource = FILE_SERVER + resource

		try:
			file = open(resource, 'rb')
			if (method == 'GET'): body = file.read()
			file.close()
			header = http_header(200)
		except Exception as e:
			print("Page not found" + str(e))
			header = http_header(404)

			if(method == "GET"):
				body = """
					<!DOCTYPE html>
					<html>
						<head>
							<title>404: Page not found</title>
						</head>
						<body>
							<h1>Page or resource not found</h1>
						</body>
					</html>
				"""

		http_response = header.encode()
		if(method == "GET"):
			http_response += body
		client_connection.sendall(http_response)
		print("HTTP Response: " + str(http_response) + "\n")

	else:
		print("Bad HTTP Request")


def serve_forever():
	# The server creates a TCP/IP socket
	listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	try:
		# Assigns a local protocol address to the socket
		listen_socket.bind(SERVER_ADDRESS)
	except socket.error as err:
		print("Bind failed. " + str(msg[0] + ' ' + msg[1]))

	# Become a server socket
	listen_socket.listen(REQUEST_QUEUE_SIZE)

	print("HTTP Sever running on port %s \n" % PORT)

	while True:
		# Accept connections from outside
		client_connection, client_address = listen_socket.accept()
		handle_request(client_connection)
		client_connection.close()

if __name__ == '__main__':
	serve_forever()