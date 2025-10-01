#%%
import shortuuid
from itertools import groupby
from operator import itemgetter

def adicionar_novo_item(item_novo, dados):
    '''
    Adiciona um novo dicionário à lista, garantindo um id único.
    '''
    item_novo_com_id = {'id': shortuuid.uuid(), **item_novo}
    dados.append(item_novo_com_id)


def valores_unicos(linhas):
    unicos = {}
    for linha in linhas:
        for k, v in linha.items():
            unicos.setdefault(k, set()).add(v)
        
    return unicos


def medias(dados, campo_grupo, coluna):
    
    dados_ordenados = sorted(dados, key=itemgetter(f'{campo_grupo}'))

    medias = {}
    for grupo, itens in groupby(dados_ordenados, key=itemgetter(f'{campo_grupo}')):
        scores = [float(item[coluna]) for item in itens]
        medias[grupo] = sum(scores) / len(scores)

    return medias

def medias_por_area_conhecimento(dados, area_conhecimento):
    nome_colunas = (list(dados[0].keys()))
    grupos = nome_colunas[1:6]
    # print(f"{area_conhecimento.upper()}")

    infos = []
    for grupo in grupos: 
        medias_g = medias(dados, grupo, area_conhecimento)
        infos.append((grupo, medias_g))
    return infos 



