# Relatório de gerência do comercial
### Floricultura Verdes Plantas · semana de 16 a 21/11/2026 · PROTÓTIPO com dados reais — não enviado

**Como ler.** Este relatório mostra se a rotina da coordenação aconteceu e para onde vai a equipe. Não mostra vendedor nem cliente: o caso a caso está com a coordenação. Com menos de 6 semanas de série, os números são **linha de base** — a seta mostra a direção, não um alarme.

## OS SINAIS DA SEMANA

| Sinal | Esta semana | Semana anterior | Direção |
|---|---|---|---|
| Lista da coordenação resolvida em 24 h (média dos dias) | **48%** | 45% | ↑ |
| Clientes novos que ficaram sem resposta | **63** | 35 | ↓ piorou |
| 1ª resposta ao cliente novo (mediana) | **78 min** | 43 min | ↓ piorou |
| Follow-up 2 com mensagem agendada (último dia útil) | **33%** | 56% | ↓ piorou |
| Correções nos cards da equipe feitas pelo coordenador (e não pelo dono) | **66%** | — | primeira medição |

## 1. A ROTINA DA COORDENAÇÃO

| | Seg 16 | Ter 17 | Qua 18 | Qui 19 | Sex 20 |
|---|---|---|---|---|---|
| Lista de ontem resolvida | 61% | 54% | 41% | 37% | feriado |

- **Relatório da coordenação lido até 9h:** ainda não medido (o relatório ainda não vai para o coordenador).
- **Reunião semanal do comercial:** ainda não medida (falta o registro no sistema).
- **Quem resolve as exceções:** nas correções feitas em cards da equipe, 23 ações do coordenador e 12 do dono (66% coordenador).

*Pergunta para a conversa com o coordenador:* a lista andou bem na segunda e perdeu força ao longo da semana. O que travou na rotina a partir de quarta?

## 2. O PROCESSO DE PÉ

| Indicador | Esta semana |
|---|---|
| 1ª resposta · mediana / P90 | 78 min / 4,7 h |
| Resposta no meio da conversa · mediana / P90 | 4,2 min / 1,8 h |
| Encerramentos com o cliente como último a falar | 28% (54 de 191 com conversa) |
| Encerramentos arrastados ou perda sem motivo | 2 de 215 |
| Mensagem de follow-up que teve resposta do cliente em até 7 dias | 47% (14 de 30) |
| Venda ganha com valor | 39 de 40 |
| Atendimentos novos com tag de tipo | 43% (85 de 199) |
| Contatos com mais de um card ativo | 3 de 192 |

**Funil parado** (cards acima de 1,5× o tempo normal da coluna):

| Coluna | Cards | Parados | Valor parado |
|---|---|---|---|
| Atendimento de Vendedores | 110 | 52 (47%) | R$ 1.709,81 |
| Follow-up 2 | 22 | 9 (41%) | R$ 170,00 |
| Atendimento Inicial | 22 | 6 (27%) | — |
| Follow-up 1 | 35 | 7 (20%) | **R$ 4.687,49** |

*Pergunta para a conversa com o coordenador:* quase metade do Atendimento de Vendedores está parada há mais tempo que o normal. Qual é o plano da coordenação para essa coluna?

## 3. O RESULTADO

**40 vendas, R$ 11.168,85** · 79 perdas · conversão da equipe **34%** (semana anterior 39%). Sexta, 20/11, foi feriado sem atendimento.

## 4. O DONO NA OPERAÇÃO

- Mensagens do dono em conversas com clientes: **128, em 8 conversas**.
- Mensagens do dono com a equipe pelo WhatsApp da loja: 15, em 2 conversas.
- Cards novos que caíram no usuário do dono: 6 · encerramentos no usuário do dono: 13.

*Pergunta para a conversa com o coordenador:* dos clientes que o dono atendeu, quais deveriam ter ido para a equipe?

---

## O SINAL DIÁRIO (exemplo — o que chegaria às 9h30, uma linha)

> **Coordenação ontem (qui, 19/11):** lista tratada ✗ (37%) · relatório aberto até 9h: —

Calibragem: com a lista resolvendo entre 37% e 61% ao dia, um limite de 80% daria vermelho todos os dias. Proposta: começar com ✓ a partir de 50% e subir 10 pontos a cada 4 semanas no verde.

---

**Notas do protótipo (não entram no relatório):**
- Fonte: base do CRM lida em 24/11 às 08h54 e pendências diárias de 16 a 19/11. Cálculo: `ferramentas/tpr-tr/gerencia.py`.
- "Cliente último a falar" inclui o "obrigado" do cliente depois do fechamento — o número real de abandono é menor. Precisa de filtro antes de virar meta.
- "Quem resolve as exceções" exclui os cards do próprio coordenador e do próprio dono (é venda, não coordenação). n ainda pequeno (35 ações).
- As conversas do dono com a equipe dependem da lista de telefones internos — hoje só Edimar, Luana Loja e o número do Financeiro estão marcados.
- O total de mensagens do dono com clientes está concentrado em poucas conversas: uma delas responde por 93 das 128.
