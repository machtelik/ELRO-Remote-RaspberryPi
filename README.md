# ELRO-Remote-RaspberryPi

Simple program that provides a web interface to control devices that can be switched by a 4 button Elro remote.

It uses a Raspberry pi, the wiring pi library and a cheap 433mhz sender chip.

To add a button simply add a hyperlink that encodes desired function e.g.

href=\"?11011,B,1\"

The first 5 bits encode the state of the dip switches, then the button (A,B,C or D) an the 0 = off or 1 = on.

