"""
Finno — Assistente Financeiro Inteligente
Projeto de conclusão do Bootcamp Python AI Backend Developer - DIO
"""

# ============================================================
# CÉLULA 1 — Instalação
# ============================================================
# !pip install groq python-dotenv --quiet


# ============================================================
# CÉLULA 2 — Configuração da API
# ============================================================
import os
import re
import time
import json
import csv
import getpass
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ============================================================
# CÉLULA 3 — Carregamento dos dados do cliente
# ============================================================
def carregar_perfil(caminho="data/perfil_investidor.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_produtos(caminho="data/produtos_financeiros.json"):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_transacoes(caminho="data/transacoes.csv"):
    transacoes = []
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['valor'] = float(row['valor'])
            transacoes.append(row)
    return transacoes

def carregar_historico(caminho="data/historico_atendimento.csv"):
    historico = []
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            historico.append(row)
    return historico

def resumir_gastos(transacoes):
    gastos = {}
    for t in transacoes:
        if t['tipo'] == 'debito' and t['categoria'] != 'investimento':
            cat = t['categoria']
            gastos[cat] = gastos.get(cat, 0) + abs(t['valor'])
    return gastos

def filtrar_produtos_por_perfil(produtos_json, perfil_risco):
    return [p for p in produtos_json['produtos'] if perfil_risco in p['indicado_para']]

def formatar_produtos(produtos):
    linhas = []
    for p in produtos:
        linhas.append(
            f"- {p['nome']} ({p['tipo']}): {p['rentabilidade']} | "
            f"Liquidez: {p['liquidez']} | Mínimo: R$ {p['investimento_minimo']:.2f} | "
            f"Risco: {p['risco']}"
        )
    return "\n".join(linhas)

def formatar_historico(historico):
    linhas = []
    for h in historico[-3:]:
        linhas.append(f"- {h['data']} ({h['canal']}): {h['assunto']} → {h['resolucao']}")
    return "\n".join(linhas)

def formatar_metas(perfil):
    linhas = []
    for m in perfil['cliente']['metas'] if 'metas' in perfil['cliente'] else perfil.get('metas', []):
        valor_alvo = m['valor_alvo']
        valor_atual = m['valor_atual']
        progresso = (valor_atual / valor_alvo) * 100
        linhas.append(f"- {m['descricao']}: R$ {valor_atual:,.2f} de R$ {valor_alvo:,.2f} ({progresso:.0f}%)")
    return "\n".join(linhas)


# ============================================================
# CÉLULA 4 — Construção do system prompt com contexto do cliente
# ============================================================
def construir_system_prompt(perfil, produtos_json, transacoes, historico):
    cliente = perfil['cliente']
    perfil_risco = cliente['perfil_risco']

    gastos = resumir_gastos(transacoes)
    gastos_fmt = "\n".join([f"- {cat.capitalize()}: R$ {val:.2f}" for cat, val in gastos.items()])

    produtos_adequados = filtrar_produtos_por_perfil(produtos_json, perfil_risco)
    produtos_fmt = formatar_produtos(produtos_adequados)

    historico_fmt = formatar_historico(historico)
    metas_fmt = formatar_metas(perfil)

    return f"""Você é o Finno, assistente financeiro inteligente do banco digital.
Seu papel é ajudar o cliente a entender suas finanças, tomar decisões de
investimento adequadas ao seu perfil e esclarecer dúvidas sobre produtos.

PERFIL DO CLIENTE:
- Nome: {cliente['nome']}
- Idade: {cliente['idade']} anos
- Renda mensal: R$ {cliente['renda_mensal']:,.2f}
- Patrimônio total: R$ {cliente['patrimonio_total']:,.2f}
- Perfil de risco: {perfil_risco}
- Objetivo principal: {cliente['objetivo_principal']}
- Horizonte de investimento: {cliente['horizonte_investimento_anos']} anos

METAS DO CLIENTE:
{metas_fmt}

RESUMO DE GASTOS DO MÊS ATUAL:
{gastos_fmt}

PRODUTOS DISPONÍVEIS PARA O PERFIL {perfil_risco.upper()}:
{produtos_fmt}

HISTÓRICO RECENTE DE ATENDIMENTO:
{historico_fmt}

REGRAS OBRIGATÓRIAS:
1. Responda sempre em português, de forma clara e objetiva
2. Nunca garanta rentabilidade futura — use "histórico" ou "estimativa"
3. Para decisões acima de R$ 10.000, sugira validar com assessor humano
4. Recuse educadamente perguntas fora do escopo financeiro
5. Use apenas os dados fornecidos acima — não invente taxas ou produtos
6. Quando não tiver informação disponível, diga claramente
"""


# ============================================================
# CÉLULA 5 — Validação de entrada (prompt injection + rate limit)
# ============================================================
_INJECTION_RE = re.compile(
    r"(ignore|esqueça|desconsidere).{0,30}(instru|regra|sistema|prompt)"
    r"|(novo papel|agora você é|fingir ser|atuar como|roleplay)",
    re.IGNORECASE,
)
_INTERVALO_MIN = 1.5  # segundos mínimos entre mensagens


def validar_entrada(texto: str) -> str | None:
    """Retorna mensagem de erro se a entrada for inválida, None se OK."""
    if len(texto) > 800:
        return "Mensagem muito longa. Por favor, seja mais conciso (máx. 800 caracteres)."
    if _INJECTION_RE.search(texto):
        return "Não posso processar essa solicitação."
    return None


# ============================================================
# CÉLULA 6 — Autenticação via PIN (opcional)
# ============================================================
def autenticar() -> bool:
    """Verifica PIN se FINNO_PIN estiver definido no ambiente."""
    pin_esperado = os.environ.get("FINNO_PIN")
    if not pin_esperado:
        return True
    for _ in range(3):
        if getpass.getpass("PIN de acesso: ") == pin_esperado:
            return True
        print("PIN incorreto.")
    return False


# ============================================================
# CÉLULA 7 — Loop de conversa com o Finno
# ============================================================
from groq import Groq


def iniciar_finno():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Variável de ambiente GROQ_API_KEY não definida. "
            "Copie .env.example para .env e preencha sua chave."
        )

    if not autenticar():
        print("Acesso negado.")
        return

    perfil = carregar_perfil()
    produtos = carregar_produtos()
    transacoes = carregar_transacoes()
    historico = carregar_historico()

    system_prompt = construir_system_prompt(perfil, produtos, transacoes, historico)
    client = Groq(api_key=api_key)
    historico_conversa = []
    ultima_mensagem = 0.0

    print("=" * 55)
    print("  Finno — Assistente Financeiro Inteligente")
    print("=" * 55)
    print(f"  Olá, {perfil['cliente']['nome'].split()[0]}! Como posso ajudar?")
    print("  (digite 'sair' para encerrar)\n")

    while True:
        pergunta = input("Você: ").strip()

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("\nFinno: Até logo! Qualquer dúvida financeira, estarei aqui.")
            break

        if not pergunta:
            continue

        agora = time.monotonic()
        if agora - ultima_mensagem < _INTERVALO_MIN:
            print("\nFinno: Aguarde um momento antes de enviar outra mensagem.\n")
            continue
        ultima_mensagem = agora

        erro = validar_entrada(pergunta)
        if erro:
            print(f"\nFinno: {erro}\n")
            continue

        historico_conversa.append({"role": "user", "content": pergunta})

        try:
            resposta = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *historico_conversa,
                ],
                max_tokens=500,
                temperature=0.4,
            )
            texto = resposta.choices[0].message.content
        except Exception:
            historico_conversa.pop()
            print("\nFinno: Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.\n")
            continue

        historico_conversa.append({"role": "assistant", "content": texto})
        print(f"\nFinno: {texto}\n")
        print("-" * 55)


# ============================================================
# CÉLULA 8 — Executar
# ============================================================
# Configure GROQ_API_KEY no arquivo .env (veja .env.example)
iniciar_finno()
