import wx
import browserHandler
import pickle
import threading
import time

loginClass = None
threadCheck = False
t = None

class Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = "Hordes.io bot")
        panel = wx.Panel(self)
        
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)#destroy the panel
        wx.StaticText(panel, label = "username", pos=(20,5)) # TODO:need to use sizer
        self.text_username = wx.TextCtrl(panel, pos =(20,35))
        wx.StaticText(panel, label = "pass", pos =(20,65))
        self.text_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD, pos =(20,95))
        login_btn = wx.Button(panel, label="Login with google", pos = (20,145))
        wx.StaticText(panel, label = "heal bot", pos=(200,5))
        bot_start_btn = wx.Button(panel, label="bot start", pos = (200,35))
        bot_stop_btn = wx.Button(panel, label="bot stop", pos = (200,95))
        #save_cookies = wx.Button(panel, label = "Save skill bar and settings", pos = (200,155))
        #save_cookies = wx.Button(panel, label = "Load skill bar and settings", pos = (200,155))

        save_cookies.Bind(wx.EVT_BUTTON, self.save_cookies)
        login_btn.Bind(wx.EVT_BUTTON, self.login_press)
        bot_start_btn.Bind(wx.EVT_BUTTON, self.bot_start)
        bot_stop_btn.Bind(wx.EVT_BUTTON, self.bot_stop)
        self.Show()

    def login_press(self, event):
        username = self.text_username.GetValue()
        print(username)
        password = self.text_password.GetValue()
        print(password)

        global loginClass
        loginClass = browserHandler.Login()
        #loginClass.login(username,password)
        #loginClass.selectCharacterAndJoin()

    def bot_start(self, event):
        global loginClass
        #loginClass.botStart()
        global t
        t = threading.Thread(target=Frame.botTh,args=(self,"on"))
        t.setDaemon(True)
        t.start()
        #t.tRun = False
        #t.join()
        
    
    def bot_stop(self, event):
    
        #loginClass.botStop()
        global t
        #t = threading.currentThread()
        t.tRun = False
        t.join()

    def save_cookies(self, event):
        pass
        #global loginClass
        #print(type(loginClass))
        #pickle.dump(loginClass.driver.get_cookies(), open("cookies.pkl", "wb"))
        #loginClass.saveCookies()
        #print(loginClass.driver.get_cookies())
    
    def botTh(self,arg):
        t = threading.currentThread()
        global loginClass

        while getattr(t,"tRun",True):
            loginClass.bot()
            time.sleep(0.5)
        print("stopped")
        
    
    def onDestroy(self, event):
        global loginClass
        global t
        t.tRun = False
        t.join()
        loginClass.closeBrowser()
        print("app destroyed.")
        event.Skip()
        

if __name__ == "__main__":
    app = wx.App()
    frame = Frame()
    app.MainLoop()