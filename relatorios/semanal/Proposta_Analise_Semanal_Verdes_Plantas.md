# Proposta de análise semanal do comercial
### Floricultura Verdes Plantas · desenho do método, dos agentes e do ritual · versão 1 · 27/10/2026

O relatório diário mostra o que aconteceu. A análise semanal tem outro trabalho: **separar sinal de ruído e transformar sinal em decisão do dono.** Os números diários oscilam muito — a primeira resposta da equipe foi 12 → 26 → 8 → 13 min em quatro dias úteis; os atendimentos novos, 29 → 8 → 19. Reagir a cada oscilação é o erro que a literatura de controle de processo chama de "mexer no processo estável", e que aumenta a variação em vez de reduzir.

Esta proposta junta o que sete agentes de pesquisa levantaram (um por indicador, mais um de método e um de novas análises) e desenha a rotina.

## 1. PRINCÍPIOS

1. **Igual toda semana.** Mesmo formato, mesma ordem, mesmas definições. Mudou a regra (uma tag nova, uma automação nova) → marca-se uma "nova fase" no gráfico, não se compara como se nada tivesse mudado.
2. **Mediana e P90, nunca média**, para tempo. Proporção com numerador e denominador à vista.
3. **Sinal antes de comentário.** Indicador dentro do ruído vira uma linha ("estável"). Texto só onde há sinal.
4. **Inputs antes de outputs.** O que a equipe controla (responder, agendar, classificar, encerrar certo) vem primeiro; vendas e conversão são consequência.
5. **Sistema antes de pessoa.** Se o desvio é geral, a suspeita é processo ou automação (ex.: a mensagem automática que empurra venda para a Incógnita). Se é de uma pessoa só, conversa individual — nunca ranking público.
6. **No máximo 3 decisões por semana**, cada uma com dono e data, conferidas no relatório seguinte.

## 2. O RITUAL

| Quando | O quê | Quem |
|---|---|---|
| Segunda, até 8h | Agentes rodam sobre a semana fechada (seg–sáb) e o orquestrador monta o relatório | automático |
| Segunda, manhã | Dono lê sozinho (5 min): cabeçalho + decisões pedidas | Fernando |
| Segunda, 15–20 min | Reunião curta: aprovar até 3 decisões, com dono e prazo | Fernando + consultor (+ líder comercial, se houver) |
| Durante a semana | Feedback individual, em conversa a dois | Fernando / líder |
| Segunda seguinte | Seção "decisões anteriores": a mudança produziu efeito? | orquestrador |

O relatório diário continua como está; o semanal não o substitui.

## 3. A ARQUITETURA: UM AGENTE POR INDICADOR + UM ORQUESTRADOR

| # | Agente | Pergunta que responde | Tipo | Já medimos? |
|---|---|---|---|---|
| A1 | Tempo de resposta | A espera do cliente mudou de verdade? Onde está a cauda? | input | sim (diário) |
| A2 | Qualidade do encerramento | O dado da semana é confiável? Onde o processo induz o contorno? | input | sim (diário) |
| A3 | Follow-up e estoque parado | O estoque está crescendo? Quem tem follow-up sem data? | input | sim (diário) |
| A4 | Classificação por tag | Sabemos o que o cliente pede? O mix bate com o estoque e a campanha? | input | sim (diário) |
| A5 | Carga e distribuição | Quem está acima da capacidade? A demora é carga ou disciplina? | sistema | parcial |
| A6 | Coorte e funil | O que aconteceu com os clientes que chegaram na semana? | output | **novo** |
| A7 | Demanda não atendida ("não temos") | O que os clientes pediram e a loja não tinha? | output | **novo** |
| A8 | Motivo de perda real × marcado | Por que perdemos, segundo a conversa? | output | **novo** |
| A9 | Comportamentos da conversa | O que os atendimentos ganhos fazem diferente? | aprendizado | **novo** |
| A10 | Experimentos de processo | A mudança que fizemos funcionou? | aprendizado | **novo** |
| O | Orquestrador estatístico | Isto é sinal ou ruído? Que decisão pedir ao dono? | — | — |

Cada agente entrega ao orquestrador uma série padronizada por semana: indicador, valor, numerador, denominador, vendedor, tipo (input/output) e direção desejada.

## 4. OS AGENTES DE INDICADOR

### A1 · Tempo de resposta

| Métrica | Definição | Alerta |
|---|---|---|
| 1ª resposta — mediana e P90 | do 1º texto do cliente novo à 1ª mensagem de vendedor humano, em minutos úteis (seg–sex 8h–18h) | sinal no gráfico XmR |
| % dentro da meta | % de clientes novos respondidos em até 4 min, e em até 30 min, contando os sem resposta no denominador | queda além do limite do gráfico p |
| Sem resposta | clientes que ficaram sem resposta, com o tempo útil em aberto | qualquer espera acima de 1 dia útil vai para a lista nominal |
| Mapa de calor | mediana da 1ª resposta por dia × faixa horária | faixa com P90 acima de 60 min por 3 semanas |
| 1ª resposta × resultado | conversão por faixa de espera, acumulada em 8–12 semanas | só como pergunta, nunca como alerta |

**Limites.** Abaixo de ~20 clientes novos por vendedor na semana, não ordenar vendedores; mostrar faixa e acumular 4 semanas. P90 com menos de 30 casos é instável. Para evitar a "resposta vazia" (o "oi, já te atendo" que só para o relógio), medir também o tempo até a primeira resposta com conteúdo (preço, foto ou mais de N caracteres).

### A2 · Qualidade do encerramento

| Métrica | Definição | Alerta |
|---|---|---|
| Conformidade | encerramentos pelo Ações ÷ total de encerramentos | ponto abaixo do limite do gráfico p, ou < 90% por 2 semanas |
| Taxa de Incógnita | encerramentos na Incógnita ÷ total | vendedor acima de 2× a média da equipe |
| Vendas escondidas | cards da Incógnita com nota de venda ("comprou", "vem buscar", "pagou") | qualquer caso, até a automação ser corrigida |
| Perdas com motivo válido | perdas com motivo preenchido, diferente de "outros" e com 10+ caracteres ÷ perdas | < 80% |
| Pareto de motivos | motivos de perda codificados numa lista fechada, 4 semanas móveis | categoria nova no top 3; "preço" acima de 40% sem evidência na conversa |
| Custo do registro | conversão calculada de duas formas: sem a Incógnita e tratando a Incógnita com nota de venda como venda | a diferença entre as duas é o tamanho do problema |

**Limites.** Não afirma venda sem evidência no texto; sorteia 10 cards por semana para conferência humana (o método "Friday Afternoon Measurement" de Redman).

### A3 · Follow-up, cadência e estoque parado

| Métrica | Definição | Alerta |
|---|---|---|
| Cobertura de agendamento | cards em Follow-up 1 e 2 com mensagem agendada para o futuro ÷ cards em Follow-up | < 80% (hoje ~5–10%) |
| Agendamentos vencidos | agendamentos com data passada e não enviados | > 0 |
| Notas com data | notas da semana com data de retorno ÷ notas da semana | < 80% |
| Dias sem toque | agora − última mensagem do vendedor ou último agendamento enviado (nota e arrasto de coluna não contam) | mais de 7 dias sem toque e sem agendamento = "dormindo" |
| Idade na coluna | tempo desde a última movimentação, comparado ao P50/P85 de quem já fechou | Atendimento > 2 dias; Follow-up > P85 |
| Fluxo | estoque por coluna no sábado; entradas (cards criados); saídas (encerramentos); tempo implícito = estoque ÷ saídas (Lei de Little) | entradas > saídas por 3 semanas seguidas |

**Achado-chave da pesquisa.** Compromisso com **data e hora** funciona melhor que com data só (Milkman et al., 2011), e lembrete por mensagem reduz falta a compromisso (revisão Cochrane, Gurol-Urganci et al., 2013). Isso sustenta a regra do dono: follow-up com mensagem agendada, nota com data.

**Lista de ação.** O agente classifica os cards dormindo em três grupos: reativar (interesse registrado, menos de 30 dias); último toque de despedida (30–60 dias); propor encerramento. **Ele só propõe; não move card.**

### A4 · Classificação por tag

| Métrica | Definição | Alerta |
|---|---|---|
| Cobertura | cards novos com tag de tipo em até 24 h ÷ cards novos | < 80%, ou queda de 10 p.p. contra a média de 4 semanas |
| Tempo até a tag | mediana entre a criação do card e a primeira tag de tipo | > 4 h |
| Concordância | kappa entre a tag do vendedor e a de um auditor (ou do LLM validado), em amostra de 30–50 cards | κ < 0,60 |
| Mix de demanda | participação de cada tipo nos atendimentos novos | variação atípica contra 8 semanas e contra o mesmo período do ano anterior |
| Conversão e ticket por tipo | ganhos ÷ encerrados da coorte, por tipo, com intervalo | só alertar com n ≥ 20 |

**Ajustes de desenho recomendados.** (1) Separar três dimensões que hoje disputam o mesmo campo: tipo de produto, etapa de processo (ORÇAMENTO, QUALIFICADO) e campanha (FINADOS 2025). (2) Criar PAISAGISMO e OUTROS. (3) Regra de desempate: "tag principal = primeira demanda explícita do cliente". (4) Avaliar 4–5 grupos maiores (Presentes e datas · Plantas · Insumos · Serviços) com subtags.

**Papel do LLM.** Sugerir a tag a partir das primeiras mensagens do cliente (sem nome e telefone), com trecho que justifica e nível de confiança. Antes de usar: o dono rotula 150–200 cards às cegas; o LLM só vira auditor se a concordância for κ ≥ 0,75. A tag inferida entra no mix, mas não conta na cobertura do vendedor.

### A5 · Carga e distribuição

| Métrica | Definição | Alerta |
|---|---|---|
| Carteira ativa | cards abertos por vendedor no sábado, por coluna | > 1,5× a mediana da equipe |
| Conversas ativas | cards com mensagem do cliente nas últimas 48 h | acima do teto calibrado do vendedor |
| Concentração (HHI) | soma dos quadrados das participações na carteira (4 vendedores iguais = 0,25) | > 0,35 |
| Carga × 1ª resposta | gráfico semanal por vendedor | o "joelho": a carga a partir da qual a resposta piora |
| Conversão ajustada | conversão "encolhida" para a média da equipe (Bayes empírico), com intervalo | só sinalizar se o intervalo não cruzar a média |

**Achado-chave.** Carga alta por muito tempo piora velocidade e qualidade (KC & Terwiesch, 2009), e o vendedor sobrecarregado para de vender e passa a só despachar (Tan & Netessine, 2014). Pela teoria de filas, a espera cresce rápido quando a ocupação passa de 80–85%, e a distribuição em lote piora a espera. **Implicação:** a primeira resposta lenta do Edimar pode ser efeito da carteira (52% dos cards ativos), não da pessoa.

**Proposta de regra.** Distribuição alternada (rodízio) ponderada pela capacidade livre, com teto por vendedor, sem lotes, e transbordo para o Fernando quando todos estiverem no teto. Testar por 2–4 semanas antes de concluir.

## 5. O ORQUESTRADOR ESTATÍSTICO

1. **Agrega** o diário em semanal: tempo pela mediana e P90; contagem por soma; proporção por numerador ÷ denominador.
2. **Escolhe o gráfico** pelo tipo de dado: contagem → XmR; proporção → gráfico p com limites que se alargam quando o n é pequeno; tempo → XmR sobre a mediana semanal.
3. **Respeita a fase**: menos de 6 semanas de histórico → só gráfico de sequência e a frase "linha de base em formação", **sem alarme**; 6 a 19 semanas → limites provisórios; 20+ → limites fixos, recalculados só depois de uma mudança deliberada.
4. **Usa só três regras de sinal**: (R1) ponto fora dos limites; (R2) 8 semanas seguidas do mesmo lado da linha central; (R3) 3 de 4 semanas mais perto de um limite que do centro. Somar todas as regras clássicas em 10 indicadores gera alarme falso quase toda semana.
5. **Protege contra n pequeno**: proporção por vendedor só com 10–15 casos na semana; abaixo disso, junta 2 semanas. Sinal de vendedor precisa se confirmar na semana seguinte antes de virar recomendação de treinamento.
6. **Explica com contexto**: cruza o sinal com o que se sabe da semana (feriado, folga, campanha, mudança de automação).
7. **Traduz sinal em decisão** por uma tabela fixa — ex.: 1ª resposta alta só num vendedor + carga alta → redistribuir; follow-up sem agendamento em todos → revisar o processo ou a ferramenta; Incógnita com vendas → corrigir a automação.

**Formato da saída (uma página):** cabeçalho ("semana estável" ou "N sinais" + até 3 decisões pedidas) → painel de inputs em pequenos gráficos lado a lado (12 semanas cada) → painel de outputs → por vendedor, só sinais, em tom de tarefa ("7 follow-ups sem agendamento"), nunca de pessoa → sinais e hipóteses → decisões anteriores.

**Por que esse cuidado com o tom.** Na maior meta-análise sobre feedback (Kluger & DeNisi, 1996, 607 efeitos), mais de um terço das intervenções **piorou** o desempenho — sobretudo quando o feedback desviou a atenção da tarefa para a pessoa. O feedback funciona melhor quando vem do supervisor, com meta explícita, com regularidade e com ação concreta sugerida (Ivers et al., Cochrane 2012; Brehaut et al., 2016).

## 6. AS NOVAS ANÁLISES

| # | Agente | O que entrega | Esforço | Valor |
|---|---|---|---|---|
| A6 | Coorte e funil | dos clientes que chegaram na semana: % venda, perda, Incógnita e ainda aberto em 7/14/30 dias; tempo até a venda; reativação (RFM) | baixo | médio-alto |
| A7 | Demanda não atendida | ranking dos produtos pedidos que a loja não tinha ("não temos", "acabou"), com valor perdido estimado e aceitação de substituto → lista de compras | baixo | alto |
| A8 | Motivo de perda real | motivo segundo a conversa (preço, frete, sem estoque, sumiu, comprou fora, demora nossa...) × motivo marcado, com trecho que comprova | baixo-médio | alto |
| A9 | Comportamentos da conversa | o que os ganhos fazem diferente: perguntas de descoberta, momento do preço, foto enviada, próximo passo com data, linguagem concreta | médio | alto |
| A10 | Experimentos | testes alternando dias ou semanas (ex.: nova mensagem automática, nova regra de distribuição), com métrica definida antes | médio | alto no médio prazo |
| — | Juiz de qualidade | nota por rubrica (0–2 em 5–6 critérios) de 20–30 atendimentos por vendedor, com citação antes da nota; calibrado pelo dono 10 vezes por mês | médio | médio-alto |

**Regras para todo agente que lê texto de cliente (LGPD):** retirar nome, telefone, endereço e CPF antes de mandar ao modelo; mandar só o necessário; provedor que não treina com os dados; nenhum trecho identificável no relatório; prazo de guarda definido. Dado pseudonimizado continua sendo dado pessoal.

**Regras para todo agente que usa LLM:** validação inicial contra rótulo humano (kappa); citação literal obrigatória e opção "indeterminado"; temperatura 0 e duas execuções; revalidação a cada trimestre. A nota do LLM é para treinar, **nunca para punir** — se virar cobrança, o vendedor passa a escrever para o robô.

## 7. IMPLANTAÇÃO

| Etapa | O quê | Prazo |
|---|---|---|
| 1 | Primeiro relatório semanal (19–24/10) com o que já é medido — feito, ver documento anexo | 27/10 |
| 2 | Guardar uma série semanal padronizada por indicador (base dos gráficos de controle) | contínuo |
| 3 | Fechar com o Fernando: horário de sábado; separar tag de tipo / processo / campanha; criar PAISAGISMO e OUTROS; lista fechada de motivos de perda | próxima reunião |
| 4 | A6 (coorte) e A7 ("não temos") — sem LLM ou com LLM simples | 2 semanas |
| 5 | Validação humana do LLM (150–200 cards) para A4 e A8 | 3–4 semanas |
| 6 | Gráficos de controle com limites provisórios (6 semanas de série) | início de dezembro |
| 7 | A9, juiz de qualidade e A10 | a partir de dezembro |

**Lacunas de dado hoje:** o CRM guarda só a última movimentação de cada card (não o histórico), então movimento e carga diários dependem dos relatórios diários já salvos; a data em que a tag foi posta não está sendo lida ainda; e falta a escala de folgas dos vendedores.

## 8. FONTES

**Como foram verificadas.** Os agentes de pesquisa confirmaram autores, títulos, veículos e DOIs pelos resultados de busca e pelos resumos; o bloqueio de rede deste ambiente impediu abrir o texto completo. **Antes de citar um número ao cliente, abrir a fonte original.** Fontes de fornecedor estão marcadas — servem como hipótese, nunca como meta.

**Tempo de resposta**
- Oldroyd, McElheran & Elkington (2011). The Short Life of Online Sales Leads. *Harvard Business Review* 89(3):28. scholarsarchive.byu.edu/facpub/9711
- Lead Response Management Study (InsideSales, 2007) — **fornecedor**; telefone; não mede fechamento.
- Brown, Gans, Mandelbaum et al. (2005). Statistical Analysis of a Telephone Call Center. *JASA* 100(469):36–50.
- Castellanos, Yom-Tov & Goldberg. Silent Abandonment in Text-Based Contact Centers (preprint).
- Pesquisas de expectativa no WhatsApp (Octadesk/Opinion Box CX Trends; eLife) — **fornecedor**; respostas declaradas.

**Qualidade do registro**
- Wang & Strong (1996). Beyond Accuracy: What Data Quality Means to Data Consumers. *J. Management Information Systems* 12(4):5–33.
- Nagle, Redman & Sammon (2017). Only 3% of Companies' Data Meets Basic Quality Standards. *HBR*.
- Alter (2014). Theory of Workarounds. *Communications of the AIS* 34:55. DOI 10.17705/1CAIS.03455
- Avlonitis & Panagopoulos (2005). *Industrial Marketing Management* 34(4):355–368; Jayachandran et al. (2005). *Journal of Marketing* 69(4):177–192.
- Laney (2002). Improved control charts for attributes. *Quality Engineering* 14(4):531–537.

**Follow-up e fluxo**
- Gollwitzer & Sheeran (2006). Implementation intentions and goal achievement: a meta-analysis. *Adv. Exp. Social Psychology* 38:69–119.
- Milkman, Beshears, Choi, Laibson & Madrian (2011). *PNAS* 108(26):10415–10420. DOI 10.1073/pnas.1103170108
- Gurol-Urganci et al. (2013). Mobile phone messaging reminders for attendance at healthcare appointments. *Cochrane* CD007458.
- Little (1961). A proof for the queuing formula L = λW. *Operations Research* 9(3):383–387.
- Vacanti & Coleman (2020). *The Kanban Guide* — métricas de fluxo (estoque, vazão, idade, tempo de ciclo).
- Velocify/InsideSales sobre número de tentativas — **fornecedor**.

**Classificação**
- Krippendorff, *Content Analysis* (2018); Landis & Koch (1977). *Biometrics* 33:159–174; McHugh (2012). *Biochemia Medica* 22(3):276–282.
- Gilardi, Alizadeh & Kubli (2023). ChatGPT outperforms crowd workers for text-annotation tasks. *PNAS* 120(30). DOI 10.1073/pnas.2305016120
- Pangakis, Wolken & Fasching (2023). Automated Annotation with Generative AI Requires Validation. arXiv:2306.00176
- Ibraflor via imprensa: Dia das Mães ≈ 20% do faturamento anual do setor; Finados ≈ 3%.

**Carga e distribuição**
- KC & Terwiesch (2009). *Management Science* 55(9):1486–1498. DOI 10.1287/mnsc.1090.1037
- Tan & Netessine (2014). When Does the Devil Make Work? *Management Science* 60(6):1574–1593. DOI 10.1287/mnsc.2013.1823
- Goes, Ilk, Lin & Zhao (2018). When More Is Less: multitasking. *Management Science* 64(7):3033–3054.
- Armony & Ward (2010). Fair Dynamic Routing. *Operations Research* 58(3):624–637.
- Gans, Koole & Mandelbaum (2003). Telephone Call Centers: Tutorial. *MSOM* 5(2):79–141.
- Efron & Morris (1977). Stein's Paradox in Statistics. *Scientific American* 236(5).

**Método semanal e feedback**
- Perla, Provost & Murray (2011). The run chart. *BMJ Quality & Safety* 20(1):46–51.
- Mohammed, Worthington & Woodall (2008). Plotting basic control charts. *Qual Saf Health Care* 17(2):137–145.
- Wheeler. *Understanding Variation* (livro; via fontes secundárias).
- Kluger & DeNisi (1996). *Psychological Bulletin* 119(2):254–284.
- Ivers et al. (2012). Audit and feedback. *Cochrane* CD000259.
- Brehaut et al. (2016). Practice Feedback Interventions: 15 Suggestions. *Annals of Internal Medicine* 164(6):435–441.
- Locke & Latham (2002). *American Psychologist* 57(9):705–717.
- Amazon Weekly Business Review (métricas de input × output) — relatos de ex-executivos (Commoncog), não acadêmico.

**Novas análises**
- Sun, Chen & Fan (2021). Effect of Live Chat on Traffic-to-Sales Conversion. *Production and Operations Management* 30(5). DOI 10.1111/poms.13320
- Packard, Moore & McFerran (2018). (I'm) Happy to Help (You). *J. Marketing Research* 55(4):541–555.
- Packard & Berger (2021). How Concrete Language Shapes Customer Satisfaction. *J. Consumer Research* 47(5).
- Zheng et al. (2023). Judging LLM-as-a-Judge. NeurIPS; Wang et al. (2024). Large Language Models are not Fair Evaluators. ACL.
- Corsten & Gruen (2003). Desperately seeking shelf availability. *IJRDM*.
- Deng, Xu, Kohavi & Walker (2013). CUPED. WSDM.
- Fader, Hardie & Lee (2005). RFM and CLV. *J. Marketing Research* 42(4).
- Gong Labs (perguntas por conversa, fala × escuta) — **fornecedor**; B2B por voz.
