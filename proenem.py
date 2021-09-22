import requests
import json
import os
from bs4 import BeautifulSoup as bs

proenem_session = requests.Session()

class Downloader():

    def index(self):
        
        proenem_session.headers['authority'] = 'api.prodigioeducacao.com'
        proenem_session.headers['x-brand'] = 'proenem'
        proenem_session.headers['authorization'] = 'Bearer'
        proenem_session.headers['x-context'] = 'course'
        proenem_session.headers['x-course'] = ''
        proenem_session.headers['content-type'] = 'application/json'
        proenem_session.headers['accept'] = 'application/json, text/plain, */*'
        proenem_session.headers ['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        proenem_session.headers['x-platform'] = 'web'
        proenem_session.headers['sec-gpc'] = '1'
        proenem_session.headers['origin'] = 'https] =//app.proenem.com.br'
        proenem_session.headers['sec-fetch-site'] = 'cross-site'
        proenem_session.headers['sec-fetch-mode'] = 'cors'
        proenem_session.headers['sec-fetch-dest'] = 'empty'
        proenem_session.headers['referer'] = 'https://app.proenem.com.br/'
        proenem_session.headers['accept-language'] = 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        
        os.system('cls')
        #email = input('email: ')
        ##password = input('password: ')
        
        #data = {"username":email,"password": password}

        #tokens = proenem_session.get('https://api.prodigioeducacao.com/v1/token', headers=headers, data=data)
        token = input('Bearer Token: ')
        #proenem_session.headers['authorization'] = 'Bearer ' + tokens.json()['token']
        proenem_session.headers['authorization'] = token

        lista = proenem_session.get('https://api.prodigioeducacao.com/v1/person/me').json()
        cursos = lista['courses']
        print(cursos)
        input()
        #self.get_courses(cursos)

    #def get_courses(self, cursos):
        
        for curso in cursos:
            curso_nome = self.replacer(curso['name'].strip())
            actual_path = self.mkdir(curso_nome)
            curso_slug = curso['slug']

            proenem_session.headers['x-course'] = curso_slug

            lesson_plan = proenem_session.get('https://api.prodigioeducacao.com/v1/student/lessonplan').json()

            lesson_modules = lesson_plan['modules']

            for lesson_module in lesson_modules:

                lesson_id = lesson_module['id']

                lesson_infos = proenem_session.get(f'https://api.prodigioeducacao.com/v1/student/lessonplanmodule/{lesson_id}').json()

                lesson_name = self.replacer(lesson_infos['name'].strip())
                lesson_events = lesson_infos['events']

                for lesson_event in lesson_events:
                    for ev_key, ev_val in lesson_event.items():
                        for hour, index in enumerate(ev_val, start=0):
                            if hour < 10:
                                hour = f'0{hour}'
                            for aula in index.values():
                                if len(aula) == 0:
                                    continue

                                year = ev_key[0:4]
                                month = ev_key[4:6]
                                day = ev_key[6:8]

                                for aulin in aula:

                                    aulin_title = self.replacer(aulin['title'].strip())
                                    
                                    try:
                                        ev_path = self.mkdir(f'{actual_path}/{lesson_name}/{day}.{month}.{year} - {hour} horas/{aulin["subject"]}/{aulin_title}')
                                    except:
                                        ev_path = self.mkdir(f'{actual_path}/{lesson_name}/{day}.{month}.{year} - {hour} horas/{aulin_title}')
                                            
                                    aulin_id = aulin['id']
                                    
                                    aulin_infos = proenem_session.get(f'https://api.prodigioeducacao.com/v1/lessonplanevent/{aulin_id}').json()

                                    try:
                                        for content in aulin_infos['contentPerType']:
                                            content_type = content['type']
                                            material_compl = content['title']
                                            if content_type == 'Material' or content_type == 'Apostila':
                                                for item in content['items']:
                                                    material = item['learningObject']['material']
                                                    material_title = self.replacer(material['title'].strip())
                                                    material_ext = material['fileName'].split('.')[-1]
                                                    material_link = material['url']
                                                    material_path = self.mkdir(f'{ev_path}/{material_compl}')
                                                    material_final = f"{material_path}/{material_title}.{material_ext}" 
                                                    os.system(f'aria2c -o "{material_final}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5 "{material_link}"')
                                                    print(material_final)

                                            elif content_type == 'Video':
                                                for video in content['items']:
                                                    video = video['learningObject']['video']
                                                    video_title = self.replacer(material['title'].strip())
                                                    video_link = video['url']
                                                    video_path = self.mkdir(f'{ev_path}/{material_compl}')
                                                    video_fin_com = f"{video_path}/{video_title}.mp4" 
                                                    if os.path.exists(video_fin_com):
                                                        continue
                                                    if 'vzaar' in video_link:
                                                        vzaar_id = video['videoKey']
                                                        vzaar_link = requests.get(f'https://playback.dacast.com/content/access?contentId={vzaar_id}&provider=vzaar').json()['mp4']
                                                        os.system(f'aria2c -o "{video_fin_com}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5 "{vzaar_link}"')
                                                    elif 'prodigio' in video_link:
                                                        os.system(f'ffmpeg -i "{video_link}" -preset ultrafast "{video_fin_com}" -nostats -loglevel 0')
                                                        continue
                                                    print(video_fin_com)
                                    except:
                                        pass

                                    video = aulin['video']
                                    if video == None:
                                        continue
                                    video_title = self.replacer(video['title'].strip())
                                    video_url = video['url']
                                    video_id = video['id']

                                    if video_url == None:
                                        if len(video['videoKey']) < 15:
                                            video_url = f'https://www.youtube.com/embed/{video["videoKey"]}'

                                    video_final = f'{ev_path}/{video_title}.mp4'
                                    
                                    if 'vzaar' in video_url:
                                        vzaar_id = video['videoKey']
                                        vzaar_link = requests.get(f'https://playback.dacast.com/content/access?contentId={vzaar_id}&provider=vzaar').json()['mp4']
                                        os.system(f'aria2c -o "{video_final}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5 "{vzaar_link}"')
                                        
                                    elif 'livestreamapis' in video_url:
                                        video_json = proenem_session.get(f'https://api.prodigioeducacao.com/v1/video/{video_id}').json()
                                        try:
                                            video_embed = video_json['videoEmbed']
                                        except:
                                            continue
                                            #print(video_json)
                                            #exit(0)                                        video_src = bs(video_embed, 'html.parser').find('iframe')['src']
                                        video_source = str(requests.get(video_src).text)
                                        video_json =  video_source.split('window.config = ')[1].split(';')[0]
                                        try:
                                            video_jsoned = json.loads(video_json)
                                        except:
                                            continue
                                        video_event= video_jsoned['event']
                                        video_feed = video_event['feed']
                                        video_data = video_feed['data'][0]['data']
                                        video_url = video_data['m3u8_url']
                                        os.system(f'ffmpeg -i "{video_url}" -preset ultrafast "{video_final}" -nostats -loglevel 0')
                                        pass
                                    elif 'youtube' in video_url:
                                        os.system(f'youtube-dl "{video_url}" -o "{video_final}" --quiet')
                                        pass

                                    print(video_final)

    def replacer(self, text):
        
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        
        return text   

    def mkdir(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)
        
        return path

#Downloader().index()