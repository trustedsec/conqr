import pexpect
import sys
try:
    ipaddr = sys.argv[1]
except IndexError:
    print("Usage: python con_noprompt.py <ipaddr of conqr server>")
    sys.exit()

child = pexpect.spawn("python conqr.py 4")
child.expect("Enter the IP address to point machines")
child.sendline(ipaddr)
child.interact()
