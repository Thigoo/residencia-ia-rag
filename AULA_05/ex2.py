import json
from pathlib import Path

SCHEMA = {
  
    "fonte":          "nome do arquivo .md de origem (ex.: 'bioetica_e_ia.md')",
    "documento_id":   "identificador do documento (ex.: 'doc03')",
    "chunk_index":    "posição do chunk dentro do documento (0, 1, 2, ...)",
    "estrategia":     "qual das 10 estratégias gerou o chunk (ex.: 'recursive')",
    "chunk_size":     "tamanho de chunk configurado na estratégia",
    "chunk_overlap":  "overlap configurado na estratégia",
    "n_caracteres":   "tamanho real do chunk em caracteres",

 
    "n_tokens":       "número de tokens do chunk (contado com tiktoken)",
    "idioma":         "idioma do documento ('pt' ou 'en')",
    "secao":          "heading/seção de onde o chunk veio (quando disponível)",
}

JUSTIFICATIVAS = {
    "n_tokens": (
        "Permite responder: 'este chunk cabe na janela de contexto do LLM?'. "
        "O custo e o limite de um LLM são medidos em tokens, não em caracteres. "
        "Já foi calculado na Aula 04, então é reaproveitamento direto."
    ),
    "idioma": (
        "A base é heterogênea (artigos em português + papers em inglês). "
        "Este campo permite FILTRAR a busca por idioma — ex.: recuperar só "
        "trechos em português para uma pergunta em português, evitando "
        "misturar idiomas na resposta."
    ),
    "secao": (
        "Guarda o heading da seção de origem (capturado pela estratégia markdown). "
        "Permite CITAR a fonte com precisão na resposta final do RAG: "
        "'segundo a seção X do documento Y', em vez de só citar o arquivo."
    ),
}

def imprimir_schema():
    print("=" * 70)
    print("SCHEMA DE METADADOS")
    print("=" * 70)
    for campo, desc in SCHEMA.items():
        print(f"  {campo:<16} {desc}")

    print("\n" + "=" * 70)
    print("JUSTIFICATIVA DOS CAMPOS PRÓPRIOS")
    print("=" * 70)
    for campo, just in JUSTIFICATIVAS.items():
        print(f"\n  [{campo}]")
        print(f"  {just}")


def exemplo_preenchido():
    """Exemplo real de um chunk seguindo o schema (Entrega 3)."""
    exemplo = {
        "fonte": "bioetica_e_ia.md",
        "documento_id": "doc03",
        "chunk_index": 12,
        "estrategia": "recursive",
        "chunk_size": 1000,
        "chunk_overlap": 100,
        "n_caracteres": 487,
        "n_tokens": 118,
        "idioma": "pt",
        "secao": "Autonomia e opacidade algorítmica",
    }
    print("\n" + "=" * 70)
    print("EXEMPLO PREENCHIDO (JSON)")
    print("=" * 70)
    print(json.dumps(exemplo, ensure_ascii=False, indent=2))
    return exemplo

if __name__ == "__main__":
    imprimir_schema()
    exemplo_preenchido()
    
    print("\n" + "=" * 70)
    print("RESPOSTAS")
    print("=" * 70)
    print("""
1. Qual campo você incluiria para citar a fonte na resposta final do RAG?
   -> 'fonte' + 'secao'. Juntos permitem dizer ao usuário exatamente de onde
      veio a informação: qual documento (fonte) e qual seção (secao). Só o nome
      do arquivo é vago em documentos longos; a seção dá precisão à citação.

2. Por que 'chunk_index' é útil?
   -> Quando um trecho recuperado está cortado no meio de uma explicação, o
      chunk_index permite buscar os chunks VIZINHOS (index-1 e index+1) do mesmo
      documento e reconstruir o contexto completo. Sem ele, você tem o trecho
      isolado mas não sabe o que vem antes ou depois. É a "coordenada" do chunk
      dentro do documento.
""")