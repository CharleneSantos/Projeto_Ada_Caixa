
import kagglehub
import os
import csv
import shortuuid
import matplotlib.pyplot as plt
from collections import Counter
import streamlit as st
from funcoes import valores_unicos, adicionar_novo_item, medias, medias_por_area_conhecimento


path = kagglehub.dataset_download("spscientist/students-performance-in-exams")
arquivo = "StudentsPerformance.csv"
arquivo = os.path.join(path, arquivo)



try:
    with open(arquivo, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        dados = list(reader)
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")



for i, item in enumerate(dados):
    if 'id' not in item:
        novo_item = {'id': shortuuid.uuid(), **item}
        dados[i] = novo_item


v_unicos = valores_unicos(dados)
for k, v in v_unicos.items():
    valores = list(v)
    print(f"{k}: {len(v)} valores únicos ---> {valores}")


#%%Criar função para calcular médias/min/máx/mediana/desvio padrão/%quartis
nota_leitura_genero = medias(dados, 'gender', 'reading score' )
medias_matematica_por_grupo = medias_por_area_conhecimento(dados, 'math score' )
nota_media_matematica = sum([float(item['math score']) for item in dados]) / len(dados)
medias_leitura_por_grupo = medias_por_area_conhecimento(dados, 'reading score' )
nota_media_leitura = sum([float(item['reading score']) for item in dados]) / len(dados)
medias_escrita_por_grupo = medias_por_area_conhecimento(dados, 'writing score' )
nota_media_escrita = sum([float(item['writing score']) for item in dados]) / len(dados)

print(f"Medias das notas de leitura por grupo:\n {medias_leitura_por_grupo}")
print(f"Nota media de matematica: {nota_media_matematica}")
# %%



def porcentagem_generos(dados, campo='gender'):
    contagem = Counter()
    total = len(dados)

    for linha in dados:
        genero = linha.get(campo, '').strip().lower()
        if genero in ['male', 'female']:
            contagem[genero] += 1

    porcentagens = {g: round((contagem[g] / total) * 100, 2) for g in contagem}
    return porcentagens

pc_generos = porcentagem_generos(dados=dados, campo='gender').values()


#%%
plt.figure(figsize=(6, 6))
plt.pie(pc_generos, labels=['Masculino', 'Feminino'], autopct='%1.1f%%', colors=['blue', 'salmon'])
plt.title('Estudantes Avaliados(por gênero)')
plt.show()
# %%

st.title('Análise de Gênero')

# Chama a função para obter as porcentagens

pc_generos_st = porcentagem_generos(dados=dados, campo='gender')

if pc_generos_st:
    # Separa os rótulos e valores para o gráfico de pizza
    rotulos = pc_generos_st.keys()
    valores = pc_generos_st.values()
    # Cria a figura e os eixos do Matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(valores, labels=rotulos, autopct='%1.1f%%', colors=['lightgreen', 'salmon'])
    ax.set_title('Proporção por Gênero')

    # Exibe o gráfico no Streamlit usando st.pyplot()
    st.pyplot(fig)
else:
    st.warning('Não há dados de gênero válidos para exibir.')

# %%
