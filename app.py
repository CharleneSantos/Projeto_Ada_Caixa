#%%
import kagglehub
import os
import pandas as pd
import csv
from kagglehub import KaggleDatasetAdapter
#%%
path = kagglehub.dataset_download("spscientist/students-performance-in-exams")
dataset = "StudentsPerformance.csv"
arquivo = os.path.join(path, dataset)

with open(arquivo, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    dados = list(reader)

    for dado in dados[:5]:
        print(dado)
# %%



# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "spscientist/students-performance-in-exams",
  dataset

)
#%%

df.describe()
#%%
df.info()

