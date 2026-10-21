# DKW — API

> O vault original (base_conhecimento) não estava no container da sessão de 21/10/2026.
> Este arquivo traz só a seção nova; incorporar à página `wiki/entities/dkw-api.md` do vault.

## Dashboard — tempo de resposta [medido 2026-10-21]

Coleta só de leitura, no painel gestao.portilhoconsultoria.com.br, com a conta da Portilho personificando
a Floricultura Verdes Plantas Ltda (companyId 7078). A personificação foi encerrada ao final (voltou para 7061).
A janela "Qual empresa é a sua?" não apareceu.

### 1. Documentação oficial (Automações → API, v1.0.0, seção Dashboard) — transcrição

Base real da doc: `https://api-gestao.portilhoconsultoria.com.br/api/...` (a barra lateral exibe
`https://gestao.portilhoconsultoria.com.br/dashboard/...`). Todas as rotas da seção têm a mesma entrada:

- HEADERS: `api-key` string required — "Chave de autenticação da empresa"
- QUERY PARAMS:
  - `date_from` string required — "Data inicial (obrigatório). Formato: d/m/Y, opcionalmente com horário d/m/Y H:i:s (ex: 09/02/2025 14:30:00)"
  - `date_to` string required — "Data final (obrigatório). Formato: d/m/Y, opcionalmente com horário d/m/Y H:i:s (ex: 09/02/2025 18:00:00)"
- RESPONSES: 200 (abaixo) · 400 "Parâmetros inválidos" · 401 "Falta de autenticação"

A doc não tem aba de exemplo nem "Campos do Payload": só o schema do 200 ("Show body", APPLICATION/JSON).
Também não documenta filtro por usuário.

**GET /dashboard/chats — Métricas de Conversas** (prioridade)
"Retorna métricas de conversas agrupadas por data"
200 "Métricas de conversas por período":
```
success boolean
data object
  chats array of object
    date string
    label string
    totalChats integer
    responseTime number   — "Tempo médio de resposta em segundos"
    totalChatsCreated integer
    totalChatsWithResponse integer
```

**GET /dashboard/counters — Contadores do Dashboard**
"Retorna contadores principais: contatos, tickets, negócios, etc."
```
contacts {total, new, active} integer
tickets {total, open, closed, pending} integer
commercialOrders {total, won, lost, open} integer, totalAmount number
messages {sent, received} integer
```

**GET /dashboard/list/presale — Ranking de Pré-venda**
"Retorna ranking individual da equipe de pré-venda (SDR)"
```
success boolean
data.presaleRanking[]: position, totalLeadsWorked, totalCalls, totalConnections,
                       totalMeetingsScheduled, totalMeetingsRealized (integer)
```

**GET /dashboard/list/closer — Ranking de Closers**
"Ranking da equipe de fechamento (Closers)"
```
success boolean
data.closerRanking[]: position, totalMeetingsRealized, totalSales (integer), totalSalesAmount (number)
```

Outras rotas da seção (sem campo de tempo de resposta): `/dashboard/calls` (único campo de tempo:
"Chamadas com duração maior que 180 segundos"), `/dashboard/tags`, `/dashboard/activities`,
`/dashboard/presale`, `/dashboard/closer`, `/dashboard/list/products`.

**Conclusão:** a única fonte oficial de tempo de resposta é `responseTime`, em `/dashboard/chats`, em segundos.

### 2. Tela do painel (Relatórios → Métricas = "Conversas")

- URL: `/dashboard/reports`. O seletor "Métricas" tem estas opções: Vendas · Atividades · Conversas ·
  Ligações · SDR · Closer · CARINE · CARINE.
- Nome exato do indicador: **"Tempo de resposta"**. Tooltip: "Tempo médio de resposta representa o tempo que
  uma conversa aguardou uma mensagem enviada por uma conexão da plataforma dentro do período selecionado."
- Período padrão: 01/10/2026 – 21/10/2026. Valor exibido: **"298 minutos"**.
- Os outros cards da mesma tela são: Novos contatos 457 · Conversas respondidas 438 ·
  Conversas interagidas 1.788 · Aguardando resposta 65 · Conversas finalizadas 803.
- Filtros (ícone de funil): Vendedor · Produtos · Tags. O filtro Vendedor envia `userIds=<id>`.
  A tela não tem tempo por atendente lado a lado: é preciso filtrar um vendedor de cada vez.

### 3. Requisição de rede capturada (API do painel)

```
GET https://api.integrador-crm.com/dashboard/chats?timezone=UTC&date_from=2026-10-01&date_to=2026-10-21[&userIds=12198]
headers: authorization (Bearer do localStorage) + tenant: portilho-gestao-comercial-inteligente
```
A rota do painel usa `date_from`/`date_to` em ISO (Y-m-d), e não d/m/Y como na doc oficial.
Ela aceita `userIds`, que a doc não menciona, e `timezone`. Com período de 1 dia e
`timezone=America/Sao_Paulo`, os baldes passam a ser por hora (label "00:00"…"23:00").

Resposta: `{"chats":[{date,label,totalChats,responseTime,totalChatsClosed,totalChatsCreated,totalChatsWithResponse}],"waitingChats":N,"period":"day"}`.
O campo `totalChatsClosed` não aparece na doc oficial.

Para 01–21/10, a média diária de `responseTime` variou de 0,01 s a 2.191,8 s.

### 4. Valores de hoje (21/10/2026) por vendedor

Fonte: `/dashboard/chats?timezone=UTC&date_from=2026-10-21&date_to=2026-10-22&userIds=…`, chamada às ~19h05.
Usei o balde com label "2026-10-21", que é o dia UTC (de 20/10 21h a 21/10 21h, horário de Brasília).

| Vendedor (userId) | responseTime (s) | totalChats | totalChatsCreated | totalChatsWithResponse | waitingChats |
|---|---|---|---|---|---|
| Empresa (sem filtro) | 20,3 | 89 | 15 | 15 | 21 |
| Edimar (12198) | 9,07 | 34 | 5 | 5 | 8 |
| Carine (21035) | 2,53 | 21 | 4 | 4 | 5 |
| Douglas (15948) | 38,48 | 11 | 6 | 4 | 5 |
| Luana (28637) | 0 | 0 | 0 | 0 | 0 |
| Fernando (12152) | 0 | 3 | 0 | 0 | 3 |

### 5. Leitura crítica (regra zero) — NÃO usar como TPR/TR sem tratamento

1. **A unidade da tela está errada.** "298 minutos" é a média simples dos 21 `responseTime` diários,
   que vêm em **segundos** (297,6 s). O valor real é ≈ 4,96 min. A média ponderada por
   `totalChatsWithResponse` dá 255,8 s (≈ 4,3 min).
2. **A média inclui automação.** Há baldes com 0,01–0,02 s, inclusive às 01:00 de hoje, atribuídos ao
   Edimar e idênticos ao total da empresa. Isso é resposta automática ou do sistema contada como resposta.
   O tooltip confirma o critério: "mensagem enviada por uma conexão da plataforma", e não por um vendedor.
3. **Mede só conversas novas.** O número de conversas respondidas acompanha `totalChatsCreated`
   (15/15 hoje), e não as 89 conversas interagidas. É o tempo da 1ª resposta a conversas criadas no período,
   não o tempo de resposta por mensagem.
4. **É média, sem mediana nem P90, e não respeita o expediente.** Conta 24 h por dia, sábado e domingo
   incluídos. Não atende à definição de TPR/TR em `kpis-atendimento-comercial-verdes-plantas.md`
   (seg–sex, 08–18h, mediana e P90).
5. **A agregação não é reproduzível.** O balde das 12:00 do Douglas tem `responseTime` 131 s com
   `totalChatsWithResponse` 0, e o valor diário dele (38,5 s) não sai da ponderação dos baldes horários (1,7 s).
6. **O gráfico está deslocado e o padrão omite hoje.** Com `timezone=UTC`, o `date` de cada balde é o fim do
   dia UTC (21h de Brasília). O gráfico plota pelo `date`, então o eixo mostra o dia seguinte ao do dado.
   No período padrão (`date_to=2026-10-21`), o dia de hoje fica fora da série.
7. A doc oficial e a rota do painel não batem: formato de data, `userIds` e `totalChatsClosed` diferem.

**Decisão sugerida:** `/dashboard/chats` serve para conferir a ordem de grandeza e o volume de conversas
novas por vendedor. O TPR/TR do relatório deve continuar sendo calculado por mensagem: vendedor identificado
pelo prefixo `*Nome:*`, mensagens com `sendBySystem`/`generatedByAi` excluídas, dentro do expediente,
com mediana e P90. Ainda não medido.
