import requests
import urllib
import json
import os
from bs4 import BeautifulSoup as bs

b7_session = requests.Session()

class Downloader():

    def index(self):   


        cookies = {
            '__zlcmid': '10njWsF63pMVwX4',
            '_fbp': 'fb.2.1603399594189.1477464965',
        }

        headers = {
            'Host': 'alunos.b7web.com.br',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Content-Type': 'application/json',
            'Origin': 'https://alunos.b7web.com.br',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://alunos.b7web.com.br/login',
            'Accept-Language': 'pt-BR,pt;q=0.9',
        }
        user = 'ocoisa081@gmail.com'
        password = '18020301.pP'
        data = f'*"email":"{user}","password":"{password}"#'
        data = data.replace('*', '{').replace('#', '}')
        response = b7_session.post('https://alunos.b7web.com.br/api/login', headers=headers, cookies=cookies, data=data)

        cookies['token'] = response.json()['token']
        
        b7web_text = b7_session.get('https://alunos.b7web.com.br/meus-cursos', headers=headers, cookies=cookies).content

        b7web_soup = bs(b7web_text, 'html.parser')
        b7web_script = json.loads(str(b7web_soup.find('script', {'id': '__NEXT_DATA__'})).split('</scr')[0].split('>')[1])

        #b7web_script = json.loads(open('files.json', 'r', encoding='utf8').read())
        self.get_courses(b7web_script)

    def get_courses(self, b7web_json):
        b7web_courses = b7web_json['props']['pageProps']['data']['myCourses']
        status = ['active', 'free']
        while True:
            for curso in b7web_courses:
                os.system('cls')
                curso_nome = self.replacer(curso['course']['name'])
                if curso['course']['status'] == 'old' or 'Do Zero Ao Profissional' in curso_nome:
                    maincategory = 'Do Zero Ao Profissional' 
                    print(f'O {curso_nome} será baixado na pasta {maincategory}')               
                elif curso['course']['status'] in status:
                    maincategory = "FullStack"
                    print(f'O {curso_nome} será baixado na pasta {maincategory}')
                elif curso['course']['status'] == 'soon':
                    print(f'O {curso_nome} ainda não foi lançado.')
                    continue                   
        
                path = f'{maincategory}/{curso_nome}'
                if os.path.exists(path) is False:
                    os.makedirs(path)
                curso_slug = curso['course']['slug']
                curso_modulos = curso['course']['modules']
                self.get_model(curso_modulos, path, curso_slug, curso_nome)

    def get_model(self, modules, path, curso_slug, curso_nome):
        for module in modules:
            module_name =  self.replacer(str(module['name']).strip())
            module_order = module['order']
            module_final_name = self.replacer(f'{module_order} - {module_name}').strip()    
            module_lessons = module['lessons']
            print(f'\tBaixando modulo {module_name}')
            for lesson in module_lessons:
                if lesson['videocode'] == 'None' or lesson['videocode'] == None or int(len(lesson['videocode']) < 8):
                    continue
                lesson_name =  self.replacer(str(lesson['name']).strip())
                if lesson_name == 'ESTOU ADICIONANDO O RESTANTE DAS AULAS':
                    continue
                lesson_order = lesson['order']
                lesson_slug = lesson['slug']
                lesson_final_name = self.replacer(f'{lesson_order} - {lesson_name}').strip()
                lesson_video = f'''http://player.vimeo.com/video/{lesson['videocode']}/config'''
                lesson_file = lesson['files']
                lesson_path = f'{path}/{module_final_name}'
                class_path = f'{lesson_path}/{lesson_final_name}'
                slug = f'{curso_slug}/{lesson_slug}'
                
                if os.path.exists(lesson_path) is False:
                    os.makedirs(lesson_path)
                #phase = f'A baixar {curso_nome} / {module_name} / {lesson_name}'
                if os.path.exists(f'{class_path}.mp4') is False:
                    self.video_download(lesson_video, class_path, slug)
                print(f'\t\tBaixando {lesson_name}')
                
                if len(lesson_file) > 0:
                    self.files_download(lesson_file, lesson_path, lesson_final_name)
                    

    def video_download(self, lesson_video, path, slug):
        headers = {'Referer': 'https://alunos.b7web.com.br/'}
        print(lesson_video)
        vimeo_video = requests.get(lesson_video, headers=headers).json()
        vimeo_download = sorted(vimeo_video["request"]["files"]["progressive"], key = lambda i:i['height'])
        vimeo_url = vimeo_download[-1]['url']
        
        if os.path.exists(f'{path}.mp4') is False:
            #os.system(f'''ffmpeg -i {vimeo_url} -loglevel quiet -stats "{path}.mp4"''')
            os.system(f'aria2c -o "{path}.mp4" "{vimeo_url}" --quiet --continue=true')

    def files_download(self, files, lesson_path, lesson_final_name):
        
        for archive in files:
            try:
                file_name = archive['name']
                file_name2 = archive['filename']
                file_ext = file_name2.split('.')[-1]
                #efile_final = f'{file_name} - {file_name2}'
                file_path = f'{lesson_path}\Arquivos'
                if os.path.exists(file_path) is False:
                    os.mkdir(file_path)
                file_save = f'{file_path}/{lesson_final_name}.{file_ext}'
                file_link = f'''https://alunos.b7web.com.br/media/files/{archive['filename']}'''
                if os.path.exists(file_save) is False:
                    #urllib.request.urlretrieve(file_link, filename=file_save)
                    os.system(f'aria2c -o "{file_save}" "{file_link}"')
                    print(f'\t\t\tBaixando {file_save}')
            except:
                pass

    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

#bot = Downloader()
#bot.index()
