from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os
import csv

def get_date(url):
    headers = {
        "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept - Language": "ru - RU, ru;q = 0.9, en - US;q = 0.8, en;q = 0.7",
        "Cache - Control": "max - age = 0",
        "Connection": "keep - alive",
        "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 91.0.4472.101Safari / 537.36"
    }

# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
url = "https://ekinobilet.fond-kino.ru/films/"
# driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",chrome_options=chrome_options)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")

def read_page():
    driver.get(url=url)
    put_button_load= driver.find_element_by_xpath(".//*[@href=\"#load\"]")
    for i in range(17):
        put_button_load.click()
        time.sleep(4)
    page_sor = driver.page_source
    soup = BeautifulSoup(page_sor,'lxml')
    if not os.path.exists("data"):
        os.mkdir("data")
    with open("data/page_1.html", "w",encoding='utf8') as file:
        file.write(page_sor)

    list_categorial = driver.find_elements_by_xpath(".//*[@class=\'tc-pict\']")
    list_categorial[0].click()
    time.sleep(15)
    with open("data/page_1.html",encoding='utf8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    films_count = soup.find_all(class_="tc-info")
    films_date = []
    for i in films_count:
        # print(i.text.strip())
        films_date.append(datetime.datetime.strptime(i.text.strip(), '%d.%m.%Y'))
    print(min(films_date))

def screen_fk(soup,text_1,list_grd):
    k=soup.find(text=text_1).find_next().text
    return list_grd.append(k)




try:
    read_page()
    with open("data/page_1.html",encoding='utf8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    item_packs = soup.find_all(class_="tc-desc")
    with open("list_of_films.csv","w",encoding='utf8',newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Name",
                "Date",
                "URL"
            )
        )
    with open("list_of_cash.csv","w",encoding='utf8',newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "general_fees",
                "pre_sell",
                "first_day_sell",
                "first_weekend_sell",
                "next_weekend_sell",
                "date_of_start",
                "year_create",
                "director",
                "distributor",
                "URL"
            )
        )
    data_url=[]
    for item in item_packs:
        film_name = item.find(class_="tc-title").text
        film_date = item.find("time").text.strip()
        film_url = f'https://ekinobilet.fond-kino.ru/{item.find(class_="tc-title").get("href")}'

        data_url.append(film_url)
        # print(f"film:{film_name}, date:{film_date}, url:{film_url}")
        with open("list_of_films.csv", "a",encoding='utf8',newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    film_name,
                    film_date,
                    film_url
                )
            )

    for i in data_url:
        try:
            driver.get(url=i)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source,"lxml")
            grd_legend = []
            general_fees = soup.find(class_='grd-canvas').find(class_="-val").text
            grd_legend.append(general_fees)
            item_block = soup.find(class_="grd-legend")
            number_of_grd_legend= item_block.find_all(class_="-val")
            for j in number_of_grd_legend:
                grd_legend.append(j.text.strip())
            screen_fk(soup,"Старт:",grd_legend)
            screen_fk(soup,"Год:",grd_legend)
            screen_fk(soup,"Режиссер:",grd_legend)
            try:
                film_distibuter = soup.find(text="Дистрибьютор:").find_next().text.strip()
                grd_legend.append(film_distibuter)
            except Exception as ex2:
                print("no distibuter   -   ",ex2)
                grd_legend.append(":(")
            grd_legend.append(i)
            with open("list_of_cash.csv", "a", encoding='utf8',newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        grd_legend[0],
                        grd_legend[1],
                        grd_legend[2],
                        grd_legend[3],
                        grd_legend[4],
                        grd_legend[5],
                        grd_legend[6],
                        grd_legend[7],
                        grd_legend[8],
                        grd_legend[9]
                    )
                )



            print(grd_legend)
        except Exception as ex1:
            print(ex1)
            with open("list_of_cash.csv", "a", encoding='utf8',newline="") as file:
                writer = csv.writer(file)
                writer.writerow((f" , , , , , , ,{i}"))
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
