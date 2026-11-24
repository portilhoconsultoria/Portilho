---
name: "prospeccao-linkedin"
description: "Prospecção da Portilho no LinkedIn com o Claude no Chrome: qualifica quem comentou nos posts do Jhonatan ou busca decisores novos (perfil de cliente igual ao do DKW/WVI), devolve tabela com nota e gancho, escreve rascunhos de convite e manda os leads aprovados para a etapa \"Claude\" do pipeline Prospecção no DKW, onde a régua de WhatsApp já existente assume. Use SEMPRE que Jhonatan mencionar \"prospecção no LinkedIn\", \"LinkedIn\", \"qualificar quem comentou\", \"leads do LinkedIn\", \"comentou CLIENTE\", \"buscar decisores\", \"Sales Navigator\", \"convite de conexão\", ou pedir para levar leads do LinkedIn para o DKW. NÃO use para a captura do Google Maps/Apify (skill `prospeccao`) nem para a régua de WhatsApp em si."
---

# Prospecção LinkedIn → DKW

> Fonte do método: guia "Prospecção no LinkedIn com o Claude" (Bruna Santanna, nov/2026),
> adaptado à operação da Portilho. Criada em 24/11/2026.

Duas metades, com um portão humano no meio:

1. **LinkedIn (Claude no Chrome, aba logada do Jhonatan):** ler perfis, dar nota, achar gancho, rascunhar convite.
   **Só lê. Nunca conecta, curte, segue, comenta nem manda mensagem.**
2. **DKW (script `scripts/linkedin_para_dkw.py`):** os leads que o Jhonatan aprovou e que têm
   WhatsApp viram card na etapa `Claude` do pipeline `Prospecção`. A cota das 09:05 e a régua
   de 5 toques fazem o resto — **nada novo no DKW, nenhuma automação nova.**

## 🔒 Travas (não negociáveis)

- **O LinkedIn proíbe automação e raspagem** e pode restringir a conta. A conta é a pessoal do
  Jhonatan, o ativo mais caro do comercial. Por isso: **modo "Manually approve"** na extensão,
  **no máximo 15 perfis por rodada**, **no máximo 2 rodadas por dia**, Jhonatan na frente da tela.
- **Nenhum envio no LinkedIn sai do Claude.** Rascunho aparece no painel; quem cola e envia é ele,
  um por vez.
- **Não montar base.** A tabela é da rodada. Não guardar perfis que não viraram lead aprovado.
- **Nota do Claude é palpite.** Nada vai ao DKW sem o Jhonatan aprovar a lista (portão humano).
- **Script do DKW roda em modo seco por padrão.** `--executar` só depois de ele ver o relatório seco.

## Pré-requisitos

- Claude **desktop/Chrome** com a extensão Claude in Chrome (plano pago) — esta skill **não roda
  em sessão de nuvem**: lá não há LinkedIn logado. Se estiver na nuvem, diga isso e pare na parte 1.
- LinkedIn logado na aba. Extensão em **Manually approve**.
- Para a parte 2: chave da API oficial do DKW na variável `DKW_API_KEY` (a mesma do Railway;
  na máquina dele está no `.env` do `D:\portilho-agente`). **Nunca colar a chave no chat nem em arquivo versionado.**

## Passo 1 — Contexto do negócio (colar antes de toda missão)

Perfil de cliente = **o mesmo da prospecção do DKW** (WhatsApp Vendedor Inteligente — WVI):

```
Antes da missão, o contexto do meu negócio:
1. O que eu vendo: o WhatsApp Vendedor Inteligente — uma estrutura (CRM + IA + régua de mensagens)
   que faz a empresa voltar a vender para a carteira de clientes que já compraram e sumiram.
   Quem fecha a venda continua sendo o dono ou a equipe dele.
2. Para quem: dono, sócio ou gestor comercial de pequena e média empresa (até ~50 pessoas) que
   vende e atende pelo WhatsApp e tem recompra — serviços, estética, saúde privada, academias,
   pet, turismo, imobiliárias, autopeças/oficinas, varejo local, eventos, educação livre. Brasil.
3. O problema que eu resolvo: dinheiro parado na carteira — o cliente que já comprou só volta se
   alguém chamar, e ninguém chama; o WhatsApp vira balcão de atendimento, não de venda.
4. Quem NÃO é meu cliente: empresa que já tem IA/chatbot próprio de atendimento; grandes empresas
   e multinacionais; franquia sem autonomia comercial; quem vende só B2B enterprise com ciclo longo;
   consultores e agências de marketing/automação (concorrentes); estudantes e quem busca emprego;
   funcionário sem poder de decisão.
5. Sinais de que a pessoa está pronta: posta sobre vendas, atendimento, WhatsApp, fidelização ou
   cliente que some; empresa contratando atendente, vendedor ou SDR; reclama de equipe
   sobrecarregada; abriu filial ou mudou de cargo recentemente; operação de 1–2 pessoas
   atendendo muito volume.
Se faltar alguma informação para você julgar quem é lead, me faça todas as perguntas que precisar,
de uma vez só, numeradas, antes de começar.
```

## Passo 2 — Escolher a missão

### 2A. Leads quentes — quem comentou num post dele (comece por aqui)

Abrir o post com mais comentários e colar:

```
Use o contexto do meu negócio que eu mandei acima.
Neste post aberto na aba, leia quem comentou. Abra o perfil de cada pessoa, um por vez, com calma,
e olhe cargo, empresa e os últimos posts dela. Pare em 15 perfis.
Me entregue uma tabela com: nome, cargo, empresa, cidade, link do perfil, nota de 0 a 10 de quanto
a pessoa tem cara de cliente, o motivo da nota em uma linha e o gancho (o assunto concreto de um
post ou fato dela que serve para abrir conversa).
Ordene da nota mais alta para a mais baixa. Não curta, não comente, não siga e não mande mensagem
para ninguém. Só leia e me devolva a tabela.
```

### 2B. Leads novos — busca de pessoas

Preencher cargo/setor/região (ex.: "proprietário" + "clínica de estética" + "Curitiba"):

```
Use o contexto do meu negócio que eu mandei acima.
Na busca de pessoas do LinkedIn, procure [cargo] de empresas de [setor] em [cidade/estado].
Abra os perfis um por vez, olhe cargo, empresa e o que cada pessoa posta, e pare em 15 perfis.
Me entregue uma tabela com: nome, cargo, empresa, cidade, link do perfil, se a pessoa posta com
frequência (sim ou não), nota de 0 a 10, o motivo da nota em uma linha e o gancho.
Separe no fim os 5 melhores e diga qual assunto dos posts de cada um serve de gancho para uma
conversa. Não conecte, não siga e não mande mensagem para ninguém.
```

✅ Toda missão tem **escopo, limite e trava**. "Acha clientes pra mim" não é missão.

## Passo 3 — Rascunho do convite (LinkedIn)

```
Para cada um dos [N] melhores da tabela, escreva uma nota de convite de conexão de no máximo
4 linhas (até 300 caracteres):
1. Uma frase citando algo concreto que a pessoa postou ou fez.
2. Uma frase ligando isso a clientes que já compraram e não voltam / vendas pelo WhatsApp.
3. Uma pergunta no fim que dê vontade de responder.
Sem "espero que esteja bem", sem pitch, sem link, sem adjetivo sobre mim, tom de dono para dono.
Me mostre todas aqui no painel. Não envie nenhuma.
```

Jhonatan revisa, ajusta e envia **à mão**.

## Passo 4 — Achar o WhatsApp (só dos aprovados, nota ≥ 7)

A régua do DKW é **WhatsApp**: sem número, não há card. Ordem de busca, parando no primeiro achado:

1. "Informações de contato" do perfil (só aparece para conexão de 1º grau).
2. Site da empresa: link `wa.me`/`api.whatsapp.com`, botão de WhatsApp, rodapé, "fale conosco".
3. Ficha da empresa no Google Maps.
4. Instagram da empresa (link da bio).

Anotar **de onde veio** (`fonte_telefone`). Telefone **fixo não serve** (a captura também descarta).
Número de central/SAC de empresa grande = sinal de que não é ICP. **Não inventar nem deduzir número.**
Quem ficou sem WhatsApp segue só no LinkedIn (convite manual) e **não** vai ao DKW.

## Passo 5 — Portão humano + lote

Mostrar ao Jhonatan a lista final (nome, empresa, telefone, fonte, nota, gancho) e **esperar o ok**.
Aprovado, salvar o lote em `linkedin_lote_AAAA-MM-DD.json` (pasta de trabalho, fora do git):

```json
[
  {"nome": "Ana Souza", "cargo": "Sócia", "empresa": "Clínica X", "cidade": "Curitiba/PR",
   "linkedin": "https://www.linkedin.com/in/...", "telefone": "41 99999-9999",
   "fonte_telefone": "site", "nota": 8, "motivo": "posta sobre retorno de pacientes",
   "gancho": "post de 12/11 sobre pacientes que somem após a 1ª sessão",
   "missao": "comentou post 20/11"}
]
```

## Passo 6 — Mandar para o DKW

```
python scripts/linkedin_para_dkw.py linkedin_lote_AAAA-MM-DD.json            # seco: só relata
python scripts/linkedin_para_dkw.py linkedin_lote_AAAA-MM-DD.json --executar --limite 1   # 1º card
python scripts/linkedin_para_dkw.py linkedin_lote_AAAA-MM-DD.json --executar  # resto
```

O script, por lead: normaliza o número para `55DDD9NNNNNNNN` → barra fixo, nota < 7 e duplicado no
lote → **consulta o DKW e pula quem já é contato** (lead conhecido não volta para o início da
régua) → `POST /commercial-order` na etapa `Claude` → tag `origem_linkedin` no contato →
nota no contato com cargo, link do LinkedIn, gancho e fonte do telefone.

**Depois do 1º card (`--limite 1`), conferir na tela do DKW** (gestao.portilhoconsultoria.com.br):
card em `Claude`, **nome do contato preenchido** (o M1 começa por ele), tag e nota presentes. Só
então rodar o resto. Se o nome vier vazio ou a nota falhar, parar e ajustar o script — não
compensar na mão card a card.

## O que acontece depois (já existe, não mexer)

`Claude` → cota das **09:05** (20/dia, FIFO — **o lote do LinkedIn entra na fila atrás da captura
do Maps**) → `Disparados` → M1 + toques 2–5 → triador → Clara. Ver skill `prospeccao`.

⚠️ **Tradeoff assumido:** o M1 do WhatsApp é o texto padrão da régua; o gancho personalizado vive
no convite do LinkedIn e na nota do card (para quem atender ler). Se os leads do LinkedIn
converterem melhor, o próximo passo é uma etapa própria com M1 que use o gancho — decisão dele,
medida depois de ~30 cards.

⚠️ **Tag via API não dispara fluxo do DKW** (lei medida 16/10). `origem_linkedin` é só rótulo para
medir resultado por origem — não usar como gatilho.

## Medir (a cada 30 cards de origem LinkedIn)

Taxa de resposta no WhatsApp e taxa de reunião de `origem_linkedin` contra a captura do Maps, e
taxa de aceite do convite no LinkedIn. Se não superar o Maps, o LinkedIn fica só para os quentes (2A).
