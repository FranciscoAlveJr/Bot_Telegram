import requests
import json
import os
from bs4 import BeautifulSoup as bs

filonared_session = requests.Session()

class Downloader:
    
    def index(self):
        
        os.system('cls' if os.name == 'nt' else 'clear')  

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://filonared.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        filonared_session.headers.update(headers)

        filonared_session.cookies['ARRAffinity'] = '591ed1fee6ab8fb25ff35e10dac6ab0d4ca39eee3db8cda47825597776a0fb41'
        filonared_session.cookies['.AspNetCore.Antiforgery.w5W7x28NAIs'] = 'CfDJ8Ajw88oTTK1GtuPVx2nFHBIRIzhEUZZwJxtd12_EqZhIjT4oIvSskBrpIXtL5x5zg3ErLuj6ekSfUoX1WwQnRd2CZaJiXjsemn8sz0qxQlPjYFl0dXG7dBXdO2jEvKMsUm2hRRd2DStAY6JVoFs8onU'
        filonared_session.cookies['.AspNetCore.Identity.Application'] = input('Coloque o Cookie Identity: ')
        #CfDJ8Ajw88oTTK1GtuPVx2nFHBLvZOjafT5RO0rI8OCfP5B2bjoh_SlUQqY0AjwUYpFuEdleHM22dxwiBdHaxBVtQ9dIcFFOcUmfUoLAKamo0pBQetO00cjErzdUn2KJuW0wUBCUhpNggN4olCdvxxRfN3_NMtko3Cef2YKSmwNAT8oFzmmR-LvP9hBaUC-vrURRsY09Fsb6A-6HJWKuaQuakPOx42vWlZtUWTrgcIABLsom-mmeXFKk4EbZH-A0Hm4kX90yckQ47YXhKRv9BpGWegClQXGtZjKEynUGwKGARM9RQJNsZMd9ulH3kt46-PQYs9mb-mBrdC55A-iV2S5Wc26IBN_Q3g-XHBwhrVn51HKq_4CLbEWLI_Hlf4a-_9gzK_Mq83F8C7lfZ_--aXilH6XpDVzzEbqjLrELOn3DxZg6DwUFOoQhbeNWcuK-UWHWZ5MurMydIA5nzHAw8R960FAJl0UDP5jaPtwibZTpPlWlMImgnxSKoUW0gww1tqfpI6XNT_fqfUu4vvcmR4btJ_hmIuIohKEeekiTfLHoQkV_NE0srWNJda7oCiyE_JPC1gLFfK4pv0c34f-BNYTwSFkfVqOzT7xUgrx7SygVG3FCzCuXTbhW21fFJisYOowvA5kqhU_prmYkPf6CXdrOKFkU4jBPreGOV_9dQLst6YlANqbH1wOHR7DAa2ssRs8cZC1WNlH3ltIjKYdzW8WFjTF3MHDx4-kplQsEtYkZaXyYZtkXzyBcOfydYmVY9gqFhi0Eizh933xY2m6tu5nQL6ZE5WaHdjCxIKInt3vCf7UXUrCnsV6INoSavxOt72EOkim7orFjp2xJW5ZvguAQ_WbyYVZDmHBFx7nt3zWks_1tQZxWQejLg6RugpMjuXmpRfNSbLg0E6IOf-KeEAA60_y2nfP_5efO0Lcl4CybHI8zvjBlGRqpU5Qp3Rd1cWk4e-qzlm9jR85agO-J_6LF1V56c4WDK9GAjA7KSP64BndU34YSiJ9tS5M0_oARjcqdtOYZAOGG7ODipvE6sx7c26dfV2Nqst06KnOCOlyImB87gaLlISE1AMrH24Vl9-RcgA
        os.system('cls' if os.name == 'nt' else 'clear')  

        self.get_info()

    def get_info(self):

        response = bs(filonared_session.get('https://filonared.com.br/admin').content, 'html.parser')
        sidebar_nav = response.find('ul', {'id': 'sidebarnav'})
        
        for li in sidebar_nav:
            try:
                span = li.find('span').getText().strip()
                pass
            except:
                continue
            if span == 'Cursos':
                disciplines = li.find('ul').find_all('li')
                print('Obtained "Cursos" list')
            if 'Temas' in span:
                themes = li.find('ul').find_all('li')
                print('Obtained "Temas de Redação" list')
                break
        print('\n# ', end='')
        print('-' * 30, end=' #')
        print()
        self.get_discipline(disciplines)
        self.get_themes(themes)

    def get_discipline(self, disciplines):

        for discipline in disciplines:
            link = discipline.find('a')['href'] #/Curso/5/Atualidades #https://filonared.com.br/Curso/5/Atualidades
            course = filonared_session.get(f'https://filonared.com.br{link}')
            course_parser = bs(course.content, 'html.parser')
            self.course_title = self.replacer(course_parser.find('h1', {'id': 'TituloView'}).getText()).strip()
            videos = course_parser.find('div', class_='card-deck').find_all('div')
            links = []
            for video in videos:
                try:
                    video_link = video.find('a')['href']
                    links.append(video_link)
                except:
                    #print(f'Link não encontrado: {video.getText()}')
                    break
            #exit(0)
            links = list(dict.fromkeys(links))
            for link in links:
                video = filonared_session.get(f'https://filonared.com.br{link}')
                video_parser = bs(video.content, 'html.parser')
                self.class_title = self.replacer(video_parser.find('h1', {'id': 'TituloView'}).getText()).strip()
                try:
                    vimeo = video_parser.find('iframe')['src']
                except:
                    #print(f'Not released')
                    continue
                vimeo_config = vimeo + '/config'
            
                local_path = self.create_path(f'{self.course_title}/{self.class_title}')
                path = f'{local_path}/{self.class_title}.mp4'
                print(f'Downloading video {self.class_title}: ', end='')
                self.video_download(path, vimeo_config)
                self.get_exercises(video_parser)
                self.get_files(video_parser, local_path)
    
    def get_exercises(self, html):

        exercises = html.find('div', class_='hideFormClass').find_all('a')
        #print('Pegando Exercicios')
        for exercise in exercises:
            try:
                link = exercise['href']
            except:
                continue
            if 'javascript' in link:
                continue
            video = filonared_session.get(f'https://filonared.com.br{link}')
            video_parser = bs(video.content, 'html.parser')
            ex_class_title = self.replacer(video_parser.find('h1', {'id': 'TituloView'}).getText()).strip()
            try:
                vimeo = video_parser.find('iframe')['src']
            except:
                #print(f'Not released')
                continue
            vimeo_config = vimeo + '/config'
            local_path = self.create_path(f'{self.course_title}/{self.class_title}/Exercicios/{ex_class_title}')
            path = f'{local_path}/{ex_class_title}.mp4'
            print(f'\tDownloading Video Exercise {ex_class_title}: ', end='')
            self.video_download(path, vimeo_config)
            print(f'\tDownloading File Exercise {ex_class_title}: ', end='')
            self.get_files(video_parser, local_path)

    def get_files(self, html, path):

        files = html.find('div', class_='tab-content').find_all('div')
        checker = []
        for afile in files:
            try:
                link = afile.find('a')['href']
            except:
                continue
            name_file = self.replacer(afile.find('a').getText().strip())
            checker.append(name_file)
            checker = list(dict.fromkeys(name_file))
            
            path_file = self.create_path(f'{path}/Arquivos')
            local_path = f'{path_file}/{name_file}.pdf'
            
            if os.path.exists(local_path) is False:
                os.system(f'aria2c -o "{local_path}" "{link}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5')
                print(f'\t{name_file}')
            else:
                print('')

    def create_path(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)
        return path

    def video_download(self, path, video):

        if os.path.exists(path) is False:
            vimeo_headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://filonared.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }

            check = True
            tent = 0
            while check:
                if tent == 10:
                    check == False
                    break
                try:
                    vimeo_config = requests.get(video, headers=vimeo_headers).json()
                    check = False
                    break
                except:
                    tent += 1
                    #print(f'Falha ao pegar link {video}, tentando novamente!')
                    continue
            try:
                vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
                vimeo_url = vimeo_download[-1]['url']

                os.system(f'aria2c -o "{path}" "{vimeo_url}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5')
         
                print(f'{self.class_title} at {self.course_title}')
            except:
                pass
        else:
            print('')
    
    def get_themes(self, themes):

        for theme in themes:
            link = theme.find('a')['href'] #/Curso/5/Atualidades #https://filonared.com.br/Curso/5/Atualidades
            course = filonared_session.get(f'https://filonared.com.br{link}')
            course_parser = bs(course.content, 'html.parser')
            self.course_title = self.replacer(course_parser.find('h1', {'id': 'TituloView'}).getText()).strip()
            videos = course_parser.find('div', class_='card-deck').find_all('div')
            links = []
            for video in videos:
                try:
                    video_link = video.find('a')['href']
                    links.append(video_link)
                except:
                    #print(f'Link não encontrado: {video.getText()}')
                    break
            #exit(0)
            links = list(dict.fromkeys(links))
            for link in links:
                video = filonared_session.get(f'https://filonared.com.br{link}')
                video_parser = bs(video.content, 'html.parser')
                self.class_title = self.replacer(video_parser.find('h1', {'id': 'TituloView'}).getText()).strip()
                contents = video_parser.find('div', {'id': 'TemaContent'}).find_all('div', class_='row')
                tabs = video_parser.find('div', class_='col-xl-12').find('div', class_='card-header').find_all('li')
                for tab in tabs:
                    tab_text = tab.getText().strip()
                    #print(tab_text)
                    for content in contents:
                        try:
                            video_id = content.find('iframe')['src'].split('/')[-1]
                        except:
                            continue
                        vimeo_config = 'https://player.vimeo.com/video/' + video_id + '/config'
                        #print(vimeo_config)
                        path = f'Temas de Redação/{self.course_title}/{self.class_title}/'
                        path_file = self.create_path(path)
                        local_path = f'{path_file}/{tab_text}.mp4'
                        print(f'Downloading Theme {tab_text}')
                        self.video_download(local_path, vimeo_config)
                        find_files = content.find_all('a')
                        for found in find_files:
                            try:
                                link = found['href']
                            except:
                                continue
                            if 'pdf' not in link:
                                continue
                            text = self.replacer(found.getText().strip())
                            path = f'Temas de Redação/{self.course_title}/{self.class_title}/{tab_text}'
                            path_file = self.create_path(path)
                            local_path = f'{path_file}/{text}.pdf'
                            os.system(f'aria2c -o "{local_path}" "{link}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5')

                            
                            


    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

#Downloader().index()