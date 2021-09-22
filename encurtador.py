urls = [
    'https://drive.google.com/drive/folders/121R3kcfJr25VN3TyNutQEabWplv2BudB?usp=sharing',
    'https://drive.google.com/drive/folders/1q99l3xMxSpzJJz2KGQIfqHKv2Fc1KxAN?usp=sharing',
    'https://drive.google.com/drive/folders/1_7H8-FL1JdccOzsbW0UOOUCICi1FER7b?usp=sharing',
    'https://drive.google.com/drive/folders/10Vcn8zs9utM5DF1zzaY3YBG3Y9cVqQ5m?usp=sharing',
    'https://drive.google.com/drive/folders/1Ymy67akfLh1PNyj9bBq4ZowYSXgEWnqz?usp=sharing',
    'https://drive.google.com/drive/folders/1Z0HWqXZQvZhIqJXOY2Gc-O0tKb5XjDVw?usp=sharing',
    'https://drive.google.com/drive/folders/1pP5eiQ0bCrGjUUvnDTLW8Fp8ltSU6WZY?usp=sharing',
    'https://drive.google.com/drive/folders/1A5Z1GBJ4Fi3D9gTui2req9HeH21I3CGt?usp=sharing',
    'https://drive.google.com/drive/folders/1JU4jcFTnL-OPyKnvmo9S2WJiHfnAFDlv?usp=sharing',
    'https://drive.google.com/drive/folders/1XSTDUIBvZniEBYrEGy2Ewg4T_McNatWK?usp=sharing',
    'https://drive.google.com/drive/folders/1is4qolLClvVtljApPcU4jrfXgAsFpiUk?usp=sharing',
    'https://drive.google.com/drive/folders/1E8h_fA6OMB_Sm6tkKTJAk5nsolnehRlq?usp=sharing',
    'https://drive.google.com/drive/folders/16Rhy0Lc7XmAhGRwm1vwSoUTFeQcST27X?usp=sharing',
    'https://drive.google.com/drive/folders/1_KQvAYDfYkqvNOT6g8Lh3spWrA94EVtT?usp=sharing',
    'https://drive.google.com/drive/folders/1Ho2kAKh_BehZ3O-OJWSIa8zJtb_NreeH?usp=sharing',
    'https://drive.google.com/drive/folders/1Cae-m4jWKuFzZ0Eqa439Re_No-S0sXzG?usp=sharing',
    'https://drive.google.com/drive/folders/11gGVtle-wPKBhEDrHkdayv48RxiOK5FW?usp=sharing',
    'https://drive.google.com/drive/folders/1kSDjTIm82b1v-hlsdoy14geIiisLuTVL?usp=sharing',
    'https://drive.google.com/drive/folders/1EAPyGH03vfLi0oUuuA2rMPzl9kk-v0j9?usp=sharing',
    'https://drive.google.com/drive/folders/1tjsoWoLapvp4WJLwj5JSEr63et1IFNIJ?usp=sharing',
    'https://drive.google.com/drive/folders/1JqrkWLkGUo57b7C1dViDjxDgBMleF09b?usp=sharing',
    'https://drive.google.com/drive/folders/1XW071JPCdvV2ivlPfok3oJ18Tfqj1eys?usp=sharing',
    'https://drive.google.com/drive/folders/1FQov2cqCKJsKinPMkjrhm-bx65_jOpFD?usp=sharing',
    'https://drive.google.com/drive/folders/1dWFNxlnjF8PlD5-tYdSGkBlIau-TE8fr?usp=sharing',
    'https://drive.google.com/drive/folders/1dCpihOoQsqyQFDn8GxzoNcirxePCm7Ar?usp=sharing',
    'https://drive.google.com/drive/folders/1w34pthAwTnM1iakrOrkb60LUGzhZMbHP?usp=sharing',
    'https://drive.google.com/drive/folders/1lzq0hePA4XRShOKi1M6cKctt4F-dCges?usp=sharing',
    'https://drive.google.com/drive/folders/1eaSP2cj_QkxWlQ5-odFvdTts5tD9ACrw?usp=sharing',
    'https://drive.google.com/drive/folders/1qANIUJmmfgZ72ecVFsM7UMPNpdayuPI_?usp=sharing',
    'https://drive.google.com/drive/folders/10dh5DN3KlRhPkxrLX9dDml39CXa7CXP-?usp=sharing',
    'https://drive.google.com/drive/folders/1V1fGfxmq77xlOA6e5gitNWpF_njLIcuN?usp=sharing',
    'https://drive.google.com/drive/folders/1yiWYLK_9ZoNfqWMNND6pVDMrbnSghrQF?usp=sharing',
    'https://drive.google.com/drive/folders/12N4xGf96shXke8X9btbowq5giZAmxeL_?usp=sharing',
]

def site_url(site):
    links = {}

    with open('sites.txt', 'r+') as s:
        lista = s.readlines()
        for i, nome in enumerate(lista):
            lista[i] = lista[i].rstrip('\n')
            links[lista[i]] = urls[i]
    return links[str(site)]

