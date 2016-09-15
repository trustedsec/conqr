# ConQR - An open source platform for conferences and registration
Copyright 2014 ConQR

Written by: David Kennedy (ReL1K)
Twitter: @HackingDave and @TrustedSec
Website: https://www.trustedsec.com

ConQR is an open source QR Code ticketing system designed for Windows, Linux, or OSX. It's written in Python with no third party modules needed. The tool is designed
to simplify the process for performing ticket issuing. This is the same technique used at DerbyCon 2.0 in Louisville Kentucky which had 2,000 attendees without more than
a one minute wait time. The concept is simple, issue QR Codes, track them in a database, and be able to look them up in a simplfied fashion. The way it works is by sending
the ticket in a form of a QR Code with a randomizesd hash value to an internal website name. The setup requires a wireless access point (or wired) and DNS to point to the
QR Code server. You can use any device you want, such as a iPhone, Android, tablet, etc. Download any software that you want from the AppStore or Android market that allows
you to scan QR Codes. 

Join the handheld device to the wireless network that has the QR Code server, once scanned in, the device will open a URL of the QR Code server. The server handles the request
and identifies if the person has a ticket, has already checked in, or is not found. If found and has not checked in, the user is checked in and the user can successfully enter
the conference. 

### Instructions:

Step 1: 

Run python con_setup.py. 
Answer all of the questions and generate the conference files.
This will place a conference file underneath the "conferences/" folder. 
Feel free to tweet conferences/<con_name>/configuration/config to be whatever you want.

Step 2:

When you are ready, run conqr.py and provide which option you want and a filename if applicable.

### Basic structure:

src/database/conferences.txt - contains all of the email addresses and qrcode hash 
src/database/registered.txt - contains those that have already registered
configration/config - contains the config options for the qrcode system

### QRCode Server:
 
The way that this works is in a normal network topology, you would have the QRCode server sitting on a wireless network thats closed off.

You will need to configure the wireless AP / router to point to the QRCode server for DNS. ConQR has a DNS server it uses through Python
to direct the users to the website.

The website itself runs all of the qrcode tracking. When you first created the folder to store it, that is also the link that is used when a QRCode is scanned.

At the end of the day, the URL is irrelevant, the DNS server will respond to everything. 

download a QRCode app from any App Store or Android Market and scan the QR Code *WHILE* joined to the access point that has DNS pointing to the QRCode Server and on
the same LAN. 

Handheld device ----> joined to access point ----> on same lan as QRCode Server

That's it!

### NO PROMPT

There is a file called con_noprompt.py located in the root of the conference folder. This file will automatically allow you to launch the QRCode server without any prompt. This is useful if you want to have conqr load automatically on boot. Simply just run python con_noprompt.py <IPaddr of conqr server> and that is it.

### TODO:

Web interface is ugly, first release, will make nicer in next release
