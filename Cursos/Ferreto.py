import requests
import logging
import sys
import os
import argparse
import subprocess
import base64
import json
import threading
from pathlib import Path
from unicodedata import normalize

EMAIL = 'ocoisa081@gmail.com'
SENHA = '18020301.pP'

# LOGGING CONFIGURATION
# DO NOT EDIT BELOW THIS LINE
ch = logging.StreamHandler(sys.stdout)
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)
# -----------------------------

def replacer(text):
    '''Essa Def é responsavel unicicamente por tirar os caracteres incorretos para se ter um PATH'''
    text = str(text)
    invalid = {'"': "'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
    for char in invalid:
        if char in text:
            text = text.replace(char, invalid[char])
    return text

class Downloader:

    def __init__(self):
        self.BN = {}
        self.check_pathes()
        self.__email = None
        self.__passwd = None
        self.disciplinas = []
        self.__session = requests.Session()
        self.erros = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Origin': 'https://plataforma.professorferretto.com.br/entrada/index',
            'Referer': 'https://plataforma.professorferretto.com.br/entrada/index',
        }

    def check_pathes(self):
        Path('binaries/').mkdir(parents=True, exist_ok=True)

        errored = []
        for file in ['aria2c']:
            if Path(f'binaries/{file}.exe').exists():
                self.BN[file] = str(Path(f'binaries/{file}.exe'))
            else:
                try:
                    subprocess.call([file], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                    self.BN[file] = file
                except:
                    errored += [file]
        if len(errored) > 0:
            logger.error(f"Put {', '.join([e for e in errored]) } in binaries!")
            exit()

    def login(self, email=None, passwd=None):
        if self.__email == None:
            self.__email = email
        if self.__passwd == None:
            self.__passwd = passwd

        logger.info('Login...')

        url = 'https://plataforma.professorferretto.com.br/login/authenticate'
        payload = {
            'username': self.__email,
            'password': self.__passwd,
        }

        r = self.__session.post(url, data=payload, headers=self.headers)
        if r.status_code == 200:
            logger.info('Login success!')
        else:
            logger.error('Login error!')

    def getDisciplinas(self):
        logger.info('Getting disciplines...')
        url = 'https://plataforma.professorferretto.com.br/entrada/aluno'
        r = self.__session.get(url)
        while r.status_code != 200:
            self.login(EMAIL, SENHA)
            r = self.__session.get(url)
        disciplinas = r.json()['disciplinas']
        self.disciplinas = sorted(disciplinas, key=lambda k: k["id"])
        if args.info:
            for disciplina in self.disciplinas:
                logger.info(f'Id: {disciplina["id"]} -- Nome: {disciplina["nome"]}')

    def getDisciplinaAssuntos(self, disciplina_id, path):
        url = 'https://plataforma.professorferretto.com.br/api/aluno/assuntoAula?disciplina=' + str(disciplina_id)
        r = self.__session.get(url)
        while r.status_code != 200:
            self.login(EMAIL, SENHA)
            r = self.__session.get(url)
        assuntos = r.json()
        cont = 1
        for assunto in assuntos:
            path_assunto = f'{path}/{str(cont).zfill(2)} - {replacer(assunto["nome"])}'
            cont += 1
            self.getAulas(assunto['id'], path_assunto)
    
    def getMediaToken(self, player_url, path, cont, aula):
        
        mediaTokenJson = None
        while mediaTokenJson == None:
            # request_player = self.__session.get(player_url)
            try:
                request_player = requests.get(player_url)
            except:
                logger.info(player_url)
                continue
            mediaToken = request_player.text.split("window.mediaToken = '")[-1].split("';window")[0]
            try:
                init = mediaToken[:mediaToken.index('eyJp')]
                mediaToken = mediaToken.replace(init, '')
                mediaToken = mediaToken.replace(mediaToken[mediaToken.rindex('W199'):], '')
                mediaToken = mediaToken.replace(mediaToken[mediaToken.rindex('fQ=='):], '')
                mediaToken = mediaToken.replace(mediaToken[mediaToken.rindex('XX0='):], '')
            except ValueError:
                pass

            try:
                mediaToken = base64.b64decode(mediaToken).decode()
            except:
                pass

            try:
                mediaToken = mediaToken[:mediaToken.rindex('}')+1]
            except ValueError:
                pass

            mediaToken = normalize('NFKD', mediaToken).encode('ASCII', 'ignore').decode('ASCII').strip()
            try:
                mediaTokenJson = json.loads(mediaToken)
            except:
                pass
            # self.erros.append(aula)
            # with open('erros.json', 'w') as f:
            #     json.dump(self.erros, f)
            # return
        # output = f'{path}/{str(cont).zfill(2)} - {replacer(mediaTokenJson["title"])}'

        # if os.path.exists(output):
        #     return
        urls = []
        # logger.info(f'Downloading {output}')
        for pos, media in enumerate(mediaTokenJson['deliveryRules'][1]['outputs']):
            if (media['outputName'] in '_RAW') or (int(media['outputName'][:-1]) > 720):
                pass
            else:
                urls.append(media)
        try:
            urls = sorted(urls, key=lambda k: int(k['outputName'][:-1]))
        except:
            print(urls)
        return urls[-1]['url']

    def getPlanos(self, path):
        url = 'https://plataforma.professorferretto.com.br//api/aluno/planoEstudo/extensivo'
        r = self.__session.get(url)
        while r.status_code != 200:
            self.login(EMAIL, SENHA)
            r = self.__session.get(url)
        planos = r.json()
        path += "/Planos de Estudo"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        for plano in planos:
            self.getAulasPlano(plano["nome"], plano["id"], path)


    def getAulasPlano(self, nome, id, path):
        path += f"/{nome}"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        
        url = "https://plataforma.professorferretto.com.br/api/aluno/planoEstudo/" + str(id)
        r = self.__session.get(url)
        while r.status_code != 200:
            self.login(EMAIL, SENHA)
            r = self.__session.get(url)
        try:
            semanas = r.json()["semanas"]
        except:
            print(r.text)
            exit()
        for pos, semana in enumerate(semanas):
            path_semana = path + f"/Semana {str(pos + 1).zfill(2)}"
            try:
                os.mkdir(path_semana)
            except FileExistsError:
                pass

            aulas = semanas[pos]["aulas"]
            self.getAula(aulas, path_semana)


    def getAulas(self, assunto_id, path):
        url = f'https://plataforma.professorferretto.com.br/api/aluno/assuntoAula/{assunto_id}/aulas'
        r = self.__session.get(url)
        while r.status_code != 200:
            self.login(EMAIL, SENHA)
            r = self.__session.get(url)

        try:
            os.mkdir(path)
        except FileExistsError:
            pass


        r = self.__session.get(url)
        while r.status_code != 200:
            self.login(EMAIL, SENHA)
            r = self.__session.get(url)
        aulas = r.json()["aulas"]
        
        self.getAula(aulas, path)
    
    def getAula(self, aulas, path1, cont=0):
        contDisciplinas = {}
        print(path1)
        for aula in aulas:
            try:
                path = path1 + '/' + aula["disciplina"]["nome"]
            except:
                continue
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
            try:
                contDisciplinas[aula["disciplina"]["nome"]] += 1
            except KeyError:
                contDisciplinas[aula["disciplina"]["nome"]] = 1
            cont = contDisciplinas[aula["disciplina"]["nome"]]
            for key in aula:
                if type(aula[key]) == list and key != 'publicos':
                    for i in aula[key]:

                        if key == 'assuntosExercicio':
                            
                            output = f'{path}/{str(cont).zfill(2)} - {replacer(i["assunto"]["nome"])}'
                            requests_file = self.__session.get(f'https://plataforma.professorferretto.com.br/api/aluno/arquivo/{i["assunto"]["arquivo"]}', stream=True)
                            while requests_file.status_code != 200:
                                self.login(EMAIL, SENHA)
                                requests_file = self.__session.get(f'https://plataforma.professorferretto.com.br/api/aluno/arquivo/{i["assunto"]["arquivo"]}', stream=True)
                            ext = '.pdf'
                            output += ' [MATERIAL]' + ext
                            if os.path.exists(output) == False:
                                logger.info(f'Downloading {output}')
                                with open(output, 'wb') as f:
                                    f.write(requests_file.content)
                            continue

                        if "video" in i:
                            player_url = i["video"]["url"]
                            try:
                                
                                output = path + '/' + f'{str(cont).zfill(2)} - {replacer(aula["titulo"])}.mp4'
                            
                                if os.path.exists(output) == False:
                                    url = self.getMediaToken(player_url, path, cont, aula)
                                    if url == None:
                                        continue
                                    logger.info(f'Downloading {output}')
                                    self.downloadVideo(url, output)
                                    #t = threading.Thread(targ=self.downloadVideo, args=(url, output))
                                    #while threading.active_count() > 5:
                                     #   pass
                                    #t.daemon = True
                                    #t.start()
                            except TypeError:
                                pass

                        elif i['arquivo']['publico'] == False:
                            output = f'{path}/{str(cont).zfill(2)} - {replacer(i["tipo"]["nome"])}'

                            # ext = requests_file.headers['Content-Disposition'].split('.')[-1].split('"')[0]
                            ext = 'pdf'
                            output += ' [MATERIAL].' + ext
                           

                            if os.path.exists(output) == False:
                                logger.info(f'Downloading {output}')
                                requests_file = self.__session.get(f'https://plataforma.professorferretto.com.br/api/aluno/arquivo/{i["arquivo"]["id"]}', stream=True)
                                while requests_file.status_code != 200:
                                    self.login(EMAIL, SENHA)
                                    requests_file = self.__session.get(f'https://plataforma.professorferretto.com.br/api/aluno/arquivo/{i["arquivo"]["id"]}', stream=True)
                                with open(output, 'wb') as f:
                                    f.write(requests_file.content)
                                    f.close()


    def downloadVideo(self, url, output):
    #    if os.path.exists(output) == False:
     #       requests_file = requests.get(url, stream=True)
      #      with open(output, 'wb') as f:
       #         f.write(requests_file.content)
        #        f.close()

   # def downloadVideo(self, url, output):
        os.popen(f'{self.BN["aria2c"]} -o "{output}" {url}')
        # command = [
        #     self.BN['aria2c'],
        #     '--allow-overwrite=true',
        #     '--auto-file-renaming=false',
        #     '--file-allocation=none',
        #     '--summary-interval=0',
        #     '--retry-wait=5',
        #     '--uri-selector=inorder',
        #     '--console-log-level=warn',
        #     '--allow-piece-length-change=true',
        #     '--download-result=hide',
        #     '-x16',
        #     '-j16',
        #     '-s16',
        #     '-d',
        #     os.path.dirname(output),
        #     '-o',
        #     os.path.basename(output),
        #     url,
        # ]
        # aria = subprocess.call(command)
        # print('\r')
        # if aria != 0:
        #     raise ValueError("Aria2c exited with code {}".format(aria))
    #     # logger.info('Download complete!')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Professor Ferretto RIP")
    parser.add_argument('-id', help='discipline id', default='')
    parser.add_argument('-i', '--info', action='store_true', help='print discipline information and exit', default=False)
    parser.add_argument('--planos', action='store_true', default=False)

    args = parser.parse_args()

    logger.info('Starting script!')
    ferretto = Downloader()
    ferretto.login(email=EMAIL, passwd=SENHA)
    ferretto.getDisciplinas()
    path = 'Ferretto'
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    if args.planos:
        ferretto.getPlanos(path)
    else:
        cont = 1
        for disciplina in ferretto.disciplinas:
            path_disciplina = f'{path}/{str(cont).zfill(2)} - {replacer(disciplina["nome"])}'
            cont += 1
            try:
                os.mkdir(path_disciplina)
            except FileExistsError:
                pass
            logging.info(f'Downloading: {disciplina["nome"]}...')
            ferretto.getDisciplinaAssuntos(disciplina["id"], path_disciplina)

    logger.info("Script done working!")
