# Relatórios em duas camadas — desenho do relatório de gerência (Verdes Plantas)
### v2 · 24/11/2026 (aprovada pelo Jhonatan) · INTERNO — para o Jhonatan revisar e aprovar · não enviar ao cliente

> Origem da decisão: a sessão de presidência (confidencial). Este documento não cita a origem e pode servir de base para o que for apresentado depois. A comunicação ao Fernando sobre a mudança está **fora deste escopo** — até lá, o diário segue indo para ele como hoje.

---

## 0. O que mudou na v2 (aprovado pelo Jhonatan em 24/11)

**Relatório × direcionamento são coisas diferentes.** O relatório segue o tempo de decisão do leitor (o Fernando decide tendência → semanal). A cobrança segue a fase do hábito de quem é cobrado (o coordenador está formando rotina diária → verificação diária). Por isso há **três artefatos**:

1. **Relatório de gerência** — semanal, segunda 8h (este documento).
2. **Sinal diário da coordenação** — 9h30, uma linha no WhatsApp do Fernando: *"Coordenação ontem: lista tratada ✓/✗ · relatório aberto até 9h ✓/✗"*. Sem número de itens, sem lista.
3. **15 minutos semanais Fernando × Douglas**, logo após o relatório de segunda, **com pauta do Douglas**.

**Regra de reação ao sinal:** só depois de 2 dias vermelhos seguidos, só com o coordenador e só sobre a rotina ("o que travou na coordenação?"). O sinal nunca abre detalhe.

**Fases.** Semanas 1–6: sinal diário + semanal. Passa para **só semanal + alerta por exceção** quando, por 4 semanas seguidas: lista tratada em ≥ 4 de 5 dias · reunião registrada 4 de 4 · encerramentos fora da regra sem piora · dono na operação estável ou caindo. Volta ao diário se 2 semanas seguidas ficarem ruins — comunicado como "voltamos a acompanhar diariamente", nunca como punição.

**Calibragem do sinal:** com a lista resolvendo 37–61% ao dia (16–19/11), o ✓ começa em **≥ 50%** e sobe 10 pontos a cada 4 semanas no verde.

**Pré-condição:** nenhuma cadência resolve o contorno enquanto o Fernando continuar recebendo o diário com nomes. O sinal e o relatório de gerência só valem depois que o diário passar ao coordenador (decisão da presidência).

**Indicadores acrescentados (pesquisa externa, aprovados):** quem resolve as exceções (coordenador × dono) · efeito do follow-up (cliente respondeu em até 7 dias) · resposta no meio da conversa · funil parado em R$ por coluna (substitui "carteira parada") · higiene dos dados (tag de tipo e contatos com mais de um card ativo). **Fora:** dispersão entre vendedores (n = 3 expõe), volume de atividade (vira spam), NPS semanal (n pequeno). **Regra do mínimo de 5 casos vale também para totais e subtotais.** Registro manual do Fernando (D2): opcional.

**Protótipo com dados reais:** `relatorios/gerencia/PROTOTIPO_Gerencia_VP_2026-11-16_a_21.md` (cálculo em `ferramentas/tpr-tr/gerencia.py`).

## 1. As duas camadas

| | Relatório de coordenação | Relatório de gerência |
|---|---|---|
| **Leitor** | Coordenador (Douglas) | Fernando |
| **Pergunta que responde** | Quem e qual card precisa de ação hoje? | A coordenação está funcionando? Para onde vai a tendência? |
| **Corte** | Caso individual: vendedor, cliente, telefone, card | Equipe inteira, semana e tendência — **sem nome, sem telefone, sem quebra por vendedor** |
| **Frequência** | Diário, 19h (já existe: diário + Pendências) | **Semanal**, segunda às 8h (proposta) |
| **O que muda** | Só o destinatário | Novo |

**Regra de corte (o teste de cada número):** se, com o número na mão, o Fernando consegue chegar ao vendedor X ou ao card Y, ele não entra no relatório de gerência. Consequências práticas:
- nenhuma tabela por vendedor; nenhuma lista de cards (exceção: a lista do SIGCLOUD, item E, sem nome de vendedor);
- nada quebrado em grupos com menos de 5 casos (um "1 cliente sem resposta na grama" aponta para alguém);
- o rodízio aparece como "regra respeitada: sim/não e desvio em pontos", não como "Edimar recebeu 27%".

**Consequência para o que já existe:** a análise semanal de hoje traz tabelas por vendedor (desempenho, carteira, quem respondeu). Pela regra, ela passa a ser o relatório de gerência (sem essas tabelas) ou vira material da coordenação. Proposta: **a análise semanal vira o relatório de gerência** — o Fernando já disse em 18/11 que o relatório semanal foi "uma das melhores coisas até hoje"; muda o corte, não o hábito.

---

## 2. Indicadores do relatório de gerência

Legenda — **Hoje**: o kit já mede pela API do DKW, sem ninguém digitar · **Kit**: dá para medir pela API, falta escrever o cálculo · **Config**: precisa de configuração nova no DKW · **Manual**: alguém precisa registrar.

### A. A rotina da coordenação aconteceu?

| # | Indicador | Como se mede | Situação |
|---|---|---|---|
| A1 | **Lista da coordenação resolvida em 24 h** — % dos itens da lista de ontem que estão corrigidos hoje | Pendências do dia anterior × base de hoje (o kit já calcula "resolvidas desde ontem") | **Hoje** |
| A2 | **Relatório da coordenação lido até 9h** — dias na semana (0–5) | Confirmação de leitura (ack 3) da mensagem enviada ao coordenador pelo DKW da Portilho, com o horário | **Kit** — depende de o relatório passar a ir para o Douglas |
| A3 | **Reunião semanal do comercial com registro** — sim/não | Card "Reunião comercial — semana DD/MM" num funil interno (ou tag), com a ata na nota do card. O kit lê a nota | **Config** (um funil ou tag; 10 min do Thiago) + o coordenador cria o card |

**Sobre "a verificação diária do coordenador aconteceu?":** o DKW não sabe se alguém *olhou* uma lista. A1 mede o efeito (a lista andou) e A2 mede a presença (abriu). Juntos respondem a pergunta sem ninguém digitar. Reunião semanal só existe no sistema se alguém registrar — A3 é o mínimo: um card com a ata.

### B. O processo está de pé? (equipe inteira, tendência de 8 semanas)

| # | Indicador | Situação | Observação |
|---|---|---|---|
| B1 | **Clientes esperando resposta no fim do dia** — média por dia útil e tendência | **Hoje** | Sem lista. Semana 16–21/11: 63 clientes novos sem resposta |
| B2 | **1ª resposta ao cliente novo** — mediana e P90 da equipe | **Hoje** | 16–21/11: 78 min / 4,7 h |
| B3 | **Encerramentos fora da regra** — arrastados, sem motivo, e **encerrados com o cliente como último a falar** | Arrastado e sem motivo: **Hoje** · cliente último a falar: **Kit** (lê a última mensagem da conversa no encerramento) | A "regra de saída do atendimento" já recomendada pede exatamente isso |
| B4 | **Follow-up com mensagem agendada** — % no FU2 e no FU1 (foto de sexta) | **Hoje** | |
| B5 | **Venda ganha com comprovante do cliente na conversa** — % | **Hoje** (leitura da conversa, desde 18/11) | Regra de 18/11: venda só é ganha com comprovante |
| B6 | **Venda efetivada com valor** — % | **Hoje** | Ver o alerta abaixo |
| B7 | **Carteira parada** — cards ativos sem movimento há mais de 3 dias úteis | **Hoje** | |

> **Alerta de número (regra zero).** O "39% das vendas efetivadas sem valor" é a base inteira, com o histórico anterior ao botão Ações. Medido hoje: **32% da base toda (411 de 1.285)**, mas **1% desde 20/10 (3 de 258)** e **1% desde 09/11 (2 de 139)**. O problema foi resolvido pelo botão Ações. B6 fica como guarda (meta ≥ 98%), não como manchete. Vale corrigir esse número no arquivo do caso.

### C. O resultado (o que o dono precisa para decidir negócio)

| # | Indicador | Situação |
|---|---|---|
| C1 | Vendas e faturamento do online (n, R$) e conversão da equipe | **Hoje** |
| C2 | Ciclo da venda por categoria (início da conversa → venda ganha) | **Hoje** |
| C3 | Conversão por categoria (tag) — para decidir campanha | **Hoje** (calculado, ainda não publicado) |
| C4 | Motivo da perda: % que não explica ("sem retorno") | **Hoje** |

### D. O termômetro: o operacional está subindo para o dono?

| # | Indicador | Como se mede | Situação |
|---|---|---|---|
| D1 | **Atuação do dono na operação** — mensagens do Fernando em conversas de cliente, cards encerrados no usuário dele, cards novos que caíram no usuário dele | Mensagens com `userId` do Fernando; cards por dono | **Kit** (dados já coletados; 23–24/11: 19 mensagens dele em 7 conversas de cliente) |
| D2 | **Vezes que a equipe foi direto ao Fernando em vez do coordenador** | Acontece fora do DKW (WhatsApp pessoal, balcão). O sistema não vê | **Manual**: o Fernando marca um número por semana. Alternativa futura: canal interno do DKW como única porta para dúvida de processo — aí vira **Config** |

D1 é a parte do termômetro que o sistema vê sozinho: quando a autoridade sobe para o dono, ela aparece como o dono respondendo cliente e encerrando card. Não substitui D2, mas é automático e não depende da boa vontade de ninguém.

### E. O que só o SIGCLOUD confirma (lista para o Fernando conferir)

Vendas ganhas sem baixa no SIG · clientes em Follow-up/Perdida/Incógnita que compraram na loja · grama vendida × estoque · pedidos em aberto. Vai como **lista de clientes sem nome de vendedor** — é conferência do ERP, não cobrança. **Situação:** a lista sai do CRM (**Hoje**); a conferência é do Fernando até o ERP estar conectado ao motor.

---

## 3. Formato e entrega

- **Uma página**, timbrado Portilho, segunda às 8h (WhatsApp + e-mail, como o semanal hoje).
- Topo: **3 a 5 sinais** em semáforo contra a meta (verde / amarelo / vermelho), com a seta da tendência de 8 semanas.
- Meio: blocos A a D em tabela curta, cada número com a semana anterior ao lado.
- Fim: **até 3 perguntas para a conversa do Fernando com o coordenador** — sempre sobre a rotina ("a lista andou 40% — o que travou na coordenação?"), nunca sobre vendedor.
- Regra das séries curtas (já usada no semanal): menos de 6 semanas = linha de base, sem alarme.
- Mensal: o mesmo relatório com 4 semanas consolidadas, para a reunião mensal com o marketing (já prevista no plano de 3 meses).

---

## 4. O que dá para automatizar hoje × o que depende de configuração

| Pronto hoje (só cálculo e layout) | Depende de decisão ou configuração |
|---|---|
| A1, B1, B2, B4, B5, B6, B7, C1–C4, parte de B3, lista E | **A2:** o relatório de coordenação passar a ir para o Douglas (decisão da presidência) |
| **Kit novo, sem configuração:** B3 (cliente último a falar), D1 | **A3:** funil ou tag de "Reunião comercial" no DKW (Thiago) |
| | **D2:** registro manual do Fernando, ou canal interno no DKW |
| | **Travas no sistema** (ver documento de responsáveis e travas): impedir encerramento com o cliente como último a falar; bloquear arrasto para as colunas de encerramento |

**Estimativa:** com A2 e A3 decididos, o primeiro relatório de gerência sai na segunda seguinte à aprovação, com B/C/E completos e A1 já com série histórica (as pendências diárias existem desde 29/10) e D1 recalculável para trás pelo histórico das conversas.

---

## 5. Portabilidade — o motor tem que poder virar skill no GPT da empresa

Hoje o motor roda no Claude, com os tokens do Jhonatan e a conta da Portilho personificando a Verdes. O destino provável é o GPT da própria empresa. Para a transferência ser uma cópia, não uma reconstrução:

1. **Catálogo de indicadores num arquivo só** (`indicadores_vp.md` ou `.yaml`): para cada indicador — nome, pergunta que responde, camada (coordenação/gerência), fórmula, rota do DKW, meta, regra de corte. É a especificação que qualquer modelo executa.
2. **Cálculo em scripts Python sem dependência do Claude** (já é assim: `dados_edicao.py`, `pendencias.py`, `semana.py`). Falta separar o "redigir o texto" (feito pela sessão) do "calcular" (scripts).
3. **Acesso por usuário-robô dentro da Verdes**, com o token da própria empresa — em vez da conta da Portilho personificando. Resolve também o risco da personificação ser da conta inteira.
4. **ERP:** hoje não está conectado aqui. No GPT da empresa, com o SIGCLOUD conectado, a lista E vira indicador automático (venda ganha × baixa, por telefone).

---

## 6. Decisões que preciso de você

1. **Frequência:** semanal na segunda às 8h, sem nada diário para o Fernando? (Proposta: sim. Exceção só como alerta se B1 passar do limite dois dias seguidos.)
2. **A análise semanal vira o relatório de gerência** (perde as tabelas por vendedor)?
3. **D2 manual:** o Fernando aceitaria marcar um número por semana? Ou fica só D1 até existir o canal interno?
4. **A3:** funil interno "Rotina da coordenação" ou só uma tag? (Proposta: funil — fica isolado do comercial.)
