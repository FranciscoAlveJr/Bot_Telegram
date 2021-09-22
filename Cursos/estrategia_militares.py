import requests
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time

os.system('cls')
estrategia_session = requests.Session()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.maximize_window()

class Downloader():

    def index(self):

        self.selenium_part()

        #cookies = {'sessionid': sessionid, 'csrftoken': csrftoken}
        

        selenium_cookies = driver.get_cookies()
        cookies = {}
        for cookie in selenium_cookies:
            cookies[cookie['name']] = cookie['value']
        self.account_header = {
            'authority': 'www.estrategiamilitares.com.br',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://www.estrategiamilitares.com.br',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.estrategiamilitares.com.br/autenticacao/login/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'csrftoken={cookies["csrftoken"]}; sessionid={cookies["sessionid"]}',
        }

        estrategia_session.headers.update(self.account_header)
        conta = estrategia_session.get('https://www.estrategiamilitares.com.br/aluno/perfil', headers=self.account_header, cookies=cookies)
        nome = bs(conta.content, 'html.parser').find('div', class_='name').getText()
        os.system('cls')
        print('Você está logado como ', end='')
        print(nome[4:-1])
        self.meus_cursos(cookies)
        self.meus_simulados(cookies)
    
    def selenium_part(self):

        driver.get('https://www.estrategiamilitares.com.br/autenticacao/login/')
        email = 'lucassantosmed69@gmail.com'#input('Login: ') #
        senha = 'engrumec' #input('Senha: ') #
        email = 'yagosatir@gmail.com'
        senha = 'Gpws14789'

        driver.find_element_by_xpath('/html/body/div/main/div/form/div/div/div/div[1]/div[1]/input').send_keys(email)
        driver.find_element_by_xpath('/html/body/div/main/div/form/div/div/div/div[1]/div[1]/input').send_keys(Keys.TAB, senha, Keys.RETURN)

    def meus_cursos(self, cookies):
        
        print('Iniciando a aba MEUS CURSOS')
        infos = estrategia_session.get('https://www.estrategiamilitares.com.br/aluno/', headers=self.account_header, cookies=cookies)
        cursos = bs(infos.content, 'html.parser').findAll('div', class_='card-body')
        
        for curso in cursos:
            curso_info = curso.find('a')
            curso_link = curso_info['href']
            curso_nome = self.replacer(curso_info.getText().strip())
            
            self.actual_path = self.criar_pasta(f'Militares/Meus Cursos/{curso_nome}')
            curso_parser = bs(estrategia_session.get(f'https://www.estrategiamilitares.com.br{curso_link}', headers=self.account_header, cookies=cookies).content, 'html.parser')
            find_script = curso_parser.findAll('script')
            for script in find_script:
                script = script.prettify()
                if 'title' in script:
                    base_info = script
                    break
                    
            base_info = base_info.split('var app = ')[1].split('app.$data.lectures =')[-1]#.split(';')[0]
            if 'title' in base_info:
                pass
            else:
                base_info = script.split('var app = ')[1].split('data: ')[-2]#.split(';')[0]
            base_info = base_info.replace('\t', '').replace('\n', '').replace(')', '')#.replace("\'", '"').replace('[],},]},}', '[]}]}}')
            base_info = base_info.replace('summaries:', '"summaries":')
            base_info = base_info.replace('videos:', '"videos":')
            base_info = base_info.replace('books:', '"books":')
            base_info = base_info.replace('maps:', '"maps":')
            base_info = base_info.replace('slides:', '"slides":')
            base_info = base_info.replace('trails:', '"trails":')
            base_info = base_info.replace('title:', '"title":')
            base_info = base_info.replace('is_published:', '"is_published":')
            base_info = base_info.replace('is_pdf_published:', '"is_pdf_published":')
            base_info = base_info.replace('is_video_published:', '"is_video_published":')
            base_info = base_info.replace('has_files:', '"has_files":')
            base_info = base_info.replace('has_video:', '"has_video":')
            base_info = base_info.replace('has_book:', '"has_book":')
            base_info = base_info.replace('pdf_publish_at:', '"pdf_publish_at":')
            base_info = base_info.replace('video_publish_at:', '"video_publish_at":')
            base_info = base_info.replace('publish_at:', '"publish_at":')
            base_info = base_info.replace('lectures:', '"lectures":')
            base_info = base_info.replace('currentIndex:', '"currentIndex":')
            base_info = base_info.replace('currentMenu:', '"currentMenu":')
            base_info = base_info.replace('currentMenuEssays:', '"currentMenuEssays":')
            base_info = base_info.replace('course:', '"course":')
            base_info = base_info.replace(': false', ": 'false'")
            base_info = base_info.replace(': true', ": 'true'")
            base_info = base_info.replace(',}','}')
            base_info = base_info.replace(',]',']')
            base_info = base_info.replace("'", '"')
            base_info = base_info.replace(',  ]', ']')
            base_info = base_info.replace('[  ', '[')
            base_info = base_info.replace("\'", '"')            
            if '&quot;' in base_info:
                base_info = base_info.replace('&quot;', "'")
            if '&#39;' in base_info:
                base_info = base_info.replace('&#39;', '')             
            base_info = base_info.split('</script>')[0]
            #base_info = base_info[:-1]
            
            
            try:
                data = json.loads(base_info)
                pass
            except Exception as e:
                print(base_info)
                any_error = open('Error_file.json', 'w', encoding='utf-8')
                with any_error as out_error:
                    out_error.write(json.dumps(base_info))
                print('ERRO AQUI')
                print(e)
                driver.close()
                print(f'"{base_info[ 54747: 54748]}"')
                print(f'"{base_info[ 54740: 54760]}"')
                exit(0)
            ###lectures = data['lectures']
            os.system('cls')
            print(curso_nome)
            for lecture in data:
                title_l = self.replacer(lecture['title']).strip()
                self.actual_path = self.criar_pasta(f'Militares/Meus Cursos/{curso_nome}/{title_l}')
                print(f'\t{title_l}')
                videos = lecture['videos']
                books = lecture['books']
                maps = lecture['maps']
                slides = lecture['slides']
                trails = lecture['trails']
                summaries = lecture['summaries']
                pdfs = [books, maps, slides, summaries, trails]
                for index, video in enumerate(videos, start=1):
                    self.actual_path = self.criar_pasta(f'Militares/Meus Cursos/{curso_nome}/{title_l}/Videos')
                    title = self.replacer(video['title']).strip()
                    path = f'{self.actual_path}/{index} - {title}.mp4'
                    if os.path.exists(path) is False:
                        link = f"https://www.estrategiamilitares.com.br{video['url']}"
                        driver.execute_script(f'''window.open("{link}","_blank");''')
                        time.sleep(3)
                        driver.switch_to.window(driver.window_handles[1])
                        new_link = driver.current_url
                        if 'estrategiamilitares' in new_link:
                            input('Resolva o captcha e aperte ENTER.')
                            new_link = driver.current_url

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                        self.baixar_video(path, new_link)

                for pdf in pdfs:
                    for index, archive in enumerate(pdf, start=1):
                        self.actual_path = self.criar_pasta(f'Militares/Meus Cursos/{curso_nome}/{title_l}/PDF')
                        title = self.replacer(archive['title']).strip()
                        path = f'{self.actual_path}/{index} - {title}.pdf'
                        if os.path.exists(path) is False:
                            link = f"https://www.estrategiamilitares.com.br{archive['url']}"
                            driver.execute_script(f'''window.open("{link}","_blank");''')
                            time.sleep(3)
                            driver.switch_to.window(driver.window_handles[1])
                            new_link = driver.current_url
                            if 'estrategiamilitares' in new_link:
                                input('Resolva o captcha e aperte ENTER.')
                                new_link = driver.current_url
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            
                            #print(new_link)
                            self.baixar_pdf(path, new_link)

    def meus_simulados(self, cookies):
        
        print('Iniciando a aba MEUS SIMULADOS')
        infos = estrategia_session.get('https://www.estrategiamilitares.com.br/aluno/simulados', headers=self.account_header, cookies=cookies)
        cursos = bs(infos.content, 'html.parser').findAll('div', class_='card-body')
        
        for curso in cursos:
            curso_info = curso.find('a')
            curso_link = curso_info['href']
            curso_nome = self.replacer(curso_info.getText().strip())
            
            self.actual_path = self.criar_pasta(f'Militares/Meus Simulados/{curso_nome}')
            curso_parser = bs(estrategia_session.get(f'https://www.estrategiamilitares.com.br{curso_link}', headers=self.account_header, cookies=cookies).content, 'html.parser')
            find_script = curso_parser.find('body').findAll('script')
            for script in find_script:
                script = script.prettify()
                if 'title' in script:
                    base_info = script
                    break

                    
            base_info = base_info.split('var app = ')[1].split('app.$data.lectures =')[-1]#.split(';')[0]
            if 'title' in base_info:
                pass
            else:
                base_info = script.split('var app = ')[1].split('data: ')[-2]#.split(';')[0]
            base_info = base_info.replace('\t', '').replace('\n', '').replace(')', '')#.replace("\'", '"').replace('[],},]},}', '[]}]}}')
            base_info = base_info.replace('summaries:', '"summaries":')
            base_info = base_info.replace('videos:', '"videos":')
            base_info = base_info.replace('books:', '"books":')
            base_info = base_info.replace('maps:', '"maps":')
            base_info = base_info.replace('slides:', '"slides":')
            base_info = base_info.replace('trails:', '"trails":')
            base_info = base_info.replace('title:', '"title":')
            base_info = base_info.replace('is_published:', '"is_published":')
            base_info = base_info.replace('is_pdf_published:', '"is_pdf_published":')
            base_info = base_info.replace('is_video_published:', '"is_video_published":')
            base_info = base_info.replace('has_files:', '"has_files":')
            base_info = base_info.replace('has_video:', '"has_video":')
            base_info = base_info.replace('has_book:', '"has_book":')
            base_info = base_info.replace('pdf_publish_at:', '"pdf_publish_at":')
            base_info = base_info.replace('video_publish_at:', '"video_publish_at":')
            base_info = base_info.replace('publish_at:', '"publish_at":')
            base_info = base_info.replace('lectures:', '"lectures":')
            base_info = base_info.replace('currentIndex:', '"currentIndex":')
            base_info = base_info.replace('currentMenu:', '"currentMenu":')
            base_info = base_info.replace('currentMenuEssays:', '"currentMenuEssays":')
            base_info = base_info.replace('course:', '"course":')
            base_info = base_info.replace(': false', ": 'false'")
            base_info = base_info.replace(': true', ": 'true'")
            base_info = base_info.replace(',}','}')
            base_info = base_info.replace(',]',']')
            base_info = base_info.replace("'", '"')
            base_info = base_info.replace(',  ]', ']')
            base_info = base_info.replace('[  ', '[')
            base_info = base_info.replace("\'", '"')            
            if '&quot;' in base_info:
                base_info = base_info.replace('&quot;', "'")
            if '&#39;' in base_info:
                base_info = base_info.replace('&#39;', '')             
            base_info = base_info.split('</script>')[0]
            
            
            try:
                data = json.loads(base_info)
            except Exception as e:
                print(base_info)
                any_error = open('Error_file.json', 'w', encoding='utf-8')
                with any_error as out_error:
                    out_error.write(json.dumps(base_info))
                print('ERRO AQUI')
                print(e)
            os.system('cls')
            print(curso_nome)
            for lecture in data:
                title_l = self.replacer(lecture['title']).strip()
                self.actual_path = self.criar_pasta(f'Militares/Meus Simulados/{curso_nome}/{title_l}')
                print(f'\t{title_l}')
                videos = lecture['videos']
                books = lecture['books']
                maps = lecture['maps']
                slides = lecture['slides']
                trails = lecture['trails']
                summaries = lecture['summaries']
                pdfs = [books, maps, slides, summaries, trails]
                for index, video in enumerate(videos, start=1):
                    self.actual_path = self.criar_pasta(f'Militares/Meus Simulados/{curso_nome}/{title_l}/Videos')
                    title = self.replacer(video['title']).strip()
                    path = f'{self.actual_path}/{index} - {title}.mp4'
                    if os.path.exists(path) is False:
                        link = f"https://www.estrategiamilitares.com.br{video['url']}"
                        driver.execute_script(f'''window.open("{link}","_blank");''')
                        time.sleep(3)
                        driver.switch_to.window(driver.window_handles[1])
                        new_link = driver.current_url
                        if 'estrategiamilitares' in new_link:
                            input('Resolva o captcha e aperte ENTER.')
                            new_link = driver.current_url

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                        self.baixar_video(path, new_link)
                        self.baixar_video(path, new_link)

                for pdf in pdfs:
                    for index, archive in enumerate(pdf, start=1):
                        self.actual_path = self.criar_pasta(f'Militares/Meus Simulados/{curso_nome}/{title_l}/PDF')
                        title = self.replacer(archive['title']).strip()
                        path = f'{self.actual_path}/{title}.pdf'
                        if os.path.exists(path) is False:
                            link = f"https://www.estrategiamilitares.com.br{archive['url']}"
                            driver.execute_script(f'''window.open("{link}","_blank");''')
                            time.sleep(3)
                            driver.switch_to.window(driver.window_handles[1])
                            new_link = driver.current_url
                            if 'estrategiamilitares' in new_link:
                                input('Resolva o captcha e aperte ENTER.')
                                new_link = driver.current_url
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            
                            #print(new_link)
                            self.baixar_pdf(path, new_link)



    def baixar_video(self, path, url):
        
        if os.path.exists(path) is False:
            os.system(f'aria2c -o "{path}" "{url}" --quiet --continue=true')
            print(f'\t\t{path.split("/")[-1]}')
        time.sleep(1)
        if os.path.exists(path) is False:
            try:
                video_path = open(path, 'wb')
                video_content = requests.get(url).content
                with video_path as video_out:
                    video_out.write(video_content)
                print(f'\t\t{path.split("/")[-1]} - Request')
            except:
                pass
        
    def baixar_pdf(self, path, url):
        
        if os.path.exists(path) is False:
            os.system(f'aria2c -o "{path}" "{url}" --quiet --continue=true')
            print(f'\t\t{path.split("/")[-1]} - Aria2c')
        time.sleep(1)
        if os.path.exists(path) is False:
            try:
                pdf_path = open(path, 'wb')
                pdf_content = requests.get(url).content
          
                with pdf_path as pdf_out:
                    pdf_out.write(pdf_content)
                print(f'\t\t{path.split("/")[-1]} - Request')
            except:
                pass
    def criar_pasta(self, path):
        
        if os.path.exists(path) is False:
            os.makedirs(path)

        return path

    def replacer(self, text):
        invalid = {'p/': 'para', '\t': '', r'"': r"'", '\\': " - ", "/": "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text         



"""start = Downloader()
start.index()"""





