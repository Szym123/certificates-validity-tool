#!/usr/bin/env python3
# -*- coding: utf8 -*-

from http.server import HTTPServer,BaseHTTPRequestHandler

#################################################################

Config={
    "InputFile":"/root/final.html",
    "Address":"0.0.0.0",
    "Port":8080
}

#################################################################

class MyServer(BaseHTTPRequestHandler):
	# Server class for the file

	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

		with open(Config["InputFile"],'rb')as file:
			self.wfile.write(file.read())

#################################################################

def FileServer(Adress=Config["Address"],Port=Config["Port"]):#Start the server for the file
	WebServer=HTTPServer((Adress,Port),MyServer)
	print("Start on the port:",Port)

	try:
		WebServer.serve_forever()
	except KeyboardInterrupt:
		pass
	# server support for the entire duration of the programme

	WebServer.server_close()
	print("Stop")
	# when program is turn off, it turn off the servere

#################################################################

def main():
    FileServer()

#################################################################

if __name__=="__main__":
    main()