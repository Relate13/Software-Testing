from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', ['enable-logging'])
wd = webdriver.Chrome(
    options=options,
    service=Service(r"C:\Users\Relate13\Desktop\Software Testing\chromedriver_win32\chromedriver.exe"))
case_size=10
i=0
Result={}
while i<case_size:
    success=True;
    wd.get("https://cs.nju.edu.cn/1651/list.htm")
    elements = wd.find_elements(By.CLASS_NAME,"wp_article_list_table")
    teachers = elements[2].find_elements(By.CLASS_NAME,"Article_Title")
    choice=random.choice(teachers)
    choice.click()
    if len(wd.find_elements(By.CLASS_NAME,"wp_error_msg"))>0:
        success=False
    i+=1
    if success:
        Result[choice.text]="访问成功"
    else:
        Result[choice.text]="访问失败"
print("#####测试结果#####")
for item in list(Result.items()):
    print(item)