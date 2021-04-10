# imports needed for GUI
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import messagebox

# imports needed for image acquisition and pdf creation
from PIL import ImageGrab
from time import sleep
import keyboard

# other
import json
from pathlib import Path
import os
from threading import Thread
from pynput.mouse import Listener

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
    screenshot_num = screenshots_n_var.get()
    if screenshot_num < 1:
        messagebox.showerror(
            'Invalid value', 'Screenshots number can\'t be < 1')
        return
    delay = float(delay_var.get())
    if delay < 0.1 or delay > 10:
        messagebox.showerror(
            'Invalid value', 'Delay can\'t be < 0.1 or > 10')
        return
    key = keyCombo.get()
    keyIndex = keyCombo.current()
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
        keyboard.press_and_release(key)
        sleep(delay)
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
    last['delay'] = delay
    last['key'] = keyIndex
    with open(get_abs_path
              ('last_settings.json'), 'w') as json_file:
        json.dump(last, json_file)


def insertIntoLog(str):
    logscroll.config(state=tk.NORMAL)
    logscroll.insert(tk.INSERT, str)
    logscroll.config(state=tk.DISABLED)

clicked_x = 0
clicked_y = 0
def on_click(x, y, button, pressed):
    global clicked_x
    global clicked_y
    clicked_x, clicked_y = x, y
    return False

def click_upleft_coord():
    with Listener(on_click=on_click) as listener:
        root.iconify()
        listener.join()
        upleft_x_entry.delete(0,tk.END)
        upleft_y_entry.delete(0,tk.END)
        upleft_x_entry.insert(tk.END, clicked_x)
        upleft_y_entry.insert(tk.END, clicked_y)
        root.deiconify()

def click_botright_coord():
    with Listener(on_click=on_click) as listener:
        root.iconify()
        listener.join()
        botright_x_entry.delete(0,tk.END)
        botright_y_entry.delete(0,tk.END)
        botright_x_entry.insert(tk.END, clicked_x)
        botright_y_entry.insert(tk.END, clicked_y)
        root.deiconify()

if __name__ == "__main__":
    base_path = os.getcwd()
    
    root = tk.Tk()
    root.geometry('550x300')
    root.resizable(0, 0)
    root.title("Captures to PDF - v0.4")

    ### TOP FRAME ###
    frame1 = tk.LabelFrame(root, text="Capture area")
    frame1.place(relx=0.018, rely=0.0, relheight=0.33, relwidth=0.967)

    tk.Label(frame1, text="Top-left coordinates").place(relx=0.053,
                                                        rely=0.313, height=22, width=113, bordermode='ignore')
    tk.Label(frame1, text="x").place(relx=0.275, rely=0.104,
                                     height=21, width=32, bordermode='ignore')
    tk.Label(frame1, text="y").place(relx=0.360, rely=0.104,
                                     height=21, width=31, bordermode='ignore')
    upleft_x_entry = tk.Entry(frame1)
    upleft_x_entry.place(relx=0.275, rely=0.313, height=20,
                         relwidth=0.064, bordermode='ignore')
    upleft_y_entry = tk.Entry(frame1)
    upleft_y_entry.place(relx=0.360, rely=0.313, height=20,
                         relwidth=0.064, bordermode='ignore')
    tk.Button(frame1, text="Click", command=click_upleft_coord).place(relx=0.450, rely=0.313, height=20,
                         relwidth=0.064, bordermode='ignore')

    tk.Label(frame1, text="Bottom-right coordinates").place(relx=0.450,
                                                            rely=0.635, height=21, width=141, bordermode='ignore')
    tk.Label(frame1, text="x").place(relx=0.715, rely=0.417,
                                      height=22, width=32, bordermode='ignore')
    tk.Label(frame1, text="y").place(relx=0.800, rely=0.417,
                                      height=22, width=32, bordermode='ignore')
    botright_x_entry = tk.Entry(frame1)
    botright_x_entry.place(relx=0.715, rely=0.635, height=20,
                           relwidth=0.064, bordermode='ignore')
    botright_y_entry = tk.Entry(frame1)
    botright_y_entry.place(relx=0.800, rely=0.635, height=20,
                           relwidth=0.064, bordermode='ignore')
    tk.Button(frame1, text="Click", command=click_botright_coord).place(relx=0.890, rely=0.635, height=20,
                         relwidth=0.064, bordermode='ignore')

    ### LEFT FRAME ###
    frame2 = tk.LabelFrame(root, text="Capture settings")
    frame2.place(relx=0.018, rely=0.344, relheight=0.54, relwidth=0.37)

    tk.Label(frame2, text="Number of captures").place(
        relx=0.05, rely=0.15, height=21, width=124, bordermode='ignore')
    screenshots_n_var = tk.IntVar()
    tk.Spinbox(frame2, from_=1, to=1000, textvariable=screenshots_n_var).place(
        relx=0.75, rely=0.15, relheight=0.127, relwidth=0.227, bordermode='ignore')

    tk.Label(frame2, text="Delay between captures").place(
        relx=0.05, rely=0.30, height=21, width=124, bordermode='ignore')
    delay_var = tk.StringVar()
    tk.Spinbox(frame2, from_=0.1, to=10, textvariable=delay_var, increment=0.1).place(
        relx=0.75, rely=0.30, relheight=0.127, relwidth=0.227, bordermode='ignore')

    tk.Label(frame2, text="Simulated keypress").place(
        relx=0.05, rely=0.45, height=21, width=100, bordermode='ignore')
    keyCombo = ttk.Combobox(frame2,
                 values=[
                     "up",
                     "down",
                     "left",
                     "right",
                     "page up",
                     "page down",
                     "space",
                     "enter"],
                 state="readonly")
    keyCombo.place(relx=0.57, rely=0.45, height=21,
                                         relwidth=0.4, bordermode='ignore')
    keyCombo.current(0)

    tk.Label(frame2, text="Output file name (without '.pdf')").place(
        relx=0.049, rely=0.60, height=21, width=190, bordermode='ignore')
    outname_entry = tk.Entry(frame2)
    outname_entry.place(relx=0.049, rely=0.75, height=20,
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
            screenshots_n_var.set(last['screnshot_num'])
        if 'delay' in last:
            delay_var.set(last['delay'])
        if 'key' in last:
            keyCombo.current(last['key'])

    # OTHER
    insertIntoLog("Doesn't work yet")
    root.mainloop()
