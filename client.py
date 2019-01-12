# server/client stuff https://www.geeksforgeeks.org/simple-chat-room-using-python/
import socket 
import select 
import sys
from yeelight import Bulb
import time
from urllib2 import urlopen

morseSymboles ={"a":".-", "b":"-...", "c":"-.-.", "d":"-..", "e":".", \
				"f":"..-.", "g":"--.", "h":"....", "i":"..", "j":".---",\
				"k":"-.-", "l":".-..", "m":"--", "n":"-.", \
				"o":"---", "p":".--.", "q":"--.-", "r":".-.", "s":"...",\
				"t":"-", "u":"..-", "v":"...-", "w":".--", "x":"-..-", \
				"y":"-.--", "z":"--..", "0":"-----", "1":".----", "2":"..---",\
				"3":"...--", "4":"....-", "5":".....", "6":"-....", "7":"--...",\
				"8":"---..", "9":"----.", ".":".-.-.-", "!":"-.-.--", " ":" "} 
bulb = Bulb("192.168.0.25")
bulb.set_brightness(100)
durationTi = 0.3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print "Correct usage: script, IP address, port number"
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 

my_ip = urlopen('http://ip.42.pl/raw').read()
print "Public IP is : " + str(my_ip)

while True: 
  
	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
	for socks in read_sockets: 
		if socks == server: 
			message = socks.recv(2048) 
			print message 
			for letter in message:
				try:
					for symbol in morseSymboles[letter]:
						if symbol == ".":
							bulb.set_brightness(50)
							time.sleep(durationTi)
							bulb.set_brightness(100)
						elif symbol == "-":
							bulb.set_brightness(50)
							time.sleep(durationTi*3)
							bulb.set_brightness(100)
						else:
							time.sleep(durationTi*7)
						time.sleep(durationTi)
					time.sleep(durationTi*3)
				except:
					pass
		else: 
			message = sys.stdin.readline() 
			server.send(message) 
			sys.stdout.write("<You>") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 
