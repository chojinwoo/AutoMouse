#!/usr/bin/env python3
import tkinter as tk
import tkinter.filedialog as td
import pyautogui as pi
import threading as thread
import time
import os
from tkinter import *
from tkinter import messagebox
from datetime import datetime

posText = ''

class MyFrame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)        
        bossChk = IntVar()
        bossMin = None
        bossSec = None

        def save():
            f = td.asksaveasfile(mode='w', defaultextension=".txt")
            if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            text2save = str(lblText.get(1.0, END)) # starts from `1.0`, not `0.0`
            f.write(text2save)
            f.close() # `()` was missing.

        def load():
            fname = td.askopenfile(mode='r', defaultextension=".txt")
            f = open(fname.name)
            for line in f:
                lblText.insert(INSERT, str(line))

        def delete():
            lblText.delete('1.0', END)

        def start():
            while self._th2_running:
                comm = str(lblText.get(1.0, END))
                lines = comm.split('\n')
                if bossChk.get() == 1:
                    for l in lines:
                        strs = l.split(':')
                        if strs[0] == 'CLICK':
                            pi.click(int(strs[1]), int(strs[2]))
                        elif strs[0] == 'SLEEP':
                            boss()
                            for idx in range(int(strs[1])):
                                print(idx)
                                time.sleep(1)
                else:
                    for l in lines:
                        strs = l.split(':')
                        if strs[0] == 'CLICK':
                            pi.click(int(strs[1]), int(strs[2]))
                        elif strs[0] == 'SLEEP':
                            time.sleep(int(strs[1]))
                    
        
        def startThread():
            self._th2_running = True
            th2 = thread.Thread(target=start)   
            th2.daemon = True
            th2.start()      

        def stopThread():
            self._th2_running = False

        def posThread():
            while self._th1_running:
                x, y = pi.position()
                posText['text'] = str(x) + ':' + str(y)
                f1Timer['text'] = datetime.today().strftime("%H:%M:%S")
                time.sleep(1)
        
        def posStart():
            self._th1_running = True        
            th = thread.Thread(target=posThread)
            th.start()

        def posStop():
            self._th1_running = False

        def boss():
            #datetime.today().strftime("%Y%m%d%H%M%S")    # YYYYmmddHHMMSS 형태의 시간 출력
            minute = datetime.today().strftime("%M")
            second = datetime.today().strftime("%S")
            print(minute + ':'+second)
            bossMin = f7Entry.get()
            bossSec = f7Entry2.get()
            try:
                if minute[1] == bossMin:
                    if int(second) >= (bossSec - 10):
                        self._th2_running = False
                        print('next')
                        time.sleep(2)
                        startThread()
            except:
                print('minute not find~')
                raise
            if (bossSec + 30) >= 60:
                bossMin = bossMin + 1
                bossSec = (bossSec + 30) - 60
            f7Entry.insert(0, bossMin)
            f7Entry2.insert(0, bossSec)

        def list():
            x,y = pi.position()
            lblText.insert(INSERT, "CLICK:"+str(x)+":"+str(y) + ":L\n")
            lblText.insert(INSERT,"SLEEP:1\n")

        def quit(event):
            on_closing()

        def menuQuit():
            stopThread()
            posStop()
            master.destroy()

        menubar  = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="save", command=save)
        filemenu.add_command(label="load", command=load)
        filemenu.add_separator()
        filemenu.add_command(label="exit", command=menuQuit)
        menubar.add_cascade(label="File", menu=filemenu)


        self.master = master
        self.master.title("AutoMouse")
        self.pack(fill=BOTH, expand=True)


        self.master.config(menu=menubar)

        # position
        frame1 = Frame(self)
        frame1.pack(fill=X)

        lblPos = Label(frame1, text="좌표", width=5)
        lblPos.pack(side=LEFT, padx=10, pady=10)

        x, y = pi.position()
        posText = Label(frame1)
        posText.pack(side=LEFT, padx=5, pady=10)

        f1Time = Label(frame1, text='시간 : ', width=5)
        f1Time.pack(side=LEFT, padx=10, pady=10)

        f1Timer = Label(frame1)
        f1Timer.pack(side=LEFT, padx=5, pady=10)

        posStart()
        

        # action add
        frame2 = Frame(self)
        frame2.pack(fill=X)

        lblAct = Label(frame2, text='행동', width=5)
        lblAct.pack(side=LEFT, padx=10, pady=10)

        #action setting
        frame3 = Frame(self)
        frame3.pack(fill=X)

        lblX = Label(frame3, text="X : ", width=5)
        lblX.pack(side=LEFT, padx=10, pady=10)

        lblXinput = Entry(frame3, width=3)
        lblXinput.pack(side=LEFT, padx=1, pady=10)

        lblY = Label(frame3, text="Y : ", width=5)
        lblY.pack(side=LEFT, padx=10, pady=10)

        lblYinput = Entry(frame3, width=3)
        lblYinput.pack(side=LEFT, padx=1, pady=10)

        lblD = Label(frame3, text="Delay : ", width=5)
        lblD.pack(side=LEFT, padx=10, pady=10)

        lblDinput = Entry(frame3, width=5)
        lblDinput.pack(side=LEFT, padx=1, pady=10) 

        lblBtn = Button(frame3, text='추가', width=5, command=list)
        lblBtn.pack(side=RIGHT, padx=15, pady=10)


        #boss timer
        frame7 = Frame(self)
        frame7.pack(fill=X)

        f7label2 = Label(frame7, text='사용여부 : ', width=10)
        f7label2.pack(side=LEFT, padx=10, pady=5)

        f7Check = Checkbutton(frame7, variable=bossChk)
        f7Check.pack(side=LEFT, padx=1, pady=5)        

        f7label = Label(frame7, text="보스타이머 : ", width=10)
        f7label.pack(side=LEFT, padx=15, pady=5)

        f7Entry = Entry(frame7, width=3)
        f7Entry.pack(side=LEFT, padx=5, pady=5)
        f7Min = Label(frame7, text='분', width=2)
        f7Min.pack(side=LEFT, padx=0, pady=5)
        
        f7Entry2 = Entry(frame7, width=3)
        f7Entry2.pack(side=LEFT, padx=5, pady=5)
        f7Sec = Label(frame7, text='초', width=2)
        f7Sec.pack(side=LEFT, padx=0, pady=5)

        # list title
        frame4 = Frame(self)
        frame4.pack(fill=X)

        lblTitle1 = Label(frame4, text="목록", width=5)
        lblTitle1.pack(side=LEFT, padx=10, pady=10)

        # list
        frame5 = Frame(self)
        frame5.pack(fill=X)

        lblText = Text(frame5, height=15)
        lblText.pack(side=LEFT, padx=10, pady=10)


        # start or end
        frame6 = Frame(self)
        frame6.pack(fill=X)

        sRemove = Button(frame6, text='삭제', width=10, command=delete)
        sRemove.pack(side=RIGHT, padx=10, pady=10)
    
        sStop = Button(frame6, text='정지', width=10, command=stopThread)
        sStop.pack(side=RIGHT, padx=10, pady=10)

        sBtn = Button(frame6, text='시작', width=10, command=startThread)
        sBtn.pack(side=RIGHT, padx=10, pady=10)

        def saveShortcut(event):
            save()

        def loadShortcut(event):
            load()
        
        def startShortcut(event):
            startThread()

        def listShortcut(event):
            list()

        def startShortcut(event):
            startThread()

        def stopShortcut(event):
            stopThread()

        def on_closing():
            if messagebox.askokcancel("Quit", "종료 하시겠습니까?"):
                self._th1_running = False
                self._th2_running = False
                menuQuit()

        master.protocol("WM_DELETE_WINDOW", on_closing)

        master.bind('<Alt-c>', listShortcut)
        master.bind('<Control-l>', loadShortcut)
        master.bind_all('<Control-s>', saveShortcut)
        master.bind('<Control-q>', quit)
        master.bind('<Alt-s>', startShortcut)
        master.bind('<Alt-p>', stopShortcut)

def main():

    root = Tk()
    root.geometry('500x545+10+10')
    myframe = MyFrame(root)
    root.mainloop()



if __name__ == '__main__':
    thMain = thread.Thread(target=main)

    thMain.start()
