---
name: "relatorio-comercial-vp"
description: "Relatório diário do comercial da Floricultura Verdes Plantas (e outros clientes com CRM DKW) + configuração do ambiente DKW. Use SEMPRE que Jhonatan mencionar \"relatório diário\", \"relatório do comercial\", \"relatório da Verdes Plantas\", \"relatório para o Fernando\", \"edição do relatório\", \"tempo de resposta\", \"TPR\", \"TR\", \"tags de atendimento\", \"classificação por tag\", \"encerramento por Ações\", \"mensagem agendada no follow-up\", \"cards na Incógnita\", \"notas dos cards\", \"ticket-notes\", \"nova negociação por contato\", \"travar o arrasto de coluna\", ou pedir para rodar, ajustar, enviar ou automatizar o relatório comercial de cliente no DKW."
---

# RELATÓRIO COMERCIAL DKW — Verdes Plantas

Gera o **relatório diário do comercial** a partir da base do CRM DKW e mantém o **checklist de configuração** do ambiente do cliente. Nasceu no caso Floricultura Verdes Plantas (Fernando Fernandes), mas a estrutura serve a qualquer cliente da Portilho com DKW.

> Atualizada em 22/10/2026 (edição nº 2 enviada). Mudanças desta versão: regra da versão única, seção de tempo de resposta, seção "O que eu pedi ontem", seção de classificação por tag (a partir de 22/10), `wonAt` carimbado por Ações, rotas de mensagens e de cards por coluna, envio por WhatsApp + e-mail.

---

## 0. REGRA DA VERSÃO ÚNICA — O ERRO DE 21/10

Em 21/10/2026 foi enviado ao Fernando um documento **paralelo** (só tempo de resposta, outro formato) em vez da edição nº 2 do relatório diário. O Jhonatan rejeitou.

> **O relatório é um só.** Toda informação nova entra como **seção nova da edição seguinte**, no mesmo formato, com a numeração de edição sequencial. Nunca mandar ao cliente um documento paralelo, uma "versão resumida" diferente da completa, ou um formato novo sem aprovação. Se a mensagem do WhatsApp/e-mail tiver texto, é só apresentação — os números estão no documento.

Também: **nada vai ao cliente sem o Jhonatan aprovar o formato** quando o formato muda. Edição de rotina (mesmo formato, dia novo) pode sair direto.

---

## 1. REGRA ZERO — O ERRO QUE JÁ FOI COMETIDO

Em 18/10/2026 este projeto reportou *"138 de 142 cards sem nota, regra com 0% de adoção"*. **Era falso.** O campo `observation` do negócio é preenchido pelo sistema; as notas dos vendedores ficam em outra entidade.

> **Quando um indicador der 0% ou 100% — ou saltar sem explicação — a primeira hipótese é instrumento errado, não comportamento extremo.** Validar contra o texto real antes de escrever qualquer coisa.

Casos já registrados:
- `observation` lido como nota (18/10).
- `wonAt` passou a ser carimbado em **todo encerramento pelo botão Ações** (Incógnita, perda e ganho) desde que os 4 estados foram liberados em 20/10. Contar "ganho" por `wonAt` fez o indicador saltar de 191 para 220 sem nada ter piorado. **Ganho = `status === "WON"`.** (21/10)
- `sendBySystem` vem `true` também em mensagem humana — não serve para separar automação (21/10).
- O card "Tempo de resposta" do painel (Relatórios › Conversas) mostra **segundos rotulados como minutos** e inclui automação — não usar como TPR/TR (21/10).

**Em todo relatório, declarar o que NÃO foi medido, em seção própria.** Nunca inventar número; sempre separar o que foi lido do que foi concluído. Conferir totais citados no texto contra a coleta do dia (em 22/10 saiu "9.839 mensagens" — número da coleta semanal — num relatório diário de 2.332).

---

## 2. ACESSO AO DKW

Painel: `https://gestao.portilhoconsultoria.com.br` · API do painel: `https://api.integrador-crm.com`

**Headers** (montar DENTRO da página, nunca copiar o token para fora):

```js
const c = s => (s||'').replace(/^"|"$/g,'');
const h = { Authorization: 'Bearer ' + c(localStorage.getItem('token')),
            TENANT: 'portilho-gestao-comercial-inteligente' };
```

**Personificar o cliente**: menu ⋮ no rodapé da barra lateral → *Personificar empresa* → Floricultura Verdes Plantas Ltda → Confirmar. Na janela "Qual empresa é a sua?" → **"Agora não"**. Confirmar lendo `localStorage.user` → `company.id === 7078` e `personificated: true`. **Desfazer ao final** (botão "Voltar para empresa original"; volta a 7061). Antes de abrir o menu, fechar anúncios do painel ("Novidades do DKW System") com Esc ou "Dispensar" — eles cobrem o menu.

**Rodando na nuvem (Claude Code / rotina):** Playwright + Chromium (`/opt/pw-browsers/chromium`), login com as variáveis `VP_ROBO_EMAIL` / `VP_ROBO_SENHA` (hoje são a conta da Portilho, que personifica — o usuário-robô dentro da Verdes ainda não existe). Kit pronto: `kit_tpr_tr.sh` na pasta verdes-plantas do Drive (recria `ferramentas/tpr-tr/`). Domínio `storage.integrador-crm.com` (imagens/logo) costuma estar bloqueado na nuvem — não é necessário.

**Caminho recomendado de longo prazo:** usuário-robô dentro da empresa do cliente, perfil de leitura. Credenciais em variável de ambiente, nunca no código.

---

## 3. ROTAS

| O quê | Rota |
|---|---|
| Negócios (base inteira) | `GET /commercial-order?pageNumber=N&pageSize=40` |
| Cards de uma coluna (com tags) | `GET /commercial-order/step/{stepId}?sortBy=lastMessageHour&sortDirection=DESC&archived=false&timezone=UTC&pageNumber=N` |
| **Mensagens de um ticket** | `GET /messages/{ticketId}?pageNumber=N` (página 1 = mais recentes; `hasMore`) |
| **Notas do card** | `GET /ticket-notes/contact/{contactId}?commercialOrderId={orderId}` |
| Mensagens agendadas | `GET /schedules?pageNumber=N` (`status` PENDENTE/ENVIADA, `sendAt`, `sentAt`, `contactId`) |
| Tags cadastradas | `GET /tags/list` |
| Etapas do funil | `GET /commercial-sales-step` |
| Usuários | `GET /users?pageNumber=1` |
| Contato | `GET /contacts/{id}` (**plural**) · busca: `GET /contacts/?searchParam=<8 últimos dígitos>` |
| Tickets de um contato | `GET /tickets?searchParam=<8 últimos dígitos>&showAll=true` |
| Tempo de resposta do painel | `GET /dashboard/chats?timezone=UTC&date_from=AAAA-MM-DD&date_to=AAAA-MM-DD[&userIds=N]` — **segundos, inclui automação; não é TPR/TR** |

**Campos e armadilhas medidas:**

- `pageSize` tem teto **40**; só `pageNumber` avança. `commercialSalesStepId` como filtro de query **é ignorado** — paginar tudo e filtrar em memória. A base traz negócios de outros funis: filtrar pelas 8 etapas do pipeline 10541.
- Negócio: `status` (OPEN · WON · LOST · CANCELLED · nulo), `amount`, `wonAt`, `lostAt`, `lostReason`, `lastTimeMoved` (só o último movimento), `userId`, `contactId`.
- **Encerrado por Ações** = `status` ≠ OPEN/nulo. **Arrastado** = card numa coluna de encerramento com `status` OPEN/nulo.
- **Ganho = `status === "WON"`**, nunca `wonAt` (ver Regra Zero).
- `observation` do negócio **não é** a nota do vendedor.
- **Quem escreveu cada mensagem** (rota `/messages/{ticketId}`): `fromMe` **funciona** aqui (true = loja). Vendedor = `fromMe` + `userId` preenchido (o texto traz o prefixo `*Nome:*`). Automação = `fromMe` sem `userId`. Cliente = `fromMe` false. Em outras rotas o `fromMe` veio sempre `false` — conferir na rota usada.
- **Tags:** `tags` = tag do **contato** (acompanha o cliente para sempre; um card novo herda GRAMA de agosto). `orderTags` = tag do **card** (desta negociação). Classificação do atendimento = `orderTags`.
- Download programático (Blob + `a.click()`) **não funciona** na aba automatizada.

**Verdes Plantas — pipeline 10541, companyId 7078:**

```
44341  Atendimento Inicial      69421  ATENDIMENTO VENDEDORES
36971  FOLLOW-UP 1              113074 FOLLOW-UP 2
32318  VENDA EFETIVADA          36613  VENDA PERDIDA
121919 NÃO COMERCIAL            44334  INCÓGNITA
```

Usuários: Carine 21035 · Douglas 15948 · Edimar 12198 · Fernando 12152 · Luana 28637 · Jaqueline 12197 · Portilho 12107.

---

## 4. AS REGRAS DO CLIENTE QUE O RELATÓRIO COBRA

Fechadas com o Fernando em 20/10/2026:

1. **Encerramento só por Ações** — venda ganha (com valor), venda perdida (com motivo), incógnita, não comercial. Arrastar a coluna **não contabiliza**.
2. **Manutenção × encerramento:** arrastar coluna é manutenção (Atendimento → Vendedores → FU1 → FU2); Ações é encerramento.
3. **Todo card em Follow-up precisa de mensagem agendada.**
4. **Coluna Atendimento esvaziada todo dia** — só quem está em atendimento naquele dia.
5. **Nota com data.** `parou de responder, reativei · retorno dia 23`.
6. **Incógnita só para quem não se sabe o que aconteceu.** Se a nota diz que comprou → Venda Efetivada; se diz por que perdeu → Venda Perdida com motivo.
7. **Contato recorrente gera nova negociação**, não reusa o card.
8. **Classificar o atendimento por tag no início** (pedido do Jhonatan em 22/10): todo atendimento iniciado recebe a tag do tipo — buquê, grama, paisagismo etc.

Expediente: **segunda a sexta, 08:00–18:00**. Sábado não publicado — fica fora do cálculo até o Fernando confirmar.

---

## 5. ESTRUTURA DO RELATÓRIO DIÁRIO

Destinatário: o dono. Lê em PDF, decide rápido. Título fixo **"Relatório diário do comercial"**, subtítulo `Floricultura Verdes Plantas · movimento de DD/MM/AAAA · edição nº N`. Abre com 2–3 linhas ao Fernando (a novidade do dia, boa primeiro). Ordem das seções — **manter sempre**:

**1. O que aconteceu hoje.** Cards movidos no dia (`lastTimeMoved` no dia, horário de Brasília) por destino. Comparar com a edição anterior e dizer a hora do corte.

**2. Encerramentos que não contaram.** Abre com "X dos Y encerramentos passaram pelo Ações".
- 2.1 vendas que entraram em Venda Efetivada sem Ações (`status` ≠ WON) ou sem valor — "N de M";
- 2.2 perdas sem `lostReason` — **listar todas** as N do "N de M". Checar se há card gêmeo do mesmo contato encerrado certo (duplicidade);
- 2.3 Incógnita cuja nota indica venda (`já fez o pedido`, `comprou`, `vem buscar`, `vai vir`, `vai passar na loja`, `veio até a loja`, `entregamos`) ou motivo de perda (`caro`, `mais barato`, `frete`, `outra cidade`, `desistiu`, `não temos`), e cards `WON` parados na Incógnita;
- 2.4 acumulado (série por data): perdida sem motivo · efetivada sem valor · **ganhos (status WON) fora da Venda Efetivada** — linha de base 124 em 21/10.

Sempre com **vendedor, cliente, telefone, valor e o trecho da nota**.

Kit automático: `rodar_edicao.sh <dia> <dados_anterior.json>` gera `dados.json` com todas as seções (`dados_edicao.py`); a sessão redige o texto no formato da edição anterior e preenche `pedidos_amanha` (texto + telefones), que viram a seção "O que eu pedi ontem" da edição seguinte.

**3. Mensagem agendada no Follow-up.** Cards em FU1+FU2 × com agendamento pendente (`sentAt` nulo, `sendAt` futuro, join por `contactId`). Série dia a dia. Totais da base (pendentes / história).

**4. As notas do dia.** Quantas (nos cards movidos no dia), por quem, quantas com data/prazo.

**5. A coluna Atendimento.** Contagem por coluna ativa e **quantos dormiram** (cards em Atendimento Inicial/Vendedores sem nenhum movimento no dia).

**6. Tempo de resposta.** TPR e TR por vendedor (mediana e P90), contra a meta de 4 min (TPR) e a proposta de 15 min (TR). Sem resposta no fim do dia e as que chegaram após 18h (não são atraso). Definições na seção 6-A.

**7. Classificação do atendimento por tag** (a partir da edição de 22/10). Nos atendimentos **iniciados no dia** (cards criados no dia no pipeline 10541): quantos receberam tag no card (`orderTags`), quais tags, por vendedor; quantos ficaram sem tag de tipo. Separar **tag de tipo** (BUQUES, GRAMA, FLOR DE PRESENTE, FLOR DE CORTE, PLANTAS ORNAMENTAIS, FRUTÍFERAS, ÁRVORES DE SOMBRA, PALMEIRA, CEDROS, EUCALIPTO, TREPADEIRA, FORRAÇÃO, PEDRA, TERRA/SUBSTRATO, VASOS, CESTA DE CAFÉ) de **tag de processo/campanha** (Follow-up, ORÇAMENTO, QUALIFICADO, PEDIDO DE CLIENTE, MENSAGEM AGENDADA, REMARKETING, SEMI PRESENCIAL, IA DESATIVADA, FORNECEDOR, 700, FESTIVAL DE PRIMAVERA, FINADOS CRISANTEMOS 2025, RASPINHA VP, SORTEIO RADIO). Tag do contato (`tags`) aparece à parte, como herança — não conta como classificação do dia. **Não existe tag PAISAGISMO** (medido 22/10): reportar até ser criada.

**8. Carga do dia por vendedor.** Cards ativos (Atendimento, Vendedores, FU1, FU2) por vendedor, com série dia a dia (para a decisão de redistribuir leads).

**9. O que eu pedi ontem.** Cada pedido da edição anterior com a situação de hoje (feito / não feito), relido na base pelo telefone do contato.

**10. O que eu peço para amanhã.** No máximo 4 itens, nominais, acionáveis hoje.

**11. Como o relatório é feito.** Fonte, hora da leitura, volume lido (números da coleta **do dia**) e o que ainda não entra. Correções de edições anteriores, assumidas aqui.

### 6-A. Tempo de resposta — definições (TPR/TR)

Fonte: `/messages/{ticketId}` dos tickets dos cards com mensagem no dia. Relógio só no expediente; fora dele começa na abertura do dia útil seguinte. Só vendedor humano para o relógio.
- **Bloco** = mensagens consecutivas do cliente; relógio na primeira. Cliente que volta após >24 h de silêncio abre bloco novo (o anterior fecha como abandonado).
- **TPR** = bloco sem resposta humana no ticket nas 24 h anteriores. Os demais blocos são **TR**.
- Respondido fora do expediente (ex.: sábado) sai da mediana e é contado à parte. Sem resposta até a coleta: separado entre "prazo correndo" e "chegou após 18h".
- Reportar **mediana e P90**, nunca média. Regras assumidas, a validar com o Fernando.
- Limitação: "ok/obrigado" de encerramento conta como bloco sem resposta.

### Tom

- Reconhecer o que está certo antes de apontar o que está errado, com número.
- Quando um vendedor acerta, citar nominalmente como modelo.
- Erro do consultor se assume no corpo do documento, não em nota de rodapé.
- Nunca transformar falha de desenho em cobrança de pessoa: se a Incógnita é a única saída sem exigência, o problema é a saída.
- Não escrever "o sistema calcula sozinho" nem "relatório automático" enquanto a montagem passar pelo consultor.

---

## 6. SAÍDA EM PDF E WORD

Usar `timbrado_engine.py` (markdown → PDF timbrado) e `gerar_doc.py` (PDF + .docx do mesmo markdown).

```python
from timbrado_engine import gerar_pdf
gerar_pdf("Relatorio_Diario_Verdes_Plantas_<dd-mm>.pdf", md, marca="portilho")
```

- **marca `portilho`** — cliente, vendedores, qualquer pessoa de fora.
- **marca `conselho`** — somente conselheiros. **Nunca** em documento que vá para cliente ou colaborador do cliente: O Conselho é confidencial.
- No Linux a fonte é a Carlito do sistema (`/usr/share/fonts/truetype/crosextra`). Sem `assets/logo_portilho_ic_branco.png`, o cabeçalho escreve "PORTILHO Inteligência Comercial" em texto branco.
- Símbolos ✅/❌ não existem na fonte: virar "(na meta)"/"(fora)".
- Renderizar as páginas (`pdftoppm`) e conferir antes de enviar.

Padrão completo: `wiki/entities/padrao-documentos-portilho.md`.

---

## 7. ENVIO

Autorizado pelo Jhonatan em 22/10/2026, **todo dia útil às 20h, com o movimento do próprio dia** (leitura depois das 18h; edição nº 3 = quinta 22/10). Tarefa agendada "Relatório diário Verdes Plantas — 20h" acorda a conversa Comercial Verdesplantas às 19:41 (seg–sex), que já tem Drive, Gmail e o kit:

1. **WhatsApp ao Fernando** pelo DKW **da Portilho** (empresa 7061 — nunca pelo WhatsApp da cliente): contato "Fernando - Verdes Plantas" (id 5517468, +55 42 99958-9335). Script `enviar.js <pdf> "<legenda>"` acha a conversa sozinho e confere a empresa. Legenda só apresenta; números ficam no PDF.
2. **E-mail** para **`verdes_plantas@yahoo.com.br`** com o relatório no corpo (HTML de `md_html.py`, mesmo conteúdo do PDF). Assunto: `Relatório diário do comercial — Verdes Plantas — movimento de DD/MM (edição nº N)`.
   **Conferência do envio (22/10):** o POST devolve 200 antes de o WhatsApp entregar. O envio vai para o `@lid` do Fernando (mesmo identificador dos áudios dele), e no celular do Jhonatan pode não aparecer na hora — em 22/10 ele achou que não tinha chegado e reenviou, duplicando. Depois do envio, ler `/messages/4719278` e reportar o `ack` da mensagem (1 enviada · 2 entregue · 3 lida); só dizer "entregue" com ack ≥ 2.
3. Salvar o markdown da edição no Drive (pasta `relatorios` da verdes-plantas) — marca o dia como enviado e evita reenvio.

No Railway (`D:\portilho-agente`) existe `alerta_email.py` (SMTP Gmail) — alternativa ao conector Gmail.

---

## 8. CHECKLIST DE CONFIGURAÇÃO DO AMBIENTE

Perguntas a fazer ao suporte do DKW quando o ambiente de um cliente ainda não força as regras:

1. *"Para cada contato que entra no atendimento inicial, precisamos que gere uma **nova negociação** e siga o fluxo do CRM. Como fazemos isso?"*
2. *"Como **impedir que um card seja movido manualmente** para Venda Efetivada, Venda Perdida, Não Comercial e Incógnita? Queremos que a entrada nessas colunas só aconteça pelo botão Ações."*
3. *"O DKW consegue **criar mensagem agendada automaticamente** quando o card entra em Follow-up 1 (D+2) e Follow-up 2 (D+7)?"*
4. *"O card 'Tempo de resposta' (Relatórios › Conversas) mostra segundos rotulados como minutos e conta mensagem automática — podem corrigir e documentar `userIds` na API?"* (mensagem pronta em `comunicacoes/2026-10-21_dkw_tempo-de-resposta.md`).
5. *"É possível tornar a tag de tipo de atendimento obrigatória ao mover o card de Atendimento Inicial?"* (sustenta a regra 8).

Conferir também que os **quatro estados** aparecem em Ações (venda ganha, venda perdida, incógnita, não comercial) e que existe tag para cada tipo de atendimento (em 22/10 faltava PAISAGISMO).

> **Princípio que organiza o checklist:** regra que só serve ao gestor não se sustenta por disciplina. Antes de pedir comportamento novo, procurar o botão que faz aquilo acontecer sozinho. Foi assim que o encerramento por Ações resolveu, numa tarde, o que quatro semanas de cobrança não tinham resolvido — em 21/10, 43 de 56 encerramentos já passaram por ele.
