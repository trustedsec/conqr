#!/usr/bin/python
#####################################################
#
# con generation tool
#
#
# This tool is used to generate a conference
#
#####################################################
import shutil
import getpass
import time
import os

# make the directory if not there
if not os.path.isdir("conferences/"):
	os.mkdir("conferences/")

# initial try/except block
try:

	# start the menu system loop
	while 1:
		
		# start the menu
		print "\nWelcome to the ConQR Conference Setup Tool. This tool will walk you\nthrough setting up a new conference and generate everything you will\nneed in order to setup the conference.\n\nPlease take a moment to walk through these steps in order to setup the\nconference."

		print '\nFirst things first, what is the name of the conference, as an example "DerbyCon 3.0"'
		while 1:
			# if we dont specify a name then keep looping
			con_name = raw_input("\n[-] Enter the name of the conference: ")
			if con_name != "":
				break

		# now we need to take in what folder to store under conferences
		print "\nGreat! Thanks. Now we need to know what name to store the conference as. This will\nultimately be under the conferences/ directory in the ConQR folder root.\n\nThis can only be one word, so for example derbycon3"
		while 1:
			conference_folder = raw_input("\n[-] Enter the name to store under the conferences folder: ")
			if not " " in conference_folder:
				if conference_folder != "":
					break

		#
		# mail server to hook into
		#		
		print "\nNow we need to know if you are using your own mail server or gmail.\n\n1. I'm using my own mail server.\n2. I'm using Gmail\n"
		while 1:
			mail_handler = raw_input("[-]Enter number 1 or number 2 for mail provider: ")
			if mail_handler == "1" or mail_handler == "2":
                                # if we are using our own server
                                if mail_handler == "1":
                                        mailserver = raw_input("Enter the smtp address of the mail server: ")
                                        port = raw_input("Enter the port of the mail server: ")

				# if we are using gmail for our mail server
				if mail_handler == "2":
					mailserver = "smtp.gmail.com"
					port = "587"

				break


		#
		# specify username and pwd
		#
		print "\nEnter the username to authenticate to the server, i.e. gmail pwd or your own mail server (can be an email addy)\n"
		while 1:
			username = raw_input("Enter the username to authenticate to the mail server: ")
			if username != "":
				break

		#
		# grab the password
		# 
		print "\nNext we need the password for the account. NOTE that this is STORED in clear inside the conference folder.\n"
		while 1:
			password = getpass.getpass("Enter the password for the mail server (will not show on screen): ")
			if password != "":
				break

		#
		# conference dates
		#
		print "\nEnter the conference dates in whatever format you want, this will be sent in the standard email template (can change this later)\n"
		while 1:
			date = raw_input("Enter the dates for the conference (example September 25 - September 29, 2013): ")
			if date != "":
				break

		# prompt the user to start
		create_con = raw_input("Okay. That's everything we needed. Are you ready to create the conference? [y/n]: ")
		# if no then bomb out and exit
		if create_con == "n": break
		# if yes then omg so hot
		if create_con == "" or create_con.lower() == "y" or create_con == "yes":
			print """                                                         
  ,----..                           ,----..              
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
  `---`                             `---`                """

			print "[*] Prepping the directories needed for the conference."
			time.sleep(1)
			# if there is a conference name like that already
			if os.path.isdir("conferences/" + conference_folder):
				choice1 = raw_input("[-] Old conference detected, do you want to delete it [y/n]: ")
				if choice1 == "n":
					break

				if choice1 == "y":
					shutil.rmtree("conferences/" + conference_folder)
					print "[*] Okay removing the directories..."
					os.mkdir("conferences/" + conference_folder)

			else:
				os.mkdir("conferences/" + conference_folder)

			print "[*] Finished creating a new folder under conferences/" + conference_folder
			print "[*] Creating necessary file and folder structures..."
			os.mkdir("conferences/%s/database" % (conference_folder))
			print "[*] Created database folder, this will store the attendees."
			os.mkdir("conferences/%s/configuration" % (conference_folder))
			print ("[*] Creating the configuration directory, this will be used for your config.")			
			os.mkdir("conferences/%s/src" % (conference_folder))
			print ("[*] Created the src directory, used for housing the main application.")
			print ("[*] We have all of the necessary files, now writing out everything we need.")

			# copy the appropriate files over
			shutil.copy("src/core.py", "conferences/%s/src/" % (conference_folder))
			shutil.copy("src/conqr.py", "conferences/%s/" % (conference_folder))
			shutil.copy("src/qrcode_server.py", "conferences/%s/src" % (conference_folder))
			shutil.copy("src/__init__.py", "conferences/%s/src" % (conference_folder))
			shutil.copy("src/qrcode.py", "conferences/%s/src" % (conference_folder))
            shutil.copy("src/con_noprompt.py", "conferences/%s/src" % (conference_folder))
			# write out the file
			filewrite = file("conferences/%s/configuration/config" % (conference_folder), "w")
			filewrite.write("""
#
# ConQR automatic configuration file. This contains all of the information 
# needed in order to use the ConQR applicaton successfully
#
#
# SMTP USERNAME
SMTP_USER="%s"
# SMTP PASSWORD
SMTP_PASS="%s"
# SMTP SERVER ADDRESS
SMTP_SERVER="%s"
# PORT FOR SMTP SERVER
SMTP_PORT="%s"
# MAIN SPEAKER TEMPLATE
SPEAKER_TEMPLATE="Greetings!\\n\\nYou have been accepted to speak at %s. Attached is your QRCode and your ticket to the conference and your way to receive your speaker package.\\n\\nYou can either have this displayed on a phone or printed out when registering.\\n\\nThank you for the submission and we look forward to your talk!\\n\\nThe %s Team\\n\\nConference dates: %s"
# MAIN SPEAKER SUBJECT
SPEAKER_SUBJECT="Congratulations! You have been accepted to speak at %s!"
# MAIN ATTENDEE TEMPLATE
ATTENDEE_TEMPLATE="Greetings!\\n\\nYou have been successfully registered for %s. The attached QRCode is your ticket into the conference. Don't loose this or you will not be able to gain access to the conference. \\n\\nYou can have the attached QRCode on an electronic device such as a phone, or printed out in order to register at the door.\\n\\nWe look forward to a successful year and look forward to seeing you!\\n\\nThe %s Team\\n\\nConference Dates: %s"
# MAIN ATTENDEE SUBJECT 
ATTENDEE_SUBJECT="%s conference ticket confirmation enclosed."
# MAIN SPONSOR TEMPLATE 
SPONSOR_TEMPLATE="Greetings!\\n\\nAttached is your sponsorship QRCode for the conference. This QRCode acts as your ticket into the conference, so please don't loose it!\\n\\nThank you for the sponsorship to %s and look forward to seeing you!\\n\\nSincerely, \\n\\nThe %s Team\\n\\nConference Dates: %s"
# MAIN SPONSOR SUBJECT
SPONSOR_SUBJECT="%s sponsor tickets and instructions contained in this email!"
# CONFERENCE FOLDER
CONFERENCE_FOLDER="%s"

			""" % (username, password, mailserver, port, con_name, con_name, date, con_name, con_name, con_name, date, con_name, con_name, con_name, date, con_name, conference_folder))
			filewrite.close()
			print "[*] Finished! Congratulations. Now navigate to the conferences/%s directory and run conqr.py" % (conference_folder)
			break

except Exception, e:
	print "Something went wrong, printing the error: " + str(e)

except KeyboardInterrupt:
	print "\n\n[*] Exiting the ConQR system, thanks for shopping with us."
	print "\n[*] Visit us at https://www.trustedsec.com"

finally: 
	print "[*] Thanks for using the ConQR generator. Please visit https://www.trustedsec.com for more goodness."
