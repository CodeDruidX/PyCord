import os
def clearConsole():
    os.system('cls')
#clearConsole()
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import winsound
import pyaudio
import socket
import sys
import keyboard
import threading

IP = socket.gethostbyname(socket.gethostname())    #Свой айпи

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()


def Listener(stream,con):

    while 1:
        try:
            sound=con.recv(CHUNK)

            stream.write(sound)
        except socket.timeout:
            pass


def Speaker(stream,con):
    while 1:
        try:
            data = stream.read(CHUNK, exception_on_overflow = False)
            print(len(data))
            con.send(data)
        except socket.timeout:
            pass

def validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True

def call(friend):
    if validIP(friend):
        pass
    else:
        messagebox.showerror("Invalid IP", "Address <"+friend+"> is not IP")
        return 1
    winsound.PlaySound(str(os.path.dirname(__file__)+"/PyCordData/"+'ring.wav').replace("\\","/"), winsound.SND_LOOP + winsound.SND_ASYNC)
    FIP=friend
    sock=socket.socket()
    conex=False
    try:
        sock.connect((FIP, 65432))
        winsound.PlaySound(None, winsound.SND_PURGE)
    except ConnectionRefusedError:
        conex=True
    if conex:
        sock=socket.socket()
        sock.bind((IP, 65432))
        sock.listen()
        sock, addr = sock.accept()
        winsound.PlaySound(None, winsound.SND_PURGE)

    s=threading.Thread(target=Speaker,args=(stream,sock))
    l=threading.Thread(target=Listener,args=(stream,sock))
    l.start()
    s.start()

def on_closing():
    if messagebox.askokcancel("Exit", "U really want to exit PyCord?"):
        win.destroy()
        os._exit(0)

win= tk.Tk()
win.title("Droid's PyCord")
win.iconphoto(False, tk.PhotoImage(file=str(os.path.dirname(__file__)+"/PyCordData/"+'pycordlogo.png')))
win.geometry("300x200")
win.protocol("WM_DELETE_WINDOW", on_closing)

style = ttk.Style(win)

lab= ttk.Label(win,text="Your IP: "+IP,font="calibri 12")
lab.focus_set()
lab.pack()

text=tk.StringVar(value='Friend`s IP')
entry= ttk.Entry(win, width= 40,textvariable=text)
entry.focus_set()
entry.pack()

lab= tk.Label(win,text="")
lab.focus_set()
lab.pack()

var = tk.IntVar()
button = ttk.Button(win,  text="Call", command=lambda: threading.Thread(target=lambda: call(text.get())).start())
img = tk.PhotoImage(file=str(os.path.dirname(__file__)+"/PyCordData/"+'call.png'))
button.config(image=img)
button.pack() 


stream=p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK)

win.mainloop()
sock=call(input())
