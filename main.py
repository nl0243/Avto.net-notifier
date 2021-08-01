import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import yagmail

baseurl = "https://www.avto.net/Ads/results_100.asp"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def loop(url, headers):
    time.sleep(5)

    table = []
    now = datetime.now()  # current date and time
    year = now.strftime("%Y")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    for cars in soup.findAll('div', class_='GO-Results-Row'):
        try:
            ime = cars.find("div", class_="GO-Results-Naziv").text

            base_link=cars.find("a", class_="stretched-link")['href']
            link="https://www.avto.net" + base_link[2:]
            podatki = cars.findAll("tr")
            registracija = int(podatki[0].text.split("\n")[2])
            prevozenih= int(podatki[1].text.split("\n")[2][:-2])
            menjalnik= podatki[2].text.split("\n")[2]
            motor= podatki[3].text.split("\n")[3]

            cena= int(cars.find("div", class_="GO-Results-Price-TXT-Regular").text[:-2].replace(".", ""))

            #Nalovi pogoji
            if(prevozenih < 70000 and registracija > 2016 and cena < 7000):
                contents = [
                    "Ime:" + ime,
                    "registracija:" + str(registracija),
                    "prevozenih:" + str(prevozenih),
                    "menjalnik:" + menjalnik,
                    "motor:" + motor,
                    "cena:" + str(cena),
                    "link: " + link
                ]
                try:
                    yag = yagmail.SMTP('avton376@gmail.com', 'mojegeslo')
                    yag.send('luksic11111@gmail.com', 'Nov oglas na avto.net', contents)
                    print(ime, link, registracija, prevozenih, menjalnik, motor, cena)
                except Exception as error:
                    print('Caught this error: ' + repr(error))
        except:
            print("Oglas ni popoln.")
loop(baseurl, headers)