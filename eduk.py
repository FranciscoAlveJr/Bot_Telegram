import requests
import json
from datetime import datetime
import time
start = datetime.now()

#print(str(start)[11:-7])

eduk_session = requests.Session()
headers = {
    'authority': 'www.eduk.com.br',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://www.eduk.com.br',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.eduk.com.br/login?return_to=/^%^3Fref^%^3Dlogout-page',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'v=eduk-mais-teste-50-pct; test_232_pricing_bf=control; test_256_new_search=variation_b',
}


data = {"email": "ocoisa081@gmail.com", "password": "18020301.pP"}
response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
COOKIES = eduk_session.cookies.get_dict()
#COOKIES = {'_dc_gtm_UA-37019485-1': '1', '_fbp': 'fb.2.1603574653336.1361558537', '_ga': 'GA1.3.1368479780.1603574653', '_gcl_au': '1.1.169833723.1603574652', '_gid': 'GA1.3.1420474019.1603574653', '_hjid': '0d8bc013-03ab-4959-9fd5-ce44d49ca53f', '_hjTLDTest': '1', 'amplitude_id_0eecff0adabc361c01a5eaa4227058f4eduk.com.br': 'eyJkZXZpY2VJZCI6ImJjODkwYmNjLWY2MWItNGZmZi1hNGZiLTkxNWY2MWI2MzFmM1IiLCJ1c2VySWQiOiI0NzE0MTU3Iiwib3B0T3V0IjpmYWxzZSwic2Vzc2lvbklkIjoxNjAzNTc0NjUyNzQ5LCJsYXN0RXZlbnRUaW1lIjoxNjAzNTc0NjY4NDc5LCJldmVudElkIjo1LCJpZGVudGlmeUlkIjo4LCJzZXF1ZW5jZU51bWJlciI6MTN9', 'eduk_token': 'b4256136608e401db24181e48dd16047', 'intercom-id-edzzw9vy': '973841a7-55f4-4ac5-baba-5de6e072f5e1', 'intercom-session-edzzw9vy': 'bUxBWWRHN2J5cjMrR0lhK0hPV1BDU0pDSVo5c2s0cldaV25LV0VhQjVQWXRGNEo2RnUwMDJsOHo2eHFUdytveC0tL0RSTlk2U25IZWUwaWdaRkE1dzR4Zz09--9de9aee7d00c48f54e2f468718d4ec6e2a8e2200', 'test_232_pricing_bf': 'control', 'test_256_new_search': 'variation_a', 'test_259_login': 'control', 'v': 'eduk-mais-teste-50-pct'}


def getTotalCursos(idi):
    #response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
    #COOKIES = eduk_session.cookies.get_dict()

    while True:
        try:
            r = eduk_session.get(f'https://beta.eduk.com.br/api/v1/categories/{idi}/stats', cookies=COOKIES)
            break
        except:
            print('Descansando 5 minutos')
            time.sleep(300)
            response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
            COOKIES = eduk_session.cookies.get_dict()
            continue

    
    return r.text

def getCursos(idi, total):
    #response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
    #COOKIES = eduk_session.cookies.get_dict()

    while True:
        try:
            r = eduk_session.get(f'https://beta.eduk.com.br/api/v1/categories/{idi}/courses?limit={total}', cookies=COOKIES)
            break
        except:
            print('Descansando 5 minutos')
            time.sleep(300)
            response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
            COOKIES = eduk_session.cookies.get_dict()
            continue

    
    return r.json()

def getMaterialApoio(idi):
    #response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
    #COOKIES = eduk_session.cookies.get_dict()
    while True:
        try:
            r = eduk_session.get(f'https://beta.eduk.com.br/api/v1/courses/{idi}/additional-contents', cookies=COOKIES)
            break
        except:
            print('Descansando 5 minutos')
            time.sleep(300)
            response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
            COOKIES = eduk_session.cookies.get_dict()
            continue
    return r.json()

def getVideos(idi):
    #
    #
    while True:
        try:
            r = eduk_session.get(f'https://beta.eduk.com.br/api/v1/courses/{idi}/activities', cookies=COOKIES)
            break
        except:
            print('Descansando 5 minutos')
            time.sleep(300)
            response = eduk_session.post('https://www.eduk.com.br/api/v1/session', headers=headers, data=data)
            COOKIES = eduk_session.cookies.get_dict()
            continue
    

    return limpJSONVideos(r.json())

def limpJSONVideos(videos):
    v = []
    modulo = None
    for video in videos:
        if video['is_chapter']:
            modulo = video['title']
        else:
            video['modulo'] = modulo
            v.append(video)

    j = 0
    while j < len(v):
        if v[j]['is_chapter']:
            v.pop(j)
            j = 0
            continue
        j += 1
    return v
        

d = {}

r = eduk_session.get('https://beta.eduk.com.br/api/v1/categories/')
categorias = r.json()


for count, categoria in enumerate(categorias, start=1):
    print(f"{count} - {categoria['name']}")
choi = int(input('Escolha a categoria para gerar o JSON: '))-1

for categoria in categorias[choi:-1]:
    d[categoria['name']] = {}
    #d[categoria['name']]['descricao'] = categoria['description'].strip()
    #d[categoria['name']]['id'] = categoria['id']
    #d[categoria['name']]['url'] = 'https://beta.eduk.com.br/categorias/' + categoria['slug']
    d[categoria['name']]['total_cursos'] = getTotalCursos(categoria['id'])
    print(f"{categoria['name']} tem um total de {d[categoria['name']]['total_cursos']} cursos")
    d[categoria['name']]['cursos'] = []

    cursos = getCursos(categoria['id'], d[categoria['name']]['total_cursos'])
    for curso in cursos:
        dic_curso = {}
        dic_curso['nome'] = curso['title'].strip()
        
        #print(f"\t{}")
        #dic_curso['img'] = curso['cover_image_urls']['1280x360']
        id_curso = curso['slug']
        id_curso = id_curso.split('/')[-1]
        id_curso = id_curso.split('-')[0]
        #dic_curso['id'] = id_curso
        subcategory_name = json.loads((eduk_session.get(f"https://beta.eduk.com.br/api/v1/courses/{id_curso}").text))['subcategory_name']
        dic_curso['subcategoria'] = subcategory_name
        print(f"\t{dic_curso['subcategoria']} - Categoria")
        print(f"\t\t{dic_curso['nome']} - Curso")
        #dic_curso['professores'] = [professor['name'] for professor in curso['_embed']['authors']]
        dic_curso['status'] = curso['status']
        dic_curso['url'] = 'https://beta.eduk.com.br/cursos/' + curso['slug']
        dic_curso['material_apoio'] = []
        dic_curso['videos'] = []

        material_apoio = getMaterialApoio(id_curso)

        for material in material_apoio:
            dic_material = {}
            #dic_material['id'] = material['id']
            dic_material['name'] = material['content_name']
            dic_material['url'] = material['download_url']
            print(f"\t\t\t{dic_material['name']} - Material")

            dic_curso['material_apoio'].append(dic_material)

        videos = getVideos(id_curso)
        
        for video in videos:
            dic_video = {}
            dic_video['position'] = video['position']
            dic_video['title'] = video['title']
            try:
                dic_video['video_url'] = video['video_url'].replace('vimeo.com/', 'player.vimeo.com/video/')
                break
            except:
                pass
            print(f"\t\t\t{dic_video['title']} - Video")
            dic_curso['videos'].append(dic_video)
        
        d[categoria['name']]['cursos'].append(dic_curso)
        
        dic_cursos = {'categorias': d}    
        with open(f'{categoria["name"]}.json', 'w') as f:
            json.dump(dic_cursos, f)
       
dic_cursos = {'categorias': d}    

with open('cursos_2020.json', 'w') as f:
    json.dump(dic_cursos, f)
stop = datetime.now()
print(str(stop)[11:-7])
