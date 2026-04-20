# Finno — Assistente Financeiro Inteligente

Projeto de conclusão do Bootcamp Python AI Backend Developer da DIO.

Assistente conversacional com IA generativa voltado ao relacionamento financeiro digital, com respostas personalizadas baseadas no perfil, extrato e portfólio real do cliente.

---

## Sobre o projeto

O Finno resolve um problema central no setor financeiro: clientes com dúvidas simples aguardam longos tempos de atendimento humano, enquanto uma IA com acesso ao contexto certo poderia resolver 80% dessas situações em segundos.

O agente acessa o perfil de risco, o resumo de gastos do mês e os produtos adequados ao cliente — e usa esse contexto para gerar respostas precisas, seguras e personalizadas.

---

## Funcionalidades

- Recomendação de investimentos filtrada por perfil de risco
- Análise de gastos por categoria com base no extrato
- Simulações financeiras com estimativas baseadas em dados reais
- Persistência de contexto durante a conversa
- Regras de segurança anti-alucinação embutidas no prompt

---

## Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| LLM | LLaMA 3.1 8B Instant via Groq API |
| Linguagem | Python 3 |
| Ambiente | Google Colab |
| Dados | JSON + CSV (mockados) |

---

## Estrutura do repositório

```
finno-assistente-financeiro/
├── data/
│   ├── perfil_investidor.json
│   ├── produtos_financeiros.json
│   ├── transacoes.csv
│   └── historico_atendimento.csv
├── docs/
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
├── src/
│   └── app.py
└── README.md
```

---

## Como executar

**Pré-requisito:** conta gratuita na [Groq](https://console.groq.com) para obter a API key.

**No Google Colab:**
1. Faça upload dos arquivos da pasta `data/` e `src/app.py`
2. Configure o secret `FINNO_GROQ_TOKEN` nos Secrets do Colab
3. Execute as células do `app.py` em ordem
4. Converse com o Finno pelo terminal do Colab

**Localmente:**
```bash
pip install groq
python src/app.py
```

---

## Exemplos de perguntas

- "Tenho R$ 2.000 sobrando. Onde investir?"
- "Quanto gastei em alimentação este mês?"
- "Qual meu progresso na meta de aposentadoria?"
- "Explica o que é LCI e se vale para mim"
- "Se eu investir R$ 500 por mês por 25 anos, quanto terei?"

---
