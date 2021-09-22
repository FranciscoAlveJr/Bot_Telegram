import requests
import json
from bs4 import BeautifulSoup as bs
import os

upinside_session = requests.Session()


class Download():

    def index(self):
        upinside_session.headers = {'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'en-US,en;q=0.8',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Connection': 'keep-alive'}

        username = 'ocoisa081@gmail.com'
        password = '18020301.pP'
        data = {'email': username, 'password': password, 'case': 'login_login'}
        upinside_session.post('https://www.upinside.com.br/beta/_app/dash.php', data=data) 
        upinside_source = upinside_session.get('https://www.upinside.com.br/beta/cursos/meuscursos')
        upinside_soup = bs(upinside_source.text, 'html.parser')
        upinside_list_courses = upinside_soup.find_all('a', class_='dash_view_inline_course_btn')
        for upinside_course in upinside_list_courses:
            upinside_course_url = upinside_course['href']
            self.get_cursos(upinside_course_url)

    def get_cursos(self, url):
        upinside_get_course = upinside_session.get(url)
        upinside_course_info = bs(upinside_get_course.text, 'html.parser')
        upinside_course_title = upinside_course_info.find('h2', 'dash_main_header_view').find('a').get('title')
        # Titulo do curso
        upinside_course_path = upinside_course_title
        if os.path.exists(upinside_course_path) is False:
            os.makedirs(upinside_course_path)
        upinside_course_modules = upinside_course_info.find_all('section', class_='dash_view_course_module')
        for count, upinside_modules in enumerate(upinside_course_modules, start=1):
            upinside_module_title = upinside_modules.find('header', class_='dash_view_course_module_header').find(
                'h2').getText().strip()
            # Titulo do Modulo
            path = f'{upinside_course_path}/{count} - {upinside_module_title}'
            upinside_course_classes = upinside_modules.find_all('a', class_='dash_view_course_module_class_link')
            for counter, upinside_course_class in enumerate(upinside_course_classes, start=1):
                upsinde_course_class_url = upinside_course_class.get('href')
                upinside_class = upinside_session.get(upsinde_course_class_url)
                upinside_class_info = bs(upinside_class.text, 'html.parser')
                upinside_class_video = upinside_class_info.find('iframe', class_='dash_view_class_media_player_vimeo').get('src').split('?')[0] + '/config'
                upinside_class_name = upinside_class_info.find('h2', class_='dash_main_header_view').getText().split('/')[-1]
                # Titulo da Aula

                upinside_class_download = f'{path}/{counter} - {upinside_class_name}.mp4'
                temp_headers = {'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'en-US,en;q=0.8',
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                'Referer': 'https://www.upinside.com.br/', 'Connection': 'keep-alive'}
                vimeo_video = requests.get(upinside_class_video, headers=temp_headers).json()
                vimeo_download = sorted(vimeo_video["request"]["files"]["progressive"], key=lambda i: i['height'])
                vimeo_url = vimeo_download[-1]['url']
                if os.path.exists(upinside_class_download) is False:
                    os.system(f'aria2c -o "{upinside_class_download}" "{vimeo_url}" --quiet')
                    print(upinside_class_download)

        upinside_last_class = upsinde_course_class_url
        upinside_last_class_info = bs(upinside_session.get(upinside_last_class).text, 'html.parser')
        upinside_folder = upinside_last_class_info.find('div', class_='dash_view_class_folder')
        upinside_folder_title = upinside_folder.find('p', class_='dash_view_class_folder_title').getText()
        upinside_folders = upinside_folder.find_all('div', class_='dash_view_class_folder_content_f')
        upinside_folders_path = f'{upinside_course_title}/{upinside_folder_title}'

        if os.path.exists(upinside_folders_path) is False:
            os.makedirs(upinside_folders_path)
        for upinside_folder in upinside_folders:
            upinside_archive = upinside_folder.find('a')
            upinside_archive_title = upinside_archive.getText().strip()
            upinside_archive_download = upinside_archive.get('href')
            upinside_archive_path = f'{upinside_folders_path}/{upinside_archive_title}.zip'
            if os.path.exists(upinside_archive_path) is False:
                #urllib.request.urlretrieve(upinside_archive_download, filename=upinside_archive_path)
                os.system(f'aria2c -o "{upinside_archive_path}" "{upinside_archive_download}" --quiet')
                print(upinside_archive_path)

"""bot = Download()
bot.index()
"""