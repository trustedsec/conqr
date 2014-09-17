#!/usr/bin/env python
###############################################################################
#
#  ConQR Web Server. Should work on any OS with Python
#
#  Written by: Dave Kennedy (ReL1K)
#  Website: https://www.trustedsec.com
#
################################################################################

import subprocess
import sys
import socket
import os
import BaseHTTPServer,SimpleHTTPServer,cgi
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from email.MIMEText import MIMEText
import urlparse
import multiprocessing

# main dns class
class DNSQuery:
  def __init__(self, data):
    self.data=data
    self.dominio=''

    tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
    if tipo == 0:                     # Standard query
      ini=12
      lon=ord(data[ini])
      while lon != 0:
        self.dominio+=data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(data[ini])

  def respuesta(self, ip):
    packet=''
    if self.dominio:
      packet+=self.data[:2] + "\x81\x80"
      packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
      packet+=self.data[12:]                                         # Original Domain Name Question
      packet+='\xc0\x0c'                                             # Pointer to domain name
      packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
      packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
    return packet

# grab the ipaddress 
ipaddr = raw_input("Enter the IP address to point machines to the QR Code Web Server: ")

# main dns routine
def dns(ipaddr):
  print "[*] Started DNS Server for ConQR.."
  print "[*] You NEED to configure your wireless AP or network to give DNS to THIS server"
  print "[*] This server will redirect all DNS requests when the QRCode is scanned to the server!"
  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udps.bind(('',53))

  try:
    while 1:
      data, addr = udps.recvfrom(1024)
      p=DNSQuery(data)
      udps.sendto(p.respuesta(ipaddr), addr)
      print 'Response: %s -> %s' % (p.dominio, ipaddr)
  except KeyboardInterrupt:
    print "Exiting the DNS Server.."
    udps.close()

# start dns with multiprocessing
p = multiprocessing.Process(target=dns, args=(ipaddr,))
p.start()

			
# Handler for handling POST requests and general setup through SSL
class HTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	# handle basic GET requests
	def do_GET(self):
	# import proper style css files here
		parsed_path = urlparse.urlparse(self.path)

		counter = 0

		path = parsed_path.path
		query = parsed_path.query

		if path == "/qrcode":
			query = query.replace("q=", "")
			self.send_response(200)
			self.send_header('Content_type', 'text/html')
			self.end_headers()
			fileopen = file("database/conference.txt", "r")
			data = fileopen.read()
			if query in data:
				if not os.path.isfile("database/registered.txt"):
					filewrite = file("database/registered.txt", "w")
					filewrite.write("")
					filewrite.close()

				reg = file("database/registered.txt", "r")
				reg_write = file("database/registered.txt", "a")
				reg_data = reg.read()
				if query in reg_data:
					self.wfile.write("User has already registered at the desk. Please check into this.")

				else:
					reg_write.write(query)
					reg_write.close()
					self.wfile.write('<html><body><BODY BGCOLOR="#66ff66">User has been registered successfully. Refreshing in 10 seconds.<meta HTTP-EQUIV="REFRESH" content="10; url=./"></body></html>')

            	# if it doesnt match then write user wasnt found
            	else:
   				self.wfile.write('<html><body>[!] User was not found. Try manual methods :-(')

		if self.path == "/":
        	        self.send_response(200)
        	        self.send_header('Content_type', 'text/html')
        	        self.end_headers()
                        # title here
                        self.wfile.write("<html><title>ConQR Central Registration Web Server</title>")
                        # main body of the site
                        self.wfile.write("""
  <body onload="document.barcodeform.barcode.focus()">
 <b><br><br><br><center>
<b>Welcome to the ConQR QRCode and Ticketing Web System.</b>
<br><br>
Written by: David Kennedy<br>
Website: <a href="https://www.trustedsec.com">https://www.trustedsec.com</a><br>
Twitter: <a href="https://twitter.com/HackingDave">HackingDave</a> and <a href="https://twitter.com/trustedsec">TrustedSec</a><br>

<br><br>
Instructions:<br><br>
Simply scan a QR code using a mobile device of some sort, doesn't matter which application. When scanned, they will be sent here to check to see if they have already registered or not. If they have, it will let you know and register them.
<br>
</body>
""")               
                        # close up body and html
                        self.wfile.write("</body></html>")

# this ultimately handles the http requests and stuff
def main(server_class=BaseHTTPServer.HTTPServer,handler_class=HTTPHandler):
	try:
	        server_address = ('', int(80))
		httpd = server_class(server_address, handler_class)
		httpd.serve_forever()

        # handle keyboardinterrupts
        except KeyboardInterrupt:
                print "[!] Exiting the web server...\n"
	# handle the rest
	except Exception, error:
                print "[!] Something went wrong, printing error: " + str(error)
		sys.exit()

#if __name__ == "__main__":
print "{*} The ConQR Server is running on port 80, open a local browser or remote to view... {*}"
main()
