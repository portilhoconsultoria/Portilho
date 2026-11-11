# Briefing de configuração do CRM e do agente de IA
### Floricultura Verdes Plantas · para Thiago Coréas · 11/11/2026

Thiago, este documento responde ao seu questionário e junta o que você precisa para configurar o CRM (DKW) e o agente de IA da Verdes Plantas. As respostas vêm da reunião com o Fernando em 10/11, das respostas dele por escrito e da leitura diária da base do CRM que a Portilho faz desde outubro. Onde algo ainda precisa ser confirmado com o Fernando, está marcado **(a confirmar)**.

**Regra de leitura:** onde este documento diverge dos prompts antigos da IA ou da planilha de perguntas e respostas, **vale este documento** — o material antigo é ponto de partida, não está atualizado.

## 1. A EMPRESA

**Floricultura Verdes Plantas Ltda** — Rua Trajano Grácia, 960, Stroparo, Irati (PR). Atacado e varejo. WhatsApp (42) 99936-5082 · Instagram @verdesplantasoficial · e-mail verdes_plantas@yahoo.com.br.

**O que vende:** grama (maior item; Esmeralda, Sempre Verde/São Carlos, Preta, Azul, Amendoim, Tomilho), mudas e plantas (frutíferas, ornamentais, folhagens, palmeiras, árvores de sombra, eucalipto, cedros), buquês, flores e arranjos, pedras, terra, substrato e adubo, vasos e presentes. Também faz **serviço de jardinagem e paisagismo** com equipe própria.

**Para quem:** consumidor final (loja e online), muitos da área rural, e clientes de atacado. O público é conservador; atendimento humano e próximo faz diferença.

## 2. CANAIS

- **WhatsApp** — principal, conectado ao DKW.
- **Instagram** — chega ao DKW, mas **não gera negócio** e a conversa encerra após 24 horas (janela da Meta).
- **Messenger do Facebook** — **a conectar.** Recebe de 10 a 30 mensagens por mês e hoje ninguém responde.
- Origem dos clientes: anúncios pagos, Google Meu Negócio, rádio, indicação e loja física. A **origem do lead** passa a vir do **Tintim** (já em uso, com o Matheus, que cuida do tráfego).

## 3. O QUE JÁ FUNCIONA NO CRM

Medido na base do DKW (semana de 02 a 07/11 e dia 10/11):

- 7 acessos, funil "Verdes Plantas – Gestão do atendimento" (ID 10541) com 8 colunas.
- **Encerramento pelo botão Ações:** 99% dos encerramentos na última semana.
- **Motivo da perda preenchido:** 97% das perdas desde 20/10.
- Tags por tipo de produto no card, notas nos cards e mensagens agendadas (o recurso funciona; o uso pela equipe ainda é baixo).
- Automações que disparam: **boas-vindas** (ID 46387), **Raspinha** na Venda Perdida (ID 56000) e **"Obrigado por escolher a Verdes Plantas"** no pós-venda.
- O agente de IA (Luna Verde) **existiu e foi desligado** — ver seção 10.

## 4. O QUE PRECISA SER CORRIGIDO

Em ordem de impacto:

| # | Problema | Evidência |
|---|---|---|
| 1 | **Cliente que volta reabre o card antigo** em vez de gerar nova negociação. Quando o card é reencerrado fora da Venda Efetivada, a venda é cancelada | 29 a 55 vendas por dia de volta no atendimento; caso de uma venda de R$ 1.699 cancelada duas vezes |
| 2 | **Automação 55993 não dispara** (coluna inicial e venda ganha). Erro: `ERR_NO_DEF_WAPP_FOUND in COMPANY 12198` | 12198 é o ID do usuário de um vendedor, não da empresa: a automação parece procurar a conexão pelo vendedor. 0 disparos em todos os dias medidos |
| 3 | **Transferência:** quando outro vendedor responde, a conversa passa para ele, mas a **negociação (card) fica com o dono antigo** | 6 clientes no dia 10/11 respondidos por quem não era o dono do card |
| 4 | **Raspinha e avaliação do Google em loop** — quem responde volta como lead novo | Confirmado pelo Fernando |
| 5 | **Instagram não gera negócio** e encerra em 24 horas | Pedido do Fernando (03/11) |
| 6 | **Cancelar a mensagem agendada** quando o cliente responde antes do horário | Pedido do Fernando (03/11) |
| 7 | **Arrastar card × botão Ações:** a equipe mistura os dois e gera erros (venda arrastada sem valor, card ganho em coluna errada) | Regra combinada: **arrastar é manutenção; Ações é encerramento**. Bloquear o arrasto para as 4 colunas de encerramento |
| 8 | **Perfis como administrador** — limitar o acesso de cada usuário | Decidido em 10/11 |
| 9 | **Tags do CRM diferentes das categorias do ERP (SIGCLOUD)** | Decidido em 10/11: as tags devem ser as categorias do SIGCLOUD |
| 10 | Clientes novos caindo em usuários que não vendem e em **cards sem dono** | 16% dos clientes novos na semana; 4 cards sem dono em 10/11 |

O valor da negociação na aba Conversas, pedido pelo Fernando, **já existe** — é questão de mostrar à equipe.

## 5. USUÁRIOS

Nomes e e-mails já estão cadastrados no DKW. Funções:

| Pessoa | Função |
|---|---|
| Fernando | Dono e vendedor |
| Carine | Vendedora (foco em buquês) |
| Douglas | Vendedor (online) |
| Edimar | Vendedor (foco em grama e eucalipto) |
| Luana | Financeiro |
| Jaqueline | Conteúdo; hoje praticamente não atende no CRM |
| Maria | Caixa; dispara avisos de pedido **usando o login da Luana** — falta decidir se terá usuário próprio |
| Thiago Coréas | Configuração do sistema e do agente de IA |

## 6. DO PRIMEIRO CONTATO À VENDA

1. **Atendimento Inicial** — cliente chega (é onde a IA vai atuar).
2. **Atendimento de Vendedores** — negociação acontecendo agora.
3. **Follow-up 1** — aguardando o cliente. **Todo card precisa de mensagem agendada.** Se o cliente não respondeu, continua no FU1 com nova mensagem agendada.
4. **Follow-up 2** — só quem **respondeu e renegociou** (lead quente). Também com mensagem agendada. É mais importante que o FU1.
5. **Encerramento pelo botão Ações:** Venda Efetivada (com valor), Venda Perdida (com motivo e valor), Não Comercial ou Incógnita (produto não identificado).

Sem contato nenhum depois das tentativas → **Venda Perdida**. O critério para mudar de follow-up é **interação, não tempo nem produto**. **Toda conversa nova de um cliente gera uma nova negociação** — nunca reaproveitar card antigo.

## 7. DISTRIBUIÇÃO DOS CLIENTES

**Manter como está:** rodízio automático entre os três vendedores — **Carine 40% · Douglas 40% · Edimar 20%**. A IA, ao terminar a qualificação, entrega o cliente para esse mesmo rodízio. Cliente antigo que volta **segue o rodízio** (não precisa cair no mesmo vendedor).

Dois ajustes de configuração: o rodízio de 10/11 entregou Edimar 40%, Douglas 37% e Carine 23% — vale conferir a regra no DKW; e Fernando, Luana, Jaqueline e cards sem dono não devem receber cliente novo do rodízio.

## 8. INFORMAÇÕES PARA O ORÇAMENTO

Não existe um padrão único: **cada categoria tem a sua especificidade**, e a forma de vender buquê e grama ainda está sendo desenvolvida. O que vale para todas:

- **Produto, quantidade, cidade, data.**
- **Retirar ou entregar.** Se for entrega: **o endereço** e **o que deve ser feito**.

Por categoria, o que já está definido:

| Categoria | O que perguntar |
|---|---|
| **Grama** | Variedade (ou onde vai plantar, para indicar), **metragem em m²**, cidade, data, retirada ou entrega. Na retirada, o veículo (ver seção 9) |
| **Buquês e flores** | Ocasião, modelo ou estilo (catálogo), cores, data, retirada ou entrega |
| **Frutíferas** | Espécie e variedade, quantidade, **plantio doméstico ou comercial** |
| **Demais** | Produto e quantidade; o vendedor detalha |

**Sugestão do Fernando:** analisar as conversas que os próprios vendedores já fizeram, por categoria, para descobrir as perguntas certas e melhorar o roteiro. A Portilho tem as conversas coletadas e pode fazer essa análise começando por buquê e grama.

## 9. REGRAS COMERCIAIS

Não haverá um documento de regras rígidas: prazos, pedido mínimo e condições **dependem do produto e da negociação**, e ficam com o vendedor. O que já está definido e a IA pode usar:

- **Horário** (a confirmar): segunda a sexta, 8h às 18h; sábado, 8h às 15h; domingo fechado. Retirada ou entrega fora do horário: combinar com o vendedor.
- **Entrega:** Irati e região (Fernandes Pinheiro, Rebouças, Imbituva, Teixeira Soares, Mallet, Prudentópolis, Rio Azul, Guamiranga, Inácio Martins, Palmeira, Ponta Grossa, Guarapuava, São João do Triunfo). **Grama vai mais longe — já foi vendida até para Curitiba.** O valor do frete é calculado pelo vendedor no orçamento. **Não há entrega por transportadora.** A IA não deve recusar cidade nenhuma: coleta o endereço e passa ao vendedor.
- **Preço da grama — a IA pode citar o "a partir de":** R$ 10,99/m² acima de 400 m²; R$ 9,99/m² acima de 1.000 m² (a confirmar se estes valores seguem vigentes). Os demais preços ficam com o vendedor.
- **Grama — dados técnicos:** cada m² pesa 20 a 25 kg; 4 blocos por m²; palete de 50 a 55 m²; conferência no carregamento. Capacidade por veículo: Gol 10 m² · Strada 30 m² · VUC/HR 70 m² · F4000 160 m² · Cargo 1319 350–400 m² · Cargo 2429 550 m² · Bitruck 760 m².
- **Citros:** só mudas certificadas e autorizadas para plantio no Paraná. Variedades não autorizadas (ex.: Laranja Champanhe, Açúcar, Bahia) não se vendem, encomendam nem indicam a terceiros.
- **Frutíferas para plantio comercial:** a IA encaminha o atendimento para o **Fernando**.
- **Buquês:** linhas simples, intermediário, luxo e personalizado; flores de Holambra; oferecer **galhos adicionais** (gipso, astromélia, lírios, rosas, girassol); no Mix Colorido, avisar que flores e cores variam conforme o dia; foto antes de finalizar, quando combinado.

## 10. O AGENTE DE IA

**Histórico.** A IA "Luna Verde" já funcionou no atendimento. Foi **desligada** porque começou uma série de mudanças no agente que exigia uma atenção que ninguém conseguiu dar, e o resultado frustrou. A decisão foi esperar alguém dedicado a ela — **é o seu papel agora.** Seguem dois prompts antigos e a planilha de perguntas e respostas como ponto de partida.

**Papel: SDR (pré-atendimento).** O desenho dos prompts antigos continua valendo na essência:

- **Faz:** acolhe, identifica o produto (inclusive por foto), coleta as informações da seção 8, responde dúvidas com a base de conhecimento, marca o card como QUALIFICADO e passa ao vendedor do rodízio.
- **Não faz:** não fecha venda, não negocia e não passa preço — **exceto o "a partir de" da grama**. Não pergunta o número de WhatsApp.
- **Chama uma pessoa quando:** o cliente pede, tem urgência, termina a qualificação, faz pergunta que não está na base, é atacado ou volume grande de grama, ou plantio comercial de frutíferas.
- **Tom:** curto, humano, uma pergunta por mensagem, sem repetir o que o cliente já disse.

**O que atualizar nos prompts antigos:**

| No prompt antigo | Como deve ficar |
|---|---|
| Flores → Jaqueline; grama e outros → Edimar | Transferir para o **rodízio atual** (Carine 40% · Douglas 40% · Edimar 20%) |
| Move o card para a coluna "ATENDIMENTO HUMANO" | Essa coluna não existe mais: mover para **Atendimento de Vendedores** |
| Horários de entrega de sábado até 18h e domingo até 12h; catálogo do Dia das Mulheres | Eram da campanha de março. Usar o horário da seção 9 e o catálogo vigente |
| Entrega só em Irati, Fernandes Pinheiro e Rebouças | Irati e região; grama vai mais longe; nunca recusar cidade |
| "Temos sim! … incluindo essa que você procurou" | **Nem negar nem confirmar estoque:** "vou verificar com o vendedor". Produto em falta é a 2ª maior causa de perda registrada — prometer e não ter gera frustração |
| Nunca falar preço | Pode citar o "a partir de" da grama |

**O que os dados dizem sobre onde a IA ajuda:** a primeira resposta ao cliente novo variou de 8 a 39 minutos de mediana nos últimos dias, e piora na segunda-feira e no horário das 13h. Mas **60% das perdas registradas são "o cliente parou de responder"** depois do vendedor mandar preço ou foto, e o follow-up quase não tem mensagem agendada. Ou seja: a IA resolve a entrada (responder em segundos, qualificar, classificar); a retomada depois do vendedor continua sendo o maior ponto de perda. O Fernando colocou exatamente essa pergunta — **o sucesso da IA deve ser medido pelo que acontece na fase do vendedor** (conversão e perdas "sem retorno", com e sem IA), não só pela velocidade.

**Sugestão de piloto de menor risco:** começar onde hoje ninguém atende — fora do expediente, sábado à tarde, domingo, Instagram e Messenger.

## 11. O QUE DEVE ACONTECER AUTOMATICAMENTE

- Nova negociação sempre que o cliente volta a escrever.
- Ao assumir a conversa, o vendedor assume também a negociação.
- Cancelar a mensagem agendada quando o cliente responde antes.
- Lembrete ou exigência de mensagem agendada ao entrar no Follow-up 1 e 2.
- Bloquear o arrasto para as colunas de encerramento (encerrar só pelo Ações, com valor e motivo).
- Tag automática de origem para Instagram e Facebook, com prioridade dentro da janela de 24 horas.
- Corrigir os loops da Raspinha e da avaliação do Google.
- Corrigir a automação 55993 (coluna inicial e venda ganha).

## 12. SISTEMAS E INTEGRAÇÕES

**SIGCLOUD (ERP)** — o principal. **A chave entre os dois sistemas é o telefone** (no online o cliente muitas vezes não passa CPF). O que se quer:

1. **Lista de preços do SIGCLOUD disponível para a IA consultar** — a empresa não tem tabela fora do ERP.
2. **Relatório de orçamentos e pedidos parados** no SIGCLOUD, com a justificativa do cancelamento (a mesma lógica do motivo da perda no CRM).
3. **Ligar os cadastros** para saber quem foi atendido no online e comprou no balcão — resolve o caso "o cliente não respondeu, mas veio e comprou", que hoje vira perda no CRM.
4. **Tags do CRM = categorias do SIGCLOUD.**

**Tintim** — origem do lead; o Fernando quer espelhar CRM × Tintim (alinhar com o Matheus).
**Power BI** — já conectado ao SIGCLOUD.

## 13. MATERIAIS

| Material | Situação |
|---|---|
| Planilha de perguntas e respostas da IA (geral, grama, buquês, frutíferas) | Existe — usar como base, com as correções deste documento |
| Dois prompts antigos da Luna Verde | Existem — ponto de partida (ver seção 10) |
| Catálogo de buquês (PDF) | Existe no Drive; conferir se é o vigente |
| Lista de preços | **Não existe fora do SIGCLOUD** — puxar pela integração |
| Fichas de pedras, terra, mudas ornamentais, palmeiras e paisagismo | **Não existem** — montar a partir da análise das conversas por categoria |

**A confirmar com o Fernando:** horário de funcionamento atual (encontramos versões diferentes); se o preço "a partir de" da grama segue vigente; se a Maria terá usuário próprio.
