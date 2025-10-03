#%%
import shortuuid
from itertools import groupby
from operator import itemgetter
from collections import Counter


def adicionar_novo_item(item_novo, dados):
    '''
    Adiciona um novo dicionário à lista, garantindo um id único.
    '''
    item_novo_com_id = {'id': shortuuid.uuid(), **item_novo}
    dados.append(item_novo_com_id)



def valores_unicos_por_grupo(linhas, grupo):
    unicos = {}
    for linha in linhas:
        for k, v in linha.items():
            unicos.setdefault(k, set()).add(v)
        
    return unicos[grupo]


def valores_unicos(dados, *grupos):
    print("VALORES ÚNICOS POR GRUPO")
    for grupo in grupos:
        valores = valores_unicos_por_grupo(dados, grupo)
        print(f"\t{grupo}: {len(valores)} valores únicos ---> {list(valores)}")

def porcentagem_por_grupos(dados, grupo):
    contagem = Counter()
    total = len(dados)
    valores = list(valores_unicos_por_grupo(dados, grupo))


    for linha in dados:
        valor = linha.get(grupo, '')
        if valor in valores:
            contagem[valor] += 1

    porcentagens = {g: round((contagem[g] / total) * 100, 2) for g in contagem}
    retorno  = f'''{grupo}:\n'''
    
    for g, p in sorted(porcentagens.items()):
        retorno += f'''     {g}: {p}%\n'''

    return retorno
    

def medias(dados, campo_grupo, coluna):
    
    dados_ordenados = sorted(dados, key=itemgetter(f'{campo_grupo}'))

    medias = {}
    for grupo, itens in groupby(dados_ordenados, key=itemgetter(f'{campo_grupo}')):
        scores = [float(item[coluna]) for item in itens]
        medias[grupo] = round(sum(scores) / len(scores),2)

    return medias

def mostrar_medias_por_area(dados, areas_conhecimento):
    nome_colunas = list(dados[0].keys())
    grupos = nome_colunas[1:6]  # Ajuste conforme os grupos desejados


    for area in areas_conhecimento:
        print(f"\nMedias {area.upper()} por grupo")
        for grupo in grupos:
            medias_g = medias(dados, grupo, area)
            print(f"\n\tGrupo: {grupo}")
            for categoria, valor in sorted(medias_g.items(), key=lambda x: x[1], reverse=True):
                print(f"\t- {categoria}: {round(valor, 2)}")


            


def calcular_nota_media(area_conhecimento, dados):

    nota = round(sum([float(item[area_conhecimento]) for item in dados]) / len(dados),2)
  
    return nota




def calcular_estatisticas(area_conhecimento, dados):
    from statistics import mean, median, stdev, quantiles

    notas = [float(item[area_conhecimento]) for item in dados]
    estatisticas = {
        'mínimo': round(min(notas), 2),
        'máximo': round(max(notas), 2),
        'média': round(mean(notas), 2),
        'mediana': round(median(notas), 2),
        'desvio padrão': round(stdev(notas), 2),
        'quartis': [round(q, 2) for q in quantiles(notas, n=4)]
    }
    return estatisticas

def st_porcentagem_por_grupos(dados, grupo):
    from collections import Counter

    contagem = Counter()
    total = len(dados)
    valores = list(valores_unicos_por_grupo(dados, grupo))

    for linha in dados:
        valor = linha.get(grupo, '').strip()
        if valor in valores:
            contagem[valor] += 1

    porcentagens = {g: round((contagem[g] / total) * 100, 2) for g in contagem}
    return porcentagens




def salvar_dic_em_csv(arquivo_novo, dataset):
# novo_arquivo = "StudentsPerformance_salvo.csv"
    import csv

    with open(arquivo_novo, mode='w', newline='', encoding='utf-8') as f_out:
        campos = dataset[0].keys()  # Usa os cabeçalhos do primeiro dicionário
        escritor = csv.DictWriter(f_out, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(dataset)

        print(f"✅ Arquivo salvo como '{arquivo_novo}' com sucesso!")




import matplotlib.pyplot as plt

def grafico_porcentagem(dados, grupo, cor='#00B5E5'):
    porcentagens = st_porcentagem_por_grupos(dados, grupo)
    
    categorias = list(porcentagens.keys())
    valores = list(porcentagens.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categorias, valores, color=cor)
    plt.title(f'Porcentagem por {grupo}', fontsize=14)
    plt.ylabel('Porcentagem (%)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()