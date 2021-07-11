from pandas import read_excel, read_html
from collections import defaultdict
import unidecode
import csv
import requests


def pos_pagos(n):
    if str(n)[::-1].find('.') == 1:
        n = int(n)
    else:
        n = str("%.3f" % n).replace('.', '_') if '.' in str("%.3f" % n) else str("%.3f" % n)
    return int(n)


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


def uf(estado):
    if len(estado) > 1:
        if 'GROSSO' in estado and not 'SUL' in estado:
            return estado, 'MT'
        else:
            return estado, estado[0][0] + estado[-1][0]
    else:
        if 'RORAIMA' in estado:
            return estado, 'RR'
        elif 'PARAIBA' in estado:
            return estado, 'PB'
        elif 'PARANA' in estado:
            return estado, 'PR'
        elif 'AMAPA' in estado:
            return estado, 'AP'
        else:
            return estado, estado[0][:2]


populacao_estadual = defaultdict(list)
incorporador = defaultdict(list)
densidade_pos_pago_estado = defaultdict(list)
preparar_calculo: dict = {}

dados: dict = {}
r = requests.get("https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_popula%C3%A7%C3%A3o_(2020)")
df_list = read_html(r.text)
df_populacao = df_list[0][['Município', 'Unidade federativa', 'População']]

for index, row in df_populacao.iterrows():
    dados[unidecode.unidecode(row['Município']).upper()] = int('_'.join(row['População'].split()))
    estado = (uf(unidecode.unidecode(row['Unidade federativa']).upper().split()))
    populacao_estadual[estado[-1]].append(int('_'.join(row['População'].split())))

    incorporador[unidecode.unidecode(row['Município']).upper()].append(estado[-1])
    incorporador[unidecode.unidecode(row['Município']).upper()].append(int('_'.join(row['População'].split())))
    incorporador[unidecode.unidecode(row['Município']).upper()].append(coef(int('_'.join(row['População'].split()))))

for i, j in populacao_estadual.items():
    populacao_estadual[i] = [sum(j)]


r = requests.get("https://www.br.undp.org/content/brazil/pt/home/idh0/rankings/idhm-municipios-2010.html")
df_list = read_html(r.text)
df_idh = df_list[0][['Município', 'IDHM 2010']]

for index, row in df_idh.iterrows():
    try:
        incorporador[unidecode.unidecode(' '.join(row['Município'].split()[:-1])).upper()].append(
            float((row['IDHM 2010']) / 1000))
        # incorporador[unidecode.unidecode(' '.join(row['Município'].split()[:-1])).upper()].append(
        #     coef(int(dados[unidecode.unidecode(' '.join(row['Município'].split()[:-1])).upper()])))
    except:
        pass

    #
r = requests.get("https://www.teleco.com.br/nceluf.asp")
df_list = read_html(r.text)
df_pos_pagos = df_list[-4][[('Estado', 'Estado'), ('Maio de 2021', 'Nº Cel.'), ('Maio de 2021', 'Pré  Pagos')]]
for index, row in df_pos_pagos.iterrows():
    estado = uf(unidecode.unidecode(row[('Estado', 'Estado')]).upper().split())
    densidade_pos_pago_estado[estado[-1]].append((pos_pagos(row[('Maio de 2021', 'Nº Cel.')]) - pos_pagos(row[('Maio de 2021', 'Pré  Pagos')])))

for i, j in densidade_pos_pago_estado.items():
    # Adicionar densidade por estado em populacao_estadual [populacao total, densidade]
    populacao_estadual[i].append(j[0])

# for i, j in incorporador.items():
#     densidade = densidade_pos_pago_estado[j[0]] if j and len(j) > 0 else ''
#     incorporador[i].append(densidade[0] if len(densidade) > 0 else '')
#
for i, j in incorporador.items():
    preparar_calculo[i] = j + populacao_estadual[j[0]]
    # [estado atrelado com populacao estadual e densidade, populacao municipal, coeficiente, idh]

for i, j in preparar_calculo.items():
    print(i, j)
# for i, j in populacao_estadual.items():
#     print(i, j)
