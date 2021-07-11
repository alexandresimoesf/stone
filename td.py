from pandas import read_excel, read_html
from collections import defaultdict
import unidecode
import csv
import requests


def coef(n):
    if n < 5000:
        return 5
    elif 5000 >= n < 20000:
        return 10
    elif 20000 >= n < 100000:
        return 15
    elif 100000 >= n < 500000:
        return 20
    else:
        return 25


# dados: dict = {}
# r = requests.get("https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o_(2020)")
# df_list = read_html(r.text)
# df = df_list[0][['Município', 'População']]
#
# for index, row in df.iterrows():
#     print(coef(int('_'.join(row['População'].split()))))
    # dados[unidecode.unidecode(row['Município'])] = int('_'.join(row['População'].split()))

# r = requests.get("https://www.br.undp.org/content/brazil/pt/home/idh0/rankings/idhm-municipios-2010.html")
# df_list = read_html(r.text)
# df = df_list[0][['Município', 'IDHM 2010']]
# for index, row in df.iterrows():
#     print(' '.join(row['Município'].split()[:-1]), row['Município'].split()[-1], row['IDHM 2010'])
#
#
def pos_pagos(cel, pre):
    if str(cel)[::-1].find('.') == 1:
        cel = int(cel)
    else:
        cel = str("%.3f" % cel).replace('.', '_') if '.' in str("%.3f" % cel) else str("%.3f" % cel)
    if str(pre)[::-1].find('.') == 1:
        pre = int(pre)
    else:
        pre = str("%.3f" % pre).replace('.', '_') if '.' in str("%.3f" % pre) else str("%.3f" % pre)

    return int(cel) - int(pre)


r = requests.get("https://www.teleco.com.br/nceluf.asp")
df_list = read_html(r.text)
df = df_list[-4][[(      'Estado',      'Estado'), (        'Maio de 2021',              'Nº Cel.'), ('Maio de 2021',  'Pré  Pagos')]]
for index, row in df.iterrows():
    print(row[(      'Estado',      'Estado')], pos_pagos(row[(        'Maio de 2021',              'Nº Cel.')], row[('Maio de 2021',  'Pré  Pagos')]))
