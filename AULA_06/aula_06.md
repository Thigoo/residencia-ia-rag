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
