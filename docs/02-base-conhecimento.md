# Base de Conhecimento — Finno

## Estratégia de Dados

O Finno utiliza dados mockados que simulam um cliente real de banco digital. Todos os dados são carregados no contexto da conversa via injeção no system prompt, garantindo que o LLM responda com base em informações reais do cliente — não em suposições.

---

## Fontes de Dados

### perfil_investidor.json
Contém o perfil completo do cliente:
- Dados demográficos e renda
- Perfil de risco (conservador / moderado / arrojado)
- Objetivos financeiros e metas com valores e prazos
- Preferências de investimento e aversões

**Uso no agente:** injetado no system prompt para personalizar todas as recomendações.

---

### transacoes.csv
Histórico de transações dos últimos 2 meses:
- Data, descrição, categoria, valor e tipo (débito/crédito)
- Categorias: moradia, alimentação, investimento, saúde, transporte, lazer, utilidades

**Uso no agente:** resumo de gastos por categoria calculado em Python antes de enviar ao LLM, para responder perguntas como "quanto gastei em alimentação este mês?".

---

### produtos_financeiros.json
Catálogo de produtos disponíveis no banco:
- CDB, Tesouro Direto, Fundos, Renda Variável, LCI
- Rentabilidade, liquidez, risco e perfil indicado

**Uso no agente:** filtrado por perfil de risco do cliente antes de recomendar.

---

### historico_atendimento.csv
Registro de interações anteriores do cliente com o banco:
- Canal, assunto, resolução e nota de satisfação

**Uso no agente:** contexto para o agente não repetir explicações já dadas e personalizar abordagem.

---

## Como os Dados São Injetados

```python
# Resumo de gastos calculado antes do prompt
gastos_por_categoria = transacoes_df[transacoes_df['tipo'] == 'debito'] \
    .groupby('categoria')['valor'].sum().abs().to_dict()

# Produtos filtrados por perfil
perfil = perfil_json['cliente']['perfil_risco']
produtos_adequados = [p for p in produtos_json['produtos']
                      if perfil in p['indicado_para']]

# Tudo injetado no system prompt como contexto estruturado
```
