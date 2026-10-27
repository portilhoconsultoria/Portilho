// Coleta só leitura para o Relatório Diário do Comercial (Verdes Plantas, empresa 7078).
// Variante semanal: notas e contatos de todos os cards movidos de <ini> até agora. Uso: node coletar_semana.js <ini AAAA-MM-DD> <fim AAAA-MM-DD (exclusivo)> <dir saída>
// Grava: negocios.json (base inteira), agendamentos.json, notas.json (cards movidos no dia + acompanhados), contatos.json, meta_edicao.json
const { open } = require('./common');
const { personify, unpersonify } = require('./pers');
const { installApi } = require('./common_api');
const fs = require('fs');
const [INI, FIM, OUT] = process.argv.slice(2); const DIA = INI + '_' + FIM, FONES = '';
const ini = new Date(INI + 'T03:00:00Z'), fim = new Date(FIM + 'T03:00:00Z');
(async () => {
  const t0 = Date.now(); let calls = 0;
  const { ctx, page } = await open();
  await personify(page); await installApi(page);
  const get = async p => { calls++; const r = await page.evaluate(p => window.__apiGet(p), p); if (r.status !== 200) throw new Error(r.status + ' ' + p); return JSON.parse(r.body); };
  // 1. negócios: pageSize tem teto 40; o filtro por etapa é ignorado — pagina tudo
  const neg = [];
  for (let pg = 1; pg < 1000; pg++) {
    const d = await get(`/commercial-order?pageNumber=${pg}&pageSize=40`);
    neg.push(...(d.orders || []).map(o => ({ id: o.id, step: o.commercialSalesStepId, userId: o.userId, contactId: o.contactId, amount: o.amount, status: o.status, wonAt: o.wonAt, lostAt: o.lostAt, lostReason: o.lostReason, moved: o.lastTimeMoved, createdAt: o.createdAt, updatedAt: o.updatedAt, archived: o.archived })));
    if (!d.hasMore || !(d.orders || []).length) break;
  }
  // 2. agendamentos
  const ag = [];
  for (let pg = 1; pg < 500; pg++) {
    const d = await get(`/schedules?pageNumber=${pg}`);
    ag.push(...(d.schedules || []).map(s => ({ id: s.id, contactId: s.contactId, userId: s.userId, status: s.status, sendAt: s.sendAt, sentAt: s.sentAt, createdAt: s.createdAt })));
    if (!d.hasMore || !(d.schedules || []).length) break;
  }
  // 3. contatos acompanhados (pedidos da edição anterior), pelo telefone
  const acompanhar = {};
  for (const f of (FONES || '').split(',').filter(Boolean)) {
    const d = await get('/contacts/?searchParam=' + f.slice(-8) + '&pageNumber=1');
    acompanhar[f] = (d.contacts || []).filter(c => c.number === f).map(c => c.id);
  }
  const idsAcomp = new Set(Object.values(acompanhar).flat());
  // 4. notas: cards movidos no dia + cards dos contatos acompanhados
  const alvo = neg.filter(o => ((o.moved && new Date(o.moved) >= ini) || (o.createdAt && new Date(o.createdAt) >= ini && new Date(o.createdAt) < fim)) || idsAcomp.has(o.contactId));
  const notas = {};
  for (const o of alvo) {
    const d = await get(`/ticket-notes/contact/${o.contactId}?commercialOrderId=${o.id}`);
    notas[o.id] = (Array.isArray(d) ? d : d.notes || []).map(n => ({ id: n.id, body: n.body || n.note || n.text || '', userId: n.userId, createdAt: n.createdAt }));
  }
  // 5. contatos dos cards que podem aparecer em tabela (movidos no dia e acompanhados)
  const contatos = {};
  for (const cid of [...new Set(alvo.map(o => o.contactId))]) {
    try { const c = await get('/contacts/' + cid); contatos[cid] = { name: c.name, number: c.number }; } catch (e) { contatos[cid] = { erro: e.message }; }
  }
  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(OUT + '/negocios.json', JSON.stringify(neg));
  fs.writeFileSync(OUT + '/agendamentos.json', JSON.stringify(ag));
  fs.writeFileSync(OUT + '/notas.json', JSON.stringify(notas));
  fs.writeFileSync(OUT + '/contatos.json', JSON.stringify(contatos));
  fs.writeFileSync(OUT + '/acompanhar.json', JSON.stringify(acompanhar));
  const back = await unpersonify(page);
  const meta = { dia: DIA, coletadoEm: new Date(), segundos: Math.round((Date.now() - t0) / 1000), chamadas: calls, negocios: neg.length, agendamentos: ag.length, cardsComNotasLidas: alvo.length, empresaAoFinal: back };
  fs.writeFileSync(OUT + '/meta_semana.json', JSON.stringify(meta, null, 1));
  console.log(JSON.stringify(meta));
  await ctx.close();
})().catch(e => { console.error('ERRO', e.message); process.exit(1); });
