import requests
import os
import json
import urllib
import m3u8

sanar_session = requests.Session()
undownloaded = {}

class Downloader():

    def index(self):

        headers = {
            'authority': 'cognito-idp.us-east-1.amazonaws.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'x-amz-target': 'AWSCognitoIdentityProviderService.InitiateAuth',
            'x-amz-user-agent': 'aws-amplify/0.1.x js',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'content-type': 'application/x-amz-json-1.1',
            'accept': '*/*',
            'sec-gpc': '1',
            'origin': 'https://login.editorasanar.com.br',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://login.editorasanar.com.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        email = 'ocoisa081@gmail.com'
        password = '18020301.pP'

        data = {"AuthFlow":"USER_PASSWORD_AUTH","ClientId":"7abkpr1abbtfukvl6hslsmvrr6","AuthParameters":{"USERNAME": email,"PASSWORD": password},"ClientMetadata":{}}
        
        login_data = sanar_session.post('https://cognito-idp.us-east-1.amazonaws.com/', headers=headers, json=data).json()

        sanar_session.headers['authority'] = 'd27fnx2os65oro.cloudfront.net'
        sanar_session.headers['authorization'] = login_data['AuthenticationResult']['IdToken']
        sanar_session.headers['content-type'] = 'application/json'
        sanar_session.headers['origin'] = 'https://aluno.sanarflix.com.br'
        sanar_session.headers['referer'] = 'https://aluno.sanarflix.com.br/'

        self.get_courses()
        self.get_mentoria()

    def download_video(self, url, video_path, content_path):

        #if os.path.exists(video_path) is False:
            #os.system(f'ffmpeg -i "{url}" -preset ultrafast "{video_path}" -nostats -loglevel 0') 
      # if os.path.exists(video_path) is False:
           # pass
           # file_name = url.split('/')[-1]
           # os.system(f'aria2c -o "tmp/{file_name}" "{url}" --quiet --continue=true')
            #undownloaded['file_name'] = video_path
           # with open('UnDownloads.json', 'w', encoding='utf-8') as out:
                #out.write(json.dumps(undownloaded))

            #master_content = open(f"tmp/{file_name}", 'r').read()
        video_m3u8 = m3u8.loads(sanar_session.get(url).text)
        bandwidth_base = 0
        for video in video_m3u8.playlists:
            video_bandwidth = video.__dict__['stream_info'].__dict__['bandwidth']
            if video_bandwidth > bandwidth_base:
                url = video.__dict__['uri']
                bandwidth_base = video_bandwidth
        video_nome = str(video_path.split('/')[-1])[0:10]
        for mp4 in os.listdir(content_path):
            if mp4.startswith(video_nome): #mp4.startswith(video_nome) or 
                break
            if os.path.exists(video_path) is False or os.path.getsize(video_path) == 0:
                os.system(f'ffmpeg -threads 0  -i "{url}" "{video_path}" -nostats -loglevel 0') #-preset ultrafast
            #os.system(f'del tmp/{file_name}')
                
        

    def get_courses(self):

        topic_data = {"operationName":"Topics","variables":{},"query":"query Topics {\n  topics {\n    data {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n"}
        topics = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=topic_data).json()['data']['topics']['data']

        downloaded = []

        for topic in topics:

            topic_name = self.replacer(topic['name']).strip()
            topic_path = self.makedirs(topic_name)
            topic_id = topic['id']
            downloaded.append(topic_id)

            with open('downloaded.json', 'w') as output:
                output.write(str(downloaded))

            courses = self.get_topics(topic_id)
            
            for course in courses:
                
                course_name = self.replacer(course['name']).strip()
                course_path = self.makedirs(f'{topic_path}/{course_name}')
                course_id = course['id']

                referencias = open(f'{course_path}/Referências Bibliográficas.txt', 'w', encoding='utf-8')
                
                
                if os.path.exists(f'{referencias}') is False:
                    ref_name, description = self.get_references(course_id)
                    with referencias as output:
                        output.write(f'{ref_name}\nO que você irá aprender e as referências bibliográficas utilizadas.\n{description}')

                content = self.get_content(course_id)

                for content_index, content in enumerate(content, start=1):

                    if content_index < 10:
                        content_index = f'0{content_index}'
                    content_name = self.replacer(content['name']).strip()
                    content_path = self.makedirs(f'{course_path}/{content_index} - {content_name}')
                    content_id = content['id']

                    content_class = self.get_aulas(course_id, content_id)

                    for aula_index, aula in enumerate(content_class, start=1):

                        if aula_index < 10:
                            aula_index = f'0{aula_index}'

                        aula_name = self.replacer(aula['title']).strip()
                        aula_id = aula['resource_id']
                        aula_title = f"{aula_index} - {aula_name}"
                        try:
                            aula_title = aula_title.replace(' - Aula - ', ' - ')
                        except:
                            pass
                        video_path = f'{content_path}/{aula_title} - [VIDEO].mp4'

                        aula_resource_type = aula['resource_type']

                        if aula_resource_type == "Video":
                            if os.path.exists(video_path) is False:  #or os.path.getsize(video_path) == 0
                                print(f'[Downloading] - {video_path}')
                                url = self.get_video(content_id, aula_id, course_id)
                                self.download_video(url, video_path, content_path)
                            else:
                                print(f'[Downloaded] - {video_path}')
                        
                        elif aula_resource_type == "Document":
                    
                            aula_type = aula['type']

                            RESUMO = f'{content_path}/{aula_title} - [RESUMO].pdf'
                            MAPA_MENTAL = f'{content_path}/{aula_title} - [MAPA MENTAL].pdf'
                            ARTIGO = f'{content_path}/{aula_title} - [ARTIGO].pdf'
                            FLUXOGRAMA = f'{content_path}/{aula_title} - [FLUXOGRAMA].pdf'

                            ARQUIVOS = [RESUMO, MAPA_MENTAL, ARTIGO, FLUXOGRAMA]
                            for pdf in os.listdir(content_path):
                                if pdf.startswith(aula_title):
                                    break
                                for ARQUIVO in ARQUIVOS:                                    
                                    if os.path.exists(ARQUIVO) is False:
                                        if aula_type == "resume":
                                            RESUMO = f'{content_path}/{aula_title} - [RESUMO].pdf'
                                            self.download_pdf(content_id, aula_id, course_id, RESUMO, aula_type)
                                            break
                                        elif aula_type == "mentalmap":
                                            MAPA_MENTAL = f'{content_path}/{aula_title} - [MAPA MENTAL].pdf'
                                            self.download_pdf(content_id, aula_id, course_id, MAPA_MENTAL, aula_type)
                                            break
                                        elif aula_type == "article":
                                            ARTIGO = f'{content_path}/{aula_title} - [ARTIGO].pdf'
                                            self.download_pdf(content_id, aula_id, course_id, ARTIGO, aula_type)
                                            break
                                        elif aula_type == "flowchart":
                                            FLUXOGRAMA = f'{content_path}/{aula_title} - [FLUXOGRAMA].pdf'
                                            self.download_pdf(content_id, aula_id, course_id, FLUXOGRAMA, aula_type)
                                            break
                                        break
                                    else:
                                        print(f'[Downloaded {aula_type}] - {ARQUIVO}')
                                        break
                                #os.system(f'aria2c -o "{document_path}" "{document_info}"')
                        elif aula_resource_type == "Quiz":
                            print("MATERIAL NAO PEGO - [QUESTIONARIO]")


    def download_pdf(self, content_id, aula_id, course_id, ARQUIVO, aula_type):

        if os.path.exists(ARQUIVO) is False:
            document_info = self.get_document(content_id, aula_id, course_id)
            urllib.request.urlretrieve(document_info, filename=ARQUIVO)
            print(f'[Downloading {aula_type}] - {ARQUIVO}')


    def get_mentoria(self):

        mentoria_data = {"operationName":"Themes","variables":{"courseId":"5f17b1c7ed890e00139660c8"},"query":"query Themes($courseId: ID!, $skip: Int, $completeness: CompletenessType) {\n  themes(courseIds: [$courseId], skip: $skip, completeness: $completeness) {\n    data {\n      id\n      name\n      course {\n        id\n        __typename\n      }\n      __typename\n    }\n    count\n    __typename\n  }\n}\n"}

        mentorias = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=mentoria_data).json()['data']['themes']['data']

        for mentoria in mentorias:
            
            mentoria_name = self.replacer(mentoria['name']).strip()
            mentoria_path = self.makedirs(f'Mentoria/{mentoria_name}')
            mentoria_id = mentoria['id']

            courses = self.get_topics(mentoria_id)

            for course in courses:
                            
                course_name = self.replacer(course['name']).strip()
                course_path = self.makedirs(f'{mentoria_path}/{course_name}')
                course_id = course['id']

                ref_name, description = self.get_references(course_id)
                
                if os.path.exists(f'{course_path}/Referências Bibliográficas.txt') is False:
                    referencias = open(f'{course_path}/Referências Bibliográficas.txt', 'w', encoding='utf-8')
                    with referencias as output:
                        output.write(f'{ref_name}\nO que você irá aprender e as referências bibliográficas utilizadas.\n{description}')

                content = self.get_content(course_id)

                for content_index, content in enumerate(content, start=1):

                    if content_index < 10:
                        content_index = f'0{content_index}'
                    content_name = self.replacer(content['name']).strip()
                    content_path = self.makedirs(f'{course_path}/{content_index} - {content_name}')
                    content_id = content['id']

                    content_class = self.get_aulas(course_id, content_id)

                    for aula_index, aula in enumerate(content_class, start=1):

                        if aula_index < 10:
                            aula_index = f'0{aula_index}'

                        aula_name = self.replacer(aula['title']).strip()
                        aula_id = aula['resource_id']
                        aula_title = f"{aula_index} - {aula_name}"
                            
                        url = self.get_video(content_id, aula_id, course_id)
                        video_path = f'{content_path}/{aula_title} - [VIDEO].mp4'
                        self.download_video(url, video_path)

    def get_topics(self, topic_id):
        
        course_data = {"operationName":"Courses","variables":{"tagId":topic_id},"query":"query Courses($skip: Int, $tagId: ID, $completeness: CompletenessType) {\n  courses(skip: $skip, order: alphabetical, tagId: $tagId, completeness: $completeness) {\n    data {\n      id\n      name\n      progress_percentage\n      cover_pictures {\n        small {\n          url\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    count\n    __typename\n  }\n}\n"}

        courses = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=course_data).json()['data']['courses']['data']

        return courses

    def get_aulas(self, course_id, content_id):

        aulas_data = {"operationName":"ThemeContents","variables":{"courseId": course_id,"themeId": content_id},"query":"query ThemeContents($themeId: ID!, $courseId: ID!, $skip: Int) {\n  themeContents(themeId: $themeId, courseId: $courseId, skip: $skip) {\n    data {\n      id\n      index\n      resource_type\n      resource_id\n      title\n      type\n      completed\n      __typename\n    }\n    count\n    __typename\n  }\n}\n"}
         
        content_class = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=aulas_data).json()['data']['themeContents']['data']

        return content_class

    def get_content(self, course_id):
        
        content_course_data = {"operationName":"Themes","variables":{"courseId": course_id},"query":"query Themes($courseId: ID!, $skip: Int, $completeness: CompletenessType) {\n  themes(courseIds: [$courseId], skip: $skip, completeness: $completeness) {\n    data {\n      id\n      name\n      course {\n        id\n        __typename\n      }\n      __typename\n    }\n    count\n    __typename\n  }\n}\n"}

        content_course = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=content_course_data).json()['data']['themes']['data']

        return content_course

    def get_references(self, course_id):
        
        referencias_data = {"operationName":"CourseDetail","variables":{"id": course_id},"query":"query CourseDetail($id: ID) {\n  course(id: $id) {\n    id\n    name\n    description\n    progress_percentage\n    counters {\n      questions\n      certificates\n      lessons\n      resumes\n      mentalmaps\n      flowcharts\n      articles\n      __typename\n    }\n    __typename\n  }\n}\n"}

        referencias_bibliographic = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=referencias_data).json()['data']['course']
        
        course_name = referencias_bibliographic['name']
        
        description = referencias_bibliographic['description']

        return course_name, description

    def get_document(self, content_id, aula_id, course_id):

        document_data = {"operationName":"Document","variables":{"themeId": content_id,"resourceId": aula_id,"courseId": course_id},"query":"query Document($themeId: ID!, $resourceId: ID!, $courseId: ID!) {\n  resource(themeId: $themeId, resourceId: $resourceId, courseId: $courseId) {\n    ...ResourceCommon\n    document {\n      id\n      title\n      file {\n        url\n        __typename\n      }\n      progress {\n        percentage\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ResourceCommon on ThemeContent {\n  id\n  resource_type\n  type\n  title\n  course {\n    id\n    name\n    __typename\n  }\n  next {\n    id\n    title\n    resource_type\n    resource_id\n    parent {\n      id\n      __typename\n    }\n    __typename\n  }\n  previous {\n    id\n    title\n    resource_type\n    resource_id\n    parent {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
                            
        document_info = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=document_data).json()['data']['resource']['document']['file']['url']

        return document_info

    def get_video(self, content_id, aula_id, course_id):

        video_data = {"operationName":"Video","variables":{"themeId": content_id,"resourceId": aula_id,"courseId": course_id},"query":"query Video($themeId: ID!, $resourceId: ID!, $courseId: ID!) {\n  resource(themeId: $themeId, resourceId: $resourceId, courseId: $courseId) {\n    ...ResourceCommon\n    video {\n      id\n      title\n      durationInSeconds\n      progress {\n        percentage\n        timeInSeconds\n        __typename\n      }\n      thumbnails {\n        small\n        medium\n        large\n        __typename\n      }\n      rating {\n        id\n        rating {\n          value\n          __typename\n        }\n        __typename\n      }\n      providers {\n        data {\n          code\n          files {\n            smil {\n              url\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ResourceCommon on ThemeContent {\n  id\n  resource_type\n  type\n  title\n  course {\n    id\n    name\n    __typename\n  }\n  next {\n    id\n    title\n    resource_type\n    resource_id\n    parent {\n      id\n      __typename\n    }\n    __typename\n  }\n  previous {\n    id\n    title\n    resource_type\n    resource_id\n    parent {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
        
        video_info = sanar_session.post('https://d27fnx2os65oro.cloudfront.net/graphql', json=video_data).json()['data']['resource']['video']['providers']['data'][0]['files']['smil']['url']
        #print(video_info)
        return video_info

    def replacer(self, text):
        invalid = {"#": "!", r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text

    def makedirs(self, path):

        if os.path.exists(path) is False:
            os.makedirs(path)
        
        return path

#Downloader().index()

"""error = -1
while error < 3:
    try:
        break
    except:
        error += 1
        continue"""