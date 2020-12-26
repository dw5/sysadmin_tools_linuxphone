#!/usr/bin/python3

#iso GPL3
#Copyright (C) 2020 David Hamner
#Copyright (C) 2020 Tobias Frisch (Based on work by)

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import operator
import subprocess
import threading
import time

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from gi.repository.GdkPixbuf import Pixbuf, InterpType

script_path = os.path.dirname(os.path.realpath(__file__))
iso_folder = os.path.expanduser("~/iso")

try:
    os.mkdir(iso_folder)
except Exception:
    pass

os.chdir(iso_folder)
#########################DEFINE Globals##########################
selected_file = None
open_audiobook = None
play_speed = 1.0

files_store = None

page_stack = None
main_page = None

cover_image = None
title_label = None
chapter_progress = None
audiobook_progress = None

audio_extensions = ['wav', "mp3", "ogg"]
image_extensions = ['png','jpg','jpeg']

#########################DEFINE Functions########################
def get_time_len(file):
    global audio_extensions
    
    extension = file.split('.')[-1]
    
    if not extension in audio_extensions:
        return 0
    
    cmd = ["soxi","-D", file] #soxi -D
    return (float(subprocess.check_output(cmd).decode().strip()))

def get_time_format(current):
    seconds = current["location"]
    minutes = seconds / 60
    hours = (int(minutes / 60))
    minutes = (int(minutes) % 60)
    
    seconds = (seconds % 60)
    rest = (int(seconds * 100 - (int(seconds) * 100)))
    seconds = (int(seconds))
    
    txt = "{hours:02d}:{minutes:02d}:{seconds:02d}.{rest:02d}"
    
    return txt.format(hours=hours, minutes=minutes, seconds=seconds, rest=rest)

def get_time_value(txt):
    data = txt.split(':')
    
    hours = int(data[0])
    minutes = int(data[1])
    seconds = float(data[2])
    
    return (seconds + (minutes + (hours * 60)) * 60)

def load_bookmark(directory):
    book_mark = os.path.join(directory, "book_mark.txt")
    current = {
        "index": 0,
        "location": 0
    }
    
    if os.path.exists(book_mark):
        with open(book_mark, "r") as handle:
            data = handle.readlines()
            if (data != None) and (len(data) > 0):
                data = data[0].split('~')
                current["index"] = (int(data[0]))
                current["location"] = (float(data[1]))
    
    return current

def save_bookmark(directory, current):
    book_mark = os.path.join(directory, "book_mark.txt")
    
    with open(book_mark, "w+") as handle:
        handle.write(str(current["index"]) + '~' + str(current["location"]))


def load_store():
    global files_store
    global selected_file

    if files_store == None:
        selected_file = None
        return
    
    files_store.clear()
    file_names = os.listdir(os.getcwd())
    
    file_names.sort()
    
    for file_name in file_names:
        if (file_name[0] != '.'):
            files_store.append([ file_name ])
    
    selected_file = None

def update_progress():
    global open_audiobook
    global chapter_progress
    global audiobook_progress
    
    if open_audiobook == None:
        return
    
    full_time = open_audiobook["full_time"]
    
    if full_time <= 0:
        return
    
    times = open_audiobook["times"]
    
    current = open_audiobook["current"]
    current_index = current["index"]
    current_location = current["location"]
    
    bookmark = open_audiobook["bookmark"]
    
    if (bookmark != None) and (os.path.isdir(bookmark)):
        save_bookmark(bookmark, current)
    
    chapter_time = times[current_index]
    
    if chapter_time > 0:
        fraction = current_location / chapter_time
    else:
        fraction = 0
    
    if chapter_progress != None:
        chapter_progress.set_fraction(fraction)
    
    for index in range(current_index):
        current_location = current_location + times[index]
    
    fraction = current_location / full_time
    
    if audiobook_progress != None:
        audiobook_progress.set_fraction(fraction)

def load_audiobook():
    global open_audiobook
    global cover_image
    global title_label
    
    if open_audiobook == None:
        return
    
    if cover_image != None:
        pixbuf = Pixbuf.new_from_file(open_audiobook["cover"])
        pixbuf = pixbuf.scale_simple(280, 280, InterpType.BILINEAR)
        cover_image.set_from_pixbuf(pixbuf)
    
    if title_label != None:
        title_label.set_text(open_audiobook["title"])
    
    update_progress()

def unload_audiobook():
    global open_audiobook
    
    open_audiobook["playing"] = False
    
    thread = open_audiobook["thread"]
    
    if thread != None:
        thread.join()
    
    open_audiobook["process"] = None
    open_audiobook["thread"] = None

def load_chapter(delta, unload):
    global open_audiobook
    
    playing = open_audiobook["playing"]
    
    if (unload) and (playing):
        unload_audiobook()
    
    current = open_audiobook["current"]
    files = open_audiobook["files"]
    
    new_index = current["index"] + delta
    
    if (new_index < 0) or (new_index >= len(files)):
        new_index = 0
    
    current["index"] = new_index
    current["location"] = 0
    
    update_progress()
    
    if (new_index < len(files)) and (playing):
        GLib.idle_add(play_audiobook)

def load_chapter_by_index(index):
    global open_audiobook
    
    current = open_audiobook["current"]
    
    load_chapter(index - current["index"], True)

def skip(delta):
    global open_audiobook
    
    playing = open_audiobook["playing"]
    
    if playing:
        unload_audiobook()
    
    times = open_audiobook["times"]
    
    current = open_audiobook["current"]
    current_index = current["index"]
    current_location = current["location"]
    
    chapter_time = times[current_index]
    
    new_location = current_location + delta
    
    if current_location < chapter_time:
         new_location = min(new_location, chapter_time)
    
    if current_location > 0:
         new_location = max(new_location, 0)
    
    if new_location > chapter_time:
        load_chapter(+1, False)
    elif new_location < 0:
        load_chapter(-1, False)
    else:
        current["location"] = new_location
    
    update_progress()
    
    if playing:
        play_audiobook()

def thread_play(cmd):
    global open_audiobook
    
    open_audiobook["process"] = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = open_audiobook["process"]
    
    current = open_audiobook["current"]
    
    line = ""
    open_audiobook["playing"] = True
    
    while open_audiobook["playing"]:
        if not process.poll() is None:
            if process.returncode == 0:
                load_chapter(+1, False)
            
            open_audiobook["playing"] = False
            break
        
        output = process.stderr.read(1).decode()
        
        if output != "\r":
            line = line + output
            continue
        
        if "In:" in line:
            time_stamp = line.split("%")[-1].split("[")[0].strip()
            time_left = line.split("[")[1].split("]")[0].strip()
            
            time_stamp = get_time_value(time_stamp)
            time_left = get_time_value(time_left)
            
            current["location"] = min(time_stamp, time_stamp + time_left)
            
            GLib.idle_add(update_progress)
    
    process.kill()

def play_audiobook():
    global open_audiobook
    global play_speed
    
    unload_audiobook()
    
    update_progress()
    
    files = open_audiobook["files"]
    
    if len(files) <= 0:
        return
    
    current = open_audiobook["current"]
    current_index = current["index"]
    current_file = files[current_index]
    
    cmd = [ "play", current_file ]
    
    if current["location"] > 0:
        cmd.extend([ "trim", get_time_format(current) ])
    
    if play_speed != 1.0:
        cmd.extend([ "tempo", str(play_speed), "10", "20", "30" ])
    
    thread = threading.Thread(target=thread_play, args=(cmd,))
    open_audiobook["thread"] = thread
    thread.start()

def guess_target_device():
    found_devices = []
    for device_name in os.listdir("/dev/"):
        if device_name.startswith("sd"):
            device_name = device_name + "1"
            #strip numbers
            device_name =''.join(c for c in device_name if not c.isnumeric())
            found_devices.append(device_name)
            print(device_name)
    the_guess = "/dev/" + found_devices[0]
    return(the_guess)

def phosh_run(cmd):
    global selected_file
    global DD_TARGET
    #local_vars = f"device={DD_TARGET}; iso={selected_file}; device_or_iso={selected_file}; "
    #Local vars are not working... this is a workaround
    cmd = cmd.replace("$device_or_iso", selected_file)
    cmd = cmd.replace("$device", DD_TARGET)
    cmd = cmd.replace("$iso", selected_file)
    
    #cmd = cmd.replace("'", '"')
    #cmd = cmd.replace('"', '\\"')
    cmd = f"clear; echo \\\"{cmd}\\\";read -p \\\"WARNING this is an admin command, close to window to cancel, enter to continue: \\\";{cmd}"
    full_cmd = f"kgx --command \"bash -c '{cmd}'\""
    print(full_cmd)
    os.system(full_cmd)

#########################DEFINE Handlers#########################

def dd_usb(dd_button):
    global DD_CMD
    print(f"Run: {DD_CMD}")
    phosh_run(DD_CMD)
    
def emu_iso(emu_button):
    global EMU_CMD
    print(f"Run: {EMU_CMD}")
    phosh_run(EMU_CMD)

def dd_cmd_update(dd_entry_box):
    global DD_CMD
    DD_CMD = dd_entry_box.get_text()
    print(f"Updated DD command: {DD_CMD}")


def EMU_cmd_update(EMU_entry_box):
    global EMU_CMD
    EMU_CMD = EMU_entry_box.get_text()
    print(f"Updated EMU command: {EMU_CMD}")

def DD_target_update(DD_entry_box):
    global DD_TARGET
    DD_TARGET = DD_entry_box.get_text()
    print(f"Updated DD target: {DD_TARGET}")

def on_directory_up(up_button):
    global selected_file
    
    os.chdir("..")
    load_store()

def on_directory_chosen(browse_button):
    global selected_file
    
    chosen = browse_button.get_filename()
    selection = None
     
    if not os.path.isdir(chosen):
        selection = chosen
        chosen = os.path.split(chosen)[0]

    os.chdir(chosen)
    load_store()

    selected_file = selection

def on_open_selected(open_button):
    global page_stack
    global main_page    
    global selected_file
   
    directory = os.getcwd()
    
    if selected_file != None:
        directory = selected_file
    
    
    page_stack.set_visible_child(main_page)

def on_activated_files(file_treeview, row, col):
    global selected_file
    global page_stack
    global main_page
    global iso_label
    
    model = file_treeview.get_model()
    target = model[row][0]
    
    activated = os.path.join(os.getcwd(), target)
    
    selected_file = activated
    print(f"Selected: {activated}")
    iso_label.set_text(activated.split("/")[-1])
    page_stack.set_visible_child(main_page)

def on_selected_files(files_treeselection):
    global selected_file
    
    (model, pathlist) = files_treeselection.get_selected_rows()
    for path in pathlist:
        tree_iter = model.get_iter(path)
        target = model.get_value(tree_iter, 0)
        
        selected_file = os.path.join(os.getcwd(), target)

def on_destroy(phonic_window):
    global open_audiobook
    
    if open_audiobook != None:
        unload_audiobook()
    
    Gtk.main_quit()


##########################INIT Handlers##########################
handlers = {
    "dd_usb": dd_usb,
    "emu_iso": emu_iso,
    "dd_cmd_update":dd_cmd_update,
    "EMU_cmd_update":EMU_cmd_update,
    "DD_target_update":DD_target_update,
    "on_directory_up": on_directory_up,
    "on_destroy": on_destroy,
    "on_directory_chosen": on_directory_chosen,
    "on_open_selected": on_open_selected,
    "on_activated_files": on_activated_files,
    "on_selected_files": on_selected_files
}


###########################INIT Window###########################
builder = Gtk.Builder()
builder.add_from_file(script_path + '/iso_tools.glade')
builder.connect_signals(handlers)

iso_tools_window = builder.get_object('iso_tools_window')
files_store = builder.get_object('files_store')

page_stack = builder.get_object('page_stack')
main_page = builder.get_object('main_page')
settings_page = builder.get_object('settings_page')
files_page = builder.get_object('files_page')


iso_label = builder.get_object('iso_label')
dd_cmd_entry = builder.get_object('dd_cmd_box')
emu_cmd_entry = builder.get_object('emu_cmd_box')
DD_target_entry = builder.get_object('DD_target')
DD_TARGET = guess_target_device()
DD_target_entry.set_text(DD_TARGET)

DD_CMD = dd_cmd_entry.get_text()
EMU_CMD = emu_cmd_entry.get_text()

#TODO setup to ~/iso
selected_file = os.getcwd()
load_store()

iso_tools_window.show_all()
Gtk.main()

