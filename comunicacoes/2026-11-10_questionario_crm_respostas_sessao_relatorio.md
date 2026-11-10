# Questionário do configurador do CRM — respostas da sessão do relatório comercial
### Verdes Plantas · 10/11/2026

**Fontes desta sessão:** coletas diárias do DKW (só leitura, de 21/10 a 09/11; a última em 09/11 às 18h41), 15 edições do relatório diário, 3 análises semanais, a ata da reunião de 28/10, as mensagens do Fernando de 30/10 e 03/11 no ticket da Portilho e a transcrição da reunião de 10/11 (lida inteira, 1.117 linhas).

**Legenda.** **M** = medido por mim na base do DKW. **D** = documentado (reunião, mensagem do Fernando, ata). **S** = suposto.

**Aviso de método.** O Anexo 1 veio na mesma mensagem que o questionário, então eu o li antes de responder. Para a comparação continuar valendo, as respostas abaixo usam só as fontes desta sessão, e cada uma diz de onde veio.

---

## PARTE 1 — MINHAS RESPOSTAS

**1. O que vende e para quem.**
- Categorias que aparecem nas tags de tipo e nos motivos de perda entre 02 e 09/11 **(M)**: buquês, grama, plantas ornamentais, pedra, frutíferas, flor de presente, árvores de sombra, terra/substrato, palmeira, paisagismo, folhagens, forração, flor de corte, cedros e orçamento de jardim. Nos motivos também aparecem crisântemos e vasos de Finados, orquídeas, mudas (pinus, baleeira, laranja) e coroa — esta, a loja não trabalha.
- No online, a venda média registrada no CRM foi de R$ 254 na semana de 02 a 07/11: 49 vendas, R$ 12.454,26 **(M)**.
- Eucalipto e grama são o foco do Edimar, com ciclo de 1 a 2 meses; buquê é o foco da Carine, com decisão em até 1 semana **(D, Fernando em 10/11)**.
- **Não medido:** para quem vende (rural, atacado, licitação), faturamento e ticket do ERP. Isso vem do SIGCLOUD, que esta sessão não lê.

**2. Canais.**
- WhatsApp no DKW é o canal de tudo o que eu medi **(M)**.
- Instagram não gera negócio e a conversa encerra em 24h **(D, Fernando em 03/11)**.
- O Messenger do Facebook está para entrar, com 10 a 30 mensagens por mês segundo a contagem do próprio Fernando **(D, 10/11)**.
- Google Meu Negócio, rádio, tráfego pago, indicação e loja física **(D, lista lida pelo Jhonatan e confirmada pelo Fernando em 10/11)**.
- A origem do lead não existe como campo no CRM **(M)**; o Tintim passa a ser a fonte **(D)**.

**3. O que já funciona no CRM** (semana de 02 a 07/11, salvo indicação):
- **Encerramento pelo botão Ações:** 245 de 248 (99%) **(M)**.
- **Motivo da perda:** 105 de 105 na semana; 217 de 225 (96%) desde 20/10 **(M)**.
- **Valor na perda:** 211 de 225 (94%) desde 20/10 **(M)**.
- **Tag de tipo nos atendimentos novos:** 46% na semana; 74% em 09/11 **(M)**.
- **Notas:** 78 na semana, nenhuma com data **(M)**.
- **Automações que disparam:** a boas-vindas (46387), a Raspinha da Venda Perdida (56000) e o "Obrigado por escolher a Verdes Plantas" **(M, contadas nas mensagens)**.
- **Mensagens agendadas:** o recurso funciona — 163 enviadas no total da base —, mas o uso parou: 1 agendamento novo entre sexta e segunda **(M)**.

**4. O que corrigir.**
- **Card que volta ao atendimento** **(M)**:
  - quando o cliente escreve de novo, o mesmo card volta ao Atendimento Inicial; em 09/11, 55 vendas estavam de volta no atendimento;
  - quando o card é reencerrado fora da Venda Efetivada, a venda é cancelada — caso Ivair Zandonai, R$ 1.699,00, devolvido em 30/10 e cancelado de novo em 06/11 e 09/11;
  - "ganhos fora da Venda Efetivada": 133 cards.
- **Automação 55993:**
  - nunca aparece em nenhuma mensagem coletada, em nenhum dia **(M)**;
  - o erro do print do Fernando é `ERR_NO_DEF_WAPP_FOUND in COMPANY 12198` **(D)**; **12198 é o id do usuário do Edimar, não o da empresa (7078)** **(M)**. Hipótese: a ação procura a conexão de WhatsApp pelo vendedor e não pela empresa **(S)**.
- **Arrastar × Ações** **(M):**
  - 4 encerramentos arrastados em 09/11;
  - exemplo: a Camila Mikalski foi arrastada para Venda Efetivada sem valor, com a nota "parou de responder… agendei msg" — era follow-up, não venda.
- **Cliente novo caindo em usuário que não atende:** dos 53 clientes novos sem resposta na semana, 33 estavam nos usuários do Fernando (19), da Luana (8) e da Jaqueline (6) **(M)**.
- **A Maria não tem usuário próprio** e usa o login da Luana: 7 cards levados para Não Comercial em 09/11 **(M)**.
- **Perfis de administrador** **(D, 10/11)**. **Loops da Raspadinha e da avaliação do Google** **(D, Fernando)**. Não medi nenhum dos dois.

**5. Usuários** — fechada. Ids no DKW: Fernando 12152, Edimar 12198, Carine 21035, Douglas 15948, Luana 28637, Jaqueline 12197 e Jhonatan 12107 **(M)**. Não vi usuário da Maria nem do Thiago nos dados até 09/11.

**6. Do primeiro contato à venda.**
- Pipeline 10541 **(M)**: Atendimento Inicial (44341) → Atendimento de Vendedores (69421) → Follow-up 1 (36971) → Follow-up 2 (113074) → encerramento pelo Ações em Venda Efetivada (32318), Venda Perdida (36613), Não Comercial (121919) ou Incógnita (44334).
- Hoje o cliente que volta reabre o card antigo em vez de gerar uma negociação nova **(M)**.

**7. Distribuição.**
- **O que acontece**, contando os cards criados por dono **(M)**:

  | Semana | Douglas | Carine | Edimar | Fernando, Luana e Jaqueline |
  |---|---|---|---|---|
  | 19 a 25/10 | 38 | 41 | 30 | 17 |
  | 26/10 a 01/11 | 28 | 41 | 32 | 38 (Fernando 30) |
  | 02 a 08/11 | 38 | 37 | 23 | 18 |

  - O 20/40/40 só aparece a partir de 02/11: entre os três vendedores, 23/40/38.
  - Mesmo assim, 16% dos clientes novos ainda caem em quem não faz atendimento comercial.
- **Cliente que volta:** hoje volta ao mesmo card e ao mesmo dono **(M)**. O combinado em 10/11 é seguir o rodízio **(D)**.

**8. Dados para o orçamento.** Produto, quantidade, retirada ou entrega, cidade, data e metragem da grama **(D, 10/11)**. Endereço e o que deve ser feito **(D, seção B)**. Nas notas, "vir buscar" e "frete" aparecem pouco **(M)**.

**9. Regras comerciais** — fechada.

**10. IA** — em aberto. O que eu tenho é a dor que ela resolve:
- a primeira resposta ao cliente novo piorou de 11 min (26 a 31/10) para 28 min (02 a 07/11) e 39 min (09/11) **(M)**;
- o Edimar registrou duas perdas como "demora em responder o cliente" **(M)**.

**11. Automações desejadas.**
- Que meus dados justificam **(M)**:
  - negociação nova para o cliente que volta (55 vendas reabertas);
  - mensagem agendada obrigatória ao entrar no follow-up (4 de 72 cards têm);
  - travar o arrasto nas colunas de encerramento;
  - cliente novo só para Carine, Douglas e Edimar.
- Que o Fernando pediu **(D)**:
  - a negociação transferida junto com a conversa;
  - cancelar o agendamento quando o cliente responde antes;
  - tag automática de origem para Instagram e Facebook.

**12. Sistemas.**
- SIGCLOUD, com o telefone como chave; Power BI, já conectado ao SIGCLOUD; Tintim **(D, 10/11)**.
- Os demais não são da minha base.

---

## PARTE 2 — COMPARAÇÃO COM O ANEXO 1

| # | Resultado | Onde diverge e qual versão vale |
|---|---|---|
| 1 | Igual nas categorias; **só o Anexo tem** os números do ERP | Não tenho como conferir o faturamento de R$ 221.733/mês, o ticket de R$ 84,50 nem a grama a R$ 610 mil. Vale o Anexo, com fonte a citar |
| 2 | Igual | Acrescento o volume do Messenger (10 a 30/mês, contagem do Fernando) |
| 3 | **Diverge** | O Anexo diz que funciona bem "o que o sistema calcula sozinho". O que mais melhorou é comportamento da equipe: Ações 99%, motivo 100%, tag 46%. O que o sistema faz sozinho — automações, reabrir o card — é justamente o que está quebrado |
| 4 | **Diverge** | O Anexo diz "motivo da perda historicamente inexistente". **Está desatualizado:** 96% desde 20/10 e 100% na última semana. Faltam no Anexo os 55 cards reabertos, a venda cancelada e o id do Edimar no erro da 55993. "10 automações inativas" e "disparo duplicado": só o Anexo tem; não medi |
| 5 | **Diverge** | O Anexo lista a Maria como usuária. **Ela não tem usuário: usa o login da Luana** (medido; o próprio relatório conta os avisos dela no usuário da Luana). O Anexo também põe a Jaqueline em "conteúdo e vendas": ela respondeu 0 clientes novos na semana, e na reunião o Fernando disse "a Jaque não tá usando" |
| 6 | Igual | Acrescento o card que é reaberto |
| 7 | **Diverge (o que acontece × o que se quer)** | O 20/40/40 é a regra; na prática, 23/40/38 mais 16% para quem não vende. "Cliente que volta segue o rodízio" é o desejado; hoje ele volta ao mesmo card e ao mesmo dono |
| 8 | Igual | — |
| 9 | Igual | — |
| 10 | Igual (aberta) | Acrescento o tempo de resposta como justificativa medida |
| 11 | Quase igual | Acrescento cliente novo só para vendedores e usuário próprio da Maria |
| 12 | **Só o Anexo tem** WooCommerce, Meta, GMN, Lovable e Raspinha digital | Fora da minha base |

**Nota da seção B ("logística é a maior causa de perda registrada"): diverge, e é a divergência mais importante.**

| O que os dados mostram | |
|---|---|
| Perdas desde 20/10 | 225, sendo 217 com motivo |
| "Parou de responder", quase sempre depois de reativar | cerca de 116 (53%) |
| "Só perguntou o valor e sumiu" | cerca de 28 |
| Não temos o produto ou a pronta entrega | cerca de 25 |
| Logística explícita (outra cidade, não vem buscar, enviar para SC) | **4** |
| "Frete" nos 317 motivos distintos já lidos | 1 vez |
| "Frete" nas 720 notas lidas | 4 vezes |

A contagem foi feita por palavra-chave e é aproximada, mas a ordem de grandeza não muda. A pergunta de retirada ou entrega faz sentido para o orçamento, só não pelo motivo citado. Se a outra sessão leu notas anteriores a 20/10, de outra base ou da loja, vale registrar de onde veio.

**Seção C conferida na transcrição:**
- **C.1 está certa.** Uma ressalva: a transcrição diz "o 2 é imprescindível **não** ter mensagem agendada", mas a frase seguinte ("como é que você não vai ter mensagem agendada com cliente que tá na mesa?") mostra que é erro da transcrição. O certo é **ter**.
- **O dado confirma a percepção invertida.** Hoje o FU2 (35 cards) é quase do tamanho do FU1 (37). Têm mensagem agendada: 1 de 37 no FU1 e 3 de 35 no FU2.
- **"O Edimar aumentou as vendas"** é verdade em valor e não em quantidade:

  | Semana | Vendas do Edimar | Valor |
  |---|---|---|
  | 26/10 a 01/11 | 13 | R$ 3.200 |
  | 02 a 08/11 | 7 | R$ 6.843 |

  O valor da segunda semana vem de duas vendas grandes: R$ 4.070 e R$ 2.000.
