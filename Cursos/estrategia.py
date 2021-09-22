import requests
import json
from bs4 import BeautifulSoup as bs
import urllib
import os
import time
import sys
import datetime
import random

os.system('cls')
estrategia_session = requests.Session()

class Downloader():

    def index(self):
        self.account_header = {
            'authority': 'www.estrategiaconcursos.com.br',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://www.estrategiaconcursos.com.br',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.estrategiaconcursos.com.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        estrategia_session.headers.update(self.account_header)
        #find_csrf = bs(estrategia_session.get('https://www.estrategiaconcursos.com.br/', headers=self.account_header).content, 'html.parser').find('input', {'name': 'csrf_form_token'})['value']

        #data = {
        #'email': 'princeandrews081@gmail.com',
        #'senha': 'pc105123.p',
        #'csrf_form_token': find_csrf
        #}

        #login = estrategia_session.post('https://www.estrategiaconcursos.com.br/loja/entrar/login/', data=data,  headers=self.account_header)
        #token_info = estrategia_session.get('https://www.estrategiaconcursos.com.br/oauth/token/', headers=self.account_header).json()
        #token_type = token_info['token_type']
        #access_token =  token_info['access_token']
        #authorization = token_type + ' ' + access_token
        token = input('TOKEN: ')
        authorization = f'Bearer {token}'
        self.account_header['authorization'] = authorization
        self.escolha()
        #self.my_courses()

    def escolha(self):
        print('Escolha o método que deseja realizar os downloads:')
        print('1 - Minhas matriculas\n2 - Trilhas estrategicas\n3 - Cursos Exclusivos\n4 - Catálogo de Cursos')
        escolha = input('Opção desejada: ')
        if escolha == '1':
            self.my_courses('')
        elif escolha == '2':
            self.trilhas()
        elif escolha == '3':
            self.exclusivos()
        elif escolha == '4':
            self.catalogo()
        else:
            print('Opção errada, tente novamente.')
            exit(0)

    def catalogo(self):
        
        pagination = estrategia_session.get('https://search.estrategiaconcursos.com.br/indexes/products/search?size=51&subscriptions=84231&q=pacote&type=pacote&boost=curso&from=0', headers=self.account_header).json()['pagination']['last_page']
        concursos_list = []
        for page in range(1, pagination):
            concursos = estrategia_session.get(f'https://search.estrategiaconcursos.com.br/indexes/products/search?size=51&subscriptions=84231&q=pacote&type=pacote&boost=curso&from={page}', headers=self.account_header).json()['result']
            concursos_list.extend(concursos)
        for concurso in concursos_list:
            concurso_id = concurso['id']
            estrategia_session.put(f'https://api.estrategiaconcursos.com.br/api/aluno/assinatura/curso/{concurso_id}', headers=self.account_header, data={"inscrito": 'true'})
            self.concuso_nome = self.replacer(concurso['name']).strip()
            self.actual_path = self.criar_pasta(f'{self.concuso_nome}')
            print(self.concuso_nome)
            descricao = concurso['description']
            self.text(self.actual_path, descricao, self.concuso_nome)
            self.my_courses('pacote')
            estrategia_session.put(f'https://api.estrategiaconcursos.com.br/api/aluno/assinatura/curso/{concurso_id}', headers=self.account_header, data={"inscrito": 'false'})

    def exclusivos(self):

        pagination = estrategia_session.get('https://search.estrategiaconcursos.com.br/indexes/exclusives/search', headers=self.account_header).json()['pagination']['last_page']
        concursos_list = []
        for page in range(1, pagination):
            concursos = estrategia_session.get(f'https://search.estrategiaconcursos.com.br/indexes/exclusives/search?from={page}', headers=self.account_header).json()['result']
            concursos_list.extend(concursos)
        for concurso in concursos_list:
            try:
                concurso_id = concurso['id']
                concuso_nome = self.replacer(concurso['name']).strip()
                print(concuso_nome)
                descricao = concurso['description']
                self.curso_path = self.criar_pasta(f'Cursos Exclusivos/{concuso_nome}')
                self.text(self.curso_path, descricao, concuso_nome)
                course_actual = estrategia_session.get(f'https://api.estrategiaconcursos.com.br/api/aluno/curso/{concurso_id}', headers=self.account_header).json()
                self.get_aula(course_actual)
            except:
                continue


    def trilhas(self):

        pagination = estrategia_session.get('https://search.estrategiaconcursos.com.br/indexes/trails/search', headers=self.account_header).json()['pagination']['last_page']
        concursos_list = []
        for page in range(1, pagination):
            concursos = estrategia_session.get(f'https://search.estrategiaconcursos.com.br/indexes/trails/search?from={page}', headers=self.account_header).json()['result']
            concursos_list.extend(concursos)
        for concurso in concursos_list:
            try:
                concurso_id = concurso['id']
                concuso_nome = self.replacer(concurso['name']).strip()
                print(concuso_nome)
                descricao = concurso['description']
                self.curso_path = self.criar_pasta(f'Trilhas Estrategicas/{concuso_nome}')
                self.text(self.curso_path, descricao, concuso_nome)
                course_actual = estrategia_session.get(f'https://api.estrategiaconcursos.com.br/api/aluno/curso/{concurso_id}', headers=self.account_header).json()
                self.get_aula(course_actual)
            except:
                continue

    def text(self, path, text, name):

        txt_file = open(f'{path}/{name}.txt', 'w', encoding='utf-8')
        with txt_file as output:
            output.write(text)
                      
    def my_courses(self, tipo):

        my_courses = estrategia_session.get('https://api.estrategiaconcursos.com.br/api/aluno/curso', headers=self.account_header).json()
        course_list = my_courses['data']
        
        if tipo == 'pacote':
            cargo = self.concuso_nome
        else:
            cargo = self.replacer(course_list['cargos'][0]['nome']).strip()
        os.system('cls')
        print(cargo)
        self.criar_pasta(cargo)
        for index, course in enumerate(course_list['concursos']):
            index += 1
            course_title = self.replacer(course['titulo']).strip()
            courses = course['cursos']
            print(f'\t{index} - {course_title}')
            for enum, curso in enumerate(courses):
                enum += 1
                tipo = self.replacer(curso['tipo']).strip().capitalize()
                nome = self.replacer(curso['nome']).strip()
                curso_id = curso['id']
                print(f'\t\t{enum} - {nome}')
                self.curso_path = self.criar_pasta(f'{cargo}/{tipo}/{nome}')
                course_actual = estrategia_session.get(f'https://api.estrategiaconcursos.com.br/api/aluno/curso/{curso_id}', headers=self.account_header).json()
                self.get_aula(course_actual)

    def get_aula(self, curso):
        self.videos_baixados = 0
        self.videos_down = 0
        erros = ['None', '', ' ', 'null', None]
        for aula in curso['data']['aulas']:
            aula_nome = self.replacer(aula['nome']).strip()
            aula_conteudo = self.replacer(aula['conteudo']).strip()
            print(f'\t\t\t{aula_nome} - {aula_conteudo}')
            self.actual_path = self.criar_pasta(f'{self.curso_path}/{aula_nome}')
            self.text(self.actual_path, aula_conteudo, aula_nome)
            pdf_path = f'{self.actual_path}/{aula_conteudo}.pdf'
            pdf_edit = f'{self.actual_path}/{aula_conteudo} - [Grifado].pdf'
            pdf_url = aula['pdf']
            pdf_grifado = aula['pdf_grifado']
            try:
                if pdf_url not in erros:
                    self.baixar_pdf(pdf_path, pdf_url)
            except:
                pass
            try:
                if pdf_grifado in erros:
                    self.baixar_pdf(pdf_edit, pdf_grifado)
            except:
                pass
            videos = aula['videos']

            for number, video in enumerate(videos):
                number += 1
                titulo = self.replacer(video['titulo']).strip()
                video_path = self.criar_pasta(f'{self.actual_path}/Videos')
                video_path = f'{video_path}/{number} - {titulo}.mp4'
                audio_path = self.criar_pasta(f'{self.actual_path}/Audios')
                audio_path = f'{audio_path}/{number} - {titulo}.mp3'
                self.video_list = video['resolucoes']
                if self.video_list == '' or self.video_list == [] or self.video_list == None:
                    print('LISTA SEM VIDEOS')
                    continue
                self.video_list_keys = self.video_list.keys()
                self.video_list_list = list(self.video_list_keys) 
                self.video_sort = sorted(self.video_list_list)
                self.video_max = self.video_sort[0]
                video_url = video['resolucoes'][self.video_max]
                audio_url = video['audio']
                slide_url = video['slide']
                pdfs_path = self.criar_pasta(f'{self.actual_path}/PDFs')
                slide_title = f'{pdfs_path}/{number} - {titulo} - [SLIDE].pdf'
                mapa_mental = video['mapa_mental']
                mapa_mental_titulo = f'{pdfs_path}/{number} - {titulo} - [MAPA MENTAL].pdf'
                resumo = video['resumo'] 
                resumo_titulo = f'{pdfs_path}/{number} - {titulo} - [RESUMO].pdf'
                try:
                    if slide_url not in erros:
                        self.baixar_pdf(slide_title, slide_url)
                except:
                    pass
                try:
                    if mapa_mental not in erros:
                        self.baixar_pdf(mapa_mental_titulo, mapa_mental)
                except:
                    pass
                try:
                    if video_url not in erros:
                        self.baixar_video(video_path, video_url, 'Video')

                except:
                    pass
                try:
                    if audio_url not in erros:
                        self.baixar_video(audio_path, audio_url, 'Audio')
                except:
                    pass
                try:
                    if resumo not in erros:
                        self.baixar_pdf(resumo_titulo, resumo)
                except:
                    pass
                if self.videos_baixados > 50:
                    print(f'PAUSANDO POR 1 HORA, FORAM BAIXADOS {self.videos_down} VIDEOS DESDE QUE INICIOU.')
                    time.sleep(3600)
                    self.videos_baixados = 0


    def baixar_video(self, path, url, tipo):
        
        if tipo == 'Video':
            if os.path.exists(path) is False:
                urllib.request.urlretrieve(url, filename=path)
                print(f'\t\t\t\t{path.split("/")[-1]} - URLLIB - {self.video_max}')
                if os.path.exists(path) is False:
                    os.system(f'aria2c -o "{path}" "{url}" --quiet')
                    print(f'\t\t\t\t{path.split("/")[-1]} - ARIA2C - {self.video_max}')
                self.videos_baixados += 1
                self.videos_down += 1
                time.sleep(3)
        if tipo == 'Audio':
            if os.path.exists(path) is False:
                urllib.request.urlretrieve(url, filename=path)
                print(f'\t\t\t\t{path.split("/")[-1]} - URLLIB')
                if os.path.exists(path) is False:
                    os.system(f'aria2c -o "{path}" "{url}" --quiet')
                    print(f'\t\t\t\t{path.split("/")[-1]} - ARIA2C')
                self.videos_baixados += 1
                self.videos_down += 1
                time.sleep(3)
        
    def baixar_pdf(self, path, url):
        
        if os.path.exists(path) is False:

            parser = bs(estrategia_session.get(url, headers=self.account_header, allow_redirects=True).content, 'html.parser')
            parser_body = parser.find('body')
            pdf_content = parser_body.find('a')['href']
            os.popen(f'aria2c -o "{path}" "{pdf_content}" --quiet')
            time.sleep(3)
            if os.path.exists(path) is False:
                parser = bs(estrategia_session.get(url, headers=self.account_header, allow_redirects=True).content, 'html.parser')
                parser_body = parser.find('body')
                pdf_content = parser_body.find('a')['href']
                urllib.request.urlretrieve(pdf_content, filename=path)
                content = estrategia_session.get(pdf_content, headers=self.account_header).content
                pdf = open(path, 'wb')
                pdf.write(content)
                pdf.close()
                print(f'\t\t\t\t{path.split("/")[-1]} - REQUEST')
            else:
                print(f'\t\t\t\t{path.split("/")[-1]} - ARIA2C')
            time.sleep(3)
        
    def criar_pasta(self, path):
        
        if os.path.exists(path) is False:
            os.makedirs(path)

        return path

    def replacer(self, text):
        invalid = {'p/': 'para', '\t': ' ', r'"': r"'", '\\': " - ", "/": "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text         



#start = Downloader()
"""try:
    inicio = datetime.datetime.now()
    start.index()
except Exception as e:
    print(f"O programa iniciou no horario: {inicio}")
    print("O programa deu erro no horario: ", end='')
    print(datetime.datetime.now())
    print()
    print(e)"""