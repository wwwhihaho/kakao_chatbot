from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import time, re


USER = "아이디"
PASS = "비밀번호"


print("드라이버 추출하기 --- (※1)")
#driver = webdriver.Chrome('/home/ubuntu/Django/data/chromedriver')
#driver.implicitly_wait(3)
driver = webdriver.PhantomJS('/home/ubuntu/Django/data/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver.set_window_size(1124, 850)
driver.implicitly_wait(3)
print("1")

print("# 로그인 페이지에 접근하기 --- (※2)")
driver.get('http://www.samsungwelstory.com/customer/individual/weeklyMenui.jsp')
driver.implicitly_wait(3)
print("2")

print("텍스트 박스에 아이디와 비밀번호 입력하기 --- (※3)")
e = driver.find_element_by_id("ip_id")
e.clear()
e.send_keys(USER)
e = driver.find_element_by_id("ip_pw")
e.clear()
e.send_keys(PASS)
driver.implicitly_wait(3)
print("3")

print("# 입력 양식 전송해서 로그인하기 --- (※4)")
form = driver.find_element_by_css_selector("#ip_login")
form.submit()
print("로그인 버튼을 클릭합니다.")
driver.implicitly_wait(3)
print("4")

print("# 식당 선택")
#driver.find_element_by_id('selHall').click()
#driver.find_element_by_link_text('코리아벤쳐타운').click()
driver.find_element_by_xpath("//*[@id='selHall']/option[text()='코리아벤쳐타운']").click()
#select = Select(driver.find_element_by_id('selHall'))
#select.select_by_visible_text('코리아벤쳐타운')
driver.implicitly_wait(3)
print("5")

print("# 조회")
time.sleep(1)
driver.find_element_by_xpath('//*[@id="content_body"]/form/fieldset/div/table/tbody/tr[2]/td/div/button').click()
time.sleep(1)
driver.implicitly_wait(3)
print("6")

print("# 페이지 파싱")
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.implicitly_wait(3)
print("7")

print("# 데이터테이블 만들기")
def get_meal_data(week_number):
    meal = [i.get_text().replace('\n', ' ').strip() for i in [item for sublist in [i.find_all('ul', {'class':'foodlist'}) for i in soup.find_all('tr', {'class': 'tr_'+str(week_number)})] for item in sublist]]
    meal_num = len(soup.find_all('tr', {'class': 'tr_'+str(week_number)}))
    weekday = [i for i in str(week_number) * meal_num]
    breakfast = [meal[j] for j in range(0,meal_num*4,4)]
    lunch = [meal[j] for j in range(1,meal_num*4,4)]
    dinner = [meal[j] for j in range(2,meal_num*4,4)]
    etc = [meal[j] for j in range(3,meal_num*4,4)]
    
    df_meal = pd.DataFrame({'weekday':weekday, 'breakfast':breakfast, 'lunch':lunch, 'dinner':dinner, 'etc':etc})

    return df_meal    

dataset=[]
for i in range(1,6):
    dataset.append(get_meal_data(i))
df_meal = pd.concat(dataset)


df_meal["breakfast"] = df_meal["breakfast"].str.replace(r"^0Kcal","%!%")
df_meal["lunch"] = df_meal["lunch"].str.replace(r"^0Kcal","%!%")
df_meal["dinner"] = df_meal["dinner"].str.replace(r"^0Kcal","%!%")
df_meal["etc"] = df_meal["etc"].str.replace(r"^0Kcal","%!%")


print("# csv파일 저장")
df_meal.to_csv("meal.csv", index=False)
df_meal.to_csv("/home/ubuntu/Django/app/meal.csv", index=False)
print("end")

