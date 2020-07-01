from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service
import time
import threading
import getpass
import os

class BrowserBot:
    def __init__(self, browserName):
        if BrowserBot.browserProfileDirSet(self, browserName):
            self.driver.get("https://hordes.io")
        
    def findCharacterName(self):
        try:
            CharacterName = self.driver.find_element_by_xpath("//*[@id='ufplayer']/div[2]/div[1]/div[1]/span[1]").text
            return CharacterName
        except:
            return ""
    
    def browserProfileDirSet(self, browserName):
        username = getpass.getuser()

        if browserName == "Chrome":
            try:
                chOptions = Options()
                chOptions.add_argument("--user-data-dir=C:/Users/"+username+"/AppData/Local/Google/Chrome/User Data")
                self.driver = webdriver.Chrome(options=chOptions, executable_path="chromedriver.exe")
                return True
            except:
                pass
        if browserName == "Firefox":
            for fprofile in os.listdir("/users/"+username+"/AppData/Roaming/Mozilla/Firefox/Profiles/"):
                if "release" in fprofile:
                    fp = webdriver.FirefoxProfile("C:/Users/"+username+"/AppData/Roaming/Mozilla/Firefox/Profiles/"+fprofile)
                    self.driver = webdriver.Firefox(firefox_profile=fp, executable_path="geckodriver.exe")
                    return True
        
        return False
        

    def bot(self):
        characterClassImage = self.driver.find_element_by_xpath("//*[@id='ufplayer']/div[1]/img[1]").get_attribute("src")
        
        if("https://hordes.io/assets/ui/classes/0" in characterClassImage): #0:warrior, 1:mage, 2:rogue, 3:shaman
            self.bot_warrior()
        elif("https://hordes.io/assets/ui/classes/2" in characterClassImage): #webp - chrome : png - opera
            self.bot_rogue()
        elif("https://hordes.io/assets/ui/classes/3" in characterClassImage):
            self.bot_shaman()
    
    def bot_warrior(self):
        try:
            partyBuffs = self.driver.find_elements_by_xpath("//*[@id='ufplayer']//div[@class = 'container  svelte-wo3pyh']//div[1]")
            for currentBuff in partyBuffs:
                if "https://hordes.io/assets/ui/skills/24" in currentBuff.find_element_by_xpath("./following::img").get_attribute("src").split("?")[0] and currentBuff.text == "5'": #Enchantment
                    self.driver.find_element_by_xpath('/html/body').send_keys("1")
                    time.sleep(1.9)
                    self.driver.find_element_by_xpath('/html/body').send_keys("2")
                    time.sleep(1.9)
        except:
            pass

    def bot_rogue(self):
        try:
            partyBuffs = self.driver.find_elements_by_xpath("//*[@id='ufplayer']//div[@class = 'container  svelte-wo3pyh']//div[1]")
            
            for currentBuff in partyBuffs:
                if "https://hordes.io/assets/ui/skills/24" in currentBuff.find_element_by_xpath("./following::img").get_attribute("src").split("?")[0] and currentBuff.text == "5'": #Enchantment
                    self.driver.find_element_by_xpath('/html/body').send_keys("1")
                    time.sleep(1.9)
                    self.driver.find_element_by_xpath('/html/body').send_keys("2")
                    time.sleep(1.9)
        except:
            pass

    def bot_shaman(self):
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
                if partyHPs < 75:
                    element.click()
                    time.sleep(0.2)
                    self.driver.find_element_by_xpath('/html/body').send_keys("3")
                    time.sleep(1.9)
        except:
            pass

        #//*[@id="ufplayer"]/div[2]/div[2]/div[1] karakterin manasi every 30 sec

        partyframes = self.driver.find_elements_by_xpath("//div[starts-with(@class,'buffarray party')]")
        try:
            for element in partyframes:
                image = element.find_elements_by_xpath(".//div[starts-with(@class,'container')]")
                for i in image:
                    if  "https://hordes.io/assets/ui/skills/16" in i.find_element_by_xpath(".//div[1]/img[1]").get_attribute("src").split("?")[0]:
                        time.sleep(0.1)
                        self.driver.find_element_by_xpath('/html/body').send_keys("1")
                        time.sleep(1.9)
                        self.driver.find_element_by_xpath('/html/body').send_keys("2")
                        time.sleep(1.9)
        except:
            pass

    def acceptRequest(self):
        try:
            self.driver.find_element_by_xpath("//div[starts-with(@class,'choice') and contains(@class,'svelte-cy0tay')]").click()
        except:
            pass
    
    def closeBrowser(self):
        self.driver.close()
    
    def isBrowserClose(self):
        try:
            self.driver.title
            return False
        except:
            return True
