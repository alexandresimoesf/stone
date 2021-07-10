from pandas import read_excel, read_html
from collections import defaultdict
import unidecode
import csv
import requests

dd = defaultdict(list)
dados: dict = {}
meus_arquivos = ['202106AGENCIAS.xlsx', '202106POSTOS.xlsx', '202106PAE.xlsx']
for arquivo in meus_arquivos[0:]:
    dados[arquivo] = read_excel(arquivo)['MUNICíPIO'].value_counts().to_dict()

for d in ([arquivo for arquivo in dados.keys()]):
    for key, value in dados[d].items():
        dd[' '.join(key.split())].append(value)

dados.clear()
r = requests.get("https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o_(2020)")
df_list = read_html(r.text)
df = df_list[0][['Município', 'População']]

for index, row in df.iterrows():
    dados[unidecode.unidecode(row['Município'])] = int('_'.join(row['População'].split()))

for i, j in dados.items():
    if i.upper() in dd.keys():
        dd[i.upper()].append(j)

resposta_nb = open('nb.csv', 'w', newline='')
campos = ['Município', 'Valor']
writer = csv.DictWriter(resposta_nb, fieldnames=campos)
writer.writeheader()
for i, j in dd.items():
    writer.writerow({'Município': i, 'Valor': sum(j[:-2]) / j[-1]})
resposta_nb.close()

# r = requests.get("https://www.br.undp.org/content/brazil/pt/home/idh0/rankings/idhm-municipios-2010.html")
# df_list = read_html(r.text)
# df = df_list[0][['Município', 'IDHM 2010']]
# for index, row in df.iterrows():
#     print(' '.join(row['Município'].split()[:-1]), row['Município'].split()[-1], row['IDHM 2010'])


# r = requests.get("https://www.teleco.com.br/nceluf.asp")
# df_list = read_html(r.text)
# df = df_list[-4][[(      'Estado',      'Estado'), ('Maio de 2021',  'Pré  Pagos')]]
# print(df.head())
