import requests
import os
import urllib
import json
import youtube_dl
import shutil
from pytube import YouTube
import time

kuadro_session = requests.session()

class Downloader():

    def index(self):

        
        self.login_url = 'https://api-prod.kuadro.com.br/graphql' #URL padrão da API do site todo
        login_headers = {
            'authority': 'api-prod.kuadro.com.br',
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://pv.kuadro.com.br',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://pv.kuadro.com.br/login',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }

        email = 'ocoisa081@gmail.com'
        password = '18020301.pP'

        login = {"operationName":"login","variables":{"email": email,"password": password,"studentId":0},"query":"mutation login($email: String!, $password: String!, $studentId: Int) {\n  authPV(email: $email, password: $password, studentId: $studentId) {\n    accessToken\n    refreshToken\n    expiresIn\n    __typename\n  }\n}\n"}

        kuadro_token = kuadro_session.post(self.login_url, headers=login_headers, json=login).Json()
        kuadro_session.headers = {
            'authority': 'api-prod.kuadro.com.br',
            'accept': '*/*',
            'kuadro-token': kuadro_token['data']['authPV']['accessToken'],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://pv.kuadro.com.br',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://pv.kuadro.com.br/app/disciplinas',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            }
        studentsID = self.get_students()
        self.get_course(login_headers, studentsID, email, password)

    def get_students(self):

        getMyStudents = {
            "operationName":"getMyStudents",
            "variables":{},
            "query":"query getMyStudents {\n  getMyStudents {\n    id\n    class {\n      name\n      __typename\n    }\n    __typename\n  }\n}\n"
            }

        get_studentsID = kuadro_session.post(self.login_url, json=getMyStudents).conjson()['data']['getMyStudents']
        students_dict = {}
        students_list = []
        for index, student in enumerate(get_studentsID):
            students_dict[index] = {}
            students_dict[index]['name'] = student['class']['name']
            students_dict[index]['id'] = student['id']
            students_list.append(students_dict)

        return students_list

    def get_course(self, headers, ids, email, password):

        for index, course in enumerate(ids):
            course_name = self.replacer(course[index]['name'])
            course_id = course[index]['id']
            
            login_headers = {
                'authority': 'api-prod.kuadro.com.br',
                'accept': '*/*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'content-type': 'application/json',
                'origin': 'https://pv.kuadro.com.br',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://pv.kuadro.com.br/login',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                }
            login = {"operationName":"login","variables":{"email": email,"password": password,"studentId": course_id},"query":"mutation login($email: String!, $password: String!, $studentId: Int) {\n  authPV(email: $email, password: $password, studentId: $studentId) {\n    accessToken\n    refreshToken\n    expiresIn\n    __typename\n  }\n}\n"}
            kuadro_token = json.loads(kuadro_session.post(self.login_url, headers=login_headers, json=login).content)
            headers = {
                'authority': 'api-prod.kuadro.com.br',
                'accept': '*/*',
                'kuadro-token': kuadro_token['data']['authPV']['accessToken'],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'content-type': 'application/json',
                'origin': 'https://pv.kuadro.com.br',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://pv.kuadro.com.br/app/disciplinas',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                }

            get_all_disciplines = {"operationName":"getAllMyDisciplines","variables":{},"query":"query getAllMyDisciplines {\n  myDisciplines {\n    id\n    name\n    color\n    myMedals {\n      nGoldMedals\n      nSilverMedals\n      nBronzeMedals\n      __typename\n    }\n    myProgress\n    myGrade\n    myStars\n    nAssignments\n    __typename\n  }\n}\n"}
            all_disciplines = json.loads(kuadro_session.post(self.login_url, headers=headers, json=get_all_disciplines).content)['data']['myDisciplines']

            for index, discipline in enumerate(all_disciplines):
                discipline_id = discipline['id']
                discipline_title = self.replacer(str(discipline['name']).strip())
                discipline_title = f'{index + 1} - {discipline_title}'
                print(discipline_title)
                discipline_by = {"operationName":"getDisciplineById","variables":{"id": discipline_id},"query":"query getDisciplineById($id: Int!) {\n  discipline(id: $id) {\n    id\n    name\n    color\n    myMedals {\n      nGoldMedals\n      nSilverMedals\n      nBronzeMedals\n      __typename\n    }\n    nAssignments\n    myProgress\n    myGrade\n    myStars\n    dailyRanking(top: 10) {\n      position\n      nStars\n      student {\n        id\n        currentBelt {\n          ...BeltFragment\n          __typename\n        }\n        user {\n          name\n          imageUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    weeklyRanking(top: 10) {\n      position\n      nStars\n      student {\n        id\n        currentBelt {\n          ...BeltFragment\n          __typename\n        }\n        user {\n          name\n          imageUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    monthlyRanking(top: 10) {\n      position\n      nStars\n      student {\n        id\n        currentBelt {\n          ...BeltFragment\n          __typename\n        }\n        user {\n          name\n          imageUrl\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    modules {\n      id\n      name\n      myGrade\n      myStars\n      nAssignments\n      myProgress\n      sections {\n        id\n        name\n        myGrade\n        myStars\n        front\n        nVideos\n        nAssignments\n        myStatus\n        tags {\n          id\n          name\n          description\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BeltFragment on Belt {\n  id\n  name\n  position\n  color\n  degree\n  __typename\n}\n"}

                discipline_model = json.loads(kuadro_session.post(self.login_url, headers=headers, json=discipline_by).content)['data']['discipline']['modules']
                
                for index, model in enumerate(discipline_model):
                    model_name = self.replacer(str(model['name']).strip())
                    model_name = f'{index + 1} - {model_name}'
                    print(f'\t{model_name}')
                    #model_id = model['id']
                    model_section = model['sections']
                    for index, section in enumerate(model_section):
                        section_name = self.replacer(str(section['name']).strip())
                        section_name = f'{index + 1} - {section_name}'
                        section_id = section['id']
                        print(f'\t\t{section_name}')

                        get_lesson = {"operationName": '',"variables":{"id": section_id},"query":"query ($id: Int!) {\n  section(id: $id) {\n    id\n    name\n    myGrade\n    myStars\n    module {\n      id\n      name\n      discipline {\n        id\n        name\n        color\n        __typename\n      }\n      __typename\n    }\n    myMedals {\n      nGoldMedals\n      nSilverMedals\n      nBronzeMedals\n      __typename\n    }\n    myProgress\n    nVideos\n    nAssignments\n    assignments {\n      id\n      name\n      myStars\n      level\n      position\n      mySubmission {\n        status\n        grade\n        __typename\n      }\n      myMedals {\n        nGoldMedals\n        nSilverMedals\n        nBronzeMedals\n        __typename\n      }\n      __typename\n    }\n    lessons {\n      id\n      name\n      position\n      myStars\n      videos {\n        duration\n        myStatus\n        __typename\n      }\n      __typename\n    }\n    theories {\n      id\n      name\n      position\n      myStudentTheory {\n        id\n        __typename\n      }\n      __typename\n    }\n    requiredSections {\n      id\n      name\n      myProgress\n      __typename\n    }\n    tags {\n      id\n      name\n      description\n      __typename\n    }\n    __typename\n  }\n}\n"}

                        lesson_t = kuadro_session.post(self.login_url, headers=headers, json=get_lesson).json()
                        lessons = lesson_t['data']['section']
                        for index_theory, theory in enumerate(lessons['theories']):
                            index_theory = index_theory + 1
                            theory_id = theory['id']
                            theory_name = self.replacer(theory['name']).strip()
                            theory_name = f'{index_theory} - {theory_name}'

                            get_theory = {"operationName":"getMyTheory","variables":{"theoryId": theory_id},"query":"query getMyTheory($theoryId: Int!) {\n  theory(id: $theoryId) {\n    id\n    position\n    section {\n      id\n      name\n      module {\n        id\n        name\n        discipline {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    content\n    name\n    attachments {\n      id\n      url\n      name\n      __typename\n    }\n    myStudentTheory {\n      id\n      viewedAt\n      __typename\n    }\n    image {\n      id\n      url\n      __typename\n    }\n    __typename\n  }\n}\n"}

                            theories = json.loads(kuadro_session.post(self.login_url, headers=headers, json=get_theory).content)['data']['theory']

                            try:
                                theory_url = str(theories['image']['url'])
                                path = f'{course_name}/{discipline_title}/{model_name}/{section_name}/Arquivos'
                                if os.path.exists(path) is False:
                                    os.makedirs(path)
                                if os.path.exists(f'{path}/{theory_name}.pdf') is False:
                                    print(f'\t\t\tArquivo - {theory_name} - Arquivo Teorico')
                                    urllib.request.urlretrieve(theory_url, filename=f'{path}/{theory_name}.pdf')
                                else:
                                    print(f'\t\t\tArquivo - {theory_name} - Arquivo já existente.')
                            except:
                                pass     
                            theories_attachements = theories['attachments']
                            if len(theories_attachements) > 0:
                                for index_attachment, attachements in enumerate(theories_attachements):
                                    index_attachment = index_attachment + 1
                                    attachement_url = attachements['url']
                                    attachement_name = attachements['name']
                                    theory_name = f'{index_theory}.{index_attachment} - {attachement_name}'
                                    attachement_down = f'{path}/{theory_name}.pdf'
                                    if os.path.exists(attachement_down) is False:
                                        print(f'\t\t\t\tAnexo - {attachement_name} - Arquivo Teorico')
                                        urllib.request.urlretrieve(attachement_url, filename=attachement_down)
                                    else:
                                        print(f'\t\t\t\tAnexo - {attachement_name} - Arquivo já existente.')

                        for index, lesson in enumerate(lessons['lessons']):
                            lesson_id = lesson['id']

                            get_lessons = {"operationName":"getLessonById","variables":{"id": lesson_id},"query":"fragment AlternativePart on Alternative {\n  id\n  body\n  isCorrect\n  position\n  __typename\n}\n\nquery getLessonById($id: Int!) {\n  lesson(id: $id) {\n    id\n    name\n    lessonTheories {\n      id\n      position\n      myLessonTheory {\n        id\n        read\n        __typename\n      }\n      theory {\n        id\n        name\n        content\n        attachments {\n          id\n          name\n          url\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    lessonQuestions {\n      id\n      position\n      myLessonQuestion {\n        id\n        attempts\n        alternativeId\n        alternative {\n          ...AlternativePart\n          __typename\n        }\n        __typename\n      }\n      question {\n        id\n        body\n        solutions {\n          writtenSolution\n          videoSolution {\n            id\n            duration\n            myLastWatchedSecond\n            youtubeCode\n            vimeoCode\n            __typename\n          }\n          __typename\n        }\n        ... on MultipleChoiceQuestion {\n          alternatives {\n            ...AlternativePart\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    section {\n      id\n      name\n      module {\n        id\n        name\n        discipline {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    videos {\n      id\n      position\n      name\n      duration\n      vimeoCode\n      myLastWatchedSecond\n      youtubeCode\n      myStatus\n      myWatchedPercentage\n      teacher {\n        user {\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    teacher {\n      user {\n        name\n        __typename\n      }\n      __typename\n    }\n    myRating\n    __typename\n  }\n}\n"}

                            lesson = json.loads(kuadro_session.post(self.login_url, headers=headers, json=get_lessons).content)['data']['lesson']

                            lesson_name = self.replacer(str(lesson['name']).strip())
                            lesson_name = f'{index + 1} - {lesson_name}'
                            lesson_videos = lesson['videos']
                            print(f'\t\t\t{lesson_name}')
                            path = f'{course_name}/{discipline_title}/{model_name}/{section_name}/{lesson_name}'
                            if os.path.exists(path) is False:
                                os.makedirs(path)

                            for index_video, video in enumerate(lesson_videos):
                                video_name = self.replacer(video['name'])
                                video_name = f'{index_video + 1} - {video_name}'
                                
                                video_vimeo = video['vimeoCode']
                                video_youtube = video['youtubeCode']
                                
                                if video_youtube != None:
                                    youtube_link = 'https://youtube.com/watch?v=' + video_youtube
                                    self.youtube_downloader(youtube_link, path, video_name)
                                    pass
                                elif video_vimeo != None:
                                    vimeo_link = 'https://player.vimeo.com/video/' + video_vimeo
                                    self.vimeo_downloader(vimeo_link, path, video_name)
                                    pass
                                

    def vimeo_downloader(self, vimeo_video, path, title): #Em resumo essa def baixa os videos da VIMEO na melhor qualidade possivel
        vimeo_headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'iframe',
        'Referer': 'https://kuadro.com.br',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        vimeo_config = requests.get(f'{vimeo_video}/config', headers=vimeo_headers).json()
        vimeo_download = sorted(vimeo_config["request"]["files"]["progressive"], key = lambda i:i['height'])
        vimeo_url = vimeo_download[-1]['url']
        video_path = f'{path}/{title}.mp4'
        if os.path.exists(video_path) is False:
            print(f'\t\t\t\t{title}')
            os.system(f'''ffmpeg -i {vimeo_url} -nostats -loglevel 0 -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 "{video_path}"''')            
        else:
            print(f'\t\t\t\t{title} - Já existe, ignorado.')

    def youtube_downloader(self, video_youtube, path, title):

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


        aula_path = f'{path}'
        if os.path.exists(f'{aula_path}/{title}.mp4') is False:
            
            #urllib.request.urlretrieve(video_url, filename=f'{aula_path}/{title}.mp4')
            try:
                yt = YouTube(video_youtube)
                streams = yt.streams.get_highest_resolution().__dict__
                video_url = streams['url']
                videomp4 = requests.get(video_url, headers=headers_yt).content
                with open(f'{aula_path}/{title}.mp4', 'wb') as videodown:
                    videodown.write(videomp4)
                    videodown.close()
                    print(f'\t\t\t\t{title}')
                    time.sleep(60)
                pass
            except:
                os.system(f'youtube-dl --quiet {video_youtube} -o "{aula_path}/{title}.mp4"')
                print(f'\t\t\t\t{title}')
                time.sleep(60)
            pass
        else:
            print(f'\t\t\t\t{title} - Já existe, ignorado.')

    def replacer(self, text): #Essa Def é responsavel unicicamente por tirar os caracteres incorretos para se ter um PATH
        invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - ', '\t': ' - '}
        for char in invalid:
            if char in text:
                text = text.replace(char, invalid[char])
        return text


#start = Downloader()
os.system('cls')
#start.index()
