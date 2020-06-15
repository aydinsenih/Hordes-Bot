from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import chromedriver_binary
import pickle
import threading

t1 = None
tCheck = False

class Login:
    def __init__(self):
        chOptions = Options()
        chOptions.add_argument("--user-data-dir=C:\\Users\\aydin\\AppData\\Local\\Google\\Chrome\\User Data")
        chOptions.add_argument("--profile-directory=Profile 2")
        #chOptions.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=chOptions)
        
        #self.driver.execute_script('window.localStorage.setItem("skillbarsettings","mrb")')
        
        try:
            skillbar = pickle.load(open("skillbar.pkl", "rb"))
            print(skillbar)
            self.driver.execute_script('window.localStorage.setItem("skillbarsettings","{0}")'.format(skillbar))
        except:
            print("Cookies not found") #expected result. dont need cookies anymore
        self.driver.get("https://hordes.io")
        time.sleep(3)

    def login(self, username, password):
        
        self.driver.find_element_by_xpath('//*[@id="hero"]/div[3]/div[2]/div').click()
        self.driver.find_element_by_xpath('//*[@id="hero"]/div[3]/div/div/a').click()
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="identifierNext"]/span/span').click()
        time.sleep(4)
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="passwordNext"]/span').click()
        time.sleep(3)
    
    def selectCharacterAndJoin(self):
        self.driver.find_element_by_xpath('//*[@id="hero"]/div[3]/div/div/div/div[2]/div[1]/p[1]').click() #select first character slot
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="hero"]/div[3]/div/div/div/div[3]').click()
        time.sleep(5)

    def bot(self):
        #while not tCheck:
        partyframes = self.driver.find_elements_by_xpath("//div[starts-with(@class,'progressBar') and contains(@class, 'bghealth')]")
        charMana = self.driver.find_element_by_xpath("//*[@id='ufplayer']/div[2]/div[2]/div[1]/span[2]").text.split("/")
        if len(charMana) > 1 and ((int(charMana[1]) - int(charMana[0])) > 190): # for medium mana potion
            self.driver.find_element_by_xpath('/html/body').send_keys("0")
        # starttime = time.time()
        # time.sleep(2)
        # print(time.time()-starttime)
        # print(charMana)
        try:
            for element in partyframes:
                #print("width" + element.value_of_css_property('width')) 168.5px party hp box size while full hp
                hpbarpx = float(element.value_of_css_property('width').replace("px","")) # or string_to_number can be used
                if(hpbarpx > 170):
                    continue
                partyHPs = hpbarpx/168.5*100 # will become percentage
                if partyHPs < 85:
                    element.click()
                    time.sleep(0.2)
                    for x in range(0, 3):
                        self.driver.find_element_by_xpath('/html/body').send_keys("2")
                        time.sleep(1.9)
        except:
            pass
    
    #//*[@id="ufplayer"]/div[2]/div[2]/div[1] karakterin manasi every 30 sec
    
    def botStart(self):
        global t1
        #t1 = threading.Thread(target=Login.bot(self))
        #t1.start()
    
    def botStop(self):
        global t1
        global tCheck
        tCheck = True
    
    def closeBrowser(self):
        self.driver.close()


    def saveCookies(self):
        pickle.dump(self.driver.execute_script('return window.localStorage.getItem("skillbarsettings")'), open("skillbar.pkl", "wb"))
