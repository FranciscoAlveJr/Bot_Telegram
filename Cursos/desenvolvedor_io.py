import requests
import os
from bs4 import BeautifulSoup as bs

dev_session = requests.Session()

class Downloader():

    def index(self):

        referer = 'https://desenvolvedor.io/'
        
        #ARRAffinity =input('ARRAffinity: ')
        #TiPMix = input('TiPMix: ')
        #Antiforgery = input('.AspNetCore.Antiforgery.w5W7x28NAIs: ')
        #Identity= input('.AspNetCore.Identity.Application: ')
        
        
       # cookies  = {
           # 'ARRAffinity': ARRAffinity,
            #'TiPMix': TiPMix,
           # 'x-ms-routing-name': 'self',
            #'.AspNetCore.Antiforgery.w5W7x28NAIs': Antiforgery,
           # '.AspNetCore.Identity.Application': Identity
       # }

        cookies  = {
            'ARRAffinity': '0f2b91ab120dc45e668f6ed670a6982e261fb6f66bc8e9cd7032f60dfcbeb9be',
            'TiPMix': '22.8656486714564',
            'x-ms-routing-name': 'self',
            '.AspNetCore.Antiforgery.w5W7x28NAIs': 'CfDJ8FvaN4vysXBKjTEDYbMaJb7Y38S5YVQ9qQF2U1Crz3fyPu17-Dq-RCWcvWKwEFq0hFk6WsPiKcrbmyXMyfN0TTxBGNWOhN3x3LIAEjg_WrzWACQeTLZ6b41TMJrhH47Sj2eq34X__nd-QAnoMR-m_Mo',
            '.AspNetCore.Identity.Application': 'CfDJ8FvaN4vysXBKjTEDYbMaJb61MwNJw0hpU4NmmCquY30ZuehDe4FBsBOsoOrMx5VddjLUWNFPEy9aEJ2zc1kylO1QCHT4Bt7ksEJn8bVp9kpB5ujnvZcRWs11_0U9pak1y1V--_Brjq9aL4h-k4sETfHPul9Jc1E_8b6buE4A4MKIxqSsQWNMubF81v1XaYBs-Y-V4F6reeEarmBQjXnY0e2b-H7baGFTi6KWrLIp-20naT0zaJWUBhSkai7WhtsJ6NLWcmhjtkJ6750KQwd7duU6-zwwytZK5rhSdvhil4OQmfNU0H7olSFCeRReqikqUrsVUteCT0MwaAN_boqno24A6nFWFTQJQ1Sa6yEa1rb47w8qhARGMQx6tGiaLXCX5dh4hFAOXF9xU0-t6-PDv2Hk69oKQ9yQJplTdz6QMEi_8otO97fPK_eSlfWzWcougjVlYVCRUYuDPdQAQS7IRzVUOU8e6cco3x9gDecydudjAhHx98BJzxquDuOO39r1PDliKRj7Ovi0L7Q6GnCTjluevdOBBlgXpuXtjrD22LKRos9hKZPsRN60_n6Awzvr4to7jxxbUmKvcPuqoqtFwyv4oEx65IdlN5HiQ9wI2TXnSL4PSr-rsKmz9Ms2fJtvDHyV1C-1REWo3mDIr1GBOAvrnw5Frf_5YNTJ6jG73HAz'
        }


        headers = {
            'authority': 'desenvolvedor.io',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'origin': 'https://desenvolvedor.io',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://desenvolvedor.io/entrar',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        #token = bs(dev_session.get('https://desenvolvedor.io/entrar').content, 'html.parser').find('input', {'name': '__RequestVerificationToken'})['value']
        
        #data = {
        #    'Email': 'guida.mirella22^%^40gmail.com^',
        #    'Password': 'Nuncavaisaber^%^401^',
        #    '__RequestVerificationToken': token
        #}

        #test = dev_session.post('https://desenvolvedor.io/entrar', headers=headers, data=data)
        #print(test)
        dev_dash = dev_session.get('https://desenvolvedor.io/dashboard', cookies=cookies).content
        cursos =  bs(dev_dash,'html.parser').findAll('div', {'class': 'col-lg-4 course_col'})

        for curso in cursos:
            curso_link = curso.find('a')['href']
            aulas = bs(dev_session.get('https://desenvolvedor.io' + curso_link, cookies=cookies).content, 'html.parser')
            aula_title = self.replacer(aulas.find('div', {'class': 'course-sidebar lecture-page collapse navbar-collapse navbar-sidebar-collapse'}).find('h2').getText().strip())
            main = aulas.find('div', {'class': 'course-mainbar'}).findAll('div', {'class': 'row'})
            print(aula_title)
            for count, x in enumerate(main, start=1):
                modulo = self.replacer(x.find('div', {'class': 'section-title'}).getText().strip())
                print(f'{count} - {modulo}')
                videos = x.findAll('li')
                for index, video in enumerate(videos, start=1):
                    link = video.find('a')['href']
                    aula_nome = self.replacer(video.find('a').getText().strip()).split('\r')[0]
                   # aula_nome = aula_nome.split(' -00)')[0][:-2].strip()
                    #if aula_nome[-1] == '(':
                        #aula_nome = aula_nome.split(' -00)')[0][:-3].strip()
                   # if aula_nome[-1] == '-':
                      #  aula_nome = aula_nome[:-2]
                    try:
                        video_content = dev_session.get(f'https://desenvolvedor.io{link}', cookies=cookies).content
                        previmeo = bs(video_content, 'html.parser').find('div', {'id': 'videoPlayer'})['data-vimeo-url']#.find('iframe')['src'].split('?')[0]
                    except:
                        continue
                    path = f'Cursos/{aula_title}/{count} - {modulo}'
                    if os.path.exists(path) is False:
                        os.makedirs(path)
                    video_path = f'{path}/{index} - {aula_nome}.mp4'
                    if os.path.exists(video_path) is False:
                        self.get_video(previmeo, video_path, referer)
                    print(f'{index} - {aula_nome}')

    def replacer(self, text):
            invalid = {'  ':' ', r'"': r"'", '\\': " - ", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
            for char in invalid:
                if char in text:
                    text = text.replace(char, invalid[char])
            return text
    
    def get_video(self, video, path, referer='https://vimeo.com'):

        if os.path.exists(path) is False:
            vimeo_headers = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Dest': 'iframe',
                'Referer': f'{referer}',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }

            vimeo_url = f'{video}/config'
            
            while True:
                try:
                    vimeo_config = requests.get(vimeo_url, headers=vimeo_headers).json()
                    break
                except:
                    continue

            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])[-1]['url']
            os.system(f'aria2c -o "{path}" {vimeo_download} --quiet')


#Downloader().index()