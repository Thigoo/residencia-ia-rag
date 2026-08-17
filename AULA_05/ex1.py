from langchain_core.documents import Document


documentos = [
    Document(
        page_content="Embeddings são representações vetoriais densas de texto, "
                     "onde textos com significado parecido ficam próximos no espaço.",
        metadata={"fonte": "aula_03.md", "pagina": 1, "tipo": "teoria",
                  "tema": "embeddings", "autor": "Marco"},
    ),
    Document(
        page_content="Chunking é a divisão de documentos grandes em pedaços menores "
                     "antes de gerar embeddings, para permitir recuperação granular.",
        metadata={"fonte": "aula_04.md", "pagina": 1, "tipo": "teoria",
                  "tema": "chunking", "autor": "Marco"},
    ),
    Document(
        page_content="RAG combina recuperação de trechos relevantes com geração de "
                     "texto por um LLM, respondendo perguntas com base em documentos.",
        metadata={"fonte": "aula_01.md", "pagina": 2, "tipo": "teoria",
                  "tema": "rag", "autor": "Marco"},
    ),
    Document(
        page_content="Um token é a unidade em que o modelo divide o texto; não é uma "
                     "palavra inteira, mas um pedaço dela.",
        metadata={"fonte": "aula_02.md", "pagina": 1, "tipo": "teoria",
                  "tema": "tokenizacao", "autor": "Marco"},
    ),
    Document(
        page_content="A similaridade de cosseno mede o ângulo entre dois vetores, "
                     "ignorando o tamanho, e é a métrica padrão em sistemas de RAG.",
        metadata={"fonte": "aula_03.md", "pagina": 3, "tipo": "pratica",
                  "tema": "embeddings", "autor": "Marco"},
    ),
]


for i, doc in enumerate(documentos, start=1):
    print(f"--- Documento {i} ---")
    print(f"  page_content: {doc.page_content}")
    print(f"  metadata:     {doc.metadata}\n")


print(f"Total de documentos: {len(documentos)}")


print("\n" + "=" * 60)
print("TESTE 1: metadata aceita lista ou dicionário aninhado?")
print("=" * 60)
doc_complexo = Document(
    page_content="Teste de metadados complexos.",
    metadata={
        "fonte": "teste.md",
        "temas_lista": ["embeddings", "chunking", "rag"],   
        "config": {"chunk_size": 500, "overlap": 50},        
    },
)
print(f"  Criado com sucesso. metadata: {doc_complexo.metadata}")
print(f"  A lista dentro: {doc_complexo.metadata['temas_lista']}")
print(f"  O dict aninhado: {doc_complexo.metadata['config']}")

print("\n" + "=" * 60)
print("TESTE 2: Document sem passar metadata")
print("=" * 60)
doc_sem_meta = Document(page_content="Documento sem metadata explícito.")
print(f"  Criado com sucesso. metadata: {doc_sem_meta.metadata}")
print(f"  Tipo do metadata: {type(doc_sem_meta.metadata)}")