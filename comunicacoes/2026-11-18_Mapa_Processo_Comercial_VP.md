# Mapa do processo comercial — Floricultura Verdes Plantas
### Versão 1 · definido na reunião de 18/11/2026 (Jhonatan × Fernando) · a validar com o Fernando

**Princípio da reunião:** primeiro o processo, depois o relatório. Cada etapa abaixo diz **quem faz, o quê, onde e como se prova que foi feito** — é esta última coluna que vira indicador no relatório e cobrança do Douglas.

Onde: **CRM** = DKW · **SIG** = SIGCLOUD.

---

## Etapa 1 — Entrada e qualificação

| # | Quem | O que | Onde | Como verificar |
|---|---|---|---|---|
| 1.1 | Agente de IA *(a configurar)* | Atende, chama o cliente pelo nome; se não tiver o nome, pede e **salva no cadastro** | CRM | Contato com nome (não só telefone) |
| 1.2 | Agente de IA *(a configurar)* | Identifica o grupo de produto e **sugere a tag** | CRM | Card com tag de tipo |
| 1.3 | Vendedor | **Revisa** nome e tag; aprofunda até o grupo de produto ("qual planta? para dentro de casa, presente ou pomar?") | CRM | Tag de tipo presente e coerente com a conversa |
| 1.4 | Sistema | Card chega ao vendedor já em **Atendimento de Vendedores** — o vendedor não precisa mudar coluna nessa passagem | CRM | Sem card parado no Atendimento Inicial |

Enquanto a IA não estiver ativa, o vendedor faz 1.1 e 1.2 (hoje ele faz o papel de SDR e de vendedor).

> A IA **não pode travar** a conversa se o cliente não disser o nome (ponto levantado pelo Fernando; é "como", fica para a configuração).

## Etapa 2 — Negociação

| # | Quem | O que | Onde | Como verificar |
|---|---|---|---|---|
| 2.1 | Vendedor | Aplica o processo da categoria: data, quantidade/metragem, se já tem cotação (tenta cobrir), retirada ou entrega, forma de pagamento | CRM | Leitura da conversa |
| 2.2 | Vendedor | Venda construtiva: indicar a variedade certa (ex.: grama ideal para o local); pedir foto do local quando cabe | CRM | Leitura da conversa |

Casos com foto/paisagismo: o Douglas já acompanha alguns clientes.

## Etapa 3A — Não fechou na hora → Follow-up (rotina de 1 minuto)

Ao terminar a conversa sem fechamento, **na mesma hora**, o vendedor:

| # | O que | Tipo | Como verificar |
|---|---|---|---|
| 3.1 | Confere o **nome** | confere | Contato com nome |
| 3.2 | Confere a **tag** | confere | Tag de tipo |
| 3.3 | Coloca o **valor aproximado** da negociação | faz | Card com valor |
| 3.4 | **Agenda a mensagem** para a data combinada | faz | Card com mensagem agendada |
| 3.5 | Escreve a **nota**: por que foi para o follow-up, o que o cliente quer, próximo passo | faz | Nota no card |
| 3.6 | Move para **Follow-up** | faz | Coluna Follow-up (movimento manual; o Ações não se aplica aqui) |

**Modelo de mensagem agendada (exemplo da grama):**
> "Oi, João, tudo bem? Bom dia. Aqui é o [vendedor], passando para saber da confirmação da metragem que você ficou de passar hoje. Estou aqui para te auxiliar e dar continuidade ao seu atendimento. Você confirmou se vão ser 50 ou 70 metros?"

Regra: **a mensagem sempre termina em pergunta.**

**Ligação também vira nota (proposta de 18/11, a confirmar com o Fernando).** Quando o vendedor liga para o cliente, registra na hora uma nota no card: *data, o que foi falado e próximo passo* (ex.: "18/11 — liguei, confirmou 70 m², retira sexta; agendei mensagem para quinta"). Motivo: **toda avaliação do atendimento lê a conversa do WhatsApp e as notas do card**. Ligação sem nota aparece como um buraco no atendimento — o vendedor vai ter que explicar depois, quando for perguntado. Anotar na hora leva um minuto e evita a explicação.

## Etapa 3B — Regra de destino de quem não responde (como o Fernando descreveu)

| Situação | Destino |
|---|---|
| Não respondeu **desde o início** — não se sabe o que quer | **Incógnita** |
| Começou a responder e **parou** | **Follow-up**, com as tentativas |
| Esgotou as tentativas e não respondeu | **Venda Perdida** |
| Já se sabe o produto (ex.: perguntou o preço, recebeu e parou) | **Não vai para Incógnita** → Follow-up e, sem retorno, Venda Perdida |

## Etapa 4 — Fechou → pedido, pagamento e financeiro

| # | Quem | O que | Onde | Como verificar |
|---|---|---|---|---|
| 4.1 | Vendedor | Confirma o valor (o estimado no follow-up) | CRM | Valor no card |
| 4.2 | Vendedor | Gera o **pedido** | SIG | Pedido no SIG *(depende do SIG)* |
| 4.3 | Vendedor | Envia ao cliente o **PDF do pedido** + **Pix** (mensagem pronta); no cartão, envia o **link** | CRM | PDF do pedido e chave Pix na conversa |
| 4.4 | Vendedor | Envia a mensagem pronta **"faça o pagamento e mande o comprovante para mim"** | CRM | Mensagem na conversa |
| 4.5 | Cliente | Envia o **comprovante ao vendedor** | CRM | Imagem/PDF do cliente depois do Pix |
| 4.6 | Vendedor | Com o comprovante: **Ações → Venda ganha** e **encerra a conversa** | CRM | Card em Venda Efetivada, com valor, conversa encerrada |
| 4.7 | Sistema *(a configurar)* | Automação em Venda ganha **envia a conversa ao setor financeiro (Maria)** | CRM | Conversa no setor financeiro |
| 4.8 | Maria | Abre o pedido e o comprovante juntos e **dá baixa** | SIG | Pedido baixado *(depende do SIG)* |

**Regras:**
- **Venda só é ganha com o comprovante.** Antes disso não se marca Venda ganha (era o erro: "acabei de vender", sem pagamento).
- Sem comprovante, o pagamento não chega ao caixa e a Maria precisa caçar no extrato quem pagou o quê.
- Motivo da venda ganha: **não precisa**.

**Grama (exceção de faturamento):** o pedido pode ser gerado numa semana e faturado só na retirada/entrega; a grama muitas vezes não está em estoque. Prática atual: **cobrar o valor integral; se o cliente não puder, cobrar parte como reserva**.

**Cliente que paga na loja:** o caixa rastreia o pedido no SIG e finaliza lá; **a conversa fica aberta no CRM**. A conversa já tem o pedido enviado — dá para ler a conversa e cruzar com o SIG para saber se foi pago.

---

## Em aberto (não definido na reunião)

1. **Expedição** — hoje a Maria faz caixa e expedição; o vendedor sai da mesa para buscar produto e mandar foto. Ideia: produto pré-separado ao confirmar a venda. Fica para outra reunião.
2. **Pós-venda** — não existe ação hoje.
3. **Cliente que para de responder** — proposta de coluna **"Sem resposta"** com follow-up automático (início e meio do dia) e saída só pelo Douglas, **ou** analisar as conversas que caem em Incógnita/Venda Perdida e classificar onde travou. **Decisão: testar primeiro a análise das conversas** com o que já existe.
4. **Ligações** — os vendedores às vezes ligam e hoje não fica registro. Proposta: **toda ligação vira nota no card** (ver Etapa 3A). Pergunta enviada ao Fernando no relatório de 18/11.
5. **Nome salvo pela IA** — hoje os contatos não são salvos com nome; nunca foi definido.
6. **Atendimento Inicial Meta × WhatsApp** — o Thiago criou duas colunas de entrada; deve ser **uma só**.
7. **Mensagens prontas** — cadastrar o Pix, o pedido de comprovante e o envio do PDF do pedido para não digitar toda vez.
8. **Regra única** do que se manda ao cliente no fechamento (hoje "não tem uma regra": às vezes PDF, às vezes só o valor e o Pix na conversa).
