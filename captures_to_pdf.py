#imports needed for GUI
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import messagebox

#imports needed for image acquisition and pdf creation
from PIL import ImageGrab, Image
from time import sleep
import keyboard

#other
import json
import shutil
from zipfile import ZipFile
from pathlib import Path
import os, sys

base_path = os.getcwd()

window = tk.Tk()
window.title("Screens to PDF")
window.geometry('550x250')

tk.Label(window, text="Upper-left coordinates").grid(row=0, column=0)
tk.Label(window, text="x:").grid(row=0, column=1)
upleft_x_entry = tk.Entry(window, width=5)
upleft_x_entry.grid(row=0,column=2)
tk.Label(window, text="y:").grid(row=0, column=3)
upleft_y_entry = tk.Entry(window, width=5)
upleft_y_entry.grid(row=0,column=4)

tk.Label(window, text="Bottom-right coordinates").grid(row=2, column=0)
tk.Label(window, text="x:").grid(row=2, column=1)
botright_x_entry = tk.Entry(window, width=5)
botright_x_entry.grid(row=2,column=2)
tk.Label(window, text="y:").grid(row=2, column=3)
botright_y_entry = tk.Entry(window, width=5)
botright_y_entry.grid(row=2,column=4)

tk.Label(window, text="Number of screenshots:").grid(row=4, column=0)
var=tk.IntVar()
tk.Spinbox(window, from_=1, to=500, width=5, textvariable=var).grid(row=4, column=1)

tk.Label(window, text="Output PDF (without .pdf):").grid(row=6, column=0)
outname_entry = tk.Entry(window, width=25)
outname_entry.grid(row=6,column=5)

def resource_path(relative_path):
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
        messagebox.showerror('Invalid value', 'Screenshots number can\'t be < 1')
        return
    filename = outname_entry.get()
    filename = filename.replace('.pdf','')
    if filename == '':
        messagebox.showerror('Error', 'You forgot to specify the name of the output PDF')
        return
    compress_to_zip = chk_state.get()
    imagelist = []
    for i in range(3,0,-1):
        print('Minimize me, starting in',i,'seconds')
        sleep(1)
    for i in range(screenshot_num):
        print('Taking image number ', i+1)
        im = ImageGrab.grab(bbox=(upl_x,upl_y,botr_x,botr_y))
        imagelist.append(im)
        keyboard.press_and_release('page down')
        sleep(1)
    print('Saving PDF to', resource_path(filename.rstrip()+'.pdf'))
    imagelist[0].save(resource_path(filename.rstrip()+'.pdf'), "PDF", resolution=100.0, optimize=True, save_all=True, append_images=imagelist[1:])
    if compress_to_zip: 
        with ZipFile(resource_path(filename.rstrip()+'.zip'), "w") as newzip:
            newzip.write((filename.rstrip()+'.pdf'))
        os.remove(filename.rstrip()+'.pdf')
    print('Done')
    last={}
    last['upleft_x_entry'] = upl_x
    last['upleft_y_entry'] = upl_y
    last['botright_x_entry'] = botr_x
    last['botright_y_entry'] = botr_y
    last['screnshot_num'] = screenshot_num
    last['compress_to_zip'] = compress_to_zip
    with open(resource_path('last_settings.json'),'w') as json_file:
        json.dump(last, json_file)

chk_state = tk.BooleanVar()
tk.Checkbutton(window, text='Compress to zip', var=chk_state).grid(row=8, column=0)

tk.Button(window, text="Start capture", command=runCapture).grid(row=10, column=0)

logscroll = scrolledtext.ScrolledText(window,width=25,height=5,state=tk.DISABLED)
def insertIntoLog(str):
    logscroll.config(state=tk.NORMAL)
    logscroll.insert(tk.INSERT,str)
    logscroll.config(state=tk.DISABLED)
logscroll.grid(row=12,column=0)
insertIntoLog('work in progress\n')
insertIntoLog('NB: right now compress to zip doesn\'t really reduce file size')

if Path("last_settings.json").exists():
    with open('last_settings.json','r') as json_file:
        last = json.load(json_file)
    if 'upleft_x_entry' in last: upleft_x_entry.insert(tk.END, last['upleft_x_entry'])
    if 'upleft_y_entry' in last: upleft_y_entry.insert(tk.END, last['upleft_y_entry'])
    if 'botright_x_entry' in last: botright_x_entry.insert(tk.END, last['botright_x_entry'])
    if 'botright_y_entry' in last: botright_y_entry.insert(tk.END, last['botright_y_entry'])
    if 'screnshot_num' in last: var.set(last['screnshot_num'])
    if 'compress_to_zip' in last: chk_state.set(last['compress_to_zip'])
    
window.mainloop()