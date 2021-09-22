import requests
from bs4 import BeautifulSoup as bs
import os
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time
#from pytube import YouTube

terranegra_sessions = requests.Session()


class Download():

    def index(self):
                
        data = {
            'email': 'rhanyajudeh@hotmail.com',
            'senha': 'dD9CwZAz'
        }

        driver = webdriver.Chrome()
        driver.get('https://www.terranegraonline.com.br/login/')
        driver.find_element_by_id('email').send_keys(data['email'], Keys.TAB, data['senha'], Keys.RETURN)
        driver.get('https://www.terranegraonline.com.br/painel/dashboard/')
        links = driver.find_elements_by_css_selector('.col-md-6.col-lg-3.col-sm-6.col-xs-12')
        links_con = []
        for link in links:
            time.sleep(1)
            aula_link = link.find_element_by_tag_name('a')
            aula_link_con = aula_link.get_attribute('href')
            links_con.append(aula_link_con)
            #print(aula_link_con)

        for link_con in links_con:
            driver.get(link_con)
            videos = driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[4]/div[2]/section[1]/div/div/div')
            videos = videos.find_elements_by_class_name('col-md-3')
            #print('Getting Videos: ')
            for video in videos:
                time.sleep(1)
                video.click()
                title = driver.find_element_by_xpath('//*[@id="title1"]').text.strip()
                path = driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[1]/div[2]/div').text.strip().replace(' / ', '~')
                path = self.replacer(path)
                path = path.replace('~', '/')
                final_path = self.criar_pasta(path)
                final_path = f'{final_path}/{title}.mp4'
                if os.path.exists(final_path):
                    continue
                
                
                
                try:
                    video = driver.find_elemnt_by_xpath('/html/body/div[1]/section/div/div/div[3]/iframe')
                    video = video.get_attribute('src')
                except:
                    try:
                        video = driver.find_element_by_class_name('boxed-aula').find_element_by_tag_name('iframe').get_attribute('src')
                    except:
                        video = input('Digite a URL do video')
                
                #print(f'{final_path} - {video}')
                video_id = video.split('/')[1]
                if 'embed' in video:
                    video = video.replace('embed/', 'watch?v=')
                video = video.replace(' ', '')
                if 'vimeo' in video:
                    vimeo = f'{video}/config'
                    self.video_download(final_path, vimeo)
                elif 'youtube' in video:
                    #https://www.youtube.com/embed/loGNRG01JHU
                    #
                    print(video)
                    try:
                        self.youtube_downloader(video, final_path)
                        time.sleep(10)
                    except:
                        pass
            try:
                files = driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[4]/div[2]/section[2]/div/div/div')  
            except:
                continue
            #print('Getting Files: ')
            files = files.find_elements_by_class_name('col-md-3')
            
            for file_ in files:
                time.sleep(1)
                link = file_.find_element_by_tag_name('a')
                link_final = link.get_attribute('href')
                title = link.find_element_by_class_name('material-content').get_attribute('innerHTML')
                title = self.replacer(title.split('<span>')[1].split('</span>')[0].strip())
                path = driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[1]/div[2]/div').text.strip().replace(' / ', '~')
                path = self.replacer(path)
                path = path.replace('~', '/')
                final_path = self.criar_pasta(path)
                final_path = f'{final_path}/{title}.pdf'
                #print(title)
                os.system(f'aria2c -o "{final_path}" "{link_final}" --quiet --auto-file-renaming=false')
            try:
                audios = driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[4]/div[2]/section[3]/div/div')
                
            except:
                continue
            print('Getting Audios: ')
            audios = audios.find_elements_by_class_name('col-md-3')
            for audios in audios:
                time.sleep(1)
                audio_link = audios.find_element_by_tag_name('a')
                audio_link_f = audio_link.get_attribute('onclick')
                link_final = audio_link_f.split('toggleAudio(')[1].split(',')[0]
                link_final = link_final.replace('`', '').replace("'", '')
                title = audio_link.find_element_by_class_name('material-content').get_attribute('innerHTML')
                title = self.replacer(title.split('<span>')[1].split('</span>')[0].strip())
                path = driver.find_element_by_xpath('/html/body/div[1]/section/div/div/div[1]/div[2]/div').text.strip().replace(' / ', '~')
                path = self.replacer(path)
                path = path.replace('~', '/')
                #print(title)
                final_path = self.criar_pasta(path)
                final_path = f'{final_path}/{title}.mp3'
                os.system(f'aria2c -o "{final_path}" "{link_final}" --quiet --auto-file-renaming=false')

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
            'Referer': 'https://www.terranegraonline.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            check = True
            while check:
                try:
                    vimeo_config = requests.get(video, headers=vimeo_headers).json()
                    check = False
                    break
                except:
                    #print(f'Falha ao pegar link {video}, tentando novamente!')
                    continue

            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']

            #os.system(f'''aria2c -i {vimeo_url} -nostats -loglevel 0 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "{video_path}"''')            
            os.system(f'aria2c -o "{path}" {vimeo_url} --quiet') #
                             
    def youtube_downloader(self, video_youtube, path):

        headers_yt = {
            'authority': 'www.youtube.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        if os.path.exists(path) is False: 
            
            try:
                yt = YouTube(video_youtube)
                streams = yt.streams.get_highest_resolution().__dict__
                video_url = streams['url']
                os.system(f'aria2c -o "{path}" {video_url} --quiet')
            except:
                os.system(f'youtube-dl --quiet {video_youtube} -o "{path }"')
                #time.sleep(60)
            print(f'{path}')
            




    def criar_pasta(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)

        return path

    def replacer(self, text):
            invalid = {r'"': r"'", '\\': " - ", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
            for char in invalid:
                if char in text:
                    text = text.replace(char, invalid[char])
            return text

#Download().index()
                    



