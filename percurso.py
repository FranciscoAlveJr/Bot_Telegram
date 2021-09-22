import requests
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time

os.system('cls')
percurso_session = requests.Session()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.maximize_window()

class Downloader():

    def index(self):

        self.selenium_part()
        selenium_cookies = driver.get_cookies()
        cookies = {}
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']

        self.account_header = {
            'authority': 'www.percurso.com.br',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.percurso.com.br/minha-conta/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'_gcl_au={cookies["_gcl_au"]}; _ga={cookies["_ga"]}; _gid={cookies["_gid"]}; _gat_UA-48087668-1={cookies["_gat_UA-48087668-1"]}; __cfduid={cookies["__cfduid"]}; PHPSESSID={cookies["PHPSESSID"]}; wordpress_logged_in_f4673d48f8b32402742f216075fc262b={cookies["wordpress_logged_in_f4673d48f8b32402742f216075fc262b"]}; wpSGCacheBypass={cookies["wpSGCacheBypass"]}; fakesessid={cookies["fakesessid"]}'
            
        }

        percurso_session.headers.update(self.account_header)
        driver.get('https://www.percurso.com.br/minha-conta/')
        #self.get_medicina()
        self.get_intensivo()
        
        
        #nome = bs(driver.page_source, 'html.parser')
        #print(nome.find('button', {'name': 'save_account_details'}))
        #time.sleep(10)
    
    def selenium_part(self):


        email = "coracy2012@hotmail.com "#input('Login: ') #  
        senha = "medufu2020"#input('Senha: ') #pratodeuva123

        while True:
            try:
                driver.get('https://www.percurso.com.br/minha-conta/')
                driver.find_element_by_xpath('/html/body/div/div[2]/div/article/div/div/div/div/div/div/div/div/div/div/form/p[1]/input').send_keys(email, Keys.TAB, senha, Keys.RETURN)
                break
            except:
                driver.refresh()

    def get_medicina(self):
        driver.get('https://www.percurso.com.br/cursos/minha-medicina/')
        medicina = bs(driver.page_source, 'html.parser')
        title = str(medicina.find('h1', class_='entry-title').getText()).strip()
        video_id = str(json.loads(medicina.findAll('div', class_='ld-tab-content')[0].findAll('div')[0]['data-item'])["sources"][0]["src"]).split('/')[-1]
        vimeo_url = f'https://player.vimeo.com/video/{video_id}/config'
        path = self.criar_pasta('Minha Medicina')
        video_path = f'{path}/{title}.mp4'
        if os.path.exists(video_path) is False:
            self.video_download(video_path, vimeo_url)
        apostilas = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[1]/article/div[2]/div/div/div[2]/div[2]/div[2]').get_attribute('outerHTML')
        apostilas_source = bs(apostilas, 'html.parser')
        apost_title = 'Apostilas'
        apost_list = apostilas_source.findAll('ul')
        path = self.criar_pasta(f'{path}/{apost_title}')

        apost_list = apostilas_source.findAll('ul')[0] 
        li = apost_list.findAll('a')
        for a in li:
            li_text = a.getText()
            li_link = a['href']
            if os.path.exists(f"{path}/{li_text}.pdf") is False:
                os.system(f'aria2c -o "{path}/{li_text}.pdf" {li_link} --quiet')
        path = self.criar_pasta(f'{path}/Exercicios')
        
        apost_list = apostilas_source.findAll('ul')[1]
        li = apost_list.findAll('a')
        
        for b in li:
            try:
                li_text = b.getText()
            except:
                print(b)
                exit(0)
            li_link = b['href']
            if os.path.exists(f"{path}/{li_text}.pdf") is False:
                os.system(f'aria2c -o "{path}/{li_text}.pdf" {li_link} --quiet')

        list_items = driver.find_element_by_class_name('ld-item-list-items').get_attribute('outerHTML')
        list_source = bs(list_items, 'html.parser').findAll('div',class_='ld-table-list-item')
        index = 0
        index_help = ""
        for i in list_source:
            driver.get(i.find('a')['href']) 
            while True:
                try:
                    caminho = driver.find_element_by_class_name('ld-breadcrumbs-segments').get_attribute('outerHTML')
                    break
                except:
                    driver.refresh()
                    pass
            caminho_source = bs(caminho, 'html.parser').findAll('span')
            texts = []
            for span in caminho_source:
                text = self.replacer(str(span.find('a').getText()).strip())
                texts.append(text)
            
            if index_help == texts[1]:
                index += 1
            else:
                index = 1
            index_help = texts[1]
            paths = f"{texts[0]}/{texts[1]}/{index} - {texts[2]}"
            video_path = f'{paths}.mp4'
            print(paths)
            if os.path.exists(video_path):
                continue
            
            #text = ld-tabs-content
            #video = flowplayer
            source = bs(driver.find_element_by_class_name('ld-tab-content').get_attribute('outerHTML'), 'html.parser')
            #print(f"Dentro  do HTML '{source.getText().strip()}'")
            if source.getText().strip() == '':
                continue
            local = self.criar_pasta(f"{texts[0]}/{texts[1]}")
            #try:
            if source.find('div', class_='flowplayer'):
                video_id = json.loads(source.find('div', class_='flowplayer')['data-item'])['sources'][0]['src'].split('/')[-1]
                vimeo_url = f'https://player.vimeo.com/video/{video_id}/config'
                
                
                
                self.video_download(video_path, vimeo_url)
                try:
                    link = source.findAll('a')[-1]['href']
                    link_title = self.replacer(link.split('/')[-1])
                    if os.path.exists(f"{texts[0]}/{texts[1]}/{link_title}") is False:
                        os.system(f'aria2c -o "{texts[0]}/{texts[1]}/{index} - {link_title}" "{link}" --quiet')
                except:
                    pass
            #except:
                #with open(f'{paths}.html', 'w', encoding='utf-8') as out:
                    #out.write(str(source))


                

                    

            #self.replacer() #.strip()

    def get_intensivo(self):


        driver.get('https://www.percurso.com.br/intensivo-medicina/')
        path = self.criar_pasta('INTENSIVO 2020')
        apostilas = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/article/div/div/div/div/div/div/div[2]/div[2]/div').get_attribute('outerHTML')
        apostilas_source = bs(apostilas, 'html.parser')
        apost_title = 'Apostilas'
        apost_list = apostilas_source.findAll('ul')
        
        path = self.criar_pasta(f'{path}/{apost_title}')

        apost_list = apostilas_source.findAll('ul')[0] 
        li = apost_list.findAll('a')
        for a in li:
            li_text = a.getText()
            li_link = a['href']
            if os.path.exists(f"{path}/{li_text}.pdf") is False:
                os.system(f'aria2c -o "{path}/{li_text}.pdf" {li_link} --quiet')
        
        path = self.criar_pasta(f'{path}/Apostilas de Exercicios')
        apost_list = apostilas_source.findAll('ul')[1]
        li = apost_list.findAll('a')
        
        for b in li:
            try:
                li_text = b.getText()
            except:
                print(b)
                exit(0)
            li_link = b['href']
            if os.path.exists(f"{path}/{li_text}.pdf") is False:
                os.system(f'aria2c -o "{path}/{li_text}.pdf" {li_link} --quiet')


        for num in range(0, 10):
            try:
                listas = driver.find_elements_by_css_selector(f'.et_pb_module.et_pb_accordion.et_pb_accordion_{num}')
            except:
                exit(0)
            for lista in listas:
                index = num + 1
                mouth_path = f'{index} - Mes'
                blocos = lista.find_elements_by_css_selector('.et_pb_toggle.et_pb_module.et_pb_accordion_item')
                for bloco in blocos:
                    materias = bloco.find_elements_by_class_name('clearfix')
                    main = str(bloco.find_element_by_css_selector('.et_pb_toggle_title').text).strip()
                    for materia in materias:
                        print(f'\t{main}')
                        source = bs(materia.get_attribute('outerHTML'), 'html.parser')
                        ps = source.find_all('p')
                        uls = source.find_all('ul')
                        for enum, ul in enumerate(uls, start=0):
                            title_p = self.replacer(ps[enum].getText().strip())
                            print('\t\t', title_p)
                            lis = ul.find_all('li')
                            for vide, li in enumerate(lis):
                                a_link = li.find('a')['href']
                                a_text = self.replacer(str(li.find('a').getText()).strip())
                                print('\t\t\t', a_text)
                                driver.execute_script(f'''window.open("{a_link}","_blank");''')
                                time.sleep(3)
                                driver.switch_to.window(driver.window_handles[1])
                                sources = driver.find_elements_by_class_name('et_pb_text_inner')
                                for enume, source in enumerate(sources):
                                    new_path = self.criar_pasta(f'INTENSIVO 2020/{mouth_path}/{main}/{title_p}')
                                    bs_source = bs(source.get_attribute('outerHTML'), 'html.parser')
                                    if bs_source.find('div', class_='flowplayer'):
                                        video_id = json.loads(bs_source.find('div', class_='flowplayer')['data-item'])['sources'][0]['src'].split('/')[-1]
                                        vimeo_url = f'https://player.vimeo.com/video/{video_id}/config'
                                        paths = f'INTENSIVO 2020/{mouth_path}/{main}/{title_p}/{vide} - {a_text}.mp4'
                                        self.video_download(paths, vimeo_url)
                                        continue
                                    try:
                                        archives = bs(driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/article/div/div/div/div/div/div/div[2]/div[3]/div').get_attribute('outerHTML'), 'html.parser').findAll('a')
                                    
                                    
                                        if os.path.exists(f'INTENSIVO 2020/{mouth_path}/{main}/{title_p}/{vide} - {a_text} - {text}.pdf'):
                                            
                                            for a in archives:
                                                link = a['href']
                                                text = link.split('/')[-1]
                                                text = text.replace('-', ' ')
                                                os.system(f'aria2c -o "{mouth_path}/{main}/{title_p}/{vide} - {a_text} - {text}.pdf" "{link}" --quiet')
                                    except:
                                        pass
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])

                                

    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

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
                'Referer': 'https://www.percurso.com.br/',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            vimeo_config = requests.get(video, headers=vimeo_headers).json()
            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']
           
            os.system(f'aria2c -o "{path}" {vimeo_url} --quiet') #  
    
    def criar_pasta(self, path):
        
        if os.path.exists(path) is False:
            os.makedirs(path)

        return path

"""start = Downloader()
start.index()"""

