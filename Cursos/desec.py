import requests
from bs4 import BeautifulSoup as bs
import json
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

desec_session = requests.Session()
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=options)



class Download():

    def index(self):

        os.system('cls')
        #email = input('email: ')
        #password = input('password: ')
        email = 'nardinbrito@gmail.com'
        password = '@28EtZpXEV9H3PY'
        driver.get('https://desecsecurity.com/academy/login')
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/form/div[1]/input').send_keys(email, Keys.TAB, password, Keys.RETURN)
        selenium_cookies = driver.get_cookies()
        cookies = {}
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']
        #for k_cookie, v_cookies in cookies.items():
            #if 'sucuri' in k_cookie:
                #uuid = k_cookie
        headers = {
            'authority': 'desecsecurity.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://desecsecurity.com/academy/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'PHPSESSID={cookies["PHPSESSID"]}', #{uuid}={cookies[uuid]}; 
        }
        #d4ead87b4975aaf11c624b3cb87ad326

        desec_session.headers.update(headers)
        #url_base = 'https://desecsecurity.com/academy/'
        #desec_parser = desec_session.get(url_base, headers=headers, cookies=cookies).content
        driver.get('https://desecsecurity.com/academy/login')
        desec_source = driver.page_source
        parser = bs(desec_source, 'html.parser')
        cursos = parser.find_all('div', {'class': 'col-xs-9'})
        for index, curso in enumerate(cursos[1:]):
            curso_nome = self.replacer(curso.find('div', {'class': 'left'}).getText().strip())
            curso_link = curso.find('div', {'class': 'right'}).find('a', {'class': 'col-xs-12 bold f12 pd0 link'})['href']
            if 'desecsecurity' not in curso_link:
                curso_link = 'https://desecsecurity.com/academy/' + curso_link
                driver.get(curso_link)
                course_source = driver.page_source
            check = bs(course_source, 'html.parser')
            botao = driver.find_element_by_xpath('//*[@id="btn_finalizar_aula"]')
            botao.click
            botao.click()
            try:
                if check.find('button', {'class': 'btn-curso down'}):
                    print('Finish')
                    exit(1)
            except:
                pass
            print(index, curso_nome)
            
            
            itens = check.find_all('li', {'class': 'pdv4'})
            count = 0
            aula_count = 0
            old_model_title = ''
            for item in itens:

                aula_count += 1
                try:
                    link = item.find('a')['href']
                except:
                    print('Clique no Finalizar Aula e pressione ENTER aQUI')
                    input()
                    link = item.find('a')['href']
                if 'desecsecurity' not in link:
                    link = 'https://desecsecurity.com/academy/' + link
                    driver.get(link)
                    link_source = driver.page_source
                aula = bs(link_source, 'html.parser')
                while True:
                    try:
                        model_title = self.replacer(aula.find('h3', {'class': 'bold branco'}).getText().strip())
                        break
                    except:
                        driver.refresh()
                if model_title != old_model_title:
                    #print('model diferente')
                    count += 1
                    aula_count = 1
                old_model_title = model_title
                final_model = f'{count} - {model_title}'
                print(f'\t{final_model} | ', end='')
                aula_title = self.replacer(aula.find('div', {'class': 'col-xs-12 amarelo'}).find('h1', {'class': 'bold'}).getText().strip())
                final_aula = f'{aula_count} - {aula_title}'
                print(f'{final_aula} | ', end='') 
                tipo = aula.find('span', {'class': 'f10 cinza text-uppercase'}).getText().strip()
                path = f'{curso_nome}/{final_model}'
                local_path = self.criar_pastas_curso(path)
                if 'vídeo' in tipo:
                    video = aula.find('iframe')['src'].split('?')[0]
                    print(f'Conteúdo em video | {video}')
                    video_path = f'{local_path}/{final_aula}.pdf'
                    self.download_video(video, video_path)
                elif 'texto' in tipo:
                    print(f'Conteúdo em texto | PDF')
                    try:
                        file_url = aula.find('div', {'class': 'col-xs-12 text-justify'}).find('a')['href']
                    except:
                        continue
                    file_path = f'{local_path}/{final_aula}.pdf'
                    os.system(f'aria2c -o "{file_path}" {file_url} --quiet --continue=true')
    
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
            'Referer': 'https://desecsecurity.com/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            video = f'{video}/config'
            while True:
                try:
                    vimeo_config = requests.get(video, headers=vimeo_headers).json()
                    break
                except:
                    pass
            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']

            #os.system(f'''aria2c -i {vimeo_url} -nostats -loglevel 0 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "{video_path}"''')            
            os.popen(f'aria2c -o "{path}" {vimeo_url} --quiet --continue=true')


#Download().index()