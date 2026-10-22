// Coleta só leitura: cards do pipeline 10541 com mensagem desde DESDE e o histórico de mensagens de cada ticket.
// Uso: node coletar.js <desde ISO UTC> <dir saída>
const { open, S } = require('./common');
const { personify, unpersonify } = require('./pers');
const { installApi } = require('./common_api');
const fs = require('fs');
const STEPS = [44341, 69421, 36971, 113074, 32318, 36613, 121919, 44334];
const DESDE = new Date(process.argv[2]);
const CTX = new Date(DESDE.getTime() - 24 * 3600e3); // 24h antes, para saber se o atendimento já estava aberto
const OUT = process.argv[3];
(async () => {
  const t0 = Date.now(); let calls = 0, bytes = 0;
  const { ctx, page } = await open();
  await personify(page); await installApi(page);
  const get = async p => { calls++; const r = await page.evaluate(p => window.__apiGet(p), p); bytes += r.body.length; if (r.status !== 200) throw new Error(r.status + ' ' + p); return JSON.parse(r.body); };
  const cards = [];
  for (const step of STEPS) {
    for (let pg = 1; pg < 500; pg++) {
      const d = await get(`/commercial-order/step/${step}?searchParam=&sortBy=lastMessageHour&sortDirection=DESC&dateField=created_at&archived=false&timezone=UTC&pageNumber=${pg}`);
      const os = d.orders || [];
      for (const o of os) if (new Date(o.sortingTimestamp) >= DESDE) cards.push({ id: o.id, step, userId: o.userId, user: o.name, ticketIds: o.ticketIds, contact: o.contactName, number: o.contactNumber, createdAt: o.createdAt, last: o.sortingTimestamp, status: o.status, amount: o.amount, orderTags: (o.orderTags || []).map(t => t.name), contactTags: (o.tags || []).map(t => t.name) });
      if (!os.length || new Date(os[os.length - 1].sortingTimestamp) < DESDE) break;
    }
    console.log('coluna', step, 'cards acumulados', cards.length);
  }
  const tickets = [...new Set(cards.flatMap(c => c.ticketIds || []))];
  const msgs = {};
  for (const [i, t] of tickets.entries()) {
    const all = [];
    for (let pg = 1; pg < 200; pg++) {
      const d = await get(`/messages/${t}?pageNumber=${pg}`);
      const ms = d.messages || [];
      all.push(...ms.map(m => ({ id: m.id, at: m.createdAt, fromMe: m.fromMe, userId: m.userId, sys: m.sendBySystem, ai: m.generatedByAi, colAuto: m.columnAutomationId, flow: m.automationFlowExecutionId, type: m.mediaType, deleted: m.isDeleted, body: (m.body || '').slice(0, 40) })));
      if (!d.hasMore || !ms.length || ms.reduce((a, m) => Math.min(a, new Date(m.createdAt)), Infinity) < CTX) break;
    }
    msgs[t] = all;
    if (i % 50 === 0) console.log('tickets', i + 1, '/', tickets.length);
  }
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(OUT + '/cards.json', JSON.stringify(cards));
  fs.writeFileSync(OUT + '/mensagens.json', JSON.stringify(msgs));
  const back = await unpersonify(page);
  const meta = { desde: DESDE, coletadoEm: new Date(), segundos: Math.round((Date.now() - t0) / 1000), chamadas: calls, bytesRecebidos: bytes, cards: cards.length, tickets: tickets.length, mensagens: Object.values(msgs).reduce((a, m) => a + m.length, 0), empresaAoFinal: back };
  fs.writeFileSync(OUT + '/meta.json', JSON.stringify(meta, null, 1));
  console.log(JSON.stringify(meta));
  await ctx.close();
})().catch(e => { console.error('ERRO', e.message); process.exit(1); });
