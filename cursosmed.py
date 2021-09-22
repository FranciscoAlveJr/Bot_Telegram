import requests
from bs4 import BeautifulSoup as bs
import json
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time

os.system('cls')

med_session = requests.Session()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)


class Downloader():
    
    def index(self):



        email = 'ocoisa081@gmail.com'
        senha = '18020301.pP'

        data = {
        'log': email,
        'pwd': senha,
        }

        driver.get('https://cursomeds.com.br/wp-login.php')
        driver.find_element_by_xpath('/html/body/div[1]/form/p[1]/input').send_keys(data['log'], Keys.TAB, data['pwd'], Keys.RETURN)
        time.sleep(1)
        driver.get('https://cursomeds.com.br/cursos/extensivo-meds/')
        links = driver.find_elements_by_css_selector('.ld-item-name.ld-primary-color-hover')
        listagem = []
        for count, link in enumerate(links, start=1):
            att = link.get_attribute('href')
            listagem.append(att)
        for count, link in enumerate(listagem, start=1):
            driver.get(link)
            title = self.replacer(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/h1').text).strip()
            bloco = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/div/div[3]/div')
            items = bloco.find_elements_by_class_name('ld-table-list-item')
            outros = []
            for item in items:
                linki = item.find_element_by_tag_name('a').get_attribute('href')
                outros.append(linki)

            for outro in outros:
                driver.get(outro)
                titlei = self.replacer(driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/h1').text).strip()
                name = titlei
                
                self.path = f'Cursos MED/{count} - {title}/{name}'
                if os.path.exists(self.path) is False:
                    os.makedirs(self.path)
                try:
                    self.iftexto(name)
                    pass
                except:
                    pass
                self.ifvideo(name)

                #try:
                    #material = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]')
                    #pass
                #except:
                    #continue
                #materiais = material.find_elements_by_tag_name('a')
                #self.path2 = f'Cursos MED/{count} - {title}/{name}/Material'
                #if os.path.exists(self.path2) is False:
                    #os.makedirs(self.path2)
                #for material_link in materiais:
                    #link_id = material_link.get_attribute('href').split('?id=')[1]
                    #link_final = f"https://docs.google.com/uc?id={link_id}&export=download"
                    #os.system(f'aria2c -d "{self.path2}" "{link_final}" --continue')

        os.system('pause')
    
    def iftexto(self, name):
        texto = driver.find_element_by_class_name('ld-tabs-content').text
        if texto == '':
            return
        with open(f'{self.path}/{name}.txt', 'w', encoding='utf-8') as out:
            out.write(texto)

    def ifvideo(self, name):
        
        try:
            try:
                video = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/iframe').get_attribute('src').split('?')[0]
            except:
                 video = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/div/iframe').get_attribute('src').split('?')[0]
            pass
        except:
            return

        video_path = f'{self.path}/{name}.mp4'
        print(video_path, video)
        if os.path.exists(video_path) is False:
            vimeo_headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://cursomeds.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }

            while True:
                try:
                    vimeo_config = requests.get(f'{video}/config', headers=vimeo_headers).json()
                    break
                except:
                    return
            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']
            print(vimeo_url)
            os.system(f'aria2c -o "{video_path}" "{vimeo_url}" --quiet')

        pass

    def ifmaterial(self, name):
        pass

    def replacer(self, text):
        invalid = {'p/': 'para', '\t': '', r'"': r"'", '\\': " - ", "/": "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text         


#Downloader().index()
