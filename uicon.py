#!/usr/bin/python3

from basic_vt import *
RUNNING = True
force_while_loop = True
c = "init"
raw_c = "init"

def uicon():
    global force_while_loop
    global c
    global RUNNING
    global raw_c
    
    vt_clear()
    vt_enable_mouse()
    os.system("stty -icanon -echo")
    while RUNNING:
        try:
            #debug('tick')
            repaint_needed = False

            # get keyboard input, returns -1 if none available (force_while_loop set to true will let you set c manually)
            if not force_while_loop:
                try:
                    raw_c = sys.stdin.buffer.peek()
                    c = sys.stdin.read(1)
                    #debug("read")
                except Exception as e:
                    debug("Error reading from term")
                    debug(e)
                    #try again
                    continue
            else:
                force_while_loop = False


            ####################remap keys... ################
            #Mostly cuz I had to move away from curses (Cannot get keys on a diff thread than the one that draws)


            if len(c) < len(raw_c):
                #clear read buffer
                sys.stdin.read(len(raw_c) - len(c))

                #look for shit
                #          Ctrl + Right
                if raw_c == b'\x1b[1;5C':
                    c = "kRIT5"

                #            Ctrl + Left
                elif raw_c == b'\x1b[1;5D':
                    c = "kLFT5"

                #            Ctrl + up
                elif raw_c == b'\x1b[1;5A':
                    c = "kUP5"

                #            Ctrl + Down
                elif raw_c == b'\x1b[1;5B':
                    c = "kDN5"

                #            right
                elif raw_c == b'\x1b[C':
                    c = "KEY_RIGHT"

                #            left
                elif raw_c == b'\x1b[D':
                    c = "KEY_LEFT"

                #            up
                elif raw_c == b'\x1b[A':
                    c = "KEY_UP"

                #            down
                elif raw_c == b'\x1b[B':
                    c = "KEY_DOWN"

                #            Delete
                elif raw_c == b'\x1b[3~':
                    c = "KEY_DC"

                #            Shift + Tab
                elif raw_c == b'\x1b[Z':
                    c = "KEY_BTAB"

                #            Alt + .
                elif raw_c == b'\x1b.':
                    c = "alt_dot"

                #            Ctrl + Left
                elif raw_c == b'\x1b[1;5D':
                    c = "kLFT5"

                #            Ctrl + Left
                elif raw_c == b'\x1b[1;5D':
                    c = "kLFT5"
                    #            Ctrl + alt + backspace
                elif raw_c == b'\x1b\x08':
                    c = "CAB"
                elif raw_c.startswith(b'\x1b[<0;'):
                    strsplit = str(raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1][:-2]
                    up_down = strsplit[-1][-2:-1]
                    if up_down == "m":
                        c = f"left_mouse_up {x} {y}"
                    elif up_down == "M":
                        c = f"left_mouse_down {x} {y}"
                elif raw_c.startswith(b'\x1b[<1;'):
                    strsplit = str(raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1][:-2]
                    up_down = strsplit[-1][-2:-1]
                    if up_down == "m":
                        c = f"mid_mouse_up {x} {y}"
                    elif up_down == "M":
                        c = f"mid_mouse_down {x} {y}"   
                elif raw_c.startswith(b'\x1b[<2'):
                    strsplit = str(raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1][:-2]
                    up_down = strsplit[-1][-2:-1]
                    if up_down == "m":
                        c = f"right_mouse_up {x} {y}"
                    elif up_down == "M":
                        c = f"right_mouse_down {x} {y}"
                        
                elif raw_c.startswith(b'\x1b[<35'):
                    strsplit = str(raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1][:-2]
                    c = f"mouse_move {x} {y}"

                elif raw_c.startswith(b'\x1b[<34'):
                    strsplit = str(raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1][:-2]
                    c = f"right_drag {x} {y}"
                elif raw_c.startswith(b'\x1b[<33'):
                    strsplit = str(raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1][:-2]
                    c = f"mid_drag {x} {y}"
                elif raw_c.startswith(b'\x1b[<32'):
                    strsplit = str(raw_c).split(';')
                    x = strsplit[-2]
                    y = strsplit[-1][:-2]
                    c = f"left_drag {x} {y}"
                #History page up/down
                elif raw_c.startswith(b'\x1b[5~'):
                    screens[out_put_screen].prev_page()
                    #debug(str(screens[out_put_screen].history.position))
                    c = ""
                    raw_c = ""
                    #update_display(rerender = True)
                elif raw_c.startswith(b'\x1b[6~'):
                    screens[out_put_screen].next_page()
                    #debug(str(screens[out_put_screen].history.position))
                    c = ""
                    raw_c = ""
                    #update_display(rerender = True)
                else:
                    c = raw_c.decode("utf8")
                    #debug("Unhandled KEY: "+ str(raw_c)) #TODO don't let this happen
            else:
                #the only esc key that is one char long is... esc... :)
                
                if c == "\x1b":
                    c = "KEY_ESC"
                #            Back space
                elif raw_c == b'\x7f':
                    c = "KEY_BACK"
                #            enter
                elif raw_c == b"\n":
                    c = "KEY_ENTER"
                elif raw_c == b"\t":
                    c = "KEY_TAB"
                elif raw_c == b" ":
                    c = "KEY_SPACE"
            debug(f"KEYs setup: {c} {raw_c}")
            ############################################################################################################
            #####KEYs are setup, raw_c is input data, c is a char or a readable name like KEY_FISH###########
            ############################################################################################################
            yield((c, raw_c))


        #hanle ctrl+c
        except (KeyboardInterrupt, Exception) as E:
            if isinstance(E, KeyboardInterrupt):
                debug("ctrlc")
                c = 'CTRL_C'
                force_while_loop = True
            else:
                debug("Main Loop Error: " + str(E))
                raise(E)

def debug(error_string):
    print(error_string, file=sys.stderr)

#for event in uicon():
#    print(f"DRIVER: {event}")
