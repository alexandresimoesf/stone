from pandas import read_excel, read_html
from collections import defaultdict
import unidecode
import csv
import requests


def coef(n):
    if n < 5000:
        return 5
    elif 500 <= n < 20000:
        return 10
    elif 20000 <= n < 100000:
        return 15
    elif 10000 <= n < 500000:
        return 20
    else:
        return 25


populacao_estadual = defaultdict(list)

dados: dict = {}
r = requests.get("https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o_(2020)")
df_list = read_html(r.text)
df = df_list[0][['Município', 'Unidade federativa', 'População']]

for index, row in df.iterrows():
    # print(coef(int('_'.join(row['População'].split()))))
    dados[unidecode.unidecode(row['Município']).upper()] = int('_'.join(row['População'].split())),
#     populacao_estadual[unidecode.unidecode(row['Unidade federativa']).upper()].append(int('_'.join(row['População'].split())))


# for i, j in populacao_estadual.items():
#     print(i, sum(j))

r = requests.get("https://www.br.undp.org/content/brazil/pt/home/idh0/rankings/idhm-municipios-2010.html")
df_list = read_html(r.text)
df = df_list[0][['Município', 'IDHM 2010']]
for index, row in df.iterrows():
    print(row['Município'], int(dados[unidecode.unidecode(' '.join(row['Município'].split()[:-1])).upper()][0]), '{}%'.format('%.3f' % (float((row['IDHM 2010'])/1000) ** coef(int(dados[unidecode.unidecode(' '.join(row['Município'].split()[:-1])).upper()][0])) * 100)))
    # print(unidecode.unidecode(' '.join(row['Município'].split()[:-1])).upper(), row['IDHM 2010'])

#
# def pos_pagos(n):
#     if str(n)[::-1].find('.') == 1:
#         n = int(n)
#     else:
#         n = str("%.3f" % n).replace('.', '_') if '.' in str("%.3f" % n) else str("%.3f" % n)
#     return int(n)


#
# r = requests.get("https://www.teleco.com.br/nceluf.asp")
# df_list = read_html(r.text)
# df = df_list[-4][[('Estado', 'Estado'), ('Maio de 2021', 'Nº Cel.'), ('Maio de 2021', 'Pré  Pagos')]]
# for index, row in df.iterrows():
#     populacao_estadual[unidecode.unidecode(row[('Estado', 'Estado')]).upper()].append(
#         1000 * (pos_pagos(row[('Maio de 2021', 'Nº Cel.')]) - pos_pagos(row[('Maio de 2021', 'Pré  Pagos')])))
#     # print(unidecode.unidecode(row[(      'Estado',      'Estado')]).upper(), 1000 * (pos_pagos(row[(        'Maio de 2021',              'Nº Cel.')]) - pos_pagos(row[('Maio de 2021',  'Pré  Pagos')])))
#
# for i, j in populacao_estadual.items():
#     if sum(j[:-2]) <= 0:
#         pass
#     else:
#         print(i, '%.3f' % float(j[-1] / sum(j[:-2])))
