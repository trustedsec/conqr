###########################################
#
# QRCode Core Library for ConQr
#
###########################################
import os
import hashlib
import random
import subprocess
import re
import time
from src.qrcode import *
import shutil
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

# grab the path for current working directory
definepath = os.getcwd()

# check the config file and return value
def check_config(param):
    fileopen = file("%s/configuration/config" % (definepath), "r")
    for line in fileopen:
        # if the line starts with the param we want then we are set, otherwise if it starts with a # then ignore
        if line.startswith(param) != "#":
            if line.startswith(param):
                line = line.rstrip()
                # remove any quotes or single quotes
                line = line.replace('"', "")
                line = line.replace("'", "")
                line = line.split("=")
                return line[1]

# generate the random hash
def hash():
	# random number between 5 and 9
	rand_num=random.randrange(5,9)
	# generate random 256 character string
	random_data = os.urandom(256)
	# md5 hash the random string and convert it to hex, then take random number
	# between 5 and 9 of that hash
	return hashlib.md5(random_data).hexdigest()[:rand_num]

# generate the qrcode and save it definition 
def gen_qrcode(user, con_name, option):
	qrcode = hash() + "-" + hash() + "-" + hash() + "-" + hash()
	# generate the qrcode 
	qr = QRCode(5, QRErrorCorrectLevel.L)
	qr.addData("http://%s/qrcode?q=%s" % (con_name,qrcode))
	qr.make()
	im = qr.makeImage()
	im.save("qrcode.png", format='png')
	
	# save the qrcode hash in the database for later use
	if not os.path.isfile("database/con.database"):
		filewrite = file("database/con.database", "w")
		filewrite.write("")
		filewrite.close()

	filewrite = file("database/con.database", "a")
	# attendee
	if option == "1": option = "ATTENDEE"
	# speaker
	if option == "2": option = "SPEAKER"
	# sponsr
	if option == "3": option = "SPONSOR"
	# write out qrcode number, email address, and attendee, speaker, or sponsor
	filewrite.write(qrcode + "," + user + "," + option + "\n")
	filewrite.close()

# main mail function to send emails out
def mail(to, subject, text, attach, user, pwd, server, port):

	# Send the message from, to, subject, etc.
	msg = MIMEMultipart()
	msg['From'] = user
	msg['To'] = to
	msg['Subject'] = subject
	msg.attach(MIMEText(text))
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(open(attach, 'rb').read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition',
        		'attachment; filename="%s"' % os.path.basename(attach))
	msg.attach(part)
	mailServer = smtplib.SMTP(server, int(port))
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(user, pwd)
	mailServer.sendmail(user, to, msg.as_string())
	# Should be mailServer.quit(), but that crashes...
	mailServer.close()
