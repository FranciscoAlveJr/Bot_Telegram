import requests
import os
import json
import m3u8
import time

os.system('cls')

rocketseat_session = requests.Session()

class Downloader():

    def main(self):

        print(colors.CVIOLET + '=' * 34)
        print('- # - Rocketseat Bot Scrapy - # -')
        print('=' * 34 + '\n')

        print(colors.CGREEN + '1 - Update JSONs\n2 - Download Rocketseat')
        if choice := input('\nOption: '):
            if int(choice) == 1:
                print('\nUpdating JSONs')
                self.get_json()
            elif int(choice) == 2:
                print('\nDownloading Rocketseat\n')
                self.read_json()
            else:
                print('\nInvalid')

    def get_json(self):

        headers = {
            'authority': 'app.rocketseat.com.br',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        rocketseat_session.headers.update(headers)


        email = 'ocoisa081@gmail.com'
        senha = '18020301.pP'

        data = {'email': email, 'password': senha}

        print(colors.CBLUE + 'Log-in', end='')
        r_content, r_headers, self.r_cookies = self.login(data)
        print(colors.CGREEN + ' - Logged')
        
        self.bearer_token = f'Bearer {r_content["token"]}'

        headers = {
            'authority': 'app.rocketseat.com.br',
            'accept': 'application/json, text/plain, */*',
            'authorization': self.bearer_token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.rocketseat.com.br/dashboard',
            'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': f'_fbp=fb.2.1598158636713.1341805582; adonis-session={self.r_cookies["adonis-session"]}; adonis-session-values={self.r_cookies["adonis-session-values"]}'
        }

        rocketseat_session.headers.update(headers)
        
        print('\n' + colors.CBLUE + 'Connecting to dashboard API', end='')
        dashboard = rocketseat_session.get('https://app.rocketseat.com.br/api/account')
        print(colors.CGREEN + ' - Connected\n')

        dashboard_cookies = dashboard.cookies.get_dict()
        dashboard_models_default = dashboard.json()['journeys']
        dashboard_models = list(dict.fromkeys(dashboard_models_default))  #['bootcamp', 'bonus', 'lives', 'gostack-11', 'nlw', 'rewards', 'launchbase', 'launchbase-lives', 'starter']

        journeys_api = 'https://app.rocketseat.com.br/api/journeys'

        json_path = 'JSONs/'
        self.makedir(json_path)
        print('\n' + colors.CBLUE + 'Downloading JSON file:\n')
        
        for i in dashboard_models:
            output_directory = 'JSONs/' + i + '.json'
            if os.path.exists(output_directory) is False:
                self.save_json(journeys_api, i, output_directory)
            else:
                print(colors.CYELLOW + 'JSON file "' + colors.CRED + i + colors.CYELLOW + '" already exists!')
        
        self.read_json()

    def read_json(self):
        
        output_directory = 'JSONs/'

        if os.path.exists(output_directory) is False:
            print(colors.WARNING + '\nDirectory not found, getting JSON')
            self.get_json()

        json_files = os.listdir(output_directory)
        print(colors.CVIOLET + '=' * 34)
        print("\n Escolha o que deseja baixar:")
        print()
        courses = []
        for index, json_file in enumerate(json_files):
            index += 1
            json_content = open(f'{output_directory}{json_file}', 'r', encoding='utf-8').read()
            data = json.loads(json_content)
            courses.append(data)
            print(colors.CGREEN + f'{index} - ' + data['title'])
        print(f'{index + 1} - Downloading All')
        print()
        print(colors.CVIOLET + '=' * 34)
        if choice := input(colors.CBLUE + '\nOpção: '):
            if choice.isdigit():
                choice = int(choice)
                if choice <= len(json_files) and choice > 0:
                    print()
                    print(colors.CVIOLET + '=' * 34)
                    title = self.replacer(courses[choice-1]["title"])
                    print(colors.CGREEN + f'\nDownloading {title}\n', end='')
                    actual_path = self.makedir(title)
                    
                    course = courses[choice-1]
                    self.download_course(course, actual_path)
                elif choice == index + 1:
                    print(colors.CGREEN + 'Download All\n')
                    print(colors.CVIOLET + '=' * 34)
                    for course in courses:
                        title = self.replacer(course["title"])
                        print(colors.CRED + 'Downloading ' + title, end='')
                        actual_path = self.makedir(title)
                        self.download_course(course, actual_path)
                else:
                    print('\nInvalid')
        print(colors.CVIOLET + '=' * 34)

    def download_course(self, course, top_path):

        course_title = course['title']
        course_node = course['nodes']
        print(colors.CRED + 'Downloading ' + course_title)
        top_order = 0
        for order, node in enumerate(course_node, start=1):
            top_order += 1
            group = node['group']
            cluster = node['cluster']
            lesson = node['lesson']
            top_title = node['title']
            challenge = node['challenge']

            if top_title != None:
                top_title = self.replacer(top_title)
                top_title = f'{top_order} - {top_title}'
                print(colors.CYELLOW +  f'\t{top_title}')
            else:
                try:
                    try:
                        title = self.replacer(group['title'])
                    except:
                        title = self.replacer(cluster['title'])
                except:
                    try:
                        title = self.replacer(lesson['last']['title'])
                    except:
                        title = self.replacer(challenge['title'])
                final_title = f'{order} - {title}'
                print(colors.CYELLOW + f"\t{final_title}")

            if str(type(group))[8:-2] != 'NoneType':
                title = self.replacer(group['title'])
                final_title = f'{order} - {title}'
                print(colors.CBLUE + f"\t\t{final_title}", end='')
                local_path = f'{top_path}/{final_title}'
                actual_path = self.makedir(local_path)
                self.get_group(group, actual_path)
                continue

            if str(type(cluster))[8:-2] != 'NoneType':
                title = self.replacer(cluster['title'])
                final_title = f'{order} - {title}'
                print(colors.CBLUE + f"\t\t{final_title}", end='')
                local_path = f'{top_path}/{final_title}'
                actual_path = self.makedir(local_path)
                self.get_cluster(cluster, local_path)
                continue

            if str(type(lesson))[8:-2] != 'NoneType':
                title = self.replacer(lesson['last']['title'])
                final_title = f'{order} - {title}'
                print(colors.CBLUE + f"\t\t{final_title}", end='')
                local_path = f'{top_path}/{final_title}'
                actual_path = self.makedir(local_path)
                self.get_lesson(lesson, actual_path)
                continue

            if str(type(challenge))[8:-2] != 'NoneType':
                title = self.replacer(challenge['title'])
                final_title = f'{order} - {title}'
                print(colors.CRED + f"\t\t{final_title}", end='')
                local_path = f'{top_path}/{final_title}'
                actual_path = self.makedir(local_path)
                self.get_challenge(challenge, actual_path)
                continue   

   
    def get_group(self, source, path):

        lessons = source['lessons']

        for order, lesson in enumerate(lessons, start=1):
            title = lesson['last']['title']
            platform = lesson['last']['platform']
            final_title = f'{order} - {title}'
            video_path = f'{path}/{final_title}.mp4'
            if platform == 'vimeo':
                vimeo_id = lesson['last']['resource']
                self.download_vimeo(vimeo_id, video_path)
                print(colors.CRED + '\t\t\t' + final_title)
                pass
            elif platform == 'jupiter':
                jupiter_id = lesson['last']['resource']
                
                self.download_jupiter(jupiter_id, video_path)
                print(colors.CRED + final_title)        

    def download_jupiter(self, jupiter_id, path):


            video_path = path

            if os.path.exists(video_path) is False:
                m3u8_file = 'tmp/master.m3u8'
                video_file = 'tmp/video/1080'
                audio_file = 'tmp/audio'

                self.makedir(video_file)
                self.makedir(audio_file)

                if os.path.exists('tmp/audio.m3u8') is False:
                    headers = {
                        'Referer': 'https://app.rocketseat.com.br/',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                    }

                    response = requests.get(f'https://himalia.rocketseat.dev/outputs/{jupiter_id}/audio.m3u8', headers=headers).text
                    with open('tmp/audio.m3u8', 'w', encoding='utf-8') as out:
                        out.write(response)
                self.get_m3u8(jupiter_id, 'video_1080.m3u8', 'tmp/video_1080.m3u8')
                self.get_m3u8(jupiter_id, 'master.m3u8', m3u8_file)
                
                master_content = open('tmp/master.m3u8', 'r').read()
                video_1080_content = open('tmp/video_1080.m3u8', 'r').read()
                audio_content = open('tmp/audio.m3u8', 'r').read()
                
                video_1080_m3u8 = m3u8.loads(video_1080_content)
                audio_m3u8 = m3u8.loads(audio_content)
                master_m3u8 = m3u8.loads(master_content)

                contents = [video_1080_m3u8, audio_m3u8]

                for content in contents:
                    self.change_key(content)

                self.set_master(master_m3u8)

                video_1080_content = open('tmp/video_1080.m3u8', 'w')
                audio_content = open('tmp/audio.m3u8', 'w')
                master_content = open('tmp/master.m3u8', 'w')

                video_dumps = video_1080_m3u8.dumps()
                audio_dumps = audio_m3u8.dumps()
                master_dumps = master_m3u8.dumps()

                with video_1080_content as video_output:
                    video_output.write(video_dumps)
                
                with audio_content as audio_output:
                    audio_output.write(audio_dumps)

                with master_content as master_output:
                    master_output.write(master_dumps)

                video_segments = video_1080_m3u8.data['segments']
                audio_segments = audio_m3u8.data['segments']
                segments = {
                    video_file: video_segments,
                    audio_file: audio_segments
                }
                for path, segment in segments.items():
                    self.get_ts(segment, jupiter_id, path)
                
                
                self.get_key(jupiter_id, 1080, 'video')
                self.get_key(jupiter_id, 'undefined', 'audio')
                self.check_dir(video_path)
                os.system(f'ffmpeg -allowed_extensions ALL -i "tmp/master.m3u8" -preset ultrafast "{video_path}" -nostats -loglevel 0')
                print(colors.CBLUE + f'\t\t\t{video_path}')
                os.system('rd /s /q tmp')

    def check_dir(self, path):

        title = path.split('/')[-1]
        real_path = path.replace(title, '')

        if os.path.exists(real_path) is False:
            os.makedirs(real_path)

    def set_master(self, master):
        
        for x in master.playlists:
            if 'video_1080.m3u8' in x.__dict__['uri']:
                master.playlists = x

    def get_key(self, jupiter_id, quality, type_file):
        #cookie: _fbp=fb.2.1598838413958.65073027; bitmovin_analytics_uuid=fc4b00c3-77d4-4428-a770-747536a291b3; _ga=GA1.3.1672722255.1602364286; __zlcmid=10kjWP1iHlDkmuk; _gid=GA1.3.968860643.1605388853; _gat=1; _dd_s=rum=0&expire=1605389838973; adonis-session-values=9b406e6ced94ddefa889245cff72b9872mL0aLnonpB%2Bi71r6fO5ryFM3%2BBbagte4k%2Fy8OmjDfve0aG7N35F9XCpUm4sqKY5BpfPC%2BrX8VReGUhEjb1GGQ%3D%3D; adonis-session=afcb01ff226586cef92a69792bc0f4edXEExWChRoy1158KYF6ZcS3Ygp%2BnHChJ5C7gMhOxLRj8Lx55gQ3HP5Au74Lc6Jz8EoDoCaHMgL4Pu4XZj8Y411%2BxzOahzwQa1jP0fyxfz%2B0KHXOCIFTKiy0TLmuHidj7J

        #analystics = self.get_bitmovin()
        analystics = analystics
        #adonis_s = '364e285e0e1cf53035d1f12373d1d1f1XFzyFag2jedVhbbgF0Z%2FxwfxwFSe4VkVtGKKolkZW5dkFHTl5fzsRxegDUM%2BaW1wkidMDdOvvLgBtsxraY1FyyuD%2BcalKTrWtp1VSklO%2F2F0bW8ILcsMhvK5KikhVF%2BQ'
        #adonis_sv = '0b99331e7cfa9cc6dd171086662f39e4B%2FH%2BrSI7g4UhtVJhohXvCfHiLXU4Uwb0KWMvG3ln%2FXU1hj58%2F7MvNGBnvduDmUOiFzg2Xr6m44nO5zVgXxsaZQ%3D%3D'
        #bearer = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJjZGE4OWY5Yi1kMTQ3LTQzZDMtOTIwOC04NzM0ZTU3MTgxNDEiLCJpYXQiOjE2MTIzNzU2NjIsImV4cCI6MTYxMjU0ODQ2Mn0.3-FkavRWhJpmEa4Yv1HK-RlSXad8OaMxDsARhmJWYfY'
        #print(analystics)
        #self.bearer_token = 'fc4b00c3-77d4-4428-a770-747536a291b3'

        headers = {
            'authority': 'app.rocketseat.com.br',
            'accept': 'application/json, text/plain, */*',
            'authorization': bearer,            
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://app.rocketseat.com.br',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.rocketseat.com.br',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            #'cookie': f'_fbp=fb.2.1598838413958.65073027; bitmovin_analytics_uuid={analystics}; adonis-session={adonis_s}; adonis-session-values={adonis_sv}',
            'cookie': '_fbp=fb.2.1611340781876.684366938; bitmovin_analytics_uuid=af2e7cd8-21f0-4a8d-b9a1-3b93372b942b; adonis-session=54294d65462d505e77c9467fc4182d6axe7H58m7JS8aTDbQM5IXw5J9jH5aIPbg2Rm7%2FBYRzxsBuJZ3dWjCEBHp7JNET4%2B%2BcYYJms7oNUT3Ysd57sr1a3A5CZFHT6ZpSDIepcyIL7tiybaz2kS1ZFo%2FKUQbvRvZ; adonis-session-values=346a6755aa32d012b7f87a8b95bbfea06X9jd2UsUh6wYQTklDVJA73NsUcIXcoRY5nr8eHO5azGthyNDrFVXJLIjRX4WTLmjuZSl97Tu0gpndJRPMP2sg%3D%3D; _dd_s=rum=0&expire=1612376565410'
        }

        #data = f"""'$"i": "{jupiter_id}", "q": "{str(quality)}", "t": "{type_file}"%'"""
        #data = data.replace('$', '{').replace('%', '}')


        data = json.dumps({"i": jupiter_id, "q": str(quality), "t": type_file})
        token = rocketseat_session.post('https://app.rocketseat.com.br/api/lcs', data=data).json()['token'] #, headers=headers

        headers = {
            'authority': 'app.rocketseat.com.br',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'l': token,
            'i': jupiter_id,
            't': type_file,
            'authorization': bearer,
            'q': str(quality),
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.rocketseat.com.br/node/fase-01',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'_fbp=fb.2.1598838413958.65073027; bitmovin_analytics_uuid={analystics}; adonis-session={adonis_s}; adonis-session-values={adonis_sv}',
            }

        response = rocketseat_session.get('https://app.rocketseat.com.br/api/lcs', headers=headers).content
        with open(f'tmp/{type_file}.key', 'wb') as output_key:
            output_key.write(response)
        
    def get_bitmovin(self):

        headers = {
            'Host': 'licensing.bitmovin.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'content-type': 'text/plain;charset=UTF-8',
            'accept': '*/*',
            'origin': 'https://app.rocketseat.com.br',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://app.rocketseat.com.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        data = '{"domain":"app.rocketseat.com.br","key":"cf28e92b-2f90-49b7-87f0-267916d0b1ee","version":"8.42.0"}'

        analystics = rocketseat_session.post('https://licensing.bitmovin.com/licensing', headers=headers, data=data).json()
        if analystics['status'] == 'granted':
            return analystics['analytics']

    def change_key(self, content):
        
        for key in content.keys:
            type_file = content.files[1].split('/')[0]
            if key:
                if type_file == 'video':
                    key.uri = 'video.key'
                elif type_file == 'audio':
                    key.uri = 'audio.key'
                    
    def get_ts(self, segments, jupiter_id, path):
        
        amount = len(segments)
        print(f'TS Files - Audio/Video | (Total = {amount}): ')
        for segment in segments:
            url = segment['uri']
            segment_link = f'https://himalia.rocketseat.dev/outputs/{jupiter_id}/{url}'
            filename = segment_link.split("/")[-1]
            ts_path = f'{path}/{filename}'
            name = filename.split('_')[1].split('.')[0]
            print(f'{name} - ', end='')
            print(segment_link)
            if os.path.exists(ts_path) is False:
               
                headers = {
                    'authority': 'himalia.rocketseat.dev',
                    'pragma': 'no-cache',
                    'cache-control': 'no-cache',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Safari/537.36',
                    'accept': '*/*',
                    'origin': 'https://app.rocketseat.com.br',
                    'sec-fetch-site': 'cross-site',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://app.rocketseat.com.br/',
                    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                
                #response  = requests.get(segment_link, headers=headers).text
                #with open(ts_path, 'w') as out:
                    #out.write(response)
                check = True
                while check:
                    os.system(f'aria2c -o "{ts_path}" {segment_link} --quiet --continue=true')
                    time.sleep(1)
                    if os.path.exists(ts_path):
                        check = False
                    
                
            #
            
            time.sleep(1)

    def get_m3u8(self, jupiter_id, type_file, path):

        if os.path.exists(path) is False:
            headers = {
                'authority': 'himalia.rocketseat.dev',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Safari/537.36',
                'accept': '*/*',
                'origin': 'https://app.rocketseat.com.br',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://app.rocketseat.com.br/',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            
            response  = requests.get(f'https://himalia.rocketseat.dev/outputs/{jupiter_id}/{type_file}', headers=headers).text
            with open(path, 'w') as out:
                out.write(response)
            #os.system(f'aria2c -o "{path}" "https://himalia.rocketseat.dev/outputs/{jupiter_id}/{type_file}" --quiet --continue=true')

    def download_vimeo(self, vimeo_id, path):

        if os.path.exists(path) is False:
            vimeo_headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://app.rocketseat.com.br/',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
            video_link = f'https://player.vimeo.com/video/{vimeo_id}/config'
            vimeo_config = requests.get(video_link, headers=vimeo_headers).json()
            vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
            vimeo_url = vimeo_download[-1]['url']

            #os.system(f'''aria2c -i {vimeo_url} -nostats -loglevel 0 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "{video_path}"''')            
            os.system(f'aria2c -o "{path}" {vimeo_url} --quiet --continue=true')
            
    def get_cluster(self, source, path):

        clusters = source['groups']

        for order, cluster in enumerate(clusters, start=1):
            title = self.replacer(cluster['title'])
            final_title = f'{order} - {title}'
            print(colors.CBLUE + f"\t\t{final_title}", end='')
            local_path = f'{path}/{final_title}'
            actual_path = self.makedir(local_path)
            self.get_group(cluster, actual_path)

    def get_challenge(self, source, path):
        
        print(f'\t\t BAIXAR DESAFIO')
        pass

    def get_lesson(self, source, path, order=0):
        
        try:
            order = source['pivot']['order']
            pass
        except:
            order += 1
            pass
        lesson = source['last']
        title = self.replacer(lesson['title'])
        final_title = f'{order} - {title}'
        local_path = f'{path}/{final_title}'
        print(f'\t\t{final_title}', end='')
        actual_path = self.makedir(local_path)
        if source['type'] == 'material':
            download_link = lesson['resource_url']
            extension = lesson['resource'].split('.')[-1]
            final_title = f'{actual_path}/{final_title}.{extension}'
            os.system(f'aria2c -o "{final_title}" "{download_link}" --quiet --continue=true')

        elif source['type'] == 'video':
            vimeo_id = lesson['resource']
            final_title = f'{actual_path}/{final_title}'
            video_path = f'{final_title}.mp4'
            self.download_vimeo(vimeo_id, video_path)
            print(source['last']['platform'])
        print(f'\t\t\t{final_title}')
            
    def save_json(self, journeys_api, i, output_directory):

        journeys_content = rocketseat_session.get(f'{journeys_api}/{i}').json()
        output_file= open(output_directory, 'w', encoding='utf-8')
        with  output_file as for_write:
            for_write.write(json.dumps(journeys_content, ensure_ascii=False))
            print(colors.CBLUE + 'JSON file:"' + colors.CRED + i + colors.CBLUE + '" created with success and saved as ' + colors.CGREEN + output_directory)

    def makedir(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)
            print(colors.CGREEN + ' - Directory created with sucess: ' + path )
        else:
            print(colors.CRED + ' - Directory "' + path + '" already exists!')
        
        return path

    def login(self, data):

        request_login = rocketseat_session.post('https://app.rocketseat.com.br/api/sessions', data=data)
        
        response_content = request_login.json()
        response_headers = request_login.headers
        response_cookies = request_login.cookies.get_dict()

        return response_content, response_headers, response_cookies

    def replacer(self, text):
        invalid = {r'"': r"'", '\\': " - ", '/': " - ", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m'
    CBLINK    = '\33[5m'
    CBLINK2   = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'

    CBLACKBG  = '\33[40m'
    CREDBG    = '\33[41m'
    CGREENBG  = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG   = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG  = '\33[46m'
    CWHITEBG  = '\33[47m'

    CGREY    = '\33[90m'
    CRED2    = '\33[91m'
    CGREEN2  = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2   = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2  = '\33[96m'
    CWHITE2  = '\33[97m'

    CGREYBG    = '\33[100m'
    CREDBG2    = '\33[101m'
    CGREENBG2  = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2   = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2  = '\33[106m'
    CWHITEBG2  = '\33[107m'

#Downloader().main()