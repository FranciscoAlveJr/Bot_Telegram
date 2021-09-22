import requests
from bs4 import BeautifulSoup as bs
import selenium
import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver as se
from selenium.webdriver.chrome.options import Options
import time
import pickle
import json
import urllib

class Downloader():

    def index(self):
        waldematica_session = requests.Session()
        data = {
            'email': 'princeandrews081@gmail.com',
            'senha': '18020301.p'
        }
        driver = se.Chrome()
        driver.get('https://antigo.waldematica.com.br/login/')
        driver.find_element_by_id('user_login').send_keys(data['email'], Keys.TAB, data['senha'], Keys.RETURN)
           
        info = input('1 - Usar Lista\n2 - Atualizar Lista\nR: ') 
           
        if info.isdigit():
            if info == "2":           
                driver.get('https://antigo.waldematica.com.br/cursos-waltematica/')

                cookies_selenium = driver.get_cookies()
                cookies = {}

                for cookie in cookies_selenium:
                    cookies[cookie['name']] = cookie['value']

                pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

                driver.find_element_by_xpath('/html/body/div[1]/div[2]/section[2]/div/div/div/div/div[1]/form/div[1]/ul/li[2]/a').click()
                page_max = driver.find_element_by_xpath('/html/body/div[1]/div[2]/section[2]/div/div/div/div/div[1]/div/div[1]/div[2]/a[2]').text
                
                lista_cursos = []
                x = 0
                while x <= int(page_max):
                    x += 1
                    time.sleep(2)
                    print('Pegando cursos da pagina ' + str(x) + '.')
                    cursos = driver.find_elements_by_class_name('item-title')
                    for curso in cursos:
                        curso_link = curso.find_element_by_tag_name('a').get_attribute('href')
                        lista_cursos.append(curso_link)
                    try:
                        driver.find_element_by_css_selector('.next.page-numbers').click()
                    except:
                        break
                with open('listadecursos.json', 'w', encoding='utf-8') as out:
                    out.write(json.dumps(lista_cursos))
            elif info == "1":
                lista_cursos = json.loads(open('listadecursos.json', 'r', encoding='utf-8').read())
        else:
            print('ERRO')
            exit(0)
        headers = {
            'authority': 'waldematica.com.br',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://antigo.waldematica.com.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        os.system('cls')


        for curso in lista_cursos:
            driver.get(curso)
            title = self.replacer(driver.find_element_by_xpath('/html/body/div[1]/div[2]/section[1]/div/div/div/div/div[2]/div/h1').text)
            try:
                archive = driver.find_element_by_class_name('small_desc').find_element_by_tag_name('a')
                archive_link = archive.get_attribute('href')
                archive_title = self.replacer(archive.text)
                try:
                    filename = f'{path}/{archive_title}.zip'
                    os.system(f'aria2c -o "{filename}" "{archive_link}" --quiet')
                except:
                    print('\tNão foi possivel baixar os arquivos de auxilio.')
            except:
                pass
            path = f'Cursos/{title}'
            print(title)
            if os.path.exists(path) is False:
                os.makedirs(path)
            videos = driver.find_element_by_class_name('course_curriculum').find_elements_by_tag_name('a')
            video_lista = []
            for video in videos:
                video_lista.append(video.get_attribute('href'))

            for index, url in enumerate(video_lista):
                index += 1    
                driver.get(url)
                title = self.replacer(driver.find_element_by_css_selector('.pagetitle.unit').text)
                vimeo = driver.find_element_by_class_name('unit_content').find_element_by_tag_name('iframe').get_attribute('src').split('?')[0]
                video_path = f'{index} - {title}.mp4'
                print(f'\t{index} - {title}')
                final_path = f'{path}/{video_path}'
                if 'vimeo' in vimeo:
                    self.video_download(final_path, vimeo)
                else:
                    os.system(f'youtube-dl -o "{final_path}" {vimeo}')



    def video_download(self, path, video):
        if os.path.exists(path) is False:
            vimeo_headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Dest': 'iframe',
                'Referer': 'https://antigo.waldematica.com.br',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            
            while True:
                try:
                    vimeo_config = requests.get(f"{video}/config", headers=vimeo_headers).json()
                    break
                except:
                    pass
            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']

            #os.system(f'''aria2c -i {vimeo_url} -nostats -loglevel 0 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "{video_path}"''')            
            os.system(f'aria2c -o "{path}" {vimeo_url} --quiet') #         

    
    def replacer(self, text):
            invalid = {r'"': r"'", '\\': " - ", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
            for char in invalid:
                if char in text:
                    text = text.replace(char, invalid[char])
            return text


#Downloader().index()
    





