import requests
import urllib
import json
from bs4 import BeautifulSoup
import os

balta_session = requests.session()

class Downloader():

    def index(self):



        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'Content-Type': 'application/json',
            'Origin': 'https://app.balta.io',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://app.balta.io/',
            'Accept-Language': 'pt-BR,pt;q=0.9',
        }

        authenticate = '{"username":"33683075848","password":"fute123.p"}'
        test = balta_session.post('https://api.balta.io/v1/accounts/authenticate', headers=headers, data=authenticate).json()
        print(test)
        self.token = test['data']['token']
        headers={'Accept':'application/json, text/plain, */*','Referer':f'https://app.balta.io/courses/','DNT':'1','x-access-token':f'{self.token}','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',}
        balta_json = json.loads(balta_session.post('https://api.balta.io/portal/courses', headers=headers).text)
        self.get_course(balta_json)

    def get_course(self, cursos):
        
        while True:
            for curso in cursos:
                title = self.replacer(curso['title'])
                curso_id = curso['tag']
                try:
                    career = curso['career']
                except:
                    career = ''
                
                if career == '':
                    path = f'Sem Carreiras/{title}'
                    if os.path.exists(path) is False:
                        os.makedirs(path)
                else:
                    path = f'Carreiras/{career}/{title}'
                    if os.path.exists(path) is False:
                        os.makedirs(path)
                headers={'Accept':'application/json, text/plain, */*','Referer':f'https://app.balta.io/courses/{curso_id}','DNT':'1','x-access-token':f'{self.token}','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',}
                curso = json.loads(balta_session.get(f'https://api.balta.io/portal/courses/{curso_id}', headers=headers).text)
                print(title)
                modules = curso['modules']
                for modulo in modules:
                    title = self.replacer(modulo['title'])
                    print(f'\t{title}')
                    model_order = modulo['order']
                    video = modulo['classes']
                    model_path = f'{path}/{model_order} - {title}'
                    
                    if os.path.exists(model_path) is False:
                        os.makedirs(model_path)
                    for video in modulo['classes']:
                        video_order = video['order']
                        title = self.replacer(video['title'])
                        aula_nome = f'{video_order} - {title}.mp4'
                        aula_path = f'{model_path}/{aula_nome}'


                        print(f'\t\t{title}')
                        if  os.path.exists(aula_path) is False:
                            video_url = video['contentUrl']
                            headers = {
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                                'DNT': '1',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                'Sec-Fetch-Site': 'cross-site',
                                'Sec-Fetch-Mode': 'nested-navigate',
                                'Referer': 'https://app.balta.io/player/',
                                'Accept-Encoding': 'gzip, deflate, br',
                                'Accept-Language': 'pt-BR,pt;q=0.9,en-CA;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5,en-US;q=0.4',
                            }
                            vimeo_video = requests.get(f'https://player.vimeo.com/video/{video_url}/config', headers=headers).json()

                            try:
                                vimeo_download = sorted(vimeo_video["request"]["files"]["progressive"], key = lambda i:i['height'])
                            except:
                                print(vimeo_video)
                            
                            vimeo_url = vimeo_download[-1]['url']

                            #print(video_url, aula_path)
                            
                            os.system(f'aria2c -o "{aula_path}" {vimeo_url} --quiet')
                            #urllib.request.urlretrieve(vimeo_url, filename=f'{aula_path}')
            break
                            
    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

#bot = Downloader()
#bot.index()
