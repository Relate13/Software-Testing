from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

class APITest():
    def __init__(self,case_size=10) -> None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
        self.wd = webdriver.Chrome(
            options=options,
            service=Service(r"C:\Users\Relate13\Desktop\Software Testing\chromedriver_win32\chromedriver.exe"))
        self.City_Coordinates={}
        self.case_size=case_size


    def GetCityResult(self,selected_city):
        self.wd.get("http://www.nmc.cn/publish/forecast.html")
        Row_City_Lists=self.wd.find_elements(By.CLASS_NAME,"city-list")
        Popular_City=Row_City_Lists[0];
        Cities = Popular_City.find_elements(By.CLASS_NAME,"city")
        for city in Cities:
            title=city.find_element(By.CLASS_NAME,"col-xs-3")
            if title.text==selected_city:
                city.click()
                time.sleep(0.5)
                return self.wd.find_element(By.ID,"aqi").text

    def GetCitiesCoordinates(self):
        self.wd.get("http://www.nmc.cn/publish/forecast.html")
        Row_City_Lists=self.wd.find_elements(By.CLASS_NAME,"city-list")
        Popular_City=Row_City_Lists[0];
        Cities = Popular_City.find_elements(By.CLASS_NAME,"city")
        City_Names=[];
        for city in Cities:
            title=city.find_element(By.CLASS_NAME,"col-xs-3")
            #print(title.text)
            City_Names.append(title.text)
        print(City_Names)

        self.wd.get("https://jingweidu.bmcx.com/")
        for city_name in City_Names:
            textbox=self.wd.find_element(By.ID,"fen_xi_di_qu")
            button=self.wd.find_element(By.CLASS_NAME,"all_an_1")
            textbox.send_keys(Keys.CONTROL, "a")
            if city_name=="徐家汇":
                textbox.send_keys("上海")
            else:
                textbox.send_keys(city_name)
            button.click()
            time.sleep(0.5)
            longitude=float(self.wd.find_element(By.ID,"all_lng_show").get_attribute("value"))
            latitude=float(self.wd.find_element(By.ID,"all_lat_show").get_attribute("value"))
            pair=[longitude,latitude]
            self.City_Coordinates[city_name]=pair
        for item in self.City_Coordinates.items():
            print(item)
    def RandomTesting(self):
        print("[随机测试开始]")
        Testcase=[]
        TestResult={}
        case_size=self.case_size
        while len(Testcase)<case_size:
            candidate=random.choice(list(self.City_Coordinates.keys()))
            if candidate not in Testcase:
                Testcase.append(candidate)
        print("----------已选中样例----------")
        print(Testcase)
        for selected_city in Testcase:
            TestResult[selected_city]=self.GetCityResult(selected_city)
        print("----------随机测试结果----------")
        for item in TestResult.items():
            print(item)
        pollutions=0;
        for value in TestResult.values():
            if "污染" in value:
                pollutions+=1
        print("##########测试结论##########")
        if pollutions<1:
            print("通过")
        else:
            print("未通过")

    def FSCS_Testing(self):
        print("[FSCS自适应随机测试开始]")
        TestResult={}
        candidate_size=5
        case_size=self.case_size
        def GetMinDist(city_a):
            min_dist=float("inf")
            for city_b in list(TestResult.keys()):
                city_a_coordinate=self.City_Coordinates[city_a]
                city_b_coordinate=self.City_Coordinates[city_b]
                delta_ln=city_a_coordinate[0]-city_b_coordinate[0]
                delta_la=city_a_coordinate[1]-city_b_coordinate[1]
                dist=pow(pow(delta_ln,2)+pow(delta_la,2),0.5)
                min_dist=min(min_dist,dist)
            return min_dist
        
        i=0
        Never_Tested_Cities=list(self.City_Coordinates.keys())
        while i<case_size:
            print("----------第"+str(i+1)+"次测试----------")
            Candidate_Cases=[]
            Candidate_Dists=[]
            while len(Candidate_Cases)<candidate_size:# first random choose candidates
                Candidate_Cases.append(random.choice(Never_Tested_Cities))
            print("候选样例名单："+ str(Candidate_Cases))
            print("已测样例名单："+ str(list(TestResult.keys())))
            if len(TestResult)==0: # on first execute
                selected_city = random.choice(Candidate_Cases)
                
            else: # not first execute
                Candidate_Dists=[]
                for candidate in Candidate_Cases:
                    Candidate_Dists.append(GetMinDist(candidate))
                index=0
                chosen_index=0
                current_Max=Candidate_Dists[index]
                while index<len(Candidate_Dists):
                    if Candidate_Dists[index]>current_Max:
                        chosen_index=index
                        current_Max=Candidate_Dists[index]
                    index+=1
                selected_city = Candidate_Cases[chosen_index]
            print("候选距离："+str(Candidate_Dists))
            print("胜出样例："+str(selected_city))
            TestResult[selected_city]=self.GetCityResult(selected_city)
            Never_Tested_Cities.remove(selected_city)
            i+=1
        print("----------FSCS测试结果----------")
        for item in TestResult.items():
            print(item)    
        pollutions=0;
        for value in TestResult.values():
            if "污染" in value:
                pollutions+=1
        print("##########测试结论##########")
        if pollutions<1:
            print("通过")
        else:
            print("未通过")

    def Run(self):
        self.GetCitiesCoordinates()
        #self.RandomTesting()
        #self.FSCS_Testing()
        while True:
            self.RandomTesting()
            self.FSCS_Testing()
            input()

Test=APITest(7)
Test.Run()



