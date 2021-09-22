import requests
from bs4 import BeautifulSoup as bs
import os
import json
import m3u8
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
espartana_session = requests.Session()
driver = webdriver.Chrome(chrome_options=options)

class Downloader():

    def index(self):
        cursos = self.selenium_part()
        self.get_cursos(cursos)

    def selenium_part(self):
        url = 'https://app.escolaespartana.com.br'
        email = 'tavaresconsole-HP13015750693776'
        password = 'wOvAtcXZhRKQ'
        driver.get(url)
        driver.find_element_by_xpath('/html/body/main/section/div/form/div[2]/input').send_keys(email, Keys.TAB, password, Keys.TAB, Keys.SPACE)
        driver.find_element_by_xpath('/html/body/main/section/div/form/div[4]/a[1]').click()
        time.sleep(5)
        urls = [
            'https://app.escolaespartana.com.br/dropshipping',
            'https://app.escolaespartana.com.br/redes-sociais',
            'https://app.escolaespartana.com.br/fazer-dinheiro',
            'https://app.escolaespartana.com.br/marketing-digital',
            'https://app.escolaespartana.com.br/design-grafico',
            'https://app.escolaespartana.com.br/web-design',
            'https://app.escolaespartana.com.br/edicao-de-video',
            'https://app.escolaespartana.com.br/fotografia',
            'https://app.escolaespartana.com.br/arquitetura',
            'https://app.escolaespartana.com.br/pintura-e-desenho',
            'https://app.escolaespartana.com.br/modelagem-3d',
            'https://app.escolaespartana.com.br/criacao-de-jogos',
            'https://app.escolaespartana.com.br/financas'
        ]
        
        #self.cursos = []
        self.curso = {}
        
        for url in urls:
            driver.get(url)
            categoria = driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div[1]/h1').text
            cursos = driver.find_elements_by_css_selector('.card.flex-fill.course-card.premium-course')
            self.curso[categoria] = {}
            for index, curso in enumerate(cursos):
                curso_nome = curso.find_element_by_class_name('nomargin').find_element_by_tag_name('a').text
                curso_link = curso.find_element_by_class_name('nomargin').find_element_by_tag_name('a').get_attribute('href')
                #print(curso_nome, curso_link)
                
                self.curso[categoria][index] = {}
                self.curso[categoria][index]['nome'] = self.replacer(curso_nome)
                self.curso[categoria][index]['link'] = curso_link
        #self.cursos.append(self.curso)

            #print(self.curso)
        #with open('json.json', 'w', encoding='utf-8') as outfile:
            #outfile.write(json.dumps(self.curso))
        #print(self.cursos)
        #exit(0)
        return self.curso

    def get_cursos(self, cursos):
        headers = {
            'authority': 'app.escolaespartana.com.br',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://app.escolaespartana.com.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        s_cookies = driver.get_cookies()
        cookies = {}
        for cookie in s_cookies:
            cookies[cookie['name']] = cookie['value']
        
        for curso_key, curso_value in cursos.items():
            categoria = curso_key
            try:
                categoria.replace('#', '')
            except:
                pass
            for curso in curso_value.values():
                #print(curso[curso])
                title_curso = self.replacer(curso['nome'])
                driver.get(curso['link'])
                div_main = driver.find_element_by_class_name('lessons-listing')
                lessons = div_main.find_elements_by_css_selector('.lesson-item.shadow-sm')
                links = []
                for lesson in lessons:
                    #
                    link = lesson.find_element_by_tag_name('a').get_attribute('href')
                    links.append(link)
            
                        #print(title)
                for index, link in enumerate(links, start=1):
                    path = self.criar_pastas_curso(f'Cursos/{categoria}/{title_curso}')
                    while True:

                        driver.get(link)
                        if driver.current_url == link:
                            break
                        else:
                            try:
                                subs = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div/form/a')
                                sub_out = subs.get_attribute('innerHTML')
                                if 'Fazer' in sub_out:
                                    subs.click()
                            except:
                                try:
                                    driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div[2]/div[1]/div/form/a').send_keys(Keys.RETURN)
                                except:
                                    pass
                                pass
                            #driver.get(link)

                    title = self.replacer(driver.find_element_by_class_name('lesson-single-title').text)
                    video_path = f'{path}/{index} - {title}.mp4'
                    if os.path.exists(video_path):
                        continue
                    try:
                        video = driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div/div[1]/div/iframe').get_attribute('src')
                    except:
                        continue
                    
                    if 'vimeo' in video:

                        try:
                            video = video.split('?')[0]
                        except:
                            pass
                        video = f'{video}/config'
                        self.download_video(video, video_path)
                    elif 'youtube' in video:
                        os.system(f'youtube-dl --quiet "{video}" -o "{video_path}"')
                    elif 'loom' in video:
                        response = json.loads(str(bs(requests.get(video).content, 'html.parser').find('script')).split(' = ')[1].split(';')[0])['sources']['source-play-mp4']
                        key = '?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZG4ubG9vbS5jb20vc2Vzc2lvbnMvcmF3Lzg2YjVmNDg2NTg2MjRlNDhhZGZhODVjNGQ0NmM4ZTQyKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTYwMDk3MDg0OH19fV19&Signature=dg8QPrQcGAP3t~fvIrBtqMY~o5yy3OmWXG0gVOLNkHpy0pnHrLlJju0TxLbYoHnPKtZGsdMmMeJHTJcUpA9qghRpC2jWnJfV0AXW5zeNK1wzRq3E7JJ7HypYfmjj-iZTfIMvAR-1DPoy~QWt0BsasCu~sW6tWhSWd~~wMaJVF631azBY2Z3dZbHYCwRERWu02kifnY49Z1G8YrArs1EOiknWQpE4cxmDZ95yikEtxIlnfwHvxoTb~3~3uU~f~6Lh4p7Q0KydDbcI4u5UZQAsKfItIvO0YuLCTEYTaFPmgV4TAHqf-sCI7qNnWmqeFpYMs55dpqm4k4qlCiCSksA2wA__&Key-Pair-Id=APKAJQIC5BGSW7XXK7FQ&Expires=1600970848.051?Expires=1600970848&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZG4ubG9vbS5jb20vc2Vzc2lvbnMvcmF3Lzg2YjVmNDg2NTg2MjRlNDhhZGZhODVjNGQ0NmM4ZTQyLW1hbmlmZXN0Lm1wZCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTYwMDk3MDg0OH19fV19&Signature=KigKmIiNcOw7v4W2LonMW2UhzitwY9qmPKW9DrOhXWXe3mKe18VlL1ZN45C-Hay~PoFWu73DoTD1V3x~QPNFhdovvRdabQvu7qmuMc~G7nJdZAzBMhP-WJIcZU0oCAePqSan721qw9fH6v2AaxFoGLzSowigOMUkWpzl55RQXj64ALx~WatiiPs4C~d1CqQiyfpjIm793C7Gvq191Mil5uySfU5EHFoh-3~pTIAoDs~tTW1onMii0GDn7p6G4hnTFXIhav4ugn1sfDvsPzlvv7d0~FxK9zLDzX6AUc8sY~U21zeBgMTauSv7tLMLV7w2NjENx6cR-71lr6cx3d2qlw__&Key-Pair-Id=APKAJQIC5BGSW7XXK7FQ&selected_id=1'
                        video = f'https://cdn.loom.com/{response}{key}'
                        os.system(f'aria2c -o "{video_path}" "{video}" --quiet')
                        
                    print(video_path)


    def criar_pastas_curso(self, path):

        if os.path.exists(path) is False:
                os.makedirs(path)
        return path

    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text
    
    def download_video(self, video, path):

        if os.path.exists(path) is False:
            vimeo_headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://app.escolaespartana.com.br//',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            while True:
                try:
                    vimeo_config = requests.get(video, headers=vimeo_headers).json()
                    break
                except:
                    pass
            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']

            #os.system(f'''aria2c -i {vimeo_url} -nostats -loglevel 0 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "{video_path}"''')            
            os.system(f'aria2c -o "{path}" {vimeo_url} --quiet')

#Downloader().index()