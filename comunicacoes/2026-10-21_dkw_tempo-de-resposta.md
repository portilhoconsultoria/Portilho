Assunto: Relatórios › Conversas — "Tempo de resposta" exibido em minutos, mas calculado em segundos (e outros 4 pontos)

Olá, equipe DKW, tudo bem?

Sou o Jhonatan, da Portilho Consultoria (conta Portilho Gestão Comercial Inteligente). Acompanho o
atendimento comercial de um cliente nosso na plataforma: Floricultura Verdes Plantas Ltda, companyId 7078.
Ao montar o relatório diário de atendimento dele, encontramos inconsistências no indicador
"Tempo de resposta". Seguem os detalhes para vocês reproduzirem.

1) Unidade errada no card "Tempo de resposta" (o mais grave)
- Onde: Relatórios › Métricas = "Conversas" › card "Tempo de resposta".
- Período: 01/10/2026 a 21/10/2026, sem filtros.
- O card mostra: "298 minutos".
- A tela busca GET /dashboard/chats?timezone=UTC&date_from=2026-10-01&date_to=2026-10-21. A resposta traz
  o campo responseTime por dia, e a própria documentação da API (Automações › API › Dashboard ›
  Métricas de Conversas) o descreve como "Tempo médio de resposta em segundos".
- A média simples dos 21 valores diários de responseTime é 297,6. O card arredonda para 298 e
  rotula como minutos. O valor correto é ≈ 298 segundos (≈ 5 minutos). Hoje o card superestima o
  tempo em 60 vezes.
- Também vale avaliar: o card faz a média simples das médias diárias. Ponderado pelo número de
  conversas respondidas em cada dia, o resultado seria 255,8 s.

2) Respostas automáticas entram na média
- O tooltip diz que o indicador mede "o tempo que uma conversa aguardou uma mensagem enviada por uma
  conexão da plataforma". Na prática, mensagens automáticas (boas-vindas, "enquanto aguarda seu
  atendimento", pesquisa de avaliação) contam como resposta.
- Exemplo: em 21/10, às 01:00, há um responseTime de 0,02 s atribuído a um vendedor
  (/dashboard/chats com userIds=12198). Ninguém estava trabalhando nesse horário.
- Pedido: um filtro ou um indicador separado que considere só mensagens enviadas por usuário
  humano (mensagem com userId preenchido). É isso que o gestor precisa acompanhar.

3) Gráfico "Visão geral" deslocado em um dia
- Com timezone=UTC, cada ponto da série vem com "date" = fim do dia UTC em horário de Brasília
  (ex.: label "2026-10-04", date "2026-10-04T21:00:00-03:00"). O gráfico plota pelo "date" e
  exibe o ponto no dia seguinte.
- Exemplo: os domingos (04, 11 e 18/10, quase sem conversas) aparecem nas segundas-feiras do eixo.
- Além disso, com o período padrão terminando em "hoje" (date_to = data de hoje), o dia de hoje não
  aparece na série.

4) Agregação por vendedor não fecha
- Com userIds=15948 e período de um dia (21/10), o balde das 12:00 traz responseTime 131 s com
  totalChatsWithResponse = 0.
- O valor diário desse vendedor (38,5 s) não corresponde à ponderação dos baldes horários (≈ 1,7 s).
- Pergunta: qual é a fórmula do responseTime? Primeira resposta da conversa ou toda resposta? Média
  por conversa ou por mensagem? Qual o tratamento de conversas sem resposta?

5) Documentação da API diferente da rota usada pela tela
- A documentação (v1.0.0) pede date_from/date_to em d/m/Y. A tela usa Y-m-d.
- A tela envia userIds e timezone, que não estão documentados.
- A resposta traz totalChatsClosed e waitingChats, que também não estão no schema.
- Pedido: documentar userIds (filtro por atendente) na API pública com api-key, e publicar a
  definição exata do responseTime.

Prioridade: os itens 1 e 2. Com eles, o gestor da loja hoje lê "298 minutos" de tempo de
resposta, quando o número real é perto de 5 minutos e ainda inclui mensagens automáticas.

Posso enviar prints e o JSON das respostas, se ajudar. Fico à disposição para uma chamada rápida.

Obrigado!
Jhonatan Portilho
Portilho Consultoria
