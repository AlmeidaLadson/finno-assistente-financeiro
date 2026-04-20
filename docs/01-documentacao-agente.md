# Documentação do Agente — Finno

## Caso de Uso

O **Finno** é um assistente financeiro inteligente voltado para clientes de banco digital de perfil moderado. Ele resolve um problema central no relacionamento financeiro: a dificuldade do cliente em entender seus dados financeiros e tomar decisões de investimento com segurança, sem depender de atendimento humano para perguntas do dia a dia.

**Problema que resolve:**
- Clientes com dúvidas simples aguardam longas filas de atendimento
- Falta de personalização nas recomendações financeiras
- Dificuldade em interpretar extratos e rentabilidades

**Solução:**
Agente conversacional que acessa o perfil, extrato e portfólio do cliente para responder perguntas, realizar simulações financeiras básicas e recomendar produtos adequados ao perfil — de forma proativa e contextualizada.

---

## Persona e Tom de Voz

**Nome:** Finno  
**Personalidade:** Consultivo, direto e confiável. Fala como um assessor financeiro experiente, sem jargões desnecessários.  
**Tom:** Profissional e acessível — nem frio demais, nem informal demais.  
**Restrições de comportamento:**
- Nunca garante rentabilidade futura
- Sempre indica que decisões relevantes devem ser validadas com um assessor humano
- Não opina sobre criptomoedas, câmbio ou ativos fora do portfólio do banco

---

## Arquitetura

```
Cliente (texto)
     │
     ▼
System Prompt (persona + restrições + contexto financeiro do cliente)
     │
     ▼
LLM — LLaMA 3.1 via Groq API
     │
     ▼
Resposta contextualizada ao cliente
```

**Dados utilizados no contexto:**
- `perfil_investidor.json` → perfil de risco, objetivos e metas
- `transacoes.csv` → gastos e receitas recentes
- `produtos_financeiros.json` → produtos disponíveis para recomendação
- `historico_atendimento.csv` → contexto de interações anteriores

---

## Segurança e Anti-Alucinação

| Risco | Mitigação |
|---|---|
| Inventar rentabilidades | Produtos injetados diretamente no prompt via dados reais |
| Recomendar produtos inadequados | Perfil de risco filtrado antes da recomendação |
| Responder fora do escopo | Instrução explícita no system prompt para recusar temas não financeiros |
| Dados sensíveis | Dados mockados sem CPF, senha ou informações reais |
