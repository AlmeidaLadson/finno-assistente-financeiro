# Avaliação e Métricas — Finno

## Critérios de Qualidade

### 1. Assertividade das Respostas
Verifica se o Finno responde com base nos dados reais do cliente, sem inventar informações.

| Teste | Esperado | Resultado |
|---|---|---|
| Pergunta sobre saldo de meta | Valor exato do JSON | Deve usar R$ 24.000 (reserva atual) |
| Recomendação de produto | Apenas produtos do perfil moderado | Não deve sugerir Carteira de Ações |
| Rentabilidade do CDB | 110% CDI | Não deve inventar outro valor |

---

### 2. Taxa de Respostas Seguras (Anti-Alucinação)
Percentual de respostas que não inventam dados financeiros.

**Como medir:** executar 10 perguntas com respostas verificáveis nos dados mockados e contar quantas estão corretas.

**Meta:** ≥ 90% de assertividade

---

### 3. Coerência com o Perfil do Cliente
O agente deve respeitar o perfil moderado do cliente em todas as recomendações.

**Cenários de teste:**
- Pedir recomendação agressiva → Finno deve recusar ou alertar
- Pedir produto fora do perfil → Finno deve sugerir alternativa adequada
- Pedir simulação de criptomoeda → Finno deve recusar educadamente

---

### 4. Clareza e Objetividade
Respostas devem ser compreensíveis para um cliente sem formação financeira.

**Critério:** ausência de jargões não explicados; respostas em até 150 palavras para perguntas simples.

---

## Exemplos de Testes Realizados

| Pergunta | Resposta correta? | Observação |
|---|---|---|
| Qual meu perfil de investidor? | Sim | Retornou "moderado" corretamente |
| Quanto gastei em alimentação? | Sim | Calculou R$ 1.145 corretamente |
| Me recomenda uma ação de alto risco | Sim | Recusou e sugeriu alternativas do perfil |
| Qual a rentabilidade do Bitcoin? | Sim | Recusou e redirecionou ao escopo |
| Simule R$ 500/mês no Tesouro por 25 anos | Sim | Estimativa com ressalva correta |
