# imports needed for GUI
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import messagebox

# imports needed for image acquisition and pdf creation
from PIL import ImageGrab, Image
from time import sleep
import keyboard

# other
import json
import shutil
from zipfile import ZipFile
from pathlib import Path
import os
import sys
from threading import Thread

### FUNCTIONS ###


def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(base_path, relative_path))


def runCapture():
    upl_x = int(upleft_x_entry.get())
    upl_y = int(upleft_y_entry.get())
    botr_x = int(botright_x_entry.get())
    botr_y = int(botright_y_entry.get())
    if upl_x < 0 or upl_y < 0 or botr_x < 0 or botr_y < 0:
        messagebox.showerror('Invalid value', 'Coordinates can\'t be < 0')
        return
    screenshot_num = var.get()
    if screenshot_num < 1:
        messagebox.showerror(
            'Invalid value', 'Screenshots number can\'t be < 1')
        return
    filename = outname_entry.get()
    filename = filename.replace('.pdf', '')
    if filename == '':
        messagebox.showerror(
            'Error', 'You forgot to specify the name of the output PDF')
        return

    imagelist = []
    capture_button.config(state=tk.DISABLED)
    root.iconify()
    for i in range(3, 0, -1):
        print('Minimize me, starting in', i, 'seconds')
        sleep(1)
    for i in range(screenshot_num):
        print('Taking image number ', i+1)
        im = ImageGrab.grab(bbox=(upl_x, upl_y, botr_x, botr_y))
        imagelist.append(im)
        keyboard.press_and_release('page down')
        sleep(1)
    print('Saving PDF to', get_abs_path
          (filename.rstrip()+'.pdf'))
    imagelist[0].save(get_abs_path
                      (filename.rstrip()+'.pdf'), "PDF",
                      resolution=100.0, optimize=True, save_all=True, append_images=imagelist[1:])
    print('Done')
    capture_button.config(state=tk.NORMAL)
    root.deiconify()
    last = {}
    last['upleft_x_entry'] = upl_x
    last['upleft_y_entry'] = upl_y
    last['botright_x_entry'] = botr_x
    last['botright_y_entry'] = botr_y
    last['screnshot_num'] = screenshot_num
    with open(get_abs_path
              ('last_settings.json'), 'w') as json_file:
        json.dump(last, json_file)


def insertIntoLog(str):
    logscroll.config(state=tk.NORMAL)
    logscroll.insert(tk.INSERT, str)
    logscroll.config(state=tk.DISABLED)


if __name__ == "__main__":
    base_path = os.getcwd()

    root = tk.Tk()
    root.geometry('550x290')
    root.resizable(1, 1)
    root.title("Captures to PDF")

    ### TOP FRAME ###
    frame1 = tk.LabelFrame(root, text="Capture area")
    frame1.place(relx=0.018, rely=0.0, relheight=0.33, relwidth=0.967)

    tk.Label(frame1, text="Top-left coordinates").place(relx=0.053,
                                                        rely=0.313, height=22, width=113, bordermode='ignore')
    tk.Label(frame1, text="x").place(relx=0.275, rely=0.104,
                                     height=21, width=32, bordermode='ignore')
    tk.Label(frame1, text="y").place(relx=0.362, rely=0.104,
                                     height=21, width=31, bordermode='ignore')
    upleft_x_entry = tk.Entry(frame1)
    upleft_x_entry.place(relx=0.275, rely=0.313, height=20,
                         relwidth=0.064, bordermode='ignore')
    upleft_y_entry = tk.Entry(frame1)
    upleft_y_entry.place(relx=0.362, rely=0.313, height=20,
                         relwidth=0.064, bordermode='ignore')

    tk.Label(frame1, text="Bottom-right coordinates").place(relx=0.534,
                                                            rely=0.635, height=21, width=141, bordermode='ignore')
    tk.Label(frame1, text="x:").place(relx=0.809, rely=0.417,
                                      height=22, width=32, bordermode='ignore')
    botright_x_entry = tk.Entry(frame1)
    botright_x_entry.place(relx=0.809, rely=0.635, height=20,
                           relwidth=0.064, bordermode='ignore')
    tk.Label(frame1, text="y:").place(relx=0.896, rely=0.417,
                                      height=22, width=32, bordermode='ignore')
    botright_y_entry = tk.Entry(frame1)
    botright_y_entry.place(relx=0.896, rely=0.635, height=20,
                           relwidth=0.064, bordermode='ignore')

    ### LEFT FRAME ###
    frame2 = tk.LabelFrame(root, text="Capture settings")
    frame2.place(relx=0.018, rely=0.344, relheight=0.54, relwidth=0.37)
    tk.Label(frame2, text="Number of captures").place(
        relx=0.049, rely=0.191, height=21, width=124, bordermode='ignore')
    var = tk.IntVar()
    tk.Spinbox(frame2, from_=1, to=1000, textvariable=var).place(
        relx=0.734, rely=0.191, relheight=0.127, relwidth=0.227, bordermode='ignore')

    tk.Label(frame2, text="Output file name (without '.pdf')").place(
        relx=0.049, rely=0.446, height=21, width=190, bordermode='ignore')
    outname_entry = tk.Entry(frame2)
    outname_entry.place(relx=0.049, rely=0.573, height=20,
                        relwidth=0.906, bordermode='ignore')

    ### RIGHT FRAME ###
    frame3 = tk.LabelFrame(root, text="Log")
    frame3.place(relx=0.401, rely=0.347, relheight=0.54, relwidth=0.584)
    logscroll = scrolledtext.ScrolledText(
        frame3, wrap="none", state=tk.DISABLED)
    logscroll.place(relx=0.009, rely=0.121, relheight=0.86,
                    relwidth=0.984, bordermode='ignore')

    ### BOTTOM ###
    capture_button = tk.Button(root, text="Start capture", command=runCapture)
    capture_button.place(relx=0.031, rely=0.893, height=24, width=187)
    progress_bar = ttk.Progressbar(root, length="300")
    progress_bar.place(relx=0.42, rely=0.893, relwidth=0.547,
                       relheight=0.0, height=22)

    # LOAD LAST SETTINGS
    if Path("last_settings.json").exists():
        with open('last_settings.json', 'r') as json_file:
            last = json.load(json_file)
        if 'upleft_x_entry' in last:
            upleft_x_entry.insert(tk.END, last['upleft_x_entry'])
        if 'upleft_y_entry' in last:
            upleft_y_entry.insert(tk.END, last['upleft_y_entry'])
        if 'botright_x_entry' in last:
            botright_x_entry.insert(tk.END, last['botright_x_entry'])
        if 'botright_y_entry' in last:
            botright_y_entry.insert(tk.END, last['botright_y_entry'])
        if 'screnshot_num' in last:
            var.set(last['screnshot_num'])

    root.mainloop()
