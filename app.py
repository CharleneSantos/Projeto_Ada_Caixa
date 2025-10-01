#%%
import kagglehub
import os
import csv
import shortuuid
import matplotlib.pyplot as plt
import streamlit as st
from funcoes import adicionar_novo_item, medias, mostrar_medias_por_area, valores_unicos, calcular_nota_media, valores_unicos_por_grupo, porcentagem_por_grupos, calcular_estatisticas, st_porcentagem_por_grupos, salvar_dic_em_csv


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


salvar_dic_em_csv("StudentsPerformance_salvo.csv", dados)



################Relatórios e Análises#####################


print(f'''
      ----------------DADOS GERAIS----------------
      
    
Numero total de registros: {len(dados)}


% TOTAL DE ESTUDANTES POR GRUPO:

{porcentagem_por_grupos(dados, 'gender' )}
{porcentagem_por_grupos(dados, 'race/ethnicity' )}
{porcentagem_por_grupos(dados, 'parental level of education' )}
{porcentagem_por_grupos(dados, 'lunch' )}
{porcentagem_por_grupos(dados, 'test preparation course' )}
      ''')


valores_unicos(dados, 'gender','race/ethnicity', 'parental level of education','lunch', 'test preparation course')


print(f'''
ESTATÍSTICAS DESCRTIVAS - Matemática:''')
est_matematica = calcular_estatisticas('math score', dados)

for k, v in est_matematica.items():
     print(f'\t{k}: {v}')

print(f'''
      ESTATÍSTICAS DESCRTIVAS - Leitura:''')
est_leitura = calcular_estatisticas('reading score', dados)
for k, v in est_leitura.items():
     print(f'\t{k}: {v}')

print(f'''
      ESTATÍSTICAS DESCRTIVAS - Escrita:''')
est_escrita = calcular_estatisticas('writing score', dados)
for k, v in est_escrita.items():
	 print(f'\t{k}: {v}')


nota_media_matematica = calcular_nota_media('math score', dados)
nota_media_leitura = calcular_nota_media('reading score', dados)
nota_media_escrita = calcular_nota_media('writing score', dados)

print(f'''
NOTAS MÉDIAS POR ÁREA DO CONHECIMENTO:
      
	matemática: {nota_media_matematica}
    
	leitura: {nota_media_leitura}
    
	escrita:{nota_media_escrita}''')



print(f'''
NOTAS MÉDIAS POR GRUPOS: 
      ''')
      
mostrar_medias_por_area(dados, ['math score', 'reading score', 'writing score'])





# #%%

azul_caixa = '#005CA9'
laranja_caixa = '#F39200'		
tangerina = '#F9B000'
ceu = '#00B5E5'  # Azul Céu
goiaba = '#EF765E'
turquesa = '#54BBAB'
uva = '#B26F9B'
limao = '#AFCA0B'  # Limão
azul_marinho = '#004198'
branca = '#FFFFFF'





st.write(f"<h1 style='color: {azul_marinho};text-align: center'>Análise da Performance de Estudantes em Testes</h1>", unsafe_allow_html=True)
st.sidebar.title("Filtros")
col1, col2 = st.columns(2)

pc_genero_st = st_porcentagem_por_grupos(dados, 'gender')
if pc_genero_st:
    
    rotulos = list(pc_genero_st.keys())
    valores = list(pc_genero_st.values())
    # Cria a figura e os eixos do Matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))  # Tamanho ajustado para o Streamlit
    ax.pie(valores, 
           	labels=rotulos, 
        	autopct='%1.1f%%', 
            colors=['lightgreen', 'salmon'],
            textprops={'fontsize':8},
            
    )
    ax.set_title('Proporção por Gênero', fontsize=12, loc='left')
    col1.pyplot(fig)


else:
    st.warning('Não há dados de gênero válidos para exibir.')
    




# #%%



# print(est_matematica['minimo'])
# #%% 
# # Criar função para calcular correlação entre variavel nuimerica e categorica


# %%
