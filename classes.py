from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options


class ProfileScanner() : 
    def __init__(self, username, tag, link , Names):
        self.mainDic = dict.fromkeys(Names, None)
        self.mainDic['User Name' ]= username
        self.mainDic['Tag'] = tag
        self.mainDic['Source'] = link
        self.proccesDriver = webdriver.Chrome(executable_path="C:\Coding\ValorantTrackerProject\chromedriver.exe")
        self.openPage(link)
        # click the episode 5 act 3 button by Xpath (only doing this cause this new act too recent)
        self.proccesDriver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[1]/div/div[2]/div/ul/li[3]').click()
        sleep(1)
        # main profile gets the main headers
        self.parent = self.proccesDriver.find_element_by_class_name('trn-content')
        self.sidebar = self.proccesDriver.find_element_by_class_name('area-sidebar')
        self.mainbar = self.proccesDriver.find_element_by_class_name('area-main')
        self.setUrls()


    def setUrls(self):
        self.wepon_url = self.parent.find_element_by_link_text('View All Weapons').get_attribute('href')
        self.agents_url = self.parent.find_element_by_link_text('View All Agents').get_attribute('href')
    
    def getWeponUrl(self):
        return self.wepon_url

    def getAgentUrl(self):
        return self.agents_url

    def openPage(self,link):
        self.proccesDriver.get(link)
        sleep(4)

    def back (self):
        self.proccesDriver.back()

    def exit(self):
        self.proccesDriver.quit()


    def rank(self):
        self.currentRankInfo = self.sidebar.find_elements_by_class_name('rating-entry__rank-info')
        self.mainDic['currentRank'] =  self.currentRankInfo[0].find_element_by_class_name('label').text
        self.mainDic['currentMMR'] = self.currentRankInfo[0].find_element_by_class_name('mmr').text 
        self.mainDic['peakRank'], self.mainDic['peakMMR'] =  self.currentRankInfo[1].find_element_by_class_name('value').text .splitlines()

    def accuracry(self) :
        self.accuracyInfo = self.sidebar.find_element_by_class_name('accuracy__content').find_elements_by_class_name('stat__value')

        self.mainDic['headShotPercent'] =  round(float(self.accuracyInfo [0].text.replace("%",""))/100 , 3)
        self.mainDic['headShotHit'] = int(self.accuracyInfo [1].text)
        self.mainDic['bodyShotPercent'] =  round(float(self.accuracyInfo [2].text.replace("%",""))/100 , 3)
        self.mainDic['bodyShotHit'] = int(self.accuracyInfo [3].text)
        self.mainDic['legShotPercent'] = round(float(self.accuracyInfo [4].text.replace("%",""))/100 , 3)
        self.mainDic['legShotHit'] = int(self.accuracyInfo [5].text)

    def topWepon(self) :
        self.topWeponsInfo= self.sidebar.find_elements_by_class_name('weapon')
        self.mainDic['firstTopWeponLabel'] = self.topWeponsInfo[0].find_element_by_class_name('weapon__name').text
        self.mainDic['firstTopWeponType'] = self.topWeponsInfo[0].find_element_by_class_name('weapon__type').text
        self.mainDic['firstTopWeponKills'] = int(self.topWeponsInfo[0].find_element_by_class_name('value').text.replace(",",""))

        self.mainDic['secondTopWeponLabel'] = self.topWeponsInfo[1].find_element_by_class_name('weapon__name').text
        self.mainDic['secondTopWeponType'] = self.topWeponsInfo[1].find_element_by_class_name('weapon__type').text
        self.mainDic['secondTopWeponKills'] = int(self.topWeponsInfo[1].find_element_by_class_name('value').text.replace(",",""))

        self.mainDic['thirdTopWeponLabel'] = self.topWeponsInfo[2].find_element_by_class_name('weapon__name').text
        self.mainDic['thirdTopWeponType'] = self.topWeponsInfo[2].find_element_by_class_name('weapon__type').text
        self.mainDic['thirdTopWeponKills'] = int(self.topWeponsInfo[2].find_element_by_class_name('value').text.replace(",",""))

    def mapInfo(self) : 
        for elements in self.sidebar.find_elements_by_class_name('top-maps__maps-map'):
            mapName = elements.find_element_by_class_name('name').text
            mapWinLoss = elements.find_element_by_class_name('label').text
            winLossList = list(map(int,mapWinLoss.translate({ord("W"):None,ord("L"):None}).split('-')))
            self.mainDic[f'{mapName} Win'] = winLossList[0]
            self.mainDic[f'{mapName} Loss'] = winLossList[1]

    def winLossInfo(self):
        self.winLossInfo = self.mainbar.find_element_by_class_name('trn-profile-highlighted-content__ratio').find_elements_by_tag_name('text')
        self.mainDic["Wins"] = int(self.winLossInfo[0].text)
        self.mainDic["Loss"]  = int(self.winLossInfo[1].text)


    def generalInfo(self):
        self.nameGiantData = self.mainbar.find_element_by_class_name('giant-stats').find_elements_by_class_name("name")
        self.valueGiantData = self.mainbar.find_element_by_class_name('giant-stats').find_elements_by_class_name("value")
        for i in range(len(self.nameGiantData)) : 
            if i != 2:
                self.mainDic[f"{self.nameGiantData[i].text}"] = float(self.valueGiantData[i].text.replace("%",""))



        self.nameData = self.mainbar.find_element_by_class_name('main').find_elements_by_class_name("name")
        self.valueData = self.mainbar.find_element_by_class_name('main').find_elements_by_class_name("value")
        for i in range(len(self.nameData)):
            self.mainDic[self.nameData[i].text] = float(self.valueData[i].text.replace(",",""))

    def weponData(self) : 
        self.openPage(self.getWeponUrl())
        #self.proccesDriver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div/main/div[3]/div[3]/div[2]/div/div[3]/div[1]/div[1]/span').click()
#         sleep(1)
        self.weponMainLoop = self.proccesDriver.find_elements_by_class_name('st-content__item')
        for wepons in self.weponMainLoop[4:]:
            self.weponInfoList = wepons.find_elements_by_class_name('value')
            self.weponName = self.weponInfoList[0].text
            self.mainDic[f'{self.weponName}-Kills']  = self.weponInfoList[1].text
            self.mainDic[f'{self.weponName}-Death']  = self.weponInfoList[2].text
            self.mainDic[f'{self.weponName}-HeadShot%']  = self.weponInfoList[3].text
            self.mainDic[f'{self.weponName}-Damage/Round']  = self.weponInfoList[4].text
            self.mainDic[f'{self.weponName}-kills/Round']  = self.weponInfoList[5].text
            self.mainDic[f'{self.weponName}-Longest Kill Distance']  = self.weponInfoList[6].text

    def agentData (self):
        self.openPage(self.getAgentUrl())
#         self.proccesDriver.find_element_by_css_selector('div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.trn-grid--small.agents > div > div.st-header > div.st__item.st-header__item.st-header__item--sortable.st__item--sticky.st__item--wide.agent-row').click()
#         sleep(1)
        self.result = []
        for i in self.proccesDriver.find_elements_by_css_selector('div.value'):
            self.result.append(i.text)

        # Human Error in This part need to fix (basically 1 before HS% )   
        list_chunked = [self.result[i:i +  18] for i in range(0, len(self.result),  18)]
        for element in list_chunked:
            name = element[0]
            self.mainDic[f'{name}-TimePlayer'] = element[1]
            self.mainDic[f'{name}-Matches'] = element[2]
            self.mainDic[f'{name}-Win%'] = element[3]
            self.mainDic[f'{name}-K/D'] = element[4]
            self.mainDic[f'{name}-ADR'] = element[5]
            self.mainDic[f'{name}-ACS'] = element[6]
            self.mainDic[f'{name}-HS%'] = element[7]
            self.mainDic[f'{name}-KAST'] = element[8]

            # removing to reduce size 
            # these give wroing data have to manually go through and fix (up to whoever imroving if want to fix or not)
            # self.mainDic[f'{name}-AttackWinLoss'] = element[11]
            # self.mainDic[f'{name}-AttackWin%'] = element[12]
            # self.mainDic[f'{name}-AttackK/D'] = element[13]
            # self.mainDic[f'{name}-DefenseWinLoss'] = element[14]
            # self.mainDic[f'{name}-DefenseWin%'] = element[15]
            # self.mainDic[f'{name}-DefenseK/D'] = element[16]

    def getDictionaryKeys(self):
        return list(self.mainDic.keys())
    
    def getDictionaryValues(self):
        return list(self.mainDic.values())

    def getDictionary(self):
        return list(self.mainDic)
    
    