#!/usr/bin/python3
import sys
import os
import time


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from uicon import *

dev_file = '/dev/hidg0'

#Setup USB keyboard gadget mode
if not os.path.exists(dev_file):
    os.system("sudo ./init-usb-gadget.sh")
    time.sleep(1)

#Thanks rmed!
#https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-send-reports
NULL_CHAR = chr(0)

def write_report(report):
    with open(dev_file, 'rb+') as fd:
        fd.write(report.encode())


#Thanks Jarno Baselier!
#https://stackoverflow.com/a/49908917/5282272

#Dictionary
values = {
'a':'write_report(NULL_CHAR*2 +chr(4)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'b':'write_report(NULL_CHAR*2 +chr(5)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'c':'write_report(NULL_CHAR*2 +chr(6)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'd':'write_report(NULL_CHAR*2 +chr(7)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'e':'write_report(NULL_CHAR*2 +chr(8)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'f':'write_report(NULL_CHAR*2 +chr(9)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'g':'write_report(NULL_CHAR*2 +chr(10)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'h':'write_report(NULL_CHAR*2 +chr(11)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'i':'write_report(NULL_CHAR*2 +chr(12)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'j':'write_report(NULL_CHAR*2 +chr(13)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'k':'write_report(NULL_CHAR*2 +chr(14)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'l':'write_report(NULL_CHAR*2 +chr(15)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'm':'write_report(NULL_CHAR*2 +chr(16)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'n':'write_report(NULL_CHAR*2 +chr(17)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'o':'write_report(NULL_CHAR*2 +chr(18)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'p':'write_report(NULL_CHAR*2 +chr(19)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'q':'write_report(NULL_CHAR*2 +chr(20)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'r':'write_report(NULL_CHAR*2 +chr(21)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
's':'write_report(NULL_CHAR*2 +chr(22)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
't':'write_report(NULL_CHAR*2 +chr(23)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'u':'write_report(NULL_CHAR*2 +chr(24)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'v':'write_report(NULL_CHAR*2 +chr(25)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'w':'write_report(NULL_CHAR*2 +chr(26)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'x':'write_report(NULL_CHAR*2 +chr(27)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'y':'write_report(NULL_CHAR*2 +chr(28)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'z':'write_report(NULL_CHAR*2 +chr(29)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'A':'write_report(chr(2)+NULL_CHAR+chr(4)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'B':'write_report(chr(2)+NULL_CHAR+chr(5)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'C':'write_report(chr(2)+NULL_CHAR+chr(6)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'D':'write_report(chr(2)+NULL_CHAR+chr(7)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'E':'write_report(chr(2)+NULL_CHAR+chr(8)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'F':'write_report(chr(2)+NULL_CHAR+chr(9)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'G':'write_report(chr(2)+NULL_CHAR+chr(10)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'H':'write_report(chr(2)+NULL_CHAR+chr(11)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'I':'write_report(chr(2)+NULL_CHAR+chr(12)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'J':'write_report(chr(2)+NULL_CHAR+chr(13)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'K':'write_report(chr(2)+NULL_CHAR+chr(14)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'L':'write_report(chr(2)+NULL_CHAR+chr(15)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'M':'write_report(chr(2)+NULL_CHAR+chr(16)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'N':'write_report(chr(2)+NULL_CHAR+chr(17)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'O':'write_report(chr(2)+NULL_CHAR+chr(18)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'P':'write_report(chr(2)+NULL_CHAR+chr(19)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'Q':'write_report(chr(2)+NULL_CHAR+chr(20)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'R':'write_report(chr(2)+NULL_CHAR+chr(21)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'S':'write_report(chr(2)+NULL_CHAR+chr(22)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'T':'write_report(chr(2)+NULL_CHAR+chr(23)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'U':'write_report(chr(2)+NULL_CHAR+chr(24)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'V':'write_report(chr(2)+NULL_CHAR+chr(25)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'W':'write_report(chr(2)+NULL_CHAR+chr(26)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'X':'write_report(chr(2)+NULL_CHAR+chr(27)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'Y':'write_report(chr(2)+NULL_CHAR+chr(28)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'Z':'write_report(chr(2)+NULL_CHAR+chr(29)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'1':'write_report(NULL_CHAR*2 +chr(30)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'2':'write_report(NULL_CHAR*2 +chr(31)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'3':'write_report(NULL_CHAR*2 +chr(32)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'4':'write_report(NULL_CHAR*2 +chr(33)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'5':'write_report(NULL_CHAR*2 +chr(34)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'6':'write_report(NULL_CHAR*2 +chr(35)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'7':'write_report(NULL_CHAR*2 +chr(36)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'8':'write_report(NULL_CHAR*2 +chr(37)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'9':'write_report(NULL_CHAR*2 +chr(38)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'0':'write_report(NULL_CHAR*2 +chr(39)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'!':'write_report(chr(2)+NULL_CHAR+chr(30)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'@':'write_report(chr(2)+NULL_CHAR+chr(31)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'#':'write_report(chr(2)+NULL_CHAR+chr(32)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'&':'write_report(chr(2)+NULL_CHAR+chr(36)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'*':'write_report(chr(2)+NULL_CHAR+chr(37)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'(':'write_report(chr(2)+NULL_CHAR+chr(38)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
')':'write_report(chr(2)+NULL_CHAR+chr(39)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'-':'write_report(NULL_CHAR*2 +chr(45)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'=':'write_report(NULL_CHAR*2 +chr(46)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'{':'write_report(NULL_CHAR*2 +chr(47)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'}':'write_report(NULL_CHAR*2 +chr(48)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'\\':'write_report(NULL_CHAR*2 +chr(49)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
';':'write_report(NULL_CHAR*2 +chr(51)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'':'write_report(NULL_CHAR*2 +chr(52)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'`':'write_report(NULL_CHAR*2 +chr(53)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
',':'write_report(NULL_CHAR*2 +chr(54)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'.':'write_report(NULL_CHAR*2 +chr(55)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'/':'write_report(NULL_CHAR*2 +chr(56)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'0':'write_report(chr(2)+NULL_CHAR+chr(50)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
':':'write_report(chr(2)+NULL_CHAR+chr(51)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'"':'write_report(chr(2)+NULL_CHAR+chr(52)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'<':'write_report(chr(2)+NULL_CHAR+chr(54)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'>':'write_report(chr(2)+NULL_CHAR+chr(55)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'?':'write_report(chr(2)+NULL_CHAR+chr(56)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'}':'write_report(NULL_CHAR*2 +chr(79)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'{':'write_report(NULL_CHAR*2 +chr(80)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
']':'write_report(chr(2)+NULL_CHAR+chr(79)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',
'[':'write_report(chr(2)+NULL_CHAR+chr(80)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)',

#Next Signs are used for different keymappings - change if you want to
'KEY_ENTER':'write_report(NULL_CHAR*2 +chr(40)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #ENTER
'KEY_ESC':'write_report(NULL_CHAR*2 +chr(41)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #ESC
'KEY_BACK':'write_report(NULL_CHAR*2 +chr(42)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #BACKSPACE
'KEY_TAB':'write_report(NULL_CHAR*2 +chr(43)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #TAB
'KEY_SPACE':'write_report(NULL_CHAR*2 +chr(44)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #SPATIE
'+':'write_report(NULL_CHAR*2 +chr(70)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #PRINT SCREEN
'KEY_DC':'write_report(NULL_CHAR*2 +chr(76)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #DELETE
'CAB':'write_report(chr(5)+NULL_CHAR+chr(76)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #CTRL+ALT+DEL
'kDN5':'write_report(NULL_CHAR*2 +chr(81)+NULL_CHAR*5)\nwrite_report(NULL_CHAR * 8)', #DOWN
}


print("Sending events to /dev/hidg0...")
for event in uicon():
    char = event[0]
    print(f"debug {char}")
    if char in values:
        exec(values[char])
