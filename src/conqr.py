#
#
# ConQR - Making it easy for ticketing because, it can totally suck.
# Written by: David Kennedy
# Twitter: @dave_rel1k @TrustedSec
# Website: https://www.trustedsec.com
#
#
import sys
from src.core import *

try:
	option = sys.argv[1]
	if option != "4":
		filename = sys.argv[2]

except IndexError:
	print """  ,----..                           ,----..              
 /   /   \                         /   /   \             
|   :     :  ,---.        ,---,   /   .     :    __  ,-. 
.   |  ;. / '   ,'\   ,-+-. /  | .   /   ;.  \ ,' ,'/ /| 
.   ; /--` /   /   | ,--.'|'   |.   ;   /  ` ; '  | |' | 
;   | ;   .   ; ,. :|   |  ,"' |;   |  ; \ ; | |  |   ,' 
|   : |   '   | |: :|   | /  | ||   :  | ; | ' '  :  /   
.   | '___'   | .; :|   | |  | |.   |  ' ' ' : |  | '    
'   ; : .'|   :    ||   | |  |/ '   ;  \; /  | ;  : |    
'   | '/  :\   \  / |   | |--'   \   \  ',  . \|  , ;    
|   :    /  `----'  |   |/        ;   :      ; |---'     
 \   \ .'           '---'          \   \ .'`--"          
  `---`                             `---`                
ConQR - The Open Source Way for Conference QR Management

Written by: David Kennedy (ReL1K)
TwitteR: @dave_rel1k @TrustedSec
Website: https://www.trustedsec.com	

Verison: 0.1 Alpha Release

Options:

1. Send an email to an attendee or list of attendees
2. Send an email to a speaker or list of speakers
3. Send an email to a sponsor or list of sponsor
4. Start the QRCode Server for check-in (includes DNS server)

Filename:

Filename can either be a single email address or multiple email addresses.

You can also specify a name seperated by a comma, for example:

test@test.com,John Doe

Usage: python conqr.py <option> <filename.txt>
	"""
	sys.exit()

# here is our main routine
try:
	if option == "4":
		print "Launching the QRCode Server..."
		import src.qrcode_server
		sys.exit()
	# validation that we have the right info
	if not os.path.isfile(filename):
		print "[!] Sorry boss. The file was not found, try again."
		sys.exit()

	if option == "1" or option == "2" or option == "3":
		smtp_user = check_config("SMTP_USER=")
		smtp_pass = check_config(r"SMTP_PASS=")
		smtp_server = check_config("SMTP_SERVER=")
		smtp_port = check_config("SMTP_PORT")
		if option == "1":
			template = check_config("ATTENDEE_TEMPLATE=")
			subject = check_config("ATTENDEE_SUBJECT=")
		if option == "2":
			template = check_config("SPEAKER_TEMPLATE=")
			subject = check_config("SPEAKER_SUBJECT=")
		if option == "3":
			template = check_config("SPONSOR_TEMPLATE=")
			subject = check_config("SPONSOR_SUBJECT=")

		# fix the spacing here
		template = "\n".join(template.split("\\n"))
		# main conference folder, we will use this as a URL to visit internally
		conference_folder = check_config("CONFERENCE_FOLDER=")
		print "[*] Opening up the file and reading and sending out emails..."
		# iterate through our list of email addresses
		fileopen = file(filename, "r")
		# if there is a name then we add it to this variable
		for line in fileopen:
			template_name = template
			# strip the line
			line = line.rstrip()
			if "," in line:
				line = line.split(",")
				template_name = template.replace("Greetings!", "Greetings %s," % (line[1]))
				line = line[0]						

			print "[*] Generating QRCode and creating entry in database.."
			# generate the qr code and store in database
			# option 1 is user, option 2 will be used for URL, option 3 is to see if attendee, speaker, sponsor
			gen_qrcode(line, conference_folder, option)
			print "[*] Sending an email and QRCode to %s" % (line)
			# send the emails to the individual 
			mail(line, subject, template, "qrcode.png", smtp_user, smtp_pass, smtp_server, smtp_port)
			time.sleep(0.2)
			os.remove("qrcode.png")

except Exception, e:
	print "Something went wrong! Printing the error: " + str(e)
