from retrying import retry
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import csv
import json


with open('config.json')as f:
    data = json.load(f)
for state in data["template"]:
    break

def ArquivoMestreCSV():

    f = open("ArquivoMestre.csv", "w", newline="", encoding="utf-8")
    os.system("attrib +h ArquivoMestre.csv")
    writer = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_MINIMAL)

    url = state['yupoo_link']
    text = url

    head, sep, tail = text.partition('x.yupoo.com')
    print("Preparando para baixar as fotos de " + head + "x.yupoo.com")

    response = requests.get(url)
    
    data = response.text
    soup = BeautifulSoup(data, 'lxml') 
    #soup = BeautifulSoup(data, 'lxml')
    
    writer.writerow(["LINKS"])

    row1 = []
    count=0
    for link in soup.findAll('a', class_='album__main'):
        count=count+1
        q = (link.get('href'))

        row1.append(q)
    print("Encontrei " + str(count) + " albuns")


    for c in range(len(row1)):
        writer.writerow([row1[c]])


    f.close()
    print("Arquivo CVS com links disponivel em:" + os.getcwd())
    print("Estou baixando as fotos")

ArquivoMestreCSV()


@retry(stop_max_attempt_number=5)
def CriarArquivoLinks(X):
    try:
        with open((str(X) + 'Links'), 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            df = pd.read_csv(os.getcwd() + "\\ArquivoMestre.csv", sep=' ')

            TEXT = (df['LINKS'][X])
            url = state['yupoo_link']
            text = url
            head, sep, tail = text.partition('x.yupoo.com')
            url = head + "x.yupoo.com" + TEXT

            response = requests.get(url, timeout=None)
            data = response.content
            soup = BeautifulSoup(data, 'lxml')
            szukaj = soup.select('.image__landscape')
            writer.writerow([X])
            for x in szukaj:
                q = x['data-src']
                writer.writerow(['https:' + q])
            szukaj = soup.select('.image__portrait')
            for x in szukaj:
                q = x['data-src']
                writer.writerow(['https:' + q])
    except:
        pass


def Download(x):
    try:
        def create_directory(directory):
            if not os.path.exists(directory):
                os.makedirs(directory)

        def download_save(url, folder):
            try:
                create_directory(folder)
                c = requests.Session()
                c.get('https://photo.yupoo.com/')
                c.headers.update({'referer': 'https://photo.yupoo.com/'})
                res = c.get(url, timeout=None)
                with open(f'{folder}/{url.split("/")[-2]}.jpg', 'wb') as f:
                    f.write(res.content)
            except:
                pass

        dfzdj = pd.read_csv(os.getcwd() + '\\' + str(x) + "Links")
        count = 0
        try:
            for col in dfzdj.columns:

                for url in dfzdj[col].tolist():
                    count += 1
                    if str(url).startswith("http"):
                        download_save(url, col)
                        count

                print("Baixei " + str(count) + " Fotos em um album, proximo.")
        except:
            pass
        try:
            path = (os.getcwd() + '\\' + col)
            files = os.listdir(path)
            for index, file in enumerate(files):
                os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index), 'big.jpg'])))
        except:
            pass

    except:
        pass


for x in range(int(state['numero de produtos'])):
    CriarArquivoLinks(x)
    Download(x)
    os.remove(str(x) + 'Links')


