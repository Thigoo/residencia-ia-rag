import numpy as np
import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


def distancia_euclidiana(vec1: np.ndarray, vec2: np.ndarray) -> float:

    return float(np.linalg.norm(vec1 - vec2))


# ============================================
# TESTE RÁPIDO: Entenda a função!
# ============================================
a = np.array([0, 0])
b = np.array([3, 4])

print(f"Distância entre {a} e {b}: {distancia_euclidiana(a, b)}")
print(f"Esperado: 5.0 ✅" if abs(distancia_euclidiana(a, b) - 5.0) < 0.01 else "❌")

def similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    norma_v1 = np.linalg.norm(vec1)
    norma_v2 = np.linalg.norm(vec2)

    if norma_v1 == 0 or norma_v2 == 0:
        return 0.0

    produto_escalar = np.dot(vec1, vec2)

    return float(produto_escalar / (norma_v1 * norma_v2))

def distancia_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return float(1.0 - similaridade_cosseno(vec1, vec2))

modelo = SentenceTransformer('all-MiniLM-L6-v2')

palavras_e_frases = {
    "gato":      "gato é um animal de estimação felino",
    "felino":    "felino é um animal mamífero da família dos gatos",
    "cachorro":  "cachorro é um animal de estimação canino",
    "carro":     "carro é um veículo automotor de quatro rodas",
    "caminhão":  "caminhão é um veículo de transporte de carga",
    "moto":      "moto é um veículo motorizado de duas rodas",
    "banana":    "banana é uma fruta tropical amarela",
    "maçã":      "maçã é uma fruta vermelha ou verde",
    "goiaba":    "goiaba é uma fruta tropical brasileira"
}

embeddings = {}
for palavra, frase in palavras_e_frases.items():
    embeddings[palavra] = modelo.encode(frase)

print(f"✅ Embeddings gerados para {len(palavras_e_frases)} palavras!")
print(f"   Cada embedding tem {len(embeddings['gato'])} dimensões")

# ============================================
# TESTE 1: gato vs cachorro (animais)
# ============================================
print("=" * 60)
print(" gato  vs   cachorro")
print("=" * 60)

d_euc = distancia_euclidiana(embeddings["gato"], embeddings["cachorro"])
d_cos = distancia_cosseno(embeddings["gato"], embeddings["cachorro"])
sim   = similaridade_cosseno(embeddings["gato"], embeddings["cachorro"])

print(f"  Distância Euclidiana: {d_euc:.4f}  (quanto menor = mais parecido)")
print(f"  Distância de Cosseno:  {d_cos:.4f}  (0 = idêntico, 1 = diferente)")
print(f"  Similaridade Cosseno:  {sim:.4f}   (1 = idêntico, 0 = diferente)")
print(f"  → São parecidos! Ambos são animais de estimação ✅")

print()

# ============================================
# TESTE 2: gato vs carro (coisas diferentes)
# ============================================
print("=" * 60)
print(" gato  vs  carro")
print("=" * 60)

d_euc = distancia_euclidiana(embeddings["gato"], embeddings["carro"])
d_cos = distancia_cosseno(embeddings["gato"], embeddings["carro"])
sim   = similaridade_cosseno(embeddings["gato"], embeddings["carro"])

print(f"  Distância Euclidiana: {d_euc:.4f}")
print(f"  Distância de Cosseno:  {d_cos:.4f}")
print(f"  Similaridade Cosseno:  {sim:.4f}")
print(f"  → São bem diferentes! Nada a ver um com o outro ❌")

print()

# ============================================
# TESTE 3: gato vs felino (sinônimos!)
# ============================================
print("=" * 60)
print(" gato  vs   felino")
print("=" * 60)

d_euc = distancia_euclidiana(embeddings["gato"], embeddings["felino"])
d_cos = distancia_cosseno(embeddings["gato"], embeddings["felino"])
sim   = similaridade_cosseno(embeddings["gato"], embeddings["felino"])

print(f"  Distância Euclidiana: {d_euc:.4f}")
print(f"  Distância de Cosseno:  {d_cos:.4f}")
print(f"  Similaridade Cosseno:  {sim:.4f}")
print(f"  → Praticamente sinônimos! Maior similaridade de todas! 🎯")

CAMINHO_MARKDOWN = Path("/content")

print(f"📂 Procurando arquivos .md em: {CAMINHO_MARKDOWN}\n")

# Buscar todos os .md
arquivos_md = list(CAMINHO_MARKDOWN.glob("*.md"))

print(f"📄 {len(arquivos_md)} arquivo(s) encontrado(s):\n")
for arq in arquivos_md:
    print(f"   • {arq.name}")

if len(arquivos_md) == 0:
    print("\n⚠️  Nenhum .md encontrado! Anexe pelo ícone 📁 na barra lateral.")
else:
    print(f"\n✅ Pronto para continuar!")

"""Carregar e dividir em linhas"""

def carregar_documentos_linhas(lista_arquivos):
    """Carrega arquivos .md e divide em linhas."""
    linhas = []
    metadados = []

    for arquivo in lista_arquivos:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Divide por quebras de linha e remove linhas vazias
        linhas_arquivo = [l.strip() for l in conteudo.split("\n") if l.strip()]

        for i, linha in enumerate(linhas_arquivo, start=1):
            linhas.append(linha)
            metadados.append({
                "arquivo": arquivo.name,
                "linha": i,
                "texto": linha
            })

    return linhas, metadados

# Executar
linhas, metadados = carregar_documentos_linhas(arquivos_md)

print(f"✅ Carregadas {len(linhas)} linhas de {len(arquivos_md)} arquivo(s)\n")
print("📋 Prévia (5 primeiras linhas):")
for m in metadados[:5]:
    print(f"   [{m['arquivo']}] linha {m['linha']}: {m['texto'][:80]}...")

def busca_semantica(consulta, trechos, metadados, top_k=5):
    """
    Busca os trechos mais similares à consulta por similaridade de cosseno.
    """
    # 1. Embedding da consulta
    emb_consulta = modelo.encode([consulta])[0]

    # 2. Embeddings dos trechos
    emb_trechos = modelo.encode(trechos)

    # 3. Similaridade de cosseno
    norma_consulta = np.linalg.norm(emb_consulta)
    normas_trechos = np.linalg.norm(emb_trechos, axis=1)
    produtos = np.dot(emb_trechos, emb_consulta)
    similaridades = produtos / (norma_consulta * normas_trechos)

    # 4. Ordenar (maior → menor)
    indices_ordenados = np.argsort(similaridades)[::-1]

    # 5. Montar resultados
    resultados = []
    for idx in indices_ordenados[:top_k]:
        resultados.append({
            "similaridade": similaridades[idx],
            "texto": trechos[idx],
            "metadado": metadados[idx]
        })

    return resultados

print("✅ Função busca_semantica pronta!")

"""Testar busca por LINHAS"""

# ============================================
# CÉLULA 12 — Testar busca semântica por LINHAS
# ============================================
consulta = "inteligência artificial na área da saúde"

print(f"🔍 Buscando por: \"{consulta}\"\n")
print("=" * 60)

resultados = busca_semantica(consulta, linhas, metadados, top_k=5)

for i, res in enumerate(resultados, 1):
    print(f"\n🏆 Resultado #{i} — Similaridade: {res['similaridade']:.4f}")
    print(f"   📄 Arquivo: {res['metadado']['arquivo']}")
    print(f"   📍 Linha:   {res['metadado']['linha']}")
    print(f"   💬 Texto:   {res['texto'][:120]}{'...' if len(res['texto']) > 120 else ''}")

"""Testar busca por PARÁGRAFOS"""

import re

def carregar_documentos_paragrafos(lista_arquivos):
    """Carrega arquivos .md e divide por parágrafos."""
    paragrafos = []
    metadados = []

    for arquivo in lista_arquivos:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        # Divide por parágrafos (duas ou mais quebras de linha)
        paragrafos_arquivo = re.split(r'\n\s*\n', conteudo)
        paragrafos_arquivo = [p.strip() for p in paragrafos_arquivo if p.strip()]

        for i, paragrafo in enumerate(paragrafos_arquivo, start=1):
            paragrafos.append(paragrafo)
            metadados.append({
                "arquivo": arquivo.name,
                "paragrafo": i,
                "texto": paragrafo[:200]
            })

    return paragrafos, metadados

# Carregar parágrafos
paragrafos, metadados_parag = carregar_documentos_paragrafos(arquivos_md)
print(f"✅ Carregados {len(paragrafos)} parágrafos de {len(arquivos_md)} arquivo(s)\n")

# Buscar
consulta = "inteligência artificial na área da saúde"
print(f"🔍 Buscando por: \"{consulta}\"\n")
print("=" * 60)

resultados = busca_semantica(consulta, paragrafos, metadados_parag, top_k=3)

for i, res in enumerate(resultados, 1):
    print(f"\n🏆 Resultado #{i} — Similaridade: {res['similaridade']:.4f}")
    print(f"   📄 Arquivo:    {res['metadado']['arquivo']}")
    print(f"   📍 Parágrafo:  {res['metadado']['paragrafo']}")
    print(f"   💬 Texto:      {res['texto'][:150]}...")