import wx
import browserHandler
import pickle
import threading
import time
import tkinter
from tkinter import filedialog
import getpass
import os

loginClass = []
t = []

class Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = "Hordes.io bot",size = (420,350))
        self.panel = wx.Panel(self)
        self.botNames = []
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)#destroy the panel

        self.radiobox = wx.RadioBox(self.panel, label="Browser", choices = ["Chrome", "Firefox"])
        self.listbox = wx.ListBox(self.panel, choices = self.botNames)
        open_browser = wx.Button(self.panel, label="Open Browser")
        st_bot_list = wx.StaticText(self.panel, label = "Bot List")

        listbox_refresh_btn = wx.Button(self.panel, label="Refresh Characters Data")
        bot_start_btn = wx.Button(self.panel, label="Start")
        bot_stop_btn = wx.Button(self.panel, label="Stop")
        #sizer arrangement
        sizer_browser = wx.BoxSizer(wx.VERTICAL)
        sizer_browser.Add(self.radiobox, flag=wx.LEFT | wx.TOP, border=20)
        sizer_browser.Add(open_browser, flag=wx.LEFT | wx.TOP, border=20)

        sizer_refresh = wx.BoxSizer(wx.HORIZONTAL)
        sizer_refresh.Add(st_bot_list, flag=wx.LEFT, border=25)
        sizer_refresh.Add(listbox_refresh_btn, flag=wx.LEFT, border=20)

        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons.Add(bot_start_btn, flag=wx.LEFT, border=20)
        sizer_buttons.Add(bot_stop_btn, flag=wx.LEFT, border=20)

        sizer_list = wx.BoxSizer(wx.VERTICAL)
        sizer_list.Add(sizer_refresh, flag=wx.TOP, border=20)
        sizer_list.Add(self.listbox,flag=wx.TOP | wx.LEFT, border=20)
        sizer_list.Add(sizer_buttons, flag=wx.TOP, border=20)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sizer_browser)
        sizer.Add(sizer_list)

        self.panel.SetSizer(sizer)

        if "a" and "b" in == "ab":
            print("ok")


        listbox_refresh_btn.Bind(wx.EVT_BUTTON, self.listbox_refresh)
        bot_start_btn.Bind(wx.EVT_BUTTON, self.bot_start)
        bot_stop_btn.Bind(wx.EVT_BUTTON, self.bot_stop)
        
        open_browser.Bind(wx.EVT_BUTTON, self.login_press)
        
        self.Show()

    def login_press(self, event):
        global loginClass
        loginClass.append(browserHandler.BrowserBot(self.radiobox.GetStringSelection()))

        self.listbox.Append(str(len(loginClass)-1))
        global t
        t.append(None)
            

    def bot_start(self, event):
        global t
        index = self.listbox.GetSelection()

        t[index] = threading.Thread(target=Frame.botTh,args=(self,"on"))
        t[index].setDaemon(True)
        t[index].start()
        
    
    def bot_stop(self, event):
        global t
        index = self.listbox.GetSelection()

        t[index].tRun = False
        t[index].join()
    
    def botTh(self,arg):
        global loginClass
        index = self.listbox.GetSelection()

        t[index] = threading.currentThread()
        name = self.listbox.GetStringSelection()

        print("Bot " + name + " start!")

        while getattr(t[index],"tRun",True):
            loginClass[index].bot()
            time.sleep(0.5)
        print("Bot " + name + " stop!")
    
    def listbox_refresh(self,event):
        global loginClass
        self.listbox.Clear()
        a = 0
        newLoginClass = [x for x in loginClass if not x.isBrowserClose()]
        loginClass = newLoginClass
        for i in loginClass:
            currrentName = i.findCharacterName()
            if currrentName != "":
                self.listbox.Append(currrentName)
            else:
                self.listbox.Append(str(a))
            a +=1

        
    
    def onDestroy(self, event):
        global loginClass
        global t

        for currentT in t:
            if hasattr(currentT, 'tRun'):
                currentT.tRun = False
                currentT.join()

        Frame.listbox_refresh(self,event)

        for i in loginClass:
            i.closeBrowser()
        
        print("App destroyed.")
        event.Skip()
        

if __name__ == "__main__":
    app = wx.App()
    frame = Frame()
    app.MainLoop()