import requests
import json
import os
from bs4 import BeautifulSoup as bs
import random
import time
import base64
import m3u8

treinaweb_sessions = requests.Session()




class Downloader():

    def index(self):

        escolha = input('Qual plataforma voce deseja baixar?\n1 - TreinaWeb\n2 - AvMakers\n3 - Freelae\nResposta: ')
 
        n = [1, 2, 3]

        if escolha.isdigit():
            escolha = int(escolha)
            if  escolha in n:
                if escolha == 1:
                    self.main = 'treinaweb' 
                elif escolha == 2:
                    self.main = 'avmakers'
                elif escolha == 3:
                    self.main = 'freelae'
            else:
                print('Erro. Saindo.')
                exit(0)
        
        self.headers = {
            'authority': f'www.{self.main}.com.br',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'origin': f'https://www.{self.main}.com.br',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': f'https://www.{self.main}.com.br/login',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        cookie_jar = treinaweb_sessions.get(f'https://www.{self.main}.com.br/login', headers=self.headers).cookies.get_dict()[f'{self.main}-site']

        #self.headers['cookie'] = f"treinaweb-site={cookie_jar}; path=/; secure; httponly; samesite=lax"

        #self.cookies = {"treinaweb-site": cookie_jar}

        user = 'ocoisa081@gmail.com'
        pswd = '18020301.pP'

        data = {
            'username': user,
            'password': pswd
        }

        treinaweb_sessions.post(f'https://www.{self.main}.com.br/login', headers=self.headers, data=data)
        infos = treinaweb_sessions.get(f'https://www.{self.main}.com.br/api/painel/v1/aluno', headers=self.headers)
        self.headers['cookie'] = f"{self.main}-site={infos.cookies.get_dict()[f'{self.main}-site']}; path=/; secure; httponly; samesite=lax"
        #print(teste.headers)
        #
        
        self.quest()

    def quest(self):

        escolha = input(f'Escolha uma das funções abaixo\n1 - Baixar Cursos\n2 - Baixar Formações\n3 - Informações\n4 - Sair\nResposta: ')
        
        n = [1, 2, 3]

        if escolha.isdigit():
            escolha = int(escolha)
            if  escolha in n:
                if escolha == 1:
                    self.get_cursos()
                elif escolha == 2:
                    self.get_formacao()
                elif escolha == 3:
                    self.infos()
            else:
                print('Erro. Saindo.')
                exit(0)

    def get_cursos(self):


        #downloaded_read = json.loads(open('downloaded.json', 'r', encoding='utf-8').read())
        #downloaded_write = open('downloaded.json', 'w', encoding='utf-8')
        infos = treinaweb_sessions.get(f'https://www.{self.main}.com.br/api/painel/v1/cursos', headers=self.headers).json()
        categorias = {}
        try:
            cats = infos['meta']['categorias']['data']
        
            for cat in cats:
                categorias[cat['id']] = cat['nome']
        except:
            categorias = {
                1: 'Freelae',
                2: 'Bonus',
                3: 'Bonus',
                4: 'Bonus',
            }



        cursos = infos['data']
        for index, curso in enumerate(cursos, start=1):
            categoria = curso['categorias']
            if len(categoria) > 1:
                random_num = random.choice(categoria)
                self.categoria = categorias[random_num]
            else:
                self.categoria = categorias[categoria[0]]
            self.curso_nome = self.replacer(curso['nome'])
            print(f'{index} - {self.curso_nome}')
        print(f'{index+1} - Baixar todos')
        escolha = input('Qual curso vc quer baixar?\nR: ')

        if escolha.isdigit():
            escolha = int(escolha)
            if escolha < index + 1 :
                curso = cursos[escolha-1]
                self.get_course_here(curso)
            elif escolha == index + 1 :
                for index, curso in enumerate(cursos, start=1):
                    categoria = curso['categorias']
                    if len(categoria) > 1:
                        random_num = random.choice(categoria)
                        self.categoria = categorias[random_num]
                    else:
                        self.categoria = categorias[categoria[0]]
                    self.curso_nome = self.replacer(curso['nome'])
                    self.get_course_here(curso)
        else:
            print('Erro. Saindo.')
            exit(0)

            #downloaded_read.append(self.curso_nome)
            
            #if self.curso_nome in downloaded_read:
                #continue


            #tipos
            #1: Cursos
            #2: Direto ao ponto
        
    def get_course_here(self, curso):
    
        if curso['tipo'] == 1:
            self.tipo = 'Cursos'
            a = self.return_self(curso['links'])
            au = a['data']
            aul =au['aulas']
            aulas = aul['data']
        elif curso['tipo'] == 2:
            self.tipo = 'Direto ao Ponto'
            a = self.return_self(curso['links'])
            au = a['data']
            aul =au['aulas']
            aulas = aul['data']
        elif curso['tipo'] == 3:
            self.tipo = 'Projeto Prático'
            a = self.return_self(curso['links'])
            au = a['data']
            aul =au['aulas']
            aulas = aul['data']
        else:
            print(curso)
        
        for aula in aulas:
            modulo = self.replacer(aula['titulo'])
            
            modulo_count = aula['ordem']
            self.final_modulo = f'{modulo_count} - {modulo}'
            sub_aulas = aula['subaulas']['data']
            for sub_aula in sub_aulas:
                aula_t = self.replacer(sub_aula['titulo'])
                aula_count = sub_aula['ordem']
                self.final_aula = f'{aula_count} - {aula_t}'
                tipo = sub_aula['tipo']
                print(f'{self.categoria} | {self.curso_nome} | {self.final_modulo} | {self.final_aula} | ', end='')
                path = self.create_path(f'{self.main.capitalize()}/{self.tipo}/{self.categoria}/{self.curso_nome}/{self.final_modulo}')
                if tipo == 3:
                    print("Questionario")
                    continue
                elif tipo == 1:
                    print("Apostila")
                    self.aula_path = f'{path}/{self.final_aula}.html'
                    apostilas = self.get_apostilas(sub_aula['links'][0]['uri'])




                    css = 'body {margin: 50px 150px 50px 150px; text-align: justify} .HtmlContentRenderer_text-content-style__2TWCB {background-color: #fff font-size: 16px; font-weight: 400; color: #707070; word-break: break-word}'

                    html = f"<html lang='pt-br' data-product='treinaweb'><head><meta charset='utf-8'><style>{css}</style></head><body><h1>{self.final_aula}</h1><br><div class='HtmlContentRenderer_text'>{apostilas}</div></body></html>"

                    with open(self.aula_path, 'w', encoding='utf-8') as out:
                        out.write(html)

                    continue
                elif tipo == 2:
                    self.aula_path = f'{path}/{self.final_aula}.mp4'
                    if os.path.exists(self.aula_path):
                        continue
                    print('Video')
                    videos = self.get_video(sub_aula['links'][0]['uri'])
                    if videos['url_anexo'] != None:
                        ext = videos['url_anexo'].split('?')[0].split('.')[-1]
                        os.system(f'aria2c -o "{path}/{self.final_aula}.{ext}" "{videos["url_anexo"]}" --quiet --continue=true')
                        pass
                    
                        
                    url = videos['url']
                    encoded = str(bs(treinaweb_sessions.get(url, headers=self.headers).content, 'html.parser').find('head').find('script', {'type': 'text/javascript'}))
                    encoded = encoded.split("';")[0]
                    encoded = encoded.split("= '")[1]
                    data = json.loads(base64.b64decode(encoded))
                    signatures = data["signatures"]
                    
                    m3u8_signatures = signatures['m']
                    key_signatures = signatures['k']
                    ts_signatures = signatures['t']

                    #all_signatures = [m3u8_signatures, key_signatures, ts_signatures]
                    s3_user_hash = data["s3_user_hash"]
                    s3_video_hash =  data["s3_video_hash"]
                    sessionID = data["sessionID"]

                    master_m3u8_name = 'index.m3u8'
                    
                    self.get_m3u8(master_m3u8_name, m3u8_signatures, s3_user_hash, s3_video_hash, sessionID)

                    master_content = open(f"tmp/{master_m3u8_name}", 'r').read()
                    master_m3u8 = m3u8.loads(master_content)
                    self.set_master(master_m3u8)
                    master_content = open(f"tmp/{master_m3u8_name}", 'w')
                    master_dumps = master_m3u8.dumps()

                    
                    with master_content as master_output:
                        master_output.write(master_dumps)
                    max_resolution = master_m3u8.playlists.__dict__['uri']

                    self.get_m3u8(max_resolution, m3u8_signatures, s3_user_hash, s3_video_hash, sessionID)
                    video_1080_content = open(f'tmp/{max_resolution}', 'r').read()
                    video_1080_m3u8 = m3u8.loads(video_1080_content)
                    video_1080_content = open(f'tmp/{max_resolution}', 'w')
                    video_dumps = video_1080_m3u8.dumps()
                    with video_1080_content as video_output:
                        video_output.write(video_dumps)
                    video_segments = video_1080_m3u8.data['segments']
                    
                    key_type = max_resolution.replace('m3u8', 'key')
                    self.get_key(key_type, key_signatures, s3_user_hash, s3_video_hash, sessionID)
                    self.get_ts(video_segments, ts_signatures, s3_user_hash, s3_video_hash, sessionID)
                    
                    if os.path.exists(self.aula_path) is False:
                        os.system(f'ffmpeg -allowed_extensions ALL -i "tmp/index.m3u8" "{self.aula_path}" -preset ultrafast -nostats -loglevel 0')
                    try:
                        os.system('del /q tmp')
                    except:
                        pass
                    try:
                        os.system('rmdir /q /s tmp')
                    except:
                        pass
                    continue
                elif tipo == 4:
                    print(sub_aula)
                    exit(0)
                #tipos
                #1 = apostila
                #2 = video
                #3 = questionario
                #4 = ??
                time.sleep(1)

        #with downloaded_write as output:
            #output.write(json.dumps(downloaded_read))


    def get_key(self, tipo, signatures, s3_user_hash, s3_video_hash, sessionID):

        path = f'tmp'
        
        cfp = signatures['CloudFront-Policy']
        cfs = signatures['CloudFront-Signature']
        kpid = signatures['CloudFront-Key-Pair-Id']

        url = f'https://hls2.videos.sproutvideo.com/{s3_user_hash}/{s3_video_hash}/video/{tipo}?Policy={cfp}&Signature={cfs}&Key-Pair-Id={kpid}&sessionID={sessionID}'

        os.system(f'aria2c -o "{path}/{tipo}" "{url}" --quiet --continue=true')


    def set_master(self, master):
        
        for x in master.playlists:
            if '1080.m3u8' in x.__dict__['uri']:
                master.playlists = x
                break
            elif '720.m3u8' in x.__dict__['uri']:
                master.playlists = x
            else:
                master.playlists = x


    def get_m3u8(self, tipo, signatures, s3_user_hash, s3_video_hash, sessionID):


        path = 'tmp'

        if os.path.exists(path) is False:
            os.makedirs(path)

        cfp = signatures['CloudFront-Policy']
        cfs = signatures['CloudFront-Signature']
        kpid = signatures['CloudFront-Key-Pair-Id']

        m3u8_file = f'https://hls2.videos.sproutvideo.com/{s3_user_hash}/{s3_video_hash}/video/{tipo}?Policy={cfp}&Signature={cfs}&Key-Pair-Id={kpid}&sessionID={sessionID}'


        os.system(f'aria2c -o "{path}/{tipo}" "{m3u8_file}" --quiet --continue=true')
    
    
    def get_ts(self, segments, signatures, s3_user_hash, s3_video_hash, sessionID):
        

        cfp = signatures['CloudFront-Policy']
        cfs = signatures['CloudFront-Signature']
        kpid = signatures['CloudFront-Key-Pair-Id']

        path = 'tmp'

        for segment in segments:
            url = segment['uri']
            segment_link = f'https://hls2.videos.sproutvideo.com/{s3_user_hash}/{s3_video_hash}/video/{url}?Policy={cfp}&Signature={cfs}&Key-Pair-Id={kpid}&sessionID={sessionID}'
            filename = url
            ts_path = f'{path}/{filename}'
            if os.path.exists(ts_path) is False:
                os.system(f'aria2c -o "{ts_path}" "{segment_link}" --quiet --continue=true')
                time.sleep(0.01)
        time.sleep(0.5)







    def get_video(self, api):

        video = treinaweb_sessions.get(api, headers=self.headers).json()['data']['video']['data']

        return video


    def get_apostilas(self, api):

        apostilas = treinaweb_sessions.get(api, headers=self.headers).json()['data']['apostila']['data']['html']

        return apostilas
    def replacer(self, text):
            invalid = {'/': '-','//': ' - ', r'"': r"'", '\\': " - ", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
            for char in invalid:
                if char in text:
                    text = text.replace(char, invalid[char])
            return text




    

    
    def return_self(self, api):

        for link in api:
            if link['type'] == 'GET' and link['rel'] == 'self':
                uri = link['uri'] + '?include=aulas'
                aulas = treinaweb_sessions.get(uri, headers=self.headers).json()
                return aulas

    def create_path(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)
        return path




#Downloader().index()