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
        open_browser = wx.Button(self.panel, label="Open Browser") 
        self.botlist = wx.ListCtrl(self.panel, style = wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.botlist.InsertColumn(0, 'Bot name', width=80)
        self.botlist.InsertColumn(1, 'Status', width=80)

        botlist_refresh_btn = wx.Button(self.panel, label="Refresh Characters Data")
        bot_start_btn = wx.Button(self.panel, label="Start")
        bot_stop_btn = wx.Button(self.panel, label="Stop")
        #sizer arrangement
        sizer_browser = wx.BoxSizer(wx.VERTICAL)
        sizer_browser.Add(self.radiobox, flag=wx.LEFT | wx.TOP, border=20)
        sizer_browser.Add(open_browser, flag=wx.LEFT | wx.TOP, border=20)

        sizer_refresh = wx.BoxSizer(wx.HORIZONTAL)
        sizer_refresh.Add(botlist_refresh_btn, flag=wx.LEFT, border=20)

        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_buttons.Add(bot_start_btn, flag=wx.LEFT, border=20)
        sizer_buttons.Add(bot_stop_btn, flag=wx.LEFT, border=20)

        sizer_list = wx.BoxSizer(wx.VERTICAL)
        sizer_list.Add(sizer_refresh, flag=wx.TOP, border=20)
        sizer_list.Add(self.botlist,flag=wx.TOP | wx.LEFT, border=20)
        sizer_list.Add(sizer_buttons, flag=wx.TOP, border=20)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sizer_browser)
        sizer.Add(sizer_list)

        self.panel.SetSizer(sizer)

        botlist_refresh_btn.Bind(wx.EVT_BUTTON, self.botlist_refresh)
        bot_start_btn.Bind(wx.EVT_BUTTON, self.bot_start)
        bot_stop_btn.Bind(wx.EVT_BUTTON, self.bot_stop)
        
        open_browser.Bind(wx.EVT_BUTTON, self.login_press)
        
        self.Show()

    def login_press(self, event):
        global loginClass
        loginClass.append(browserHandler.BrowserBot(self.radiobox.GetStringSelection()))

        index = len(loginClass)-1
        self.botlist_insert(index, str(index))
        
        global t
        t.append(None)

    def bot_start(self, event):
        global t
        index = self.botlist.GetFocusedItem()

        t[index] = threading.Thread(target=Frame.botTh,args=(self,"on"))
        t[index].setDaemon(True)
        t[index].start()
        
    
    def bot_stop(self, event):
        global t
        index = self.botlist.GetFocusedItem()

        self.botlist.SetItem(index, 1, "Inactive")
        t[index].tRun = False
        t[index].join()
    
    def botTh(self,arg):
        global loginClass
        index = self.botlist.GetFocusedItem()

        t[index] = threading.currentThread()

        self.botlist.SetItem(index, 1, "Active")
        name = self.botlist.GetItemText(index)

        print("Bot " + name + " start!")

        while getattr(t[index],"tRun",True):
            loginClass[index].bot()
            time.sleep(0.5)
        print("Bot " + name + " successfully stop!")
    
    def botlist_refresh(self,event):
        global loginClass
        self.botlist.DeleteAllItems()
        index = 0
        newLoginClass = [x for x in loginClass if not x.isBrowserClose()]
        loginClass = newLoginClass
        for i in loginClass:
            currrentName = i.findCharacterName()
            if currrentName != "":
                self.botlist_insert(index, currrentName)
            else:
                self.botlist_insert(index, str(index))
            index +=1
    
    def botlist_insert(self, index, name):
        self.botlist.InsertItem(index,str(index))
        self.botlist.SetItem(index, 0, name)
        self.botlist.SetItem(index, 1, "Inactive")
    
    def onDestroy(self, event):
        global loginClass
        global t

        for currentT in t:
            if hasattr(currentT, 'tRun'):
                currentT.tRun = False
                currentT.join()

        Frame.botlist_refresh(self, event)

        for i in loginClass:
            i.closeBrowser()
        
        print("App destroyed.")
        event.Skip()
        

if __name__ == "__main__":
    app = wx.App()
    frame = Frame()
    app.MainLoop()