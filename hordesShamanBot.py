import wx
import browserHandler
import threading
import time


class Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, title = "Hordes.io bot",size = (420,350))
        self.browserClass = []
        self.t = []
        # self.choices = ["1","2","3","4","5","6","7","8","9","0"]

        #service.py in selenium line 72 has to replace with below code
        #self.process = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False, creationflags=0x08000000, close_fds=platform.system() != 'Windows')
        self.panel = wx.Panel(self)
        self.botNames = []
        self.Bind(wx.EVT_WINDOW_DESTROY, self.onDestroy)#destroy the panel

        self.radiobox = wx.RadioBox(self.panel, label="Browser", choices = ["Chrome", "Firefox"])
        open_browser = wx.Button(self.panel, label="Open Browser")
        self.botlist = wx.ListCtrl(self.panel, style = wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.botlist.InsertColumn(0, 'Bot name', width=80)
        self.botlist.InsertColumn(1, 'Status', width=80)
        st_info = wx.StaticText(self.panel, label="Revitalize slot 3\nBuffs slot 1 and 2")
        # combo_rev = wx.Choice(self.panel, choices = self.choices)
        # combo_buff1 = wx.Choice(self.panel, choices = self.choices)
        # combo_buff2 = wx.Choice(self.panel, choices = self.choices)
        
        # self.botlist.InsertItem(0,"test")
        # self.botlist.SetItemBackgroundColour(0,wx.RED)

        botlist_refresh_btn = wx.Button(self.panel, label="Refresh List/\nStop All Bots")
        accept_request_btn = wx.Button(self.panel, label="Accept\nRequest")
        bot_start_btn = wx.Button(self.panel, label="Start")
        bot_stop_btn = wx.Button(self.panel, label="Stop")
        #sizer arrangement
        sizer_browser = wx.BoxSizer(wx.VERTICAL)
        sizer_browser.Add(self.radiobox, flag=wx.LEFT | wx.TOP, border=20)
        sizer_browser.Add(open_browser, flag=wx.LEFT | wx.TOP, border=20)
        sizer_browser.Add(st_info, flag=wx.LEFT | wx.TOP, border=20)

        sizer_refresh = wx.BoxSizer(wx.HORIZONTAL)
        sizer_refresh.Add(botlist_refresh_btn, flag=wx.LEFT, border=20)
        sizer_refresh.Add(accept_request_btn, flag=wx.LEFT, border=20)

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
        accept_request_btn.Bind(wx.EVT_BUTTON, self.accept_request)
        
        open_browser.Bind(wx.EVT_BUTTON, self.login_press)
        
        self.Show()

    def login_press(self, event):
        self.browserClass.append(browserHandler.BrowserBot(self.radiobox.GetStringSelection()))

        index = len(self.browserClass)-1
        self.botlist_insert(index, str(index))
        
        self.t.append(None)

    def bot_start(self, event):
        index = self.botlist.GetFocusedItem()
        if index != -1:
            self.t[index] = threading.Thread(target=Frame.botTh,args=(self,"on"))
            self.t[index].setDaemon(True)
            self.t[index].start()
        
    
    def bot_stop(self, event):
        index = self.botlist.GetFocusedItem()
        if index != -1:
            self.botlist.SetItem(index, 1, "Inactive")
            self.t[index].tRun = False
            self.t[index].join()
    
    def botTh(self, arg):
        index = self.botlist.GetFocusedItem()

        self.t[index] = threading.currentThread()###

        self.botlist.SetItem(index, 1, "Active")
        name = self.botlist.GetItemText(index)

        print("Bot " + name + " start!")

        while getattr(self.t[index],"tRun",True):###
            self.browserClass[index].bot()
            time.sleep(0.5)
        print("Bot " + name + " successfully stop!")
    
    def botlist_refresh(self, event):
        self.botlist.DeleteAllItems()
        index = 0
        newBrowserClass = [x for x in self.browserClass if not x.isBrowserClose()]
        self.browserClass = newBrowserClass
        for i in self.browserClass:
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
    
    def accept_request(self, event):#accept when clickable!
        for i in self.browserClass:
            i.acceptRequest()
    
    def onDestroy(self, event):

        for currentT in self.t:
            if hasattr(currentT, 'tRun'):
                currentT.tRun = False
                currentT.join()

        Frame.botlist_refresh(self, event)

        for i in self.browserClass:
            i.closeBrowser()
        
        print("App destroyed.")
        event.Skip()
        

if __name__ == "__main__":
    app = wx.App()
    frame = Frame()
    app.MainLoop()