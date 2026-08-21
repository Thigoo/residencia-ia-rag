# Projeto de Arquitetura RAG: Assistente Técnico para Manutenção Automotiva

## Cenário 1: Copiloto Técnico de Oficina e Manutenção Automotiva

---

### Parte 1 - Identificação do Problema

#### 1.1 Descrição do Problema

- **O Problema:**
  Mecânicos e técnicos de manutenção enfrentam grande perda de tempo e risco de erro operacional ao consultar manuais proprietários extensos (+1.000 páginas), tabelas de torque, esquemas elétricos e boletins técnicos de recall para identificar especificações de peças ou procedimentos corretos de montagem.

- **Perfil do Usuário:**
  - **Cargo:** Mecânico / Técnico de Manutenção Automotiva.
  - **Contexto de Uso:** No chão de oficina, operando em tablets ou smartphones ao lado do veículo, necessitando de respostas imediatas e de alta precisão.
  - **Nível Técnico:** Médio a alto domínio de mecânica prática, mas com dependência de dados exatos fornecidos pelas montadoras.

- **Tipo de Informação Consultada:**
  - Textos instrucionais de procedimentos de montagem e desmontagem.
  - Dados estruturados e tabelas técnicas (ex: especificação de torque em Nm, ordem de aperto de parafusos).
  - Catálogos de equivalência e códigos de peças originais.
  - Boletins de serviço e recalls do fabricante.

- **Por que o LLM puramente não resolve?:**
  1. **Privacidade dos Dados:** Manuais de oficina e boletins técnicos de montadoras são documentos proprietários não disponíveis no conjunto de treinamento de LLMs públicos.
  2. **Risco de Alucinação:** Erros em especificações técnicas (ex: torque incorreto em um parafuso de cabeçote) resultam em danos graves ao motor e prejuízo financeiro.
  3. **Tamanho do Contexto e Custo:** Inserir manuais completos de múltiplos veículos no prompt de um LLM é inviável financeiramente e excede os limites operacionais de janela de contexto.

- **Interface de Uso:**
  - Interface Web responsiva (otimizada para dispositivos móveis e tablets), focada em rápida digitação ou entrada por comando de voz no chão da oficina.

- **Exemplos de Perguntas Reais:**
  1. _"Qual é a ordem de aperto e o torque em Nm dos parafusos do cabeçote do motor EA211 1.0?"_
  2. _"Quais são as ferramentas especiais necessárias para trocar a correia dentada do modelo X 2022?"_
  3. _"Existe algum boletim técnico ou recall ativo relacionado ao barulho na caixa de direção do veículo com código de chassi Z?"_

#### 1.2 Por que RAG?

- **Adequação da Solução RAG:**
  - **Acesso a Dados Privados e Restritos:** Permite consultar manuais proprietários, manuais de reparação e boletins técnicos de montadoras sem expor esses dados para treinamento público do LLM.
  - **Ancoragem em Fontes Confiáveis (Groundedness):** Garante que todas as instruções fornecidas ao mecânico sejam extraídas estritamente da documentação oficial cadastrada, eliminando gírias ou procedimentos não homologados.

- **Conhecimento Necessário para o Modelo:**
  - **Base Documental (RAG):** Manuais de oficina, tabelas de torques e folgas, boletins de serviço e manuais de diagnóstico.
  - **Instruções de Comportamento (System Prompt):** Diretrizes para o modelo responder de forma direta, objetiva, usando termos técnicos do setor, indicando sempre o documento/página de origem e declarando explicitamente caso a informação não seja encontrada na base.

- **Frequência de Atualização do Conhecimento:**
  - **Mensal / Trimestral:** A base documental não muda diariamente, mas precisa incorporar novos boletins técnicos, atualizações de procedimentos das montadoras e a inclusão de manuais para novos anos/modelos lançados no mercado.

- **Uso de Documentos Privados:**
  - Sim. Depende integralmente de documentações técnicas oficiais e proprietárias de montadoras e fabricantes de autopeças.

- **Risco do Conhecimento Pré-treinado do LLM (Sem RAG):**
  - O LLM puro tende a generalizar procedimentos entre veículos semelhantes ou "inventar" números plausíveis baseados na média dos dados de treinamento.
  - **Exemplo Concreto de Falha:** Ao perguntar o torque de aperto do cabeçote de um motor específico de 3 cilindros de alumínio, o LLM pré-treinado pode responder _"Aperte com 80 Nm em etapa única"_, misturando o procedimento de um motor antigo de ferro fundido. Se o mecânico aplicar essa força, a rosca do bloco de alumínio espana ou os parafusos rompem, causando a perda total do bloco do motor e prejuízo financeiro direto para a oficina.

#### 1.3 Limitações — Quando RAG Não é a Resposta

- **Casos em que o RAG Falharia ou Seria Inadequado:**
  1. **Consulta de Estoque e Preços em Tempo Real:**
     Perguntas como _"Existe a peça X no estoque e qual o preço atual?"_ exigem precisão absoluta e dados transacionais em tempo real. O RAG busca contextos textuais estáticos; para essa dor, a solução correta é uma consulta direta via API a um banco de dados relacional (SQL) do ERP da oficina.
  2. **Contagem, Agregação e Ordenação entre Múltiplos Documentos:**
     Perguntas que exigem varrer todo o acervo para agregar dados (ex: _"Listar todos os 30 modelos que usam a mesma correia e ordenar do menor para o maior torque"_) sofrem com as limitações da busca vetorial (que recupera apenas os _k_ trechos mais relevantes, omitindo o restante) e da incapacidade do LLM de realizar ordenações e contagens numéricas complexas sem alucinar.
  3. **Interpretação Pura de Esquemas elétricos e Diagramas Visuais:**
     Diagramas elétricos de chicotes e fiação são representações estritamente visuais e estruturadas. Tentar converter um diagrama vetorial em texto para o RAG resulta em perda massiva de informação contextual.

- **Trade-off de Arquitetura:**
  - Para esses cenários, a aplicação deve adotar uma abordagem **Híbrida / Agente** (onde o LLM decide se faz uma busca via RAG na documentação técnica OU se invoca uma API de banco de dados SQL / Leitor de Diagramas), em vez de tentar resolver tudo com busca de texto vetorial.

## Parte 2 - Organização dos Documentos

### 2.1 Mapeamento do Acervo Documental

- **Tipos de Arquivo:**
  - **PDFs (Predominante):** Manuais de oficina, esquemas de montagem e boletins de serviço emitidos pelas montadoras.
  - **Planilhas (XLSX / CSV):** Tabelas de aplicação de peças, conversão de códigos de fabricantes e especificações de torque/fluidos.

- **Volume Aproximado:**
  - **Centenas de Manuais Principais:** Cerca de 300 a 500 manuais de reparação cobrindo a frota circulante.
  - **Milhares de Boletins Técnicos:** Aprox. 2.000 a 5.000 comunicados de recalls, soluções de defeitos recorrentes e atualizações de serviço.

- **Tamanho Típico por Documento:**
  - **Manuais de Oficina completos:** 300 a 1.200 páginas (50 MB a 250 MB por arquivo).
  - **Boletins Técnicos e TSBs (Technical Service Bulletins):** 2 a 8 páginas (1 MB a 5 MB por arquivo).

- **Frequência de Atualização:**
  - **Mensal:** Entrada de novos boletins técnicos de serviço e recalls lançados pelas montadoras.
  - **Anual:** Substituição ou adição de novos manuais de reparação a cada lançamento de ano/modelo de veículo.

---

### 2.2 Estrutura de Pastas e Taxonomia

```text
documentos_oficina/
├── montadoras/
│   ├── volkswagen/
│   │   ├── gol/
│   │   │   ├── 2020-2023/
│   │   │   │   ├── motor/
│   │   │   │   ├── transmissao/
│   │   │   │   ├── suspensao_e_freios/
│   │   │   │   └── eletrica_e_eletronica/
│   │   └── t-cross/
│   └── fiat/
├── boletins_tecnicos/
│   ├── 2024/
│   └── 2026/
└── tabelas_referencia/
    ├── fluidos_e_lubrificantes.xlsx
    └── equivalencia_pecas.xlsx
```

## Parte 3 - Pipeline de Ingestão e Processamento de Dados

---

### 3.1 Extração de Conteúdo no Cenário Automotivo

- **Tratamento de PDFs Técnicos com Texto Selecionável:**
  - Ao receber o arquivo `manual_reparacao_engine_EA211_vw.pdf` (PDF nativo digital), o parser de layout lê a árvore de objetos do documento. Ele identifica blocos de texto e preserva a leitura em colunas mantendo a hierarquia visual dos tópicos (ex: do título `1. Bloco do Motor` para o subtítulo `1.1 Torque de Cabeçote`).

- **Tratamento de PDFs Digitalizados (Escaneados de Manuais Antigos):**
  - Ao processar um boletim de um veículo ano 2005 escaneado pela oficina (`boletim_recolhimento_2005.pdf`), o pipeline converte as páginas do PDF em imagens de alta resolução (300 DPI), aplica um filtro de binarização (preto e branco) para remover marcas de gordura ou sujeira do papel e executa o motor de OCR focado em caracteres alfanuméricos para evitar a confusão de dígitos críticos (ex: não confundir a letra `O` com o número `0` no código de motor `AP 1.8`).

- **Tratamento Específico de Tabelas de Especificação Técnica:**
  - Quando o extrator encontra a _Tabela de Torques e Sequência de Apertos_ na página 42 do manual, ele **não** a converte para texto puro corrido. O pipeline extrai a estrutura de linhas e colunas e a converte para **Markdown/HTML Table**:
    ```markdown
    | Componente     | Parafuso  | Etapa 1 | Etapa 2   | Observação          |
    | :------------- | :-------- | :------ | :-------- | :------------------ |
    | Cabeçote       | M10 x 1,5 | 30 Nm   | 90° + 90° | Substituir parafuso |
    | Cárter de Óleo | M6 x 1,0  | 10 Nm   | -         | Usar trava química  |
    ```
    Isso garante que, quando o modelo buscar o valor, a relação entre a linha `Cabeçote` e a coluna `Etapa 1` permaneça semanticamente amarrada.

- **Tratamento de Imagens e Esquemas Elétricos/Mecânicos:**
  - Diante de uma imagem técnica no manual (ex: `figura_12_ponto_correia.png` mostrando a marcação das engrenagens do comando de válvulas), a imagem é enviada para um modelo de visão computacional com o prompt: _"Descreva a posição das marcas de sincronismo visíveis nesta imagem de motor"_.
  - O modelo gera o texto: _"A marcação 'A' na engrenagem do comando de admissão deve alinhar-se perfeitamente com a ranhura 'B' na tampa traseira"_. Esse texto descritivo é inserido diretamente no corpo do documento extraído logo abaixo do cabeçalho da figura.

- **Caso Concreto de Problema na Extração:**
  - **Problema Encontrado:** Na tentativa de extrair o manual da caixa de transmissão, a ferramenta de leitura leu o código da ferramenta especial `VW-309-A` como `VW` na linha superior e `-309-A` na linha inferior por conta de uma quebra automática do PDF.
  - **Efeito no Sistema:** O mecânico pesquisava por `VW-309-A` e o sistema não encontrava nada.
  - **Solução no Pipeline:** Implementação de uma expressão regular (RegEx) na fase pós-extração para reagrupar padrões de códigos técnicos conhecidos de montadoras antes de enviar para o próximo passo.

---

### 3.2 Limpeza e Normalização Prática

- **O que o Script Remove do Documento:**
  1. **Cabeçalhos de Página Repetitivos:** O script identifica e deleta linhas no topo que contêm strings padrão como `"VW Serviços e Peças - Uso Interno - Pág. XX"`.
  2. **Rodapés com Avisos Legais Genéricos:** Remoção do bloco de texto da margem inferior: _"As informações deste manual estão sujeitas a alterações sem aviso prévio"_.
  3. **Índice Remissivo e Sumário:** O script detecta a seção inicial do documento que lista tópicos e números de página (ex: `"1.2 Sistema de Freios ..... pág 84"`) e descarta essas páginas inteiras, pois elas fazem a busca vetorial recuperar páginas de sumário em vez da instrução técnica real.

- **Padronização do Texto Extraído:**
  - **Codificação:** Conversão forçada de caracteres para `UTF-8` para evitar bugs de acentuação (ex: transformar `cabeÃ§ote` em `cabeçote`).
  - **Padronização de Unidades:** Expressões como `3 Kgfm`, `30Nm`, `30 N.m` e `22 lb-ft` são normalizadas ou anotadas no texto extraído para incluir o padrão universal em `30 Nm` (Newton-metro), garantindo que a busca do mecânico encontre a resposta mesmo que ele digite em outra unidade.

- **Perda Crítica por Limpeza Excessiva (O que NÃO remover):**
  - Se o script de limpeza remover linhas marcadas com asteriscos ou caixas de aviso (ex: `⚠️ ATENÇÃO: Os parafusos do cabeçote são do tipo deformável e NÃO podem ser reutilizados`), o mecânico receberá apenas o torque numérico, aplicará o parafuso velho e o motor falhará. Caixas de aviso e notas técnicas de rodapé são **preservadas obrigatoriamente**.

---

### 3.3 Execução da Frequência e Atualização da Base

- **Como Funciona na Prática:**
  - **Triggers de Entrada:** O pipeline não roda de forma cega em horários fixos. Ele é acionado por **evento**: assim que a equipe de engenharia da oficina faz o upload de um arquivo `TSB_2026_caixa_cambio.pdf` na pasta do sistema, o pipeline é disparado para processar exclusivamente este arquivo.

- **Ciclo de Atualização e Identificação de Arquivos Modificados:**
  1. Quando um documento chega, o script gera uma chave Hash única (**SHA-256**) baseada nos bytes do arquivo.
  2. O sistema consulta o metadado no banco: se o Hash do arquivo `manual_gol_2022.pdf` já existir e for idêntico, o processamento é interrompido para economizar recursos.
  3. Se a montadora lançou uma revisão do manual `manual_gol_2022_v2.pdf`, o Hash será diferente. O pipeline então realiza a substituição cirúrgica:
     - Localiza todos os vetores no banco que possuem a tag `document_id = manual_gol_2022`.
     - Apaga ou marca o campo desses vetores para `status = inativo`.
     - Processa, limpa, gera os novos _chunks_ e grava os novos vetores de `manual_gol_2022_v2.pdf` com `status = ativo`.
  - **Resultado:** A base de dados geral da oficina (com +500 manuais) continua intacta e operando; **apenas as 20 páginas alteradas daquele manual específico foram atualizadas**.
