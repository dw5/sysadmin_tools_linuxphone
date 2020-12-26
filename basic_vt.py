import sys
import os
DEBUG = True

##################VT stuff######################
#The basics
def vt_clear():
    sys.stdout.write('\033[2J')
    sys.stdout.flush()

def vt_move(l,c):
    sys.stdout.write('\033[' + str(int(l) + 1) + ';' + str(int(c) + 1) + 'f')
    sys.stdout.flush()
#def vt_write(na):
    #debug("BAD VT CALL: " + str(na))
def vt_write(vt100):
    try:
        sys.stdout.write(vt100)
        sys.stdout.flush()
    except Exception as E:
        debug("failed write VT\n" + str(E))

def vt_size():
    tmp = os.popen('stty size', 'r').read().split()
    return [int(tmp[0]), int(tmp[1])]

def vt_save_cursor():
    vt_write('\033[s')

def vt_restore_cursor():
    vt_write('\033[u')

def vt_cursor_off():
    vt_write('\033[?25l')
    #os.system('setterm -cursor off')

def vt_cursor_on():
    vt_write('\033[?25h')
    #os.system('setterm -cursor on')
def vt_enable_mouse():
    vt_write('\033[?1000h')
    vt_write('\033[?1003h')
    vt_write('\033[?1015h')
    vt_write('\033[?1006h')

def vt_click_down(row, col):
    return(f'\033[<0;{col};{row}M')

def vt_click_up(row, col):
    return(f'\033[<0;{col};{row}m')

def vt_disable_mouse():
    vt_write('\033[?1001h')


def vt_reset_all():
    vt_write('\033c')

def resize_as_vt(row,col):
    return(f'\033[8;{row};{col}t')

def color_as_vt(fg,bg,bold):
    return_vt = ""
    if bold:
        return_vt = return_vt + '\033[1m'
    else:
        return_vt = return_vt + '\033[0m\033[27m'

    if fg == 'black':
        return_vt = return_vt +  '\033[30m'
    if fg == 'red':
        return_vt = return_vt +  '\033[31m'
    if fg == 'green':
        return_vt = return_vt +  '\033[32m'
    if fg == 'yellow':
        return_vt = return_vt +  '\033[33m'
    if fg == 'blue':
        return_vt = return_vt +  '\033[34m'
    if fg == 'magenta':
        return_vt = return_vt +  '\033[35m'
    if fg == 'cyan':
        return_vt = return_vt +  '\033[36m'
    if fg == 'white':
        return_vt = return_vt +  '\033[37m'


    if bg == 'black':
        return_vt = return_vt +  '\033[40m'
    if bg == 'red':
        return_vt = return_vt +  '\033[41m'
    if bg == 'green':
        return_vt = return_vt +  '\033[42m'
    if bg == 'yellow':
        return_vt = return_vt +  '\033[43m'
    if bg == 'blue':
        return_vt = return_vt +  '\033[44m'
    if bg == 'magenta':
        return_vt = return_vt +  '\033[45m'
    if bg == 'cyan':
        return_vt = return_vt +  '\033[46m'
    if bg == 'white':
        return_vt = return_vt +  '\033[47m'

    return return_vt

def debug(error_string):
    global DEBUG
    global DEBUG_LOG
    DEBUG_LOG = "/dev/shm/compositerm/debug"
    
    if DEBUG:
        with open(DEBUG_LOG, 'a+') as the_log:
            the_log.write(str(error_string) + "\n")
        #print(error_string, file=sys.stderr)
