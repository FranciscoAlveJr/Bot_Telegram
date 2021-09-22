import requests
from xhtml2pdf import pisa
import json
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import urllib
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()

aulatica_session = requests.session()


class Downloader:

    def index(self):
        headers_for_login = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        login_page = bs(aulatica_session.get('https://aulatica.eadbox.com/login', headers=headers_for_login).content, 'html.parser')  
        authenticity_token = login_page.find('meta', {'name': 'csrf-token'})['content']
        #print(authenticity_token)

        data = {
            'utf8': '✓',
            'authenticity_token': authenticity_token,
            'user[email]': 'santosfelipe298@gmail.com',
            'user[password]': 'upaparamim',
            'commit': 'Login',
            'user[remember_me]': 0
            }

        aulatica_session.post('https://aulatica.eadbox.com/login', headers=headers_for_login, data=data)
        self.headers = {
            'authority': 'aulatica.eadbox.com',
            'accept': 'application/json, text/plain, */*',
            'x-newrelic-id': 'VgIGWV9XDhADUFBRBAgEUVc=',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://aulatica.eadbox.com/ng/student/courses/?page=1',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': '__cfduid=d0faa7b7aff4162bb41d5360d104b71ab1592441134; ajs_group_id=null; ajs_anonymous_id=^%^228f9b535e-3be2-4592-8913-642b06141f33^%^22; ajs_user_id=^%^225ee8f795c04a12001988270f^%^22; intercom-id-dlobwdcf=a0a28ee5-9e9c-4b28-be89-7c10aad77c9b; intercom-session-dlobwdcf=; _53542=http://10.60.27.12:8080; _session_id=ce7afabad8e34f778fb25223bb701a49',
            'if-none-match': 'W/^\\^eb4a6b2229a7fe0145826bbc69917e04^\\^',
            'if-modified-since': 'Thu, 18 Jun 2020 17:25:59 GMT',
        }
        self.selenium_part()
        self.get_infos()

    def selenium_part(self):

        driver.get('https://aulatica.eadbox.com/login')
        driver.find_element_by_id("user_email").send_keys('santosfelipe298@gmail.com')
        driver.find_element_by_id("user_password").send_keys('reliquiazero')
        driver.find_element_by_id("user_password").send_keys(Keys.RETURN)
        
    def get_infos(self):
        
        self.subscription_id = json.loads(aulatica_session.get('https://aulatica.eadbox.com/ng/api/saas.json', headers=self.headers).content)['_id']
        subscriptions = []
        get_pages = json.loads(aulatica_session.get('https://aulatica.eadbox.com/ng/api/student/subscriptions.json', headers=self.headers).content)['links']['total_pages']
        #print(get_pages)
        for pages in range(1, get_pages+1):
            #print(pages)
            get_page = json.loads(aulatica_session.get(f'https://aulatica.eadbox.com/ng/api/student/subscriptions.json?page={pages}', headers=self.headers).content)['subscriptions']
            for item in get_page:
                subscriptions.append(item)
        self.get_course(subscriptions)
        print(f'\n\n\nForam baixados {self.videos_done} videos')

    def get_course(self, subscriptions):
        #print(self.subscription_id)
        #Trabalhando com a lista recebida
        print(f'Aulática | {datetime.now().strftime("%H:%M:%S")}')
        self.videos_done = 0
        videos_error = 0
        for curso in subscriptions:
            category_name = self.replacer(str(curso['category_name']).strip())
            course_title = self.replacer(str(curso["course"]["title"]).strip())
            print(f'\t{category_name}')
            print(f'\t\t{course_title}')

            course_slug = curso["course"]["course_slug"]
            
            self.course_id = json.loads(aulatica_session.get(f'https://aulatica.eadbox.com/ng/api/student/courses/{course_slug}.json', headers=self.headers).content)['course_id']

            self.lectures = json.loads(aulatica_session.get(f'https://aulatica.eadbox.com/ng/api/student/courses/{course_slug}/subscription.json', headers=self.headers).content)['lectures']

            for lecture in self.lectures:
                lecture_title = self.replacer(str(lecture['title']).strip())
                print(f'\t\t\t{lecture_title}')
                contents = lecture['contents']
                lecture_slug = lecture['lecture_slug']
                for count, content in enumerate(contents):
                    count += 1
                    self.content_id = content['content_id']
                    content_title = self.replacer(str(content['title']).strip())
                    path = f'Aulática/{category_name}/{course_title}/{lecture_title}'
                    if os.path.exists(path) is False:
                         os.makedirs(path)
                    
                    if content['type'] == 'coconut_video' or content['type'] == 's3_video':
                        video_link = f'https://media.eadbox.com/saas_uploads/{self.subscription_id}/{self.course_id}#/{self.content_id}/contents/coconut_video/fhd_mp4_file/fhd_mp4_video.mp4'
                        filename = f'{path}/{count} - {content_title}.mp4'
                        video_down = aulatica_session.get(video_link, headers=self.headers)
                        if os.path.exists(filename) is False:
                            if video_down.status_code == 200:
                                os.popen(f'aria2c -o "{filename}" {video_link} -q')
                                print(f'\t\t\t\t{content_title} - Video - Requests!')
                            else:
                                driver.get(f'https://aulatica.eadbox.com/ng//student/courses/{course_slug}/lectures/{lecture_slug}/contents/{self.content_id}')
                                time.sleep(10)
                                try:
                                    time.sleep(5)
                                    video_link = driver.find_element_by_id('vjs_video_3_html5_api')#.get_attribute("src")
                                    video_link = video_link.find_elements_by_tag_name('source')[-1]
                                except:
                                    time.sleep(5)
                                    try:
                                        video_link = driver.find_element_by_class_name('vjs-tech')#.get_attribute("src")
                                        video_link = video_link.find_elements_by_tag_name('source')[-1]
                                    except:
                                        print(f'\t\t\t\t{content_title} - VIDEO COM ERRO')
                                        continue
                                
                                video_download = video_link.get_attribute("src")
                            #urllib.request.urlretrieve(video_download, filename=filename)
                                os.popen(f'aria2c -o "{filename}" {video_download} -q')
                                print(f'\t\t\t\t{content_title} - Video - Selenium!')
                        self.videos_done += 1
                        
                    if content['type'] == 'article':
                        print(f'\t\t\t\t{count} - {content_title} - Artigo')
                        article = str(json.loads(aulatica_session.get(f'https://aulatica.eadbox.com/ng/api/student/courses/{course_slug}/subscription/lectures/{lecture_slug}/contents/{self.content_id}.json', headers=self.headers).content)['article'])
                        filename = f'{path}/{count} - {content_title}.pdf'
                        filename_html = f'{path}/{count} - {content_title}.html'
                        if os.path.exists(filename) is False:
                            try:
                                self.convert_html_to_pdf(article, filename)
                            except:
                                with open(filename_html, 'w') as output:
                                    output.write(article)
                            
                    if content['type'] == 'new_box_view_document':
                        print(f'\t\t\t\t{count} - {content_title} - PDF')
                        filename = f'{path}/{count} - {content_title}.pdf'
                        if os.path.exists(filename) is False:
                            try:
                                pdf_file = json.loads(aulatica_session.get(f'https://aulatica.eadbox.com/ng/api/student/courses/{course_slug}/subscription/lectures/{lecture_slug}/contents/{self.content_id}.json', headers=self.headers).content)['pdf_download_url']
                            except:
                                pdf_file = json.loads(aulatica_session.get(f'https://aulatica.eadbox.com/ng/api/student/courses/{course_slug}/subscription/lectures/{lecture_slug}/contents/{self.content_id}.json', headers=self.headers).content)['file']         
                            urllib.request.urlretrieve(pdf_file, filename=filename)
                            


    #['', 'article', 'new_box_view_document', 'coconut_video', 's3_video']

    def convert_html_to_pdf(self, source_html, output_filename):

        result_file = open(output_filename, "w+b")

        pisa_status = pisa.CreatePDF(source_html, dest=result_file)
        result_file.close() 



    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - ', '\t': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text 

"""start_time = datetime.now().strftime("%H:%M:%S")
#start = Downloader()
os.system('cls')
#start.index()

print(f'Aulática\nInicio: {start_time}\nFim: {datetime.now().strftime("%H:%M:%S")}')"""