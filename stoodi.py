import requests
from bs4 import BeautifulSoup as bs
import json
import os

stoodi_session = requests.Session()


class Downloader:

    def index(self):

        cookies = {
            'initial_http_referer': 'https://www.google.com/',
            'initial_url': '/',
            'i_dt': '2021-03-06 19:10:54.487755',
            'stoodi_first_url': 'https://www.stoodi.com.br/',
            'stoodi_web_first_url': 'https://www.stoodi.com.br/',
            'stoodi_first_referrer': 'https://www.google.com/',
            'm_jrn': '7',
            'csrftoken': '6iDgrGSpPsZ0aEAg6kTNfgWZovXld9dqX7px5dhNlCOhvGqaiFTEwVC6NOF8obb8',
            'sideMenuToggle': '0',
            'alert_app': '1',
            'is_subscriber': 'false',
            'AWSALBTG': 'zDyouATthd8auDS8T4tOSQAuJt4ztjMiTqeN/FVKN15TVndXfHy8qIeuT77wEjUshWADinypDWd6+LPclLScTP3qdrj6zMjZqRqLJjIafXjRSxuYYXsho8MNMvm1mZwobqex+HD/VUkMh2VOtyDpmmeS2Hpwzs4uEdjsVqbHfK8pP/XgHm4=',
            'AWSALBTGCORS': 'zDyouATthd8auDS8T4tOSQAuJt4ztjMiTqeN/FVKN15TVndXfHy8qIeuT77wEjUshWADinypDWd6+LPclLScTP3qdrj6zMjZqRqLJjIafXjRSxuYYXsho8MNMvm1mZwobqex+HD/VUkMh2VOtyDpmmeS2Hpwzs4uEdjsVqbHfK8pP/XgHm4=',
        }

        headers = {
            'Host': 'www.stoodi.com.br',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://www.stoodi.com.br',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-gpc': '1',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.stoodi.com.br/login/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        email = 'ocoisa081@gmail.com'
        senha = '18020301.pP'

        data = f'plan=None&credit_amount=None&promoCodeLogin=None&csrfmiddlewaretoken=QT8rq8YgewxdGhMELSYbcjACRpBA09paHIUI4FnEKGmu1jCyXdY2tYgJgIjnbbnS&username={email}&password={senha}&next=%2Flogin%2F'

        response = stoodi_session.post('https://www.stoodi.com.br/login/', headers=headers, cookies=cookies, data=data).content

        materias = bs(response, 'html.parser').find('nav', {'class': 'areaList'}).findAll('li')
        for x in materias:
            link = x.find('a')['href']
            self.get_materia(link)
    
    def get_materia(self, materia):

        response = stoodi_session.get(f'https://www.stoodi.com.br{materia}').content
        parser = bs(response, 'html.parser')
        materia_titulo = self.replacer(parser.find('header', {'class': 'c-page-header c-calendar__title'}).text.strip()) #TODO:
        areas = parser.findAll('div', {'class': 'c-subareas'})
        
        print(materia_titulo)
        for area in areas:
            
            self.get_area(area, materia_titulo)

    def get_area(self, area, path):
        area_title = self.replacer(area.find('h2').text.strip())  #TODO:
        video_path = f'{path}/{area_title}'
        print('\t' + area_title)
        sub_areas = area.findAll('div', {'class': 'c-subareas__list-modules'})
        for subarea in sub_areas:
            other_areas = subarea.findAll('div', {'class': 'c-card c-card--outline'})
            for i in other_areas:

                new_area = i.find('a', {'class': 'c-card__link'})
                self.get_sub_area(new_area, video_path)

    def get_sub_area(self, subarea, video_path):

        subarea_title = self.replacer(subarea.find('h4').text.strip())  #TODO:
        video_path = f'{video_path}/{subarea_title}'
        
        print('\t\t' + subarea_title)
        link = subarea['href']

        response = stoodi_session.get(f'https://www.stoodi.com.br{link}').content
        parser = bs(response, 'html.parser')
        self.get_content(parser, video_path)

    def get_content(self, content, path):

        videos = content.find('nav', {'class': 'c-sidebar__nav'}).findAll('a', {'aria-current': 'page'})
        try:
            resumo = content.find('a', {'class': 'summary'})['href']
        except:
            resumo = ''
            pass
        path = self.os_makedirs(path)
        if resumo != '':
            resumo_path = f'{path}/Resumo Teórico.pdf'
            if os.path.exists(resumo_path) is False:
                print('\t\t\t' + resumo_path, end='')
                self.get_resumo(resumo, resumo_path)
            else:
                print(f'\t\t\t[ALREADY DOWNLOADED] - {resumo_path}')

        
        for video in videos:
            #base = video.find('a', {'class': 'c-sidebar__item play logged'})
            link = video['href']
            title = self.replacer(video.find('span', {'class': 'c-sidebar__item-txt'}).text.strip()) #TODO:
            path = self.os_makedirs(path)
            video_path = f'{path}/{title}.mp4'
            if os.path.exists(video_path):
                continue
            response = stoodi_session.get(f'https://www.stoodi.com.br{link}').content
            parser = bs(response, 'html.parser')
            infos = parser.find('section', {'class': 'c-classroom__content'})
            userid = infos.find('input', {'id': 'userid'})['value']
            videoid = infos.find('input', {'id': 'videoid'})['value']

            csrfmiddlewaretoken = parser.find('input', {'name': 'csrfmiddlewaretoken'})['value']

            data = {
            'userid': userid,
            'videoid': videoid,
            'csrfmiddlewaretoken': csrfmiddlewaretoken
            }
            print('\t\t\t' + title, end='')
            string = self.get_video_string(data)
            link = self.decrypt_video(string)



            self.download_video(link, video_path)

    def get_resumo(self, link, path):

        cookies = stoodi_session.cookies.get_dict()

        response = stoodi_session.get(f'https://www.stoodi.com.br{link}').content
        
        try:
            parser = bs(response, 'html.parser').find('a', {'class': 'summaryDownload-js btn -blue'})['href']
        except:
            parser = f'https://www.stoodi.com.br{link}'
            pass

        headers_aria = f'Cookie: csrftoken={cookies["csrftoken"]}; sessionid={cookies["sessionid"]}; AWSALBTG={cookies["AWSALBTG"]}; AWSALBTGCORS={cookies["AWSALBTGCORS"]}'

        link = f'https://www.stoodi.com.br{parser}'
        if os.path.exists(path) is False:
            handle = os.system(f'aria2c -o "{path}" "{link}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5 --header="{headers_aria}"' )

            if handle == 0:
                print(f'[DOWNLOADED] - {path}')
            else:
                print(f'[NOT DOWNLOADED | [ERROR: {handle}] - {path} - {link}')
        else:
            print(f'[ALREADY DOWNLOADED] - {path}')

    def download_video(self, link, path):

        if os.path.exists(path) is False:
            handle = os.system(f'aria2c -o "{path}" "{link}" --auto-file-renaming=false --retry-wait=5 --continue=true --check-integrity=true --quiet --max-connection-per-server=5')

            if handle == 0:
                print(f'[DOWNLOADED] - {path}')
            else:
                print(f'[NOT DOWNLOADED | [ERROR: {handle}] - {path} - {link}')
        else:
            print(f'[ALREADY DOWNLOADED] - {path}')
            
    def decrypt_video(self, s):


        #s = s.replace('=', '')
        e = {}
        b = 0
        l = 0
        r = ''
        w = chr
        L = len(s)
        A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

        for i in range(64):
            e[A[i]] = i

        for x in range(L):
            try:
                c = e[s[x]]
            except KeyError:
                continue
            b = (b << 6) + c
            l += 6
            while l >= 8:
                l -= 8
                a = (b >> l) & 0xff
                if (a < 0):
                    a *= -1

                if (a or x < L - 2):
                    r += w(a)

        return r

    def get_video_string(self, data):

        cookies = stoodi_session.cookies.get_dict()
        
        headers = {
            'authority': 'www.stoodi.com.br',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'sec-gpc': '1',
            'origin': 'https://www.stoodi.com.br',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.stoodi.com.br/materias/fisica/notacao-cientifica/notacao-cientifica/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'initial_http_referer="https://www.google.com/"; initial_url="/"; i_dt="2021-03-06 19:10:54.487755"; stoodi_first_url="https://www.stoodi.com.br/"; stoodi_web_first_url="https://www.stoodi.com.br/"; stoodi_first_referrer="https://www.google.com/"; sideMenuToggle=0; alert_app=1; is_subscriber=false; m_jrn={cookies["m_jrn"]}; csrftoken={cookies["csrftoken"]}; sessionid={cookies["sessionid"]}; AWSALBTG={cookies["AWSALBTG"]}; AWSALBTGCORS={cookies["AWSALBTGCORS"]}',
        }
        response = requests.post('https://www.stoodi.com.br/video/can-watch', headers=headers, data=data).json()['v']['mp4']
        base = 0
        for k, v in response.items():
            if int(k) > base:
                base = int(k)
                link = v

                return link

    def inative_get_video_link(self, link):

        base = """
        var s = 'linkoso'
        function dcrpt(s) {
            
            var e = #*, i, b = 0, c, x, l = 0, a, r = '', w = String.fromCharCode, L = s.length;
            var A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
            for (i = 0; i < 64; i++) {
                e[A.charAt(i)] = i;
            }
            for (x = 0; x < L; x++) {
                c = e[s.charAt(x)];
                b = (b << 6) + c;
                l += 6;
                while (l >= 8) {
                    ((a = (b >>> (l -= 8)) & 0xff) || x < L - 2) && (r += w(a));
                }
            }
            return r;
        }
        dcrpt(s)
        """
        with_link = base.replace('linkoso', link)
        with_dict = with_link.replace('#', '{').replace('*', '}')

        link = js2py.eval_js(with_dict)
        return link

    def os_makedirs(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)

        return path

    def error_message(self):

        print('Erro. Finalizando')
        exit(0)

    def replacer(self, text):
        
        invalid = {"ª": "a","º": "o", r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        
        return text

