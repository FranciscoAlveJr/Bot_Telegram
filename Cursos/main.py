sites = 'Alura  Aulática  B7Web  Balta.io  CursosMED  DankiCode  Descomplica 2020  Descomplica 2020 Enem Intensivo 2019  DESEC  Desenvolvedor.io '\
' Desenvolvimento Web - Do Zero ao primeiro projeto  Eduk  Escola Espartana  Estrategia Concursos  Estratega Vest&Mili  Filonared  Kuadro  MEDCEL  MEDCURSOS '\
' Percurso  Proenem  Professor Ferreto  Promilitares  RocketSeat  Sala do Saber  SanarFlix  Stoodi  Super-revisão de Química ENEM Medicina  Tecnicas de Estudo e Aprendizagem - Como Passar no ENEM '\
' Terra Negra  TreinaWeb  UpInside  Waldematica'


with open('sites.txt', 'w+') as s:
    for site in sites.strip('\n').lower().split('  '):
        s.write(f'{site}\n')

with open('sites.txt', 'r') as s:
    lista = s.readlines()
    for site in range(len(lista)):
        lista[site] = lista[site].rstrip('\n')
    print(lista)
    