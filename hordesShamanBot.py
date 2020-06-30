import wx
import browserHandler
import pickle
import threading
import time

loginClass = []
t = []

class Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = "Hordes.io bot")
        self.panel = wx.Panel(self)
        self.botNames = []
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)#destroy the panel
        self.radiobox = wx.RadioBox(self.panel, label="Browser", pos =(20,5), choices = ["Chrome", "Firefox"])
        self.listbox = wx.ListBox(self.panel, pos =(200,25), choices = self.botNames)
        login_btn = wx.Button(self.panel, label="Open Browser", pos = (20,55))
        wx.StaticText(self.panel, label = "Bot List", pos=(200,5))

        listbox_refresh_btn = wx.Button(self.panel, label="0", pos = (260,5), size=(20, 20))
        bot_start_btn = wx.Button(self.panel, label="bot start", pos = (200,85))
        bot_stop_btn = wx.Button(self.panel, label="bot stop", pos = (280,85))
    
        listbox_refresh_btn.Bind(wx.EVT_BUTTON, self.listbox_refresh)
        bot_start_btn.Bind(wx.EVT_BUTTON, self.bot_start)
        bot_stop_btn.Bind(wx.EVT_BUTTON, self.bot_stop)
        
        login_btn.Bind(wx.EVT_BUTTON, self.login_press)
        
        self.Show()

    def login_press(self, event):
        global loginClass
        loginClass.append(browserHandler.Login(self.radiobox.GetStringSelection()))

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

        for i in loginClass:
            i.closeBrowser()
        
        print("App destroyed.")
        event.Skip()
        

if __name__ == "__main__":
    app = wx.App()
    frame = Frame()
    app.MainLoop()