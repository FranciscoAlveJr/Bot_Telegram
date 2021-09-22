import requests
import json
import shutil
from bs4 import BeautifulSoup as bs
import urllib
import os
import time
import sys
import random
from datetime import datetime

os.system('cls')
alura_session = requests.Session()
#embaralhar = input('1 - Sim\n2 - Nâo\nEmbaralhar listas?\nR: ')
embaralhar = '2'
if embaralhar.isdigit():
    if embaralhar == '1':
        emb = True
    elif embaralhar == '2':
        emb = False
else:
    print('err')
        

class Downloader():

    def scrambled(self, orig):
        
        if emb:
            dest = orig[:]
            random.shuffle(dest)
        else:
            dest = orig
            pass
        return dest

    def create_session(self):
        
        self.account_header = {
            'authority': 'cursos.alura.com.br',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://cursos.alura.com.br',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://cursos.alura.com.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        alura_session.headers.update(self.account_header)

        #texto_base = 'Alura Cursos | Login'
        #espacamento = round((100-len(texto_base))/2)-1
        #print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        #texto_base = 'VERSÃO DE TESTE, SEM INPUT DE LOGIN'
        #espacamento = round((100-len(texto_base))/2)-1
        #print(f'{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        
        try:
            if sys.argv[1] == 'cookie':
                authorization = input('Entre com o cookie: ')
        except:
            
            
            if self.logged is False:
                #self.email = input('Email: ')
                #self.password = input('Senha: ')
                self.email = 'ocoisa081@gmail.com'   
                self.password = '18020301.pP'
                self.logged = True
                #email = 'pamcuellas@gmail.com'
                #password = 'Di10ni27!'  
                pass
            data = {
                'urlAfterLogin': 'https://cursos.alura.com.br/dashboard',
                'username': self.email,
                'password': self.password,
                'UniOnError': ''
            }

            alura_session.post('https://cursos.alura.com.br/signin', data=data, headers=self.account_header)
            authorization = alura_session.cookies.get_dict()['caelum.login.token']
            
            alura_session.headers['Authorization'] = f'Bearer {authorization}'
            self.account_header['Authorization'] = f'Bearer {authorization}'
            alura_session.headers.update(self.account_header)
           
    def index(self):

        self.url_base = 'https://www.alura.com.br'
        self.logged = False
        while True:
            os.system('cls')
            texto_base = 'Alura Cursos Crawler'
            espacamento = round((100-len(texto_base))/2)-1
            print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
            self.headers = {
                'authority': 'www.alura.com.br',
                'cache-control': 'max-age=0',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.alura.com.br/',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                }
            print('1 - Listar Cursos\n2 - Listar Formarções\n3 - Ver atualizações\n4 - Informações\n5 - Sair')
            print(f'\n{"-" * 100}\n')
            escolha = input('Escolha dentre as opções acima: ')
            print(f'\n{"-" * 100}\n')
            if escolha == '1':
                self.cursos()
                break
            elif escolha == '2':
                self.formacoes()
                break
            elif escolha == '3':
                self.get_date()
                os.system('cls')
                print('Lista dos 20 primeiros cursos atualizados:\n')
                last_ups = json.loads(open('Ultimos Updates.json', 'r').read())
                for last_up in last_ups[:20]:
                    print(f'{last_up["index"]} - {last_up["nome"]}\t[{last_up["data"]}]\n{last_up["link"]}\n')
                escolha = input('Deseja baixar os ultimos quantos? (0 para baixar nenhum)\n')
                if escolha == '0':
                    exit(0)
                elif escolha.isdigit() and int(escolha) <= 20:
                    for curso in last_ups[:int(escolha)-1]:
                        self.by_url(curso['link']) 
                    exit(0)
            elif escolha == '4':
                self.print_infos()
            elif escolha == '54':
                os.system('cls')
                texto_base = 'Saindo'
                espacamento = round((100-len(texto_base))/2)-1
                print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
                #time.sleep(3)
                exit()
            else:
                texto_base = 'Escolha errada. Tente novamente em 3 segundos.'
                espacamento = round((100-len(texto_base))/2)-1
                print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
                #time.sleep(3)
                continue

    def print_infos(self):
        
        os.system('cls')
        texto_base = 'Informações'
        espacamento = round((100-len(texto_base))/2)-1
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')

        print('\tEsse bot faz download do conteúdo da Alura Cursos (em atualização futura fará de todas as \nplataformas da empresa). Escolha baixar por módulo, categoria ou direto pelo curso\nNão se assuste durante o download com o número da aula que está sendo baixada, o programa\n\tBaixa primeiro os videos, e depois baixa os PDF. Alguns PDF tem uma scrollbar lateral,\ncom o texto cortado, basta copiar o texto e colar em outro lugar, um bloco de notas por exemplo e\nvocê conseguirá ler tudo.A macro, infelizmente não funcionou.')
        print(f'\n{"-" * 100}\n')
        input('Precise ENTER para voltar ao menu principal...')
        os.system('cls')
        self.index()

    def cursos(self):

        os.system('cls')
        self.url_base = 'https://www.alura.com.br'
        texto_base = 'Coletando dados. Aguarde.'
        espacamento = round((100-len(texto_base))/2)-2
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        base_parser = bs(requests.get(self.url_base, headers=self.headers).content, 'html.parser')
        os.system('cls')
        texto_base = 'Listando Modulos'
        espacamento = round((100-len(texto_base))/2)-1
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        listar_modulos =  base_parser.findAll('div', class_='categories__wrapper__links--home')
        cursos = {}
        self.create_session()
        for count, modulo in enumerate(listar_modulos):
            count += 1
            modulo_nome = self.replacer(modulo.find('div', class_='categories__link-wrapper--home').getText().replace('Cursos de', 'Cursos de ').strip())
            modulo_url = modulo.find('a', class_='categories__link--home')['href']
            print(f'{count} - Listar {modulo_nome}')
            cursos[count] = modulo_url
        cursos[count + 1] = '/cursos-online-tecnologia'
        print(f'{count + 1} - Listar Todos os cursos')
        print(f'{count + 2} - Baixar curso através de URL')
        print(f'\n{"-" * 100}\n')
        escolha = str(input('Escolha dentre as opções acima: '))
        print(f'\n{"-" * 100}\n')
        os.system('cls')
        if int(escolha) in cursos.keys():
            if int(escolha) != 9:
                self.listar_modulo(cursos[int(escolha)])
            elif int(escolha) == 9:
                self.listar_todos(cursos[int(escolha)])
        elif int(escolha) == 10:
            curso_url = input('Escreva a URL do curso: ')
            check_url_base = 'https://www.alura.com.br/curso-online-'
            if check_url_base not in curso_url:
                print('Houve algum erro, encerrando.')
                exit()
            elif check_url_base in curso_url:
                self.by_url(curso_url)
        else:
            print('Houve algum erro, encerrando.')
            exit()
    
    def formacoes(self):

        os.system('cls')
        texto_base = f"Listando Formações"
        espacamento = round((100-len(texto_base))/2)-2
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        formacoes = bs(alura_session.get('https://www.alura.com.br/formacoes', headers=self.headers).content, 'html.parser').findAll('li', class_='formacoes__item')
        for count, formacao in enumerate(formacoes, start=1):
            formacao_id = formacao['id']
            formacao_title = self.replacer(formacao.find('h3', 'formacoes__category-title').getText().strip()).replace('Formações em', 'Formações em ')
            formacao_totals = formacao.find('p', f'formacoes__total formacoes__total--{formacao_id}').getText().strip()
            print(f'{count} - Listar {formacao_title} - {formacao_totals}')
        print(f'{count + 1} - Baixar Formação através de URL')
        print(f'\n{"-" * 100}\n')
        escolha = str(input('Escolha dentre as opções acima: '))
        print(f'\n{"-" * 100}\n')
        os.system('cls')
        if escolha.isdigit():
            if int(escolha) == count + 1:
                print('VIA LINK')
            elif int(escolha) < count + 1:
                formacao_escolhida = formacoes[int(escolha)-1].findAll('div', 'formacao__informations')
                os.system('cls')
                texto_base = f"{formacoes[int(escolha)-1].find('h3', 'formacoes__category-title').getText().replace('Formações em', 'Formações em ')}"
                espacamento = round((100-len(texto_base))/2)-2
                print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')


                for count, escolhas in enumerate(formacao_escolhida, start=1):
                    formacao_curso = self.replacer(escolhas.find('h4', 'formacao__title').getText().strip())
                    print(f'{count} - Formação {formacao_curso}')
                print(f'{count + 1} - Baixar Todos')
                print(f'\n{"-" * 100}\n')
                escolha = str(input('Escolha dentre as opções acima: '))
                print(f'\n{"-" * 100}\n')
                os.system('cls')
                if escolha.isdigit():
                    if int(escolha) == count + 1:
                        print('BAIXAR TODOS')
                    elif int(escolha) < count + 1:
                        link = formacao_escolhida[int(escolha)-1].find('a', class_='formacao__link')['href']
                        url = f'https://cursos.alura.com.br{link}'
                        self.create_session()
                        self.by_formacao_url(url)
        else:
            print('Houve algum erro, encerrando.')
            exit(0)
        
        
    def by_formacao_url(self, url):

        os.system('cls')
        texto_base = 'Coletando dados. Aguarde.'
        espacamento = round((100-len(texto_base))/2)-2
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        page_source = bs(alura_session.get(url, headers=self.account_header).content, 'html.parser')
        self.formacao_nome = self.replacer(page_source.find('h1', class_='formacao-headline-titulo').getText().strip()
        )
        self.formacao_categoria = self.replacer(page_source.find('a', class_='formacao__info-categoria-link').getText().strip()
        )
        os.system('cls')
        espacamento = round((100-len(self.formacao_categoria))/2)-1
        index_curso = f'{self.formacao_nome}'
        espacamento_index = round((100-len(index_curso))/2)-1
        print(f'\n{"-" * 100}\n#{" " * espacamento_index}{index_curso}{" " * espacamento_index}#\n#{" " * espacamento}{self.formacao_categoria}{" " * espacamento}#\n{"-" * 100}\n')
        passos = page_source.findAll('li', class_='formacao-passos-passo')
        for passo in passos:
            self.passo_titulo = self.replacer(passo.find('div', class_='formacao-passo-titulo').getText().strip())
            if int(self.passo_titulo.split(' ')[0]) < 10:
                self.passo_titulo = f'0{self.passo_titulo}'
            contents = passo.findAll('li', class_='learning-content__item')
            print(self.passo_titulo)
            for index, content in enumerate(contents, start=1):
                if index < 10:
                    count = f'0{index}'
                else:
                    count = index
                tipo = self.replacer(content.find('span', class_='learning-content__kind').getText().strip().split(' - ')[0])
                self.tipo_nome = self.replacer(content.find('span', class_='learning-content__name').getText().strip())
                print(f'\t{index} - {self.tipo_nome} - [{tipo}]')
                tipos = ['Curso', 'Video', 'Alura+', 'Post', 'Podcast', 'Site']
                if tipo in tipos:
                    if 'Curso' in tipo:
                        self.tipo_curso(content, count)
                    elif 'Video' in tipo:
                        self.tipo_video(content, count)
                        pass
                    elif 'Alura' in tipo:
                        self.tipo_alurap(content, count)
                        pass
                    elif 'Post' in tipo:
                        self.tipo_post(content, count)
                        pass
                    elif 'Podcast' in tipo:
                        self.tipo_podcast(content, count)
                        pass
                else:
                    print(f'TIPO NAO CATALOGADO {tipo}')
                    exit(0)
                

        finish = page_source.find('h3', class_='certificate__title').getText().strip().replace('\n', ' ').replace('  ', '')
        espacamento = round((100-len(finish))/2)-2
        print(f'\n{"-" * 100}\n#{" " * espacamento}{finish}{" " * espacamento}#\n{"-" * 100}\n')
        
        
    def tipo_curso(self, content, count):

        link = content.find('a', class_='learning-content__link')['href']
        url = f'https://cursos.alura.com.br{link}'
        base_parser = bs(alura_session.get(url, headers=self.account_header).content, 'html.parser').find()
        self.curso_modulo = self.replacer(base_parser.find(class_='course-header-banner-breadcrumb__category').getText().strip())
        self.curso_categoria = self.replacer(base_parser.find(class_='course-header-banner-breadcrumb__subcategory').getText().strip())
        path = f'Cursos/{self.curso_modulo}/{self.curso_categoria}/Curso de {self.tipo_nome}'
        if os.path.exists(path) is False:
            url = self.url_base+link
            self.by_url(url)
        formacao_path = f'Formações/Formações em {self.formacao_categoria}/Formação {self.formacao_nome}/{self.passo_titulo}/{count} - Curso de {self.tipo_nome}'
        self.criar_pastas_formacao(formacao_path)
        os.system(f'@echo N|Xcopy /E /I /-y "{path}" "{formacao_path}" > NUL')
        pass  

    def tipo_video(self, content, count):
        
        link = content.find('a', class_='learning-content__link')['href']
        videdo_title = self.replacer(content.find('span', class_='learning-content__name').getText().strip())
        formacao_path = f'Formações/Formações em {self.formacao_categoria}/Formação {self.formacao_nome}/{self.passo_titulo}/{count} - {videdo_title}.mp4'
        if os.path.exists(formacao_path) is False:
            if 'youtube' in link:
                os.popen(f'youtube-dl "{link}" -o "{formacao_path}" --quiet')
        pass  

    def tipo_alurap(self, content, count):
        
        link = content.find('a', class_='learning-content__link')['href'].split('-c')[-1]
        videdo_title = self.replacer(content.find('span', class_='learning-content__name').getText().strip())
        formacao_path = f'Formações/Formações em {self.formacao_categoria}/Formação {self.formacao_nome}/{self.passo_titulo}/{count} - {videdo_title}.mp4'
        if os.path.exists(formacao_path) is False:
            #https://cursos.alura.com.br/extracontent/178/video
            hd_link = alura_session.get(f'https://cursos.alura.com.br/extracontent/{link}/video').json()
            down_link = hd_link[0]['link'] if hd_link[0]['quality'] == 'hd' else hd_link[0]['link']
            vimeo_id = down_link.split('alura/')[1].split('-')[0]
            vimeo_link = f'https://player.vimeo.com/video/{vimeo_id}/config'
            try:
                self.download_video(vimeo_link, formacao_path)
            except:
                os.system(f'ffmpeg -i "{down_link}" "{formacao_path}"  -nostats -loglevel 0')
                print(f'\t{count} - {videdo_title} - Link secundario')
        pass  

    def tipo_post(self, content, count):
        pass  

    def tipo_podcast(self, content, count):

        link = content.find('a', class_='learning-content__link')['href']
        if link[0:1] == '/h':
            link = f'https://hipsters.tech{link}'
        podcast_title = self.replacer(content.find('span', class_='learning-content__name').getText().strip())
        ext = 'mp3'
        if 'hipsters.tech' in link:
            podcast_source = bs(alura_session.get(link, headers=self.headers).content, 'html.parser')
            try:
                podcast = podcast_source.find('a', {'class': 'powerpress_link_d'})['href']
            except:
                podcast_id = str(podcast_source.find('iframe', {'class': 'youtube-player'})['src']).split('?')[0].split('/')[1]
                podcast = f'https://www.youtube.com/watch?v={podcast_id}'
                ext = 'mp4'
        else:
            try:
                podcast = bs(alura_session.get(link, headers=self.headers).content, 'html.parser').find('div', {'class': 'audio-player podcast-container'})['data-source']
            except:
                link = f'https://www.alura.com.br/podcast{link}'
                podcast = bs(alura_session.get(link, headers=self.headers).content, 'html.parser').find('div', {'class': 'audio-player podcast-container'})['data-source']
        
        formacao_path = f'Formações/Formações em {self.formacao_categoria}/Formação {self.formacao_nome}/{self.passo_titulo}/{count} - {podcast_title}.{ext}'
        if os.path.exists(formacao_path) is False:
            if 'youtube' in podcast:
                os.popen(f'youtube-dl "{podcast}" -o "{formacao_path}" --quiet')
            else:
                os.popen(f'aria2c -o "{formacao_path}" "{podcast}" --quiet')
        pass  

    def by_url(self, url):

        os.system('cls')
        texto_base = 'Coletando dados. Aguarde.'
        espacamento = round((100-len(texto_base))/2)-2
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        curso_url = url.replace('https://www.alura.com.br/curso-online-', 'https://cursos.alura.com.br/course/')
        
        error = 0
        while True:
            try:
                base_parser = bs(alura_session.get(curso_url, headers=self.account_header).content, 'html.parser')
                os.system('cls')
                self.curso_titulo = self.replacer(base_parser.find(class_='course-header-banner-title').getText().replace('\n', '').replace('Curso de', 'Curso de ').strip()).replace('  ', ' ')
                break
            except Exception as e:
                error += 1
                self.create_session()
                time.sleep(20)
                if error == 20:
                    return
                    print(f'Erro no {self.aula_title}')
                    print("O programa deu erro no horario: ", end='')
                    #print(datetime.datetime.now())
                    print()
                    print(e)
                    exit(0)
                pass
        self.curso_modulo = self.replacer(base_parser.find(class_='course-header-banner-breadcrumb__category').getText().strip())
        self.curso_categoria = self.replacer(base_parser.find(class_='course-header-banner-breadcrumb__subcategory').getText().strip())
        espacamento = round((100-len(self.curso_titulo))/2)-1
        index_curso = f'{self.curso_modulo} | {self.curso_categoria}'
        espacamento_index = round((100-len(index_curso))/2)-1
        print(f'\n{"-" * 100}\n#{" " * espacamento_index}{index_curso}{" " * espacamento_index}#\n#{" " * espacamento}{self.curso_titulo}{" " * espacamento}#\n{"-" * 100}\n')
        self.get_course(curso_url)
        #descanso = random.randint(300, 600)
        #texto_base = f'DESCANSANDO POR {descanso/60} MINUTOS.'
        espacamento = round((100-len(texto_base))/2)-1
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        #time.sleep(1200)
        #random.randint(300, 600)
        #time.sleep(10)

    def listar_modulo(self, modulo_url):

        url_base = str(f'{self.url_base}{modulo_url}')
        texto_base = 'Coletando dados. Aguarde.'
        espacamento = round((100-len(texto_base))/2)-2
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        base_parser = bs(requests.get(url_base, headers=self.headers).content, 'html.parser')
        os.system('cls')
        modulo_titulo =  str(base_parser.find('h1', class_='pagina-categoria__titulo').getText().strip())
        modulo_titulo = modulo_titulo.replace('\n', '').replace('Cursos de', 'Cursos de ')
        espacamento = round((100-len(modulo_titulo))/2)-1
        print(f'\n{"-" * 100}\n#{" " * espacamento}{modulo_titulo}{" " * espacamento}#\n{"-" * 100}\n')
        listar_modulos = base_parser.findAll('div', 'subcategoria lista-subcategorias__subcategoria')
        modulo = {}
        for count, modulo_info in enumerate(listar_modulos):
            count += 1
            modulo_name = str(modulo_info.find(class_='subcategoria__titulo').getText()).strip()
            modulo_name = modulo_name.replace('Cursos de\n', 'Cursos de ').strip()
            modulo[count] = modulo_name
            print(f'{count} - Listar {modulo_name}')
        print(f'{count + 1} - Baixar todos os modulos')
        print(f'\n{"-" * 100}\n')
        escolha = input('Escolha dentre as opções acima: ')
        print(f'\n{"-" * 100}\n')
        os.system('cls')
        if int(escolha) in modulo.keys():
            self.lista_cursos(modulo[int(escolha)], listar_modulos, escolha)
        elif int(escolha) == count + 1:
            #listar_modulos = self.scrambled(listar_modulos)
            for modulo_info in listar_modulos:
                modulo_name = str(modulo_info.find(class_='subcategoria__titulo').getText()).strip()
                modulo_name = modulo_name.replace('Cursos de\n', 'Cursos de ').strip()
                modulo_cursos = modulo_info.findAll('li', class_='subcategoria__item')
                for curso in modulo_cursos:
                    curso_link = curso.find('a')['href']
                    url = self.url_base+curso_link
                    self.by_url(url)
        else:
            print('Houve algum erro, encerrando.')
            exit()

    def lista_cursos(self, text, listar_modulos, escolha):

            texto_base = text
            espacamento = round((100-len(texto_base))/2)-2
            print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
            curso_dict = {}
            curso_list = []
            for curso in listar_modulos[int(escolha)-1]:
                listar_cursos = curso.findAll('li', class_='subcategoria__item')
                for count_curso, curso in enumerate(listar_cursos):
                    count_curso += 1
                    curso_link = curso.find('a', class_='card-curso')['href']
                    curso_nome = self.replacer(curso.find(class_='card-curso__nome').getText().strip())
                    curso_dict[count_curso] = curso_link
                    curso_list.append(curso_link)
                    print(f'{count_curso} - Baixar {curso_nome}')
            print(f'{count_curso + 1} - Baixar Todos os Cursos')
            print(f'\n{"-" * 100}\n')
            escolha_curso = input('Escolha dentre as opções acima: ')
            escolha_curso = count_curso + 1
            print(f'\n{"-" * 100}\n')
            if int(escolha_curso) in curso_dict.keys():
                url = self.url_base+curso_dict[int(escolha_curso)]
                self.by_url(url)
            elif int(escolha_curso) == count_curso + 1:
                curso_list = self.scrambled(curso_list)
                for curso in curso_list:
                    url = self.url_base+curso
                    self.by_url(url)
 
    def listar_todos(self, todos):
    
        texto_base = 'Todos os Cursos Online Alura'
        espacamento = round((100-len(texto_base))/2)-1
        print(f'\n{"-" * 100}\n#{" " * espacamento}{texto_base}{" " * espacamento}#\n{"-" * 100}\n')
        todos_url = self.url_base+todos
        cursos = bs(requests.get(todos_url, headers=self.headers).content, 'html.parser').findAll('a', class_='cursoCard')
        curso_dict = {}
        curso_list = []
        for count, curso in enumerate(cursos):
            count += 1
            curso_dict[count] = curso['href']
            curso_list.append(curso['href'])
            curso_nome = curso.find('div', class_='cursoCard-nome').getText().strip()
            print(f'{count} - {curso_nome}')
        print(f'{count + 1} - Baixar todos')
        print(f'{count + 2} - Escolher Varios')
        print(f'\n{"-" * 100}\n')
        escolha_curso = input('Escolha dentre as opções acima: ')
        print(f'\n{"-" * 100}\n')
        if int(escolha_curso) in curso_dict.keys():
            url = self.url_base+curso_dict[int(escolha_curso)]
            self.by_url(url)
        elif int(escolha_curso) == count + 2:
            escolhas = []
            x = ''
            print('0 - Parar loop')
            while x != 0:
                x = input('Escolha: ')
                if x == '0':
                    print('Baixando lista')
                    break
                elif x.isdigit():
                    escolhas.append(x)
                else:
                    print('Erro')
                    exit(0)
            for curso in escolhas:
                url = self.url_base+curso_dict[int(curso)]
                self.by_url(url)
        elif int(escolha_curso) == count + 1:
            curso_list = self.scrambled(curso_list)
            for curso in curso_list:
                url = self.url_base+curso
                self.by_url(url)
        pass

    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

    def get_course(self, url):
        
        curso_slug = url.split('/')[-1]
        alura_session.get(f'https://cursos.alura.com.br/courses/{curso_slug}/tryToEnroll', headers=self.account_header)
        curso_url = f'https://cursos.alura.com.br/mobile/v2/course/{curso_slug}'
        curso_json = json.loads(alura_session.get(curso_url, headers=self.account_header).content)
        for count_section, section in enumerate(curso_json['sections']):
            count_section += 1
            section_title = self.replacer(section['titulo']).strip()
            if count_section < 10:
                count_section = f'0{count_section}'
            self.section_title = f'{count_section} - {section_title}'
            self.criar_pastas_curso()
            section_id = section['id']
            texts = f'https://cursos.alura.com.br/mobile/course/{curso_slug}/section/{section_id}'
            print(self.section_title)
            self.get_video(section['videos'], curso_slug)
            self.get_texts(texts)

    def get_texts(self, url):
        
        base_parser = bs(alura_session.get(url, headers=self.account_header).content, 'html.parser')
        sections = base_parser.findAll('li', class_='task-menu-nav-item')
        url_base = f'https://cursos.alura.com.br'
        for section in sections:
            section_link = section.find('a')['href'].replace('/mobile/', '/')
            title_link = f'{url_base}{section_link}'
            
            error = 0
            while True:
                try:
                    aula_link = bs(alura_session.get(title_link, headers=self.account_header).content, 'html.parser').find('h1', 'task-body-header-title')
                    self.aula_title = self.replacer(aula_link.getText().strip())
                    break
                except Exception as e:
                    error += 1
                    self.create_session()
                    time.sleep(20)
                    if error == 20:
                        print('Erro no self.aula_title')
                        print("O programa deu erro no horario: ", end='')
                        print(datetime.datetime.now())
                        print()
                        print(e)
                        exit(0)
                    pass
            
            output_filename = f'{self.path}/{self.aula_title}.html'        
            if os.path.exists(output_filename) is False:
                text_base = alura_session.get(f'{url_base}/mobile{section_link}', headers=self.account_header).text
                text_base = text_base.encode().decode('utf-8')
                text_replaced = text_base.replace('href="/images', 'href="https://cursos.alura.com.br/images')
                text_replaced = text_replaced.replace('href="/style', 'href="https://cursos.alura.com.br/style')
                text_replaced = text_replaced.replace('href="/suggestions', 'href="https://cursos.alura.com.br/suggestions')
                text_replaced = text_replaced.replace('href="/assets', 'href="https://cursos.alura.com.br/assets')
                text_bs = bs(text_replaced, 'html.parser')
                remove_button = text_bs.find(class_='task-actions')
                html_final = str(str(text_bs).replace(str(remove_button), ''))
                self.html2pdf(html_final, self.aula_title)
                #time.sleep(random.randint(5, 10))

    def get_video(self, videos, curso_slug):

        for video in videos:
            
            video_nome = self.replacer(video['nome'].strip())
            video_position = video['position']
            if video_position < 10:
                video_position = str(f'0{video_position}')
            video_id = video['id']
            self.video_file = f'{video_position} - {video_nome}.mp4'
            video_path = f'{self.path}/{self.video_file}'
            if os.path.exists(video_path) is False:
                video_link = f'https://cursos.alura.com.br/mobile/courses/{curso_slug}/busca-video-{video_id}'
                error = 0
                while True:
                    try:
                        alura_connection = alura_session.get(video_link, headers=self.account_header)
                        alura_status_code = alura_connection.status_code
                        if alura_status_code != 200:
                            error += 1
                            if error == 10:
                                print('Erro de Conexao')
                                print(video_link)
                                print(self.path)
                                print("O programa deu erro no horario: ", end='')
                                print(datetime.datetime.now())
                                break
                            continue 
                        hd_link = alura_connection.json()
                        down_link = hd_link[0]['link'] if hd_link[0]['quality'] == 'hd' else hd_link[0]['link']
                        vimeo_id = down_link.split('alura/')[1].split('-')[0]
                        vimeo_link = f'https://player.vimeo.com/video/{vimeo_id}/config'
                        try:
                            self.download_video(vimeo_link)
                            break
                        except:
                            video_path = f'{self.path}/{self.video_file}'
                            if os.path.exists(video_path) is False:
                                os.system(f'ffmpeg -i "{down_link}" "{video_path}"  -nostats -loglevel 0')
                                print(f'\t{self.video_file[:-4]} - Link secundario')
                                break
                        
                    except Exception as e: 
                        error += 1
                        self.create_session()
                        time.sleep(5)
                        print(e)
                        if error == 3:
                            print('Erro no hd_link')
                            print("O programa deu erro no horario: ", end='')
                            print(datetime.datetime.now())
                            print()
                            print(e)
                            print()
                            try:
                                print(hd_link)
                            except:
                                pass
                            exit(0)
                        pass                            
                    #time.sleep(random.randint(5, 10))
               
    def download_video(self, video, video_path=None):

        if video_path == None:
            video_path = f'{self.path}/{self.video_file}'

        if os.path.exists(video_path) is False:
            vimeo_headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://cursos.alura.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }

            vimeo_config = requests.get(video, headers=vimeo_headers).json()

            try:
                if vimeo_config["message"]:
                    print(f'\t{self.video_file[:-4]} - {vimeo_config["message"]}')
                    return
            except:
                pass
            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']

            os.system(f'aria2c -o "{video_path}" {vimeo_url} --quiet')
            
            print(f'\t{self.video_file[:-4]}')

    def criar_pastas_curso(self):

        self.path = f'Cursos/{self.curso_modulo}/{self.curso_categoria}/{self.curso_titulo}/{self.section_title}'
        try:
            if os.path.exists(self.path) is False:
                os.makedirs(self.path)
            else:
                pass
            pass
        except:
            pass

    def criar_pastas_formacao(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)

    def html2pdf(self, source_html, pdf_name):
        
        html_file_w = open(f'{self.path}/{pdf_name}.html', 'w', encoding='utf-8')
        with html_file_w as out:
            out.write(source_html)
        
        #html_file_r = f'{self.path}/{pdf_name}.html'
        #output_filename = f'{self.path}/{pdf_name}.pdf'
        #html_file = f'{self.path}/{pdf_name}.html'
        #local_path = f'Z:/Oi/Alura/{html_file_r}'
        #local = local_path.replace(' ', str('\ '))
        #local = local.replace(" ", '')
        #if os.path.exists(output_filename) is False:
            
            #try:
                #pdfkit.from_string(source_html, output_filename, options={ 'quiet': ''})
                #pdfkit.from_file(html_file_r, output_filename)
                #os.system(f'wkhtmltopdf "{local_path}" "{output_filename} --quiet"')
                #os.system(f'del "{html_file_r}"')
                #pdfkit.from_string(source_html, output_filename, options={ 'quiet': '', 'margin-top': '1cm', 'margin-right': '1cm', 'margin-bottom': '1cm', 'margin-left': '1cm'})
            #except Exception as e:
                #pass
            print(f'\t{pdf_name}')
        
    def get_date(self):
        self.url_base = 'https://www.alura.com.br'
        todos_cursos = 'cursos-online-tecnologia'
        self.headers = {
            'authority': 'www.alura.com.br',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'pt-BR,pt;q=0.9',
        }
        source = requests.get(f'{self.url_base}/{todos_cursos}', headers=self.headers).content
        cursos = bs(source, 'html.parser').findAll('a', {'class': 'cursoCard'})
        info_list = []
        last_update = {}
        for index, curso in enumerate(cursos):
            link = curso['href'] #/curso-online-dotnet-mongodb
            nome, data = self.get_info(link)
            last_update[index] = {}
            last_update[index]['index'] = index + 1
            last_update[index]['nome'] = nome
            last_update[index]['data'] = str(datetime.strptime(data, '%d/%m/%Y')).split(' ')[0] #2020-09-25 00:00:00
            last_update[index]['link'] = f'{self.url_base}{link}'
            info_list.append(last_update[index])
            print(f'{index + 1} - {nome} - {data}')
        info_list.sort(key = lambda x: datetime.strptime(x['data'], '%Y-%m-%d'), reverse=True) 
        with open('Ultimos Updates.json', 'w', encoding='utf-8') as output:
            output.write(json.dumps(info_list))

    def get_info(self, link):
        curso_info = bs(requests.get(f'{self.url_base}{link}', headers=self.headers).content, 'html.parser')
        curso_titulo = curso_info.find('h1', {'class': 'curso-banner-headline-titulo'}).getText().strip().replace('\n', ' ')
        curso_data = curso_info.findAll('p', {'class': 'curso-conteudo-maisInfos-item-texto'})[-1].getText().strip()
        if '/' not in curso_data:
            curso_data = '01/01/2000'
                
        return curso_titulo, curso_data


#start = Downloader()
#start.index()

"""try:
    print()
    #start.create_session()
except Exception as e:
    print("O programa deu erro no horario: ", end='')
    print(datetime.datetime.now())
    print()
    print(e)"""
#ALURA +
#https://cursos.alura.com.br/extracontent/178/video
