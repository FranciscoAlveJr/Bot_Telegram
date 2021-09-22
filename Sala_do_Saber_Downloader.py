# -*- coding: utf-8 -*-

#########################################
# File name: Sala do Saber Downlaoder   #
# Author: H4dar                         #
# Orderer: Prince Andrews               #
# Description: Bot para realizar        #
# download dos videos e materias da     #
# plataforma SALA DO SABER, feito em    #
# Python, sob as libs de requests, para #
# as duvidas que possam a vir, o codigo #
# conta com diversos comentarios.       #
#########################################

import requests
import os
import json
from bs4 import BeautifulSoup as bs
import urllib
import time

salasaber_session = requests.session() #Cria uma sessão para evitar multiplos requests
class Downloader(): #Unica classe e reponsavel por realizar todas as funções

    def index(self): #Nossa primeira def, utilizada apenas para passar as informações iniciais

        os.system('cls')        
        ci_session = input('Cookies da Sessão: ')
        os.system('cls')

        salasaber_session.headers.clear()
        self.headers_auth = {
            'authority': 'saladosaber.com.br',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://saladosaber.com.br/auth',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'ci_session={ci_session}; TawkConnectionTime=0'
            } #O Header que usaremos daqui para frente, cujo ele tem salvo sua SESSION
        salasaber_session.headers.update(self.headers_auth)
        classes_path = 'https://saladosaber.com.br/users/account' #Pagina que usaremos como base para iniciar a extração de dados
        classes_get = salasaber_session.get(classes_path, headers=self.headers_auth) # Converte a pagina para texto
        self.get_courses(classes_get.content) #Vamos iniciar a extração passando nosso texto para essa def
        

    def get_courses(self, classes_get): #Essa def recebe o HTML para iniciar as analises

        sdsaber_infos = bs(classes_get, 'html.parser') #Converte a pagina de texto para PURO HTML
        print('Sessão Autenticada\n')
        courses_main = sdsaber_infos.find('ul', class_='list-unstyled categories')
        courses_list = courses_main.findAll('li', class_='item') #Procura pela lista de CURSOS
        for course in courses_list: #Tudo que segue aqui era ser repedito conforme o numero de CURSOS existentes na conta
            course_title = self.replacer(course.getText()) #Titulo do foco do Curso
            course_link = course.find('a')['href'] #Link do curso
            open_course = salasaber_session.get(course_link, headers=self.headers_auth).text #Para cada link detectado iremos entrar na pagina dele
            get_info = bs(open_course, 'html.parser') #Transformar o texto em HTML
            get_blocks = get_info.findAll(class_='col-12 mb-4') #Separamos em lista os blocos de cursos
            print(course_title)
            for info in get_blocks: #Será repedito até passar por todos os blocos de cursos
                title_group = info.find('h1', class_='title mb-4') 
                title_group_text = self.replacer(title_group.getText()) #Titulo referente ao bloco
                print('\t' + title_group_text) 
                new_block = info.findAll('div', class_='item d-inline-block') #Indexamos em uma lista todos as materias que aparecem na pagina
                for new in new_block: #Será repetido em todas as materias dentro do bloco
                    slick_list = new.find('a') 
                    new_title = self.replacer(slick_list.find(class_='img-fluid')['alt']) #Salvo o titulo da materia
                    img_link = slick_list.find(class_='img-fluid')['src']
                    slick_link = slick_list['href'] #O link da materia
                    print(f'\t\t{new_title}') 
                    aulas = bs(salasaber_session.get(slick_link, headers=self.headers_auth).text, 'html.parser') #Acessa a materia e converte a pagina de texto para HTML
                    list_aula = aulas.find('ul', class_='list-unstyled items')
                    try:
                        topic_aula = list_aula.findAll('li')
                    except:
                        continue #Listagem dos videos
                    #print(topic_aula[0])
                    #exit(0)
                    fuller_path = "Sala do Saber/" + course_title + '/' + title_group_text + '/'+ new_title #Caminho qual será salvo nossos arquivos
                    
                    if os.path.exists(fuller_path) is False:
                        os.makedirs(fuller_path) #Se as pastas não existe, ele cria.
                    if os.path.exists(f'{fuller_path}/{new_title}.png') is False:
                        urllib.request.urlretrieve(img_link, filename=f'{fuller_path}/{new_title}.png')
                        print(f'\t\t{new_title} - IMG') 
                    
                    for topic in topic_aula: #Iremos pegar as informações da pagina/aula
                        
                        #aula_link = topic.get('data-url')
                        aula_link = topic['data-url']
                        aula_title = self.replacer(topic.find('h1').getText().strip()) #Titulo da Aula
                        if os.path.exists(f'{fuller_path}/{aula_title}.mp4'):
                            continue
                        
                        
                        topic_class = bs(salasaber_session.get(aula_link, headers=self.headers_auth).content, 'html.parser')
                        #print(topic_class)
                        if len(topic_class) == 0:
                            print(f'\t\t\t{aula_title} - Não baixada - Aula não encontrada - {aula_link}')
                            continue
                        try:
                            source = topic_class.find('div', class_='lesson').find('input', {'name': 'video-source'})['value']
                        except:
                            continue
                        #print(source)
                        #m3u8_file = source.replace('m3u8', '_720.m3u8')
                        
                        self.vimeo_downloader(source, fuller_path, aula_title)
                        #self.vimeo_downloader(vimeo_video, fuller_path, aula_title) #Def utilizada exclusivamente para baixar os videos
                        self.download_files(topic_class, fuller_path, aula_title) #Def utilizada exclusivamente para baixar os arquivos
                        try:
                            #track = f'https://cdn.saladosaber.com.br/HLS/{vimeo_id}.hd/{vimeo_id}.hd.vtt'
                            track = topic_class.find('div', class_='lesson').find('track')['src']
                            if os.path.exists(f'{fuller_path}/{aula_title}.vtt') is False:
                                os.system(f'aria2c -o "{fuller_path}/{aula_title}.vtt" "{track}" --quiet')
                                #urllib.request.urlretrieve(track, filename=f'{fuller_path}/{aula_title}.vtt')
                                print(f'\t\t\t\t{aula_title} - Legenda')
                        except:
                            #print(f'\t\t\t\t{aula_title} - Legenda jã baixada.')
                            pass
                        

    def vimeo_downloader(self, link, path, title): #Em resumo essa def baixa os videos da VIMEO na melhor qualidade possivel

        metodo = 'non'
        video_path = f'{path}/{title}.mp4'
        #https://cdn.saladosaber.com.br/HLS/370394426.hd/370394426.hd.m3u8
        #http://player.vimeo.com/video/370394426/config
        vimeo_link_id = link.split('/')[-1].split('.')[0]
        vimeo_video = f'http://player.vimeo.com/video/{vimeo_link_id}'
        try:
            if os.path.exists(video_path) is False:
                vimeo_headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Dest': 'iframe',
                'Referer': 'https://saladosaber.com.br',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                }

                vimeo_config = requests.get(f'{vimeo_video}/config', headers=vimeo_headers).json()
                vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
                vimeo_url = vimeo_download[-1]['url']

                
                #os.system(f'''ffmpeg -i {vimeo_url} -nostats -loglevel 0 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "{video_path}"''') 
                os.system(f'aria2c -o "{video_path}" "{vimeo_url}" --quiet')
                metodo = 'Aria2c'        
        except:
            pass
        if os.path.exists(video_path) is False:
            os.system(f'ffmpeg -i "{link}" "{video_path}" -preset ultrafast -nostats -loglevel 0')
            metodo = 'FFMPEG'
        print(f'\t\t\t{title} - {metodo}')
            
             
    def download_files(self, text, path, aula_title): #Essa def é utilizada para baixarmos os arquivos disponibilizados pela plataforma

        file_path = f'{path}/Arquivos Disponiveis' #Nosso caminho de download
        files_video = text.find('div', class_='col-12 col-lg-3 lesson-files') 
        files_video = files_video.find('ul', class_='list-unstyled').findAll('li') #Lista exclusiva dos arquivos de cada video separado, quando existir.
        #print(files_video)
        try: #Como não é sempre que pode existir, usamos um try
            files_content = text.find('div', class_='col-12 lesson-files')
            files_content = files_content.find('ul', class_='list-unstyled').findAll('li') #Indexar em lista todos os arquivos
            for files in files_content: #Repetir por todos os arquivos do video.
                file_link = files.find('a')['href'] #Link do arquivo
                file_title = self.replacer(files.find('a').getText().strip()) #Titulo do arquivo
                if os.path.exists(file_path) is False: #Verificador da Pasta ARQUIVOS GERAIS
                    os.makedirs(file_path)
                if os.path.exists(f'{file_path}/{file_title}.pdf') is False:
                    print('\t\t\t' + file_title) #Essa parte verifica se o arquivo existe e faz o download na pasta indicada
                    path_file = f'{file_path}/{file_title}.pdf'
                    os.system(f'aria2c -o "{path_file}" "{file_link}" --quiet') 
                    #urllib.request.urlretrieve(file_link, filename=f'{file_path}/{file_title}.pdf')
        except:
            pass

        for files in files_video: #Repetir por todos os arquivos do video.
            file_link = files.find('a')['href']
            file_title = self.replacer(files.find('a').getText().strip())
            
            if os.path.exists(f'{file_path}/{aula_title}') is False:
                os.makedirs(f'{file_path}/{aula_title}')
            if os.path.exists(f'{file_path}/{aula_title}/{file_title}.pdf') is False:
                print('\t\t\t\t' + file_title) #Essa parte verifica se o arquivo existe e faz o download na pasta indicada
                #urllib.request.urlretrieve(file_link, filename=f'{file_path}/{aula_title}/{file_title}.pdf')
                path_file = f'{file_path}/{aula_title}/{file_title}.pdf'
                os.system(f'aria2c -o "{path_file}" "{file_link}" --quiet')
        
    def replacer(self, text): #Essa Def é responsavel unicicamente por tirar os caracteres incorretos para se ter um PATH
        invalid = {'.pdf': '', '..': '', r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

"""start = Downloader()

print('#####################')
print('   SALA DO SABER')
print('#####################\n')

start.index()""" #Aqui que tudo inicia, chamando nossa classe de Downloader

