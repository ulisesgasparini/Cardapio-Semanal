import sqlite3
import pandas as pd
import os

# Carregar os arquivos CSV da pasta local
df_pratos = pd.read_csv("pratos.csv")
df_saladas = pd.read_csv("saladas.csv")
df_base = pd.read_csv("de_base_para_ingredientes.csv")

db_path = "cardapio.db"
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Tabela pratos
cursor.execute('''
CREATE TABLE pratos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_do_prato TEXT NOT NULL,
    tempo_de_preparo TEXT,
    receita TEXT,
    legumes TEXT,
    proteinas TEXT,
    carboidratos TEXT,
    requisitos TEXT,
    calorias INTEGER
)
''')

for _, row in df_pratos.iterrows():
    nome = row.get('Nome do Prato') or row.get('nome do Prato') or row.get('nome_do_prato') or row.get('Nome')
    if pd.isna(nome) or not str(nome).strip():
        continue
    tempo = row.get('Tempo de Preparo') or row.get('tempo de preparo') or row.get('Tempo') or row.get('tempo')
    receita = row.get('Receita') or row.get('receita') or row.get('Modo de Preparo')
    legumes = row.get('Legumes') or row.get('legumes')
    proteinas = row.get('Proteínas') or row.get('proteinas')
    carbos = row.get('Carboidratos') or row.get('carboidratos')
    requisitos = row.get('Requisitos') or row.get('requisitos')
    calorias = row.get('Calorias') or row.get('calorias')
    try:
        calorias = int(float(calorias))
    except:
        calorias = 0

    cursor.execute('''
    INSERT INTO pratos (nome_do_prato, tempo_de_preparo, receita, legumes, proteinas, carboidratos, requisitos, calorias)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        str(nome).strip(),
        str(tempo).strip() if pd.notna(tempo) else "20 min",
        str(receita).strip() if pd.notna(receita) else "",
        str(legumes).strip() if pd.notna(legumes) else "",
        str(proteinas).strip() if pd.notna(proteinas) else "",
        str(carbos).strip() if pd.notna(carbos) else "",
        str(requisitos).strip() if pd.notna(requisitos) else "",
        calorias
    ))

# 2. Tabela saladas
cursor.execute('''
CREATE TABLE saladas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_da_salada TEXT NOT NULL,
    tempo TEXT,
    modo_de_preparo TEXT,
    legumes TEXT,
    proteinas TEXT,
    carboidratos TEXT,
    requisitos TEXT,
    calorias INTEGER
)
''')

for _, row in df_saladas.iterrows():
    nome = row.get('Nome da Salada') or row.get('nome da Salada') or row.get('nome_da_salada') or row.get('Nome')
    if pd.isna(nome) or not str(nome).strip():
        continue
    tempo = row.get('Tempo') or row.get('tempo')
    preparo = row.get('Modo de Preparo') or row.get('modo_de_preparo') or row.get('Receita')
    legumes = row.get('Legumes') or row.get('legumes')
    proteinas = row.get('Proteínas') or row.get('proteinas')
    carbos = row.get('Carboidratos') or row.get('carboidratos')
    requisitos = row.get('Requisitos') or row.get('requisitos')
    calorias = row.get('Calorias') or row.get('calorias')
    try:
        calorias = int(float(calorias))
    except:
        calorias = 0

    cursor.execute('''
    INSERT INTO saladas (nome_da_salada, tempo, modo_de_preparo, legumes, proteinas, carboidratos, requisitos, calorias)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        str(nome).strip(),
        str(tempo).strip() if pd.notna(tempo) else "15 min",
        str(preparo).strip() if pd.notna(preparo) else "",
        str(legumes).strip() if pd.notna(legumes) else "",
        str(proteinas).strip() if pd.notna(proteinas) else "",
        str(carbos).strip() if pd.notna(carbos) else "",
        str(requisitos).strip() if pd.notna(requisitos) else "",
        calorias
    ))

# 3. Tabela de_base_para_ingredientes
cursor.execute('''
CREATE TABLE de_base_para_ingredientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bases TEXT NOT NULL,
    ingredientes TEXT NOT NULL,
    unidades TEXT NOT NULL
)
''')

for _, row in df_base.iterrows():
    base = row.get('Bases') or row.get('bases') or row.get('Base')
    ingrediente = row.get('Ingrediente') or row.get('Ingredientes') or row.get('ingredientes')
    unidades = row.get('Unidades') or row.get('unidades') or row.get('Unidade')
    if pd.isna(base) or pd.isna(ingrediente):
        continue
    cursor.execute('''
    INSERT INTO de_base_para_ingredientes (bases, ingredientes, unidades)
    VALUES (?, ?, ?)
    ''', (
        str(base).strip(),
        str(ingrediente).strip(),
        str(unidades).strip() if pd.notna(unidades) else "1 un"
    ))

conn.commit()
conn.close()
print("Banco de dados 'cardapio.db' gerado com sucesso!")
