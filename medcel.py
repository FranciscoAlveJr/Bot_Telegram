import requests
import configparser
import os
import subprocess
import json
import threading
from datetime import datetime

def remove_char_invalid(string):
    inv = '\\/:*?"<>|'
    s = ''

    for x in string:
        if x in inv:
            if x != string[-1]:
                s += ' '
        else:
            s += x

    return s.strip()

    
def remove_char_invalidy(string):
    inv = ':*?"<>|'
    s = ''

    for x in string:
        if x in inv:
            if x != string[-1]:
                s += ' '
        else:
            s += x

    return s.strip()


class Medcel:
    __session = requests.Session()
    __student = None
    input_file = ""
    BN = {}
    config = configparser.ConfigParser()

    def __init__(self, *args, **kw):
        self.config.read("config.ini")
        self.config.sections()
        self.BN = self.config["BINARIES"]
        self.check_binaries()
        self.__session.headers.update({
            'x-host-origin': 'https://areaaluno.medcel.com.br', 
            'x-api-key': 'UdfZ3vw1qmNMrV1BMbLP7peezLKuZ9g8HUrVuOg3', 
            'x-app-version': '3.3.1'
            }
        )

    def check_binaries(self):
        print("Checking binaries...")
        
        errored = []
        for k,v in self.BN.items():
            try:
                subprocess.call([v], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            except:
                if os.path.exists(v) == False:
                    if os.path.exists(f"bin/{v}"):
                        self.BN[k] = "bin/" + v
                    else:
                        errored += [v]
                        print(f"File not found: {v}")
        if len(errored) > 0:
            exit(1)
        print("Binaries Ok!")
    
    def mkdir(self, path):

        path = remove_char_invalidy(path)

        if os.path.exists(path) is False:
            try:
                os.mkdir(path)
                return path
            except:
                print(path)
                path = input('PATH: ')
                os.mkdir(path)
                return path

#
        #except FileExistsError:
            #pass
    
    def edit_config(self, section, key, value):
        self.config[section][key] = value
        with open("config.int", "w") as configfile:
            self.config.write(configfile)
    
    def login(self):
        try:
            data = json.load(open("cookies/medcel.json"))
            self.__student = data["token"]
            print("Login success with medcel.json")
            return
        except (FileNotFoundError, KeyError, json.decoder.JSONDecodeError) as e:
            pass

        payload = {
            "email": self.config["AUTH"]["email"],
            "password": self.config["AUTH"]["password"],
        }
        r = self.__session.post('https://service.medcel.com.br/m1/students/auth', json=payload, stream=True)
        if r.status_code == 200:            
            data = {
                "token": r.json()["_id"],
            }
            self.mkdir("cookies")
            with open("cookies/medcel.json", "w") as cookie:
                json.dump(data, cookie)
        else:
            auth = {
                "email": input("Email: "),
                "password": input("Password: ")
            }
            for k in auth:
                self.edit_config("AUTH", k, auth[k])
        return self.login()

    def getContracts(self):
        url = f"https://service.medcel.com.br/m1/contracts/getContractsByStudent?_id={self.__student}"
        r = self.__session.get(url)
        data = r.json()["contracts"]

        return data

    def getCourse(self, product_id):
        url = f"https://service.medcel.com.br/m1/productContentHierarchies/getProductSpecialties?product={product_id}"
        r = self.__session.get(url)
        data = sorted(r.json(), key=lambda k: k["name"])
        return data
    
    def getThemes(self, contract_id, specialty_id, product_id, hierarchy_id):
        url = f"https://service.medcel.com.br/m1/productContentHierarchies/getThemesBySpecialty?contract={contract_id}&product={product_id}&specialty={specialty_id}&hierarchy={hierarchy_id}"
        r = self.__session.get(url)
        data = r.json()
        return sorted(data, key=lambda k: k["name"])
        
    def getAulas(self, product, studyUnit, path):
        
        url = f"https://service.medcel.com.br/m1/productContentHierarchies/getUnitOfStudyContent?product={product}&studyUnit={studyUnit}&student=5c509959f847e4303670fa7b&podcast=true"
        
        
        #requests.get('https://service.medcel.com.br/m1/productContentHierarchies/getUnitOfStudyContent?product=5b8b260e09841e6944147b24^&studyUnit=5be2df9f4b23b758f415c048^&student=5c509959f847e4303670fa7b^&podcast=false', headers=headers)
        
        aula_header =  {
            'authority': 'service.medcel.com.br',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json, text/plain, */*',
            'x-app-version': 'null',
            'x-amz-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'x-api-key': 'UdfZ3vw1qmNMrV1BMbLP7peezLKuZ9g8HUrVuOg3',
            'x-host-origin': 'https://areaaluno.medcel.com.br',
            'sec-gpc': '1',
            'origin': 'https://areaaluno.medcel.com.br',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://areaaluno.medcel.com.br/',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }


        try:
            r = self.__session.get(url, headers=aula_header)
        except:
            url = f"https://service.medcel.com.br/m1/productContentHierarchies/getUnitOfStudyContent?product={product}&studyUnit={studyUnit}&student=5c509959f847e4303670fa7b&podcast=false"
            r = self.__session.get(url, headers=aula_header)

        data = r.json()

        chapters = data["chapters"]
        videos = data["videos"]
        podcasts = data["podcast"]
        mentalmaps = data["mentalMaps"]

        self.download_materials("Ebooks", chapters, path)
        self.download_materials("Podcasts", podcasts, path)
        self.download_materials("Mapas Mentais", mentalmaps, path)
        self.download_videos(videos, path)

    def download_materials(self, name, material, path):
        if len(material) == 0:
            return
        path += name + "/"
        self.mkdir(path)
        for i, m in enumerate(material, start=1):
            ext = m["url"].split(".")[-1]
            filename = path + str(i).zfill(2) + " - " + remove_char_invalid(m["title"]) + "." + ext
            if os.path.exists(filename) == False:
                print("Downloading: %s" %filename)
                r = requests.get(m["url"])
                with open(filename, "wb") as f:
                    f.write(r.content)


    def download_videos(self, videos, path):
        path_videos = path + "Videos/"
        self.mkdir(path_videos)
        pdfs = []
        self.input_file = ""
        for i, v in enumerate(videos, start=1):
            url = "https://service.medcel.com.br/m3/videos/prepareDownloadQueue?mediaId=" + v["id"]
            r = self.__session.get(url)
            data = r.json()
            for m in data["getVideoToPlay"]["complementMaterial"]:
                pdfs.append(m)
            
            url = data["mediaToDownload"]["uri"]
            video_name = url.split("/")[-1]
            video_name_old = video_name.split("_")[:-1]
            video_name_old = "_".join(video_name_old)
            video_name_new = video_name_old + "." + video_name.split(".")[-1]
            url = url.replace(video_name, video_name_new)
            ext = url.split(".")[-1]
            filename = str(i).zfill(2) + " - " + remove_char_invalid(v["title"]) + "." + ext
            if os.path.exists(path_videos + filename):
                return
            self.input_file += url + "\n    dir=%s\n    out=%s\n" %(path_videos, filename)
            #print("Downloading: %s" %filename)
            
            # subprocess.run(command, stdout=subprocess.DEVNULL)

        if len(pdfs) > 0:
            self.mkdir(path + "PDFs")

        for j, m in enumerate(pdfs, start=1):
            ext = m["location"].split(".")[-1]
            name = m["title"] if len(m["title"]) > 0 else os.path.basename(m["location"]).split(".")[0]
            filename = path + "PDFs/" + str(j).zfill(2) + " - " + remove_char_invalid(name) + "." + ext
            if os.path.exists(filename) == False:
                print("Downloading: %s" %filename)
                r = requests.get(m["location"])
                with open(filename, "wb") as f:
                    f.write(r.content)
        
        self.download_aria()

    def download_aria(self):
        with open("input_file", "w", encoding="utf8") as f:
            f.write(self.input_file)

        command = [
            self.BN['aria2c'],
            '--auto-file-renaming=false',
            '--file-allocation=none',
            '--allow-overwrite=false',
            '--summary-interval=0',
            '--retry-wait=5',
            '--uri-selector=inorder',
            '--console-log-level=warn',
            '--allow-piece-length-change=true',
            '--download-result=hide',
            '-x16',
            '-j16',
            '-s16',
            '--continue=true',
            "--check-certificate=false",
            "-x", "5",
            "-i", "input_file"
        ]
        subprocess.run(command,)


def replacer(text):
    
    invalid = {r'"': r"'", '\\': " - ", '/': "-", '|': " - ", '<': "«", '>': "»", '*': "x", ':': ' -', '?': "¿", '\n': ' - '}
    
    for char in invalid:
        if char in text:
            text = text.replace(char, invalid[char])
    
    return text


if __name__ == "__main__":
    path = "Medcel/"
    medcel = Medcel()
    medcel.login()
    medcel.mkdir(path)
    contracts_full = medcel.getContracts()
    

    for c in contracts_full:
        path_c = path + c["product"]["name"]
        product_id = c["product"]["_id"]
        hierarchy_id = c["product"]["hierarchy"]["_id"]
        medcel.mkdir(path_c)
        course = medcel.getCourse(product_id)
        for i, s in enumerate(course, start=1):
            path_s = path_c + "/" + str(i).zfill(2) + " - " + s["name"]
            medcel.mkdir(path_s)
            themes = medcel.getThemes(contract_id=c["_id"], specialty_id=s["_id"], product_id=product_id, hierarchy_id=hierarchy_id)
            for j, t in enumerate(themes, start=1):
                nome_disso =  replacer(t["name"])
                path_t = path_s + "/" + str(j).zfill(2) + " - " + nome_disso + "/"
                medcel.mkdir(path_t)
                p_id = t["productId"]
                aulas_id = t["_id"]
                print(path_t)
                try:
                    medcel.getAulas(p_id, aulas_id, path_t)
                except Exception as e:
                    print(e)
