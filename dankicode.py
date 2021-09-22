import requests
import json
import urllib
from bs4 import BeautifulSoup as bs
import os
from datetime import datetime
import time

#import gdown



start = datetime.now()
dankicode_session = requests.Session()
vimeo_session = requests.Session()
google_session = requests.Session()

vimeo_session.headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'nested-navigate',
    'Referer': 'https://cursos.dankicode.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-CA;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5,en-US;q=0.4',
}

error_dict = {}

class Downloader():

    def index(self):
        counter = 0
        email = 'ocoisa081@gmail.com'
        senha = '18020301.pP'

        data = {'email': email, 'senha': senha, 'acao': ''}
        os.system('cls')
        print('DankiCode Scrapy')
        headers = {'Connection':'keep-alive','Accept':'application/json, text/javascript, */*; q=0.01','Origin':'https://cursos.dankicode.com','X-Requested-With':'XMLHttpRequest','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36','DNT':'1','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Referer':'https://cursos.dankicode.com/','Accept-Encoding':'gzip, deflate, br','Accept-Language':'pt-BR,pt;q=0.9,en-CA;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5,en-US;q=0.4',}
        url = 'https://cursos.dankicode.com/ajax/logar.php'
        dankicode_post = dankicode_session.post(url, headers=headers, data=data)
        dankicode_cookies = dankicode_post.cookies.get_dict()
        dankicode_session.headers = {
            'authority': 'cursos.dankicode.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'origin': 'https://cursos.dankicode.com',
            'x-requested-with': 'XMLHttpRequest',
            'sec-fetch-dest': 'empty',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://cursos.dankicode.com/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'__cfduid={dankicode_cookies["__cfduid"]}; PHPSESSID={dankicode_cookies["PHPSESSID"]}',
        }
        #'cookie': f'__cfduid={dankicode_cookies["__cfduid"]}; PHPSESSID={dankicode_cookies["PHPSESSID"]}',

        dankicode_campus = dankicode_session.get('https://cursos.dankicode.com/campus').text
        dankicode_infos =  bs(dankicode_campus, 'html.parser')
        dankicode_vitrine = dankicode_infos.find('section', class_='vitrine')
        dankicode_courses = dankicode_vitrine.find_all('div', class_='box-curso-single')

        for co, curso in enumerate(dankicode_courses, start=1):
            dankicode_curso_title = curso.find('div', class_='nome-curso').getText().strip()
            print(f'{co} - {dankicode_curso_title}')
        test = int(input('Numero: '))-1

        for curso in dankicode_courses[test:]:
            dankicode_curso_title = curso.find('div', class_='nome-curso').getText().strip()
            print(f'\t{dankicode_curso_title}')
            dankicode_curso_link = curso.find('a').get('href').split('?last')[0]
            dankicode_curso = dankicode_session.get(dankicode_curso_link).content
            dankicode_curso_infos = bs(dankicode_curso, 'html.parser')
            dankicode_modulos = dankicode_curso_infos.find_all('div', class_='modulo-single')
            for m_count, modulo in enumerate(dankicode_modulos):
                m_count += 1
                module_name = self.replacer(modulo.find('h2').getText()).strip()
                aula_path_folder =  f'{dankicode_curso_title}/{m_count} - {module_name}'
                if os.path.exists(aula_path_folder) is False:
                    os.makedirs(aula_path_folder)

                print(f'\t\t{m_count} - {module_name}')
                aulas_list = modulo.find_all('div', {'class': 'aulas-modulo-lista'})
                
                for aula_t in aulas_list:
                    aulas = aula_t.find_all('a')
                    for aula_count, aula in enumerate(aulas):
                        aula_count += 1
                        aula_title = self.replacer(aula.getText()).strip()
                        aula_path = f'{aula_path_folder}/{aula_count} - {aula_title}'
                        if os.path.exists(aula_path_folder) is False:
                            os.makedirs(aula_path_folder)
                        aula_link = aula.get('href')
                        if aula_link == "javascript:void(0)":
                            print(f'\t\t\t[Nao disponivel] - {aula_count} - {aula_title}')
                            continue
                        aula_get = dankicode_session.get(aula_link)
                        aula_info = bs(aula_get.text, 'html.parser')


                        try:
                            download_url = aula_info.find('a', {'class': 'btn-download', 'target': '_blank'}).get('href')
                            arquivos = f'{aula_path}/Arquivos/'
                            if os.path.exists(arquivos) is False:                                os.makedirs(arquivos)
                            path_size = os.path.getsize(arquivos)
                            if path_size == 0:    
                           
                                
                                download_file = download_url.replace('open?id=', 'uc?id=')
                                file_id = download_file.split('id=')[-1]
                                #filename = bs(google_session.get(f'https://drive.google.com/file/d/{file_id}/view').content, 'html.parser')
                                #teste_one = filename.find('body')
                                #teste_two = teste_one.find('meta', {'itemprop': 'name'})
                                #content_x = teste_two['content']

                                arquivo_link = f'https://drive.google.com/u/0/uc?id={file_id}&export=download'
                                #

                                handle = os.system(f'aria2c -d "{arquivos}" "{arquivo_link}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5')
                                
                            else:
                                handle = 0
                                
                            if handle == 0:
                                print(f'\t\t\t{aula_count} - {aula_title} - {handle} - Arquivo')
                            else:
                                print(f'\t\t\tArquivo Nao baixo - {aula_count} - {aula_title} - {handle} - {arquivo_link}')
                                error_dict[arquivos] = arquivo_link
                                #

                            
                        except:
                            pass
                        try:
                            aula_video = aula_info.find('iframe').get('src')
                        except:
                            continue
                        try:
                            video_final_path = f'{aula_path}/{aula_count} - {aula_title}.mp4'
                            if os.path.exists(video_final_path) is False or os.path.getsize(video_final_path) == 0:  #is False
                                vimeo_video = vimeo_session.get(f'{aula_video}/config').json()
                                vimeo_download = sorted(vimeo_video["request"]["files"]["progressive"], key = lambda i:i['height'])
                                vimeo_url = vimeo_download[-1]['url']   

                                handle = os.system(f'aria2c -o "{video_final_path}" "{vimeo_url}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5')


                                if handle == 0:
                                    print(f'\t\t\t[DOWNLOADED] - {aula_path}')
                                else:
                                    print(f'\t\t\t[NOT DOWNLOADED | [ERROR: {handle}] - {aula_path}')
                            else:
                                print(f'\t\t\t[ALREADY DOWNLOADED] - {aula_path}')
                        except:
                            pass
                        
    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text


#bot = Downloader()

#bot.index(data)
stop = datetime.now()
"""print(f'Horário de  Inicio: {str(start)[11:-7]}')
print(f'Horário de  Término : {str(stop)[11:-7]}')
print('ABAIXO OS ARQUIVOS NÃO BAIXADOS')
print(error_dict)"""
with open('Error.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(error_dict))
