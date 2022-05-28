import os
def clearConsole():
    os.system('cls')
clearConsole()
import colorama
from colorama import init,Fore
init(convert=True)
print(Fore.YELLOW)

import tkinter as tk
from tkinter import messagebox

import winsound
import pyaudio

import socket

import sys

import zlib

import json

import multiprocessing
import threading

import time

import numpy

IP = '26.249.40.72' #Свой айпи
PORT = 65432 #Можно не трогать

sockets=[]
streams=[]
lthreads=[]
sthreads=[]
#bar.finish()

print()
print()


with open('PyCordData\\friends.json', "r", encoding='utf-8') as file:
    friends = json.load(file)

if len(friends)>0:
    print(Fore.CYAN+"Друзья:")
    for i in friends.keys():
        print(Fore.CYAN+i+" - "+friends[i])
else:
    print(Fore.RED+'You have no friends( write "addfriends" to add them')
print()
"""
def New():
    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    con.bind((IP, PORT))
    con.listen()
    con, addr = con.accept()
    print(Fore.GREEN+str(addr),'connected!')

task=input("You want to connect or create a room? connect\\create\\addfriend: ").split(" ")

if task[0]=="addfriend":
    with open("friends.json", "r+") as file:
        data = json.load(file)
        data.update({task[1]:task[2]})
        file.seek(0)
        json.dump(data, file)
        exit()
if task[0]=="connect":
    try:
        FIP=friends[task[1]].split(":")[0]
        FPORT=int(friends[task[1]].split(":")[1])
    except:
        FIP=task[1].split(":")[0]
        FPORT=int(task[1].split(":")[1])
    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    con.connect((FIP, FPORT))
    print(Fore.GREEN+"Joined ",FIP,str(FPORT))

elif task[0]=="create":
    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    con.bind((IP, PORT))
    print(Fore.RED+'Room Created, waiting')
    con.listen()
    con, addr = con.accept()
    print(Fore.GREEN+str(addr),'connected!')
else:
    exit()
"""
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
"""
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)


if task=="connect":
    sound=con.recv(1024)
    print(sound)
    stream.write(sound)

con.settimeout(0.5)
"""
def Listen(stream,con):
    time.sleep(0.1)
    print(Fore.RED+'Listen Channel Activated')
    while 1:
        try:
            sound=con.recv(CHUNK)
            #sound=bytes(zlib.decompress(sound))
            stream.write(sound)
        except socket.timeout:
            pass



def Speak(stream,con):
    print(Fore.CYAN+'Speak Channel Activated')
    while 1:
        try:
            data = stream.read(CHUNK, exception_on_overflow = False)
            #data=zlib.compress(data)
            con.send(data)
        except socket.timeout:
            pass


"""
st = threading.Thread(target=Speak,args=(stream,con))
lt = threading.Thread(target=Listen,args=(stream,con))
st.start()
lt.start()
"""
def on_closing():
    if messagebox.askokcancel("Exit", "U really want to exit PyCord?"):
        win.destroy()
        os._exit(0)

def check_ip(i):
    if os.system("ping -l 1 -n 1 -w 200 " + i)==0:
        return "Online"
    else:
        return "Offline"

def work(ts,i):
    time.sleep(1)
    print(Fore.YELLOW,end='')
    if ts!=None:
        task=ts
    else:
        task=input("call <name>: ").split(" ")
    print()
    if task[0]=="join":
        try:
            FIP=friends[task[1]].split(":")[0]
            FPORT=int(friends[task[1]].split(":")[1])
        except:
            FIP=task[1].split(":")[0]
            FPORT=int(task[1].split(":")[1])
        sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sockets[i].connect((FIP, FPORT))
        print(Fore.GREEN+"Joined ",FIP,str(FPORT))

    elif task[0]=="new":
        sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        sockets[i].bind((IP, PORT))
        print(Fore.RED+'Room Created, waiting')
        sockets[i].listen()
        p.terminate()
        sockets[i], addr = sockets[i].accept()
        print(Fore.GREEN+str(addr),'connected!')
    elif task[0]=="call":
        winsound.PlaySound(str(os.path.dirname(__file__)+"/PyCordData/"+'ring.wav').replace("\\","/"), winsound.SND_LOOP + winsound.SND_ASYNC)
        try:
            FIP=friends[task[1]].split(":")[0]
            FPORT=int(friends[task[1]].split(":")[1])
        except:
            FIP=task[1].split(":")[0]
            FPORT=int(task[1].split(":")[1])
        sockets.append(socket.socket())#socket.AF_INET, socket.SOCK_STREAM
        conex=False
        try:
            sockets[i].connect((FIP, FPORT))
            print(Fore.GREEN+'Call joined')
            winsound.PlaySound(None, winsound.SND_PURGE)
        except ConnectionRefusedError:
            conex=True
        if conex:
            sockets.pop(i)
            sockets.append(socket.socket())
            sockets[i].bind((IP, PORT))
            print(Fore.CYAN+'Call started, waiting for connect')
            print()
            sockets[i].listen()
            sockets[i], addr = sockets[i].accept()
            winsound.PlaySound(None, winsound.SND_PURGE)
            print(Fore.GREEN+str(addr),'joined!')
    else:
        exit()
    sockets[i].settimeout(0.5)
    streams.append(p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK))
    lthreads.append(threading.Thread(target=Speak,args=(streams[i],sockets[i])))
    sthreads.append(threading.Thread(target=Listen,args=(streams[i],sockets[i])))
    lthreads[i].start()
    sthreads[i].start()


win= tk.Tk()
win.title("Droid's PyCord")
win.iconphoto(False, tk.PhotoImage(file=str(os.path.dirname(__file__)+"/PyCordData/"+'pycordlogo.png')))
win.geometry("300x200")

label=[]
for i in friends:
    label.append(i+" - "+friends[i]+" - "+check_ip(friends[i].split(":")[0])+"\n")
label.append("You: "+IP+":"+str(PORT)+"\n")
label.reverse()

lab= tk.Label(win,text=''.join(label))
lab.focus_set()
lab.pack()

text=tk.StringVar(value='Nick or ip:port')
entry= tk.Entry(win, width= 40,textvariable=text)
entry.focus_set()
entry.pack()

win.protocol("WM_DELETE_WINDOW", on_closing)

var = tk.IntVar()
button = tk.Button(win, width= 30, height= 2, text="Call", command=lambda: var.set(1),bg = "gold")
button.pack()                          #расположить кнопку на главном окне


i=-1
while 1:
    i=i+1
    button.wait_variable(var)
    txt=[]
    txt.append("call")
    txt=txt+text.get().split(" ")
    work(txt,i)


"""
while 1:
    print(1)
    if keyboard.is_pressed('u'):
        print('you speaken',end='')
        data = stream.read(CHUNK, exception_on_overflow = False)
        con.send(data) #CHUNK
    else:
        sound=[]
        print('you listen',end='')
        try:
            sound=con.recv(1024)
        except socket.timeout:
            pass
        if len(sound)>0:
            stream.write(sound)


stream.stop_stream()
stream.close()
p.terminate()
"""
