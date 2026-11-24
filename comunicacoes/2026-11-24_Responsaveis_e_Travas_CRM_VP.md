# CRM da Verdes Plantas — quem responde pelo quê e quais travas
### Rascunho v1 · 24/11/2026 · para o Jhonatan revisar (base: reunião de 18/11, grupo "CRM - Verdes Plantas", briefing de 11/11)

**Por que este documento existe.** Na reunião de 18/11 o Fernando pediu: *"desenhar esses caminhos, como serão feitos, quem é responsável, criar as travas — porque senão a gente se perde."* Hoje uma mudança no CRM pode nascer de qualquer um (Fernando, Thiago, Lu, um vendedor), ser feita sem registro e só ser descoberta quando um número muda no relatório. Exemplos de novembro: a coluna "Atendimento Inicial (Meta)" criada sem decisão; o rodízio configurado diferente da regra escrita; a automação de reaproveitar card desligada sem substituto, deixando cliente que volta sem negociação.

---

## 1. Os papéis

| Papel | Quem | Faz | Não faz |
|---|---|---|---|
| **Aprova** | Fernando | Decide regra comercial e prioridade; aprova toda mudança de configuração antes de ir para o sistema | Não configura nem pede direto ao vendedor para "dar um jeito" no CRM |
| **Pede** | Douglas (coordenador) | Leva as necessidades da operação, com caso e telefone; confirma no dia seguinte se a mudança resolveu | Não altera configuração |
| **Especifica e verifica** | Portilho | Escreve a regra em formato que o sistema execute; mede pelo relatório se a mudança fez efeito | Não configura no ambiente da Verdes (só leitura) |
| **Configura** | Thiago | Executa no DKW o que foi aprovado, com data, e registra o que fez | Não muda regra comercial por conta própria; não liga nem desliga automação sem registro |
| **Canais** | *a definir pelo Fernando* | Responde pelo Instagram, Facebook/Messenger e perfil do Google (senhas, conexão, administração) | — |

> A pendência do responsável pelos canais está em aberto desde a reunião de 12/11 e o plano de 3 meses também a cobra. Enquanto não houver nome, o erro do Instagram continua sem dono.

## 2. O caminho de uma mudança

1. **Pedido** no grupo "CRM - Verdes Plantas", numerado: *"Pedido 12 — [o que] — [caso de exemplo com telefone] — [quem pediu]"*.
2. **Especificação** pela Portilho em até 1 dia útil: regra, coluna ou automação afetada, como vamos saber que funcionou.
3. **Aprovação** do Fernando no próprio grupo ("aprovado 12").
4. **Configuração** pelo Thiago, com data de entrega combinada no pedido.
5. **Registro** no grupo: *"Pedido 12 feito em DD/MM — o que mudou"*. Sem esse registro, a mudança é tratada como não feita.
6. **Verificação** no relatório dos dias seguintes (coluna, automação, rodízio). Se o número não mudar, o pedido volta aberto.

**Mudança de regra comercial** (rodízio, destino da Incógnita, prazo de follow-up) só entra na **reunião semanal do comercial**, nunca no meio da semana. Correção de erro (automação parada, canal desconectado) segue o caminho acima a qualquer momento.

## 3. Mapa de responsáveis por área do CRM

| Área | Aprova | Configura | Hoje | Pendência |
|---|---|---|---|---|
| Funil e colunas | Fernando | Thiago | 9 colunas (a "Meta" sobrando) | Voltar a uma coluna de entrada; origem do lead por tag, não por coluna |
| Rodízio e filas | Fernando | Thiago | Diferente da regra de 12/11 | Jaqueline 40 · Carine 40 · Edimar 20, Douglas fora |
| Automações de coluna | Fernando | Thiago | 55993 sem disparo; Raspinha e avaliação do Google com erro | Lista única de automações ativas, com dono e data da última revisão |
| Tags | Fernando (lista de categorias) | Thiago | Tags novas aparecendo sem decisão (ALEATORIO, VAI PASSAR NA LOJA…) | Lista oficial = categorias do SIGCLOUD; criar tag só por pedido |
| Mensagens prontas | Fernando | Thiago | Faltam Pix, "mande o comprovante" e PDF do pedido | Item 2 da mensagem de 18/11 |
| Agente de IA | Fernando | Thiago | Em teste, fora do ar | Nome, sugestão de tag, transferência ao rodízio vigente |
| Usuários e permissões | Fernando | Thiago | Todos estavam como administrador | Vendedor sem permissão de configuração; Jaqueline com o próprio nome |
| Canais (WhatsApp, Instagram, Messenger, Google) | Fernando | Responsável pelos canais + Thiago | Instagram com erro | Nomear o responsável |
| Integrações (Tintim, SIGCLOUD, n8n) | Fernando | Thiago | SIG adiado | Prioridade só depois dos itens do sistema |
| Relatórios | Fernando (o que quer) | Portilho | Diário e semanal | Duas camadas (coordenação e gerência) |

## 4. Travas

**No sistema** (o DKW impede, ninguém precisa lembrar):

| # | Trava | Por quê | Situação |
|---|---|---|---|
| 1 | Coluna de encerramento só pelo botão Ações (bloquear arrasto) | Arrastado não conta e não leva motivo | Proposta desde 20/10; não implementada |
| 2 | Não sair do Atendimento Inicial sem tag de tipo | Tag é a base da conversão por categoria | Proposta; não implementada |
| 3 | Não encerrar conversa com o cliente como último a falar | Cliente deixado sem resposta | Recomendada; verificar se o DKW permite |
| 4 | Card em Follow-up exige mensagem agendada | Regra de 10/11 | Perguntar ao suporte do DKW |
| 5 | Venda ganha exige valor | Já funciona pelo Ações | Ativa |
| 6 | Cliente que volta gera negociação nova | Hoje fica "perdido no meio" | Pendente desde 14/11 |
| 7 | Vendedor sem perfil de administrador | Evita mudança acidental de configuração | Pendente |

**No processo** (quando o sistema não consegue travar):

- Mudança sem pedido numerado e sem registro no grupo = não aprovada; o relatório aponta e a configuração volta.
- Toda automação ligada ou desligada entra no registro, com o motivo.
- O relatório de coordenação lista o que a trava não pegou (encerrado com o cliente por último, arrastado, sem tag) — é a rede de segurança enquanto a trava do sistema não existe.

## 5. Para decidir

1. Fernando confirma que **nada é configurado sem o "aprovado" dele no grupo**?
2. **Quem responde pelos canais** (Instagram, Messenger, Google)?
3. Regra de mudança comercial **só na reunião semanal** — vale a partir de quando?
4. O registro de pedidos fica **no grupo** (simples) ou numa lista/planilha (mais organizado, mais um lugar para olhar)? Proposta: no grupo, com número.
