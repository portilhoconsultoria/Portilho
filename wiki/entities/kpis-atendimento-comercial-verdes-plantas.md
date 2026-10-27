---
title: "KPIs — Atendimento Comercial Verdes Plantas"
type: entity
created: 2026-10-19
updated: 2026-10-22
verified: 2026-10-22
tags: [kpi, atendimento, crm, dkw, verdes-plantas, relatorio-diario]
related: ["[[verdes-plantas]]", "[[dkw]]", "[[dkw-api]]", "[[o-conselho]]"]
status: draft
confidence: medium
---

# KPIs — ATENDIMENTO COMERCIAL VERDES PLANTAS

> **Escopo:** Floricultura Verdes Plantas (Irati/PR) — atendimento comercial no DKW.
> Outros clientes podem herdar esta estrutura, mas os números e metas desta página são **da Verdes**.
>
> **Para que existe esta página.** O Jhonatan está montando, com o Fernando, a estrutura do
> **relatório diário de atendimento** da Verdes Plantas — que depois vira um **BI em tempo real**.
> As regras vão surgindo em conversa, uma de cada vez. Esta página é o lugar onde elas ficam.
> Nada aqui é opinião: cada KPI tem **definição exata**, **fonte de dados**, **meta** e
> **se já é mensurável hoje ou não**.
>
> Regra da página: **nenhum KPI entra sem definição de início, fim e exclusões.**

---

## 0. HORÁRIO DE EXPEDIENTE — a base de todo KPI de tempo

| Dia | Horário | Fonte |
|---|---|---|
| Segunda a sexta | **08:00 – 18:00** | Google Meu Negócio + site oficial `verdesplantas.com.br` `[medido 19/10/2026]` |
| Sábado | `?` | **Não publicado.** Há atendimento real aos sábados (medido em 17/10: conversas respondidas no sábado) `[medido 2026-10-21]`. Horário oficial pendente com o Fernando |
| Domingo | fechado | `[suposto]` |

**Regras derivadas:**

- Mensagem recebida **fora da janela** → o relógio começa na abertura do dia útil seguinte.
- Mensagem respondida fora do expediente (ex.: sábado) sai da mediana e é contada à parte.
- **Sábado precisa de confirmação do Fernando** antes de entrar no cálculo.

---

## 1. TPR — TEMPO DE PRIMEIRA RESPOSTA

**Pergunta que responde:** quanto tempo o cliente espera entre falar com a loja pela primeira vez
e um humano começar a atendê-lo.

| Campo | Definição |
|---|---|
| **Início do relógio** | Primeira mensagem do cliente que abre um atendimento novo |
| **Atendimento novo** | Bloco de mensagens do cliente sem resposta de vendedor humano no ticket nas 24 h anteriores `[assumido 21/10, validar com o Fernando]` |
| **Fim do relógio** | Primeira mensagem **de um vendedor humano** naquele atendimento |
| **Não conta como resposta** | Automação (saudação, "enquanto aguarda seu atendimento", raspadinha, pedido de avaliação) |
| **Janela** | Só horário de expediente |
| **Unidade** | Minutos |
| **Como reportar** | **Mediana e P90** — nunca média |

### Meta

- **Meta do Fernando: 4 minutos** `[definido por Fernando, via Jhonatan, 19/10/2026]`

### Medição `[medido 2026-10-21]`

| Período | Mediana equipe | P90 equipe | Por vendedor (mediana) |
|---|---|---|---|
| Semana 14–20/10 | **25,2 min** | 2,3 h | Carine 23,0 · Douglas 21,3 · Edimar 36,3 |
| Dia 21/10 | **12,4 min** | 3,5 h | Carine 36,2 · Douglas 3,0 · Edimar 35,8 |

**Fonte:** `GET /messages/{ticketId}` (histórico completo por ticket — rota achada em 21/10, ver [[dkw-api]]).
Script: `tpr_tr.py` (repo Portilho, `ferramentas/tpr-tr/`). Vendedor = `fromMe` + `userId` preenchido;
automação = `fromMe` sem `userId`; nessa rota o `fromMe` **funciona**.

> ⚠️ O indicador "Tempo de resposta" da tela do DKW (Relatórios › Conversas) **não serve**: mostra segundos
> rotulados como minutos ("298 minutos" = 298 s) e inclui automação. Reportado à DKW em 22/10.

---

## 2. TR — TEMPO DE RESPOSTA EM CONVERSA ANDANDO

| Campo | Definição |
|---|---|
| **Início** | Primeira mensagem de um bloco do cliente num atendimento já aberto |
| **Fim** | Próxima mensagem do vendedor humano no mesmo atendimento |
| **Janela** | Horário de expediente |
| **Bloco abandonado** | Cliente que volta após >24 h de silêncio abre bloco novo; o anterior fecha sem resposta |

### Meta

- `?` — **a definir com o Fernando.** Proposta: **15 minutos**.

### Medição `[medido 2026-10-21]`

| Período | Mediana equipe | P90 equipe |
|---|---|---|
| Semana 14–20/10 | **5,6 min** | 1,8 h |
| Dia 21/10 | **3,7 min** | 36,0 min |

**Leitura:** com a conversa andando a equipe responde rápido; o gargalo é a **porta de entrada** (TPR).

Limitação conhecida: "ok/obrigado" de encerramento do cliente conta como bloco sem resposta.

---

## 3. MNL — MENSAGEM NÃO LIDA NO FIM DO EXPEDIENTE

| Campo | Definição |
|---|---|
| **Medição** | Contagem de atendimentos com mensagem do cliente não lida no fechamento do dia |
| **Meta** | **Zero.** |
| **Fonte** | DKW, campo de não lidas |

**Linha de base 18/10:** Edimar 10 · Carine 6 · Douglas 4 `[medido]`

---

## 4. CLIENTE FALANDO POR ÚLTIMO

- **Medição:** atendimentos ativos em que a última mensagem é do cliente, por faixa de dias parados (1–3 · 4–7 · +7).
- **Meta:** `?` — proposta: **zero acima de 3 dias**.
- Linha de base 19/10: Edimar 17 · Douglas 11 · Carine 8 `[medido]`

---

## 5. ARQUIVAMENTO SEM CRITÉRIO (INCÓGNITA)

- **Medição A:** cards movidos para a Incógnita por dia, por vendedor.
- **Medição B:** quantos desses tinham o cliente falando por último, ou nota que indica venda/perda.
- Linha de base 7 dias até 19/10: **191 arquivados, 38 com cliente falando por último (20%)** `[medido]`
- 21/10: 32 cards foram para a Incógnita; 24 pelo Ações; 8 com nota que indica venda (ex.: Toddy, R$ 372, "já fez o pedido") `[medido 2026-10-21]`

---

## 5b. NOTA NO CARD (E5)

> ⚠️ Retratação de 20/10: o relatório de 18/10 leu o campo `observation` (texto do sistema) e não a entidade de notas.

**Medição correta, 20/10:** cards ativos com nota 41/140 · arquivados na semana com nota 201/234 (86%) · **notas com data 0/53**.
**21/10:** 65 notas nos cards movidos no dia (Edimar 31 · Douglas 17 · Carine 17); **1 com data** `[medido 2026-10-21]`.

---

## 5c. SAÍDA DO CARD — venda e perda que não viram número

**Causa estrutural:** Venda Efetivada exige valor, Venda Perdida exige motivo, **Incógnita não exige nada**.

**Encerramento por Ações** (liberado com os 4 estados em 20/10) `[medido 2026-10-21]`:
- 21/10: **43 de 56 encerramentos passaram pelo Ações**; vendas arrastadas 1 de 9 (20/10: 3 de 10).
- Perdas sem motivo no dia: 3 de 12 — todas cards **duplicados** (o mesmo cliente tinha outro card encerrado certo).

---

## 6. INTEGRIDADE DE REGISTRO

| Indicador | 18/10 | 20/10 | 21/10 | Meta |
|---|---|---|---|---|
| Venda perdida **sem motivo** | 1.093 | 1.093 | 1.095 | `?` |
| Venda efetivada **sem valor** | 448 | 448 | 445 | `?` |
| Ganho **fora** da coluna Venda Efetivada | 180 | 191 | **124 (nova régua)** | 0 |

> ⚠️ **Mudança de régua em 21/10.** Até 20/10 "ganho" era contado por `wonAt`. Desde a liberação dos 4 estados
> em Ações, o DKW carimba `wonAt` em **todo** encerramento pelo botão (Incógnita, perda, ganho) — por `wonAt` o
> número iria a 220 sem nada piorar. **A partir de 21/10, ganho = `status WON`.** 124 é a nova linha de base;
> não comparar com 180/191.

---

## 7. CLASSIFICAÇÃO DO ATENDIMENTO POR TAG (novo — pedido do Jhonatan em 22/10)

**Pergunta que responde:** os vendedores estão classificando o atendimento pelo tipo (buquê, grama,
paisagismo…) logo no início?

| Campo | Definição |
|---|---|
| **Base** | Atendimentos **iniciados no dia** = cards criados no dia no pipeline 10541 |
| **Medição** | Quantos receberam **tag no card** (`orderTags`) e quais; por vendedor; quantos ficaram sem tag de tipo |
| **Tag de tipo** | BUQUES, GRAMA, FLOR DE PRESENTE, FLOR DE CORTE, PLANTAS ORNAMENTAIS, FRUTÍFERAS, ÁRVORES DE SOMBRA, PALMEIRA, CEDROS, EUCALIPTO, TREPADEIRA, FORRAÇÃO, PEDRA, TERRA/SUBSTRATO, VASOS, CESTA DE CAFÉ |
| **Não conta** | Tag de processo/campanha (Follow-up, ORÇAMENTO, QUALIFICADO, PEDIDO DE CLIENTE, MENSAGEM AGENDADA, REMARKETING, SEMI PRESENCIAL, IA DESATIVADA, FORNECEDOR, 700, FESTIVAL DE PRIMAVERA, FINADOS CRISANTEMOS 2025, RASPINHA VP, SORTEIO RADIO) e **tag do contato** (`tags`, herdada de atendimentos antigos) |
| **Meta** | `?` — proposta: 100% dos atendimentos iniciados com tag de tipo |

> ⚠️ **Não existe tag PAISAGISMO** entre as 30 tags da Verdes `[medido 2026-10-22]`. Enquanto não for criada,
> atendimento de paisagismo não tem como ser classificado.

**Mensurabilidade:** mensurável hoje pela API do painel (`/commercial-order/step/{id}` traz `tags` e `orderTags`).
A API não informa **quando** a tag foi colocada — para card criado no dia, tag no card = colocada no dia.
Entra no relatório a partir da edição de 22/10.

---

## REGRA DE OURO DESTA ESTRUTURA

> **Revisada em 20/10.** O que determina a adoção não é manual × automático, é **se cumprir a regra
> ajuda quem a cumpre**. Regra que só serve a quem está acima precisa estar **embutida no caminho**
> (campo obrigatório na transição de coluna), nunca pedida como disciplina.
>
> **Confirmação em 21/10:** depois de o Ações passar a exigir valor/motivo, 43 de 56 encerramentos
> do dia já saíram certos.

---

## ROADMAP COMBINADO

1. **Relatório diário** (Jhonatan → Fernando) — edição nº 1 em 20/10, nº 2 em 21/10 (enviada 22/10 por WhatsApp e e-mail). Formato único: ver skill `relatorio-comercial-vp`.
2. **BI em tempo real** — depois que os KPIs estabilizarem.

---

## PENDÊNCIAS ABERTAS

| O quê | Dono | Desde |
|---|---|---|
| Confirmar se a loja atende **sábado** e em que horário | Fernando | 19/10 |
| Validar a regra de "atendimento novo" (24 h sem resposta humana) | Fernando | 21/10 |
| Definir a meta do **TR** (proposta: 15 min) | Fernando | 19/10 |
| Criar a tag **PAISAGISMO** | Fernando / Luana | 22/10 |
| Definir a **regra de entrada da Incógnita** | Fernando + Jhonatan | 18/10 |
| Usuário-robô de leitura dentro da Verdes no DKW | Fernando | 20/10 |
| Tarefa diária agendada do relatório (refazer no app, com Drive e Gmail) | Jhonatan | 22/10 |

---

## HISTÓRICO DE DECISÕES

- `2026-10-22` — **Classificação por tag** entra como KPI 7 e como seção do relatório diário (pedido do Jhonatan). Medido: não existe tag PAISAGISMO.
- `2026-10-22` — **Regra da versão única** do relatório: informação nova entra como seção da edição seguinte; nada de documento paralelo ao cliente (erro de 21/10: foi enviado um relatório só de TPR/TR em formato diferente).
- `2026-10-22` — **Envio autorizado** todo dia útil às 20h, com o movimento do próprio dia: WhatsApp ao Fernando pelo DKW da Portilho + e-mail verdes_plantas@yahoo.com.br. Edição nº 3 = quinta 22/10.
- `2026-10-21` — **TPR/TR medidos pela primeira vez** (semana 14–20/10 e dia 21/10). Definições de bloco, atendimento novo e bloco abandonado fixadas (a validar).
- `2026-10-21` — **Mudança de régua do "ganho fora da coluna"**: `wonAt` → `status WON` (Regra Zero: `wonAt` passou a ser carimbado em todo encerramento por Ações).
- `2026-10-19` — **Meta de TPR = 4 minutos**, definida pelo Fernando.
- `2026-10-19` — **Horário de expediente confirmado** seg–sex 08:00–18:00.
- `2026-10-20` — **Retratação do achado "0% de notas"**. Lição: quando um número dá 0% ou 100%, a primeira hipótese é instrumento errado.
- `2026-10-19` — **Página criada.**

## Análise semanal [definida 2026-10-27]

Semana seg–sáb, enviada ao Fernando todo sábado às 13h (WhatsApp + e-mail), no timbrado da Portilho (mesmo `gerar_doc.py` do diário). Nº 1 = 19–24/10 (linha de base). Método, um agente por indicador e fontes científicas: `relatorios/semanal/Proposta_Analise_Semanal_Verdes_Plantas.md`. Kit: `ferramentas/tpr-tr/rodar_semana.sh`.
