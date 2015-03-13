#!/usr/bin/env python2

#ELRO Remote Packet:
#
#DDDDD|BBBBB|OO
#
#DDDDD = DipState
#  "0" = on
#  "2" = off
#
#
#BBBBB = Button ID
#  "02222" = A
#  "20222" = B
#  "22022" = C
#  "22202" = D
#
#OO = on/off
#  "02" = on
#  "20" = off
#
#
#---------
#
#Bit Transfer:
#
#BitLength: 320microsec
#
#
#0:
#  HIGH (BitLength*3)
#  LOW (BitLength)
#  HIGH (BitLength*3)
#  LOW (BitLength)
#
#1:
#  HIGH (BitLength)
#  LOW (BitLength*3)
#  HIGH (BitLength)
#  LOW (BitLength*3)
#
#2:
#  HIGH (BitLength)
#  LOW (BitLength*3)
#  HIGH (BitLength*3
#  LOW (BitLength)
#3:
#  HIGH (BitLength*3)
#  LOW (BitLength)
#  HIGH (BitLength)
#  LOW (BitLength*3)

#End (SyncSignal):
#  HIGH (BitLength)
#  LOW (BitLength*31)

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import wiringpi
    
pin = 4         # wiringpi pin the sender is attached to
bitLength = 320 # microseconds for each bit
repeats = 8     # sometimes the reciever won't pick up the first transmission -> try multiple times

def parseQuery(string):
        string = string.upper()
        data = []
        
        #Generate SystemCode bits
        for i in range(5):
                if string[i] == "1":
                        data.append(0)
                else:
                        data.append(2);
                        
        #Get unit code
        button = string[6]
        if button == "A":
                data.extend([0,2,2,2,2])
        elif button == "B":
                data.extend([2,0,2,2,2])
        elif button == "C":
                data.extend([2,2,0,2,2])
        elif button == "D":
                data.extend([2,2,2,0,2])
        else:
                data.extend([2,2,2,2,0])
                
        #Get on state
        if string[8] == "1":
                data.extend([0,2]);
        else:
                data.extend([2,0]);
        
        return data;
    
def init():
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(pin, wiringpi.OUTPUT);
        wiringpi.digitalWrite(pin, wiringpi.LOW);
        
        return

def send(data):
        for i in range(repeats):
                sendRawData(data)
                sendSync()
        
        return

def sendRawData(data):
        for x in data:
                if x == 0:
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength*3);
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength*3);

                elif x == 1:
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength*3);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength);
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength*3);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength);
                        
                elif x == 2:
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength*3);
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength*3);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength);
                else:
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength*3);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength);
                        wiringpi.digitalWrite(pin, wiringpi.HIGH);
                        wiringpi.delayMicroseconds(bitLength);
                        wiringpi.digitalWrite(pin, wiringpi.LOW);
                        wiringpi.delayMicroseconds(bitLength*3);
                        
        return

def sendSync():
        wiringpi.digitalWrite(pin, wiringpi.HIGH);
        wiringpi.delayMicroseconds(bitLength);
        wiringpi.digitalWrite(pin, wiringpi.LOW);
        wiringpi.delayMicroseconds(bitLength*31);
        
        return
        
class GetHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        self.wfile.write("<HTML><BODY>")
        
        self.wfile.write("<table border=\"0\" style=\"border-spacing:50px\" >")
        self.wfile.write("<caption style=\"top\">Room</caption>")
        
        self.wfile.write("<tr><td>Light</td><td><a href=\"?11011,A,1\">ON</a></td><td><a href=\"?11011,A,0\">OFF</a></td></tr>")
        self.wfile.write("<tr><td>Desklight</td><td>, the</td><td><a href=\"?11011,B,0\">OFF</a></td></tr>")
        
        self.wfile.write('</table>')
        
        self.wfile.write("</BODY></HTML>")
        
        if len(parsed_path.query) == 9:
                send(parseQuery(parsed_path.query))
        
        return

def main():
        init()

        server = HTTPServer(('', 9123), GetHandler)
        print("Remote control server started")
        
        server.serve_forever()
        
        return 0
        
if __name__ == "__main__":
    main()
