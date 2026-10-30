// Coleta só leitura para o PDF de pendências (Verdes Plantas, empresa 7078). Roda depois de coletar_edicao.js, no mesmo dir.
// Uso: node coletar_pendencias.js <dir> — lê negocios.json e contatos.json do dir.
// Grava: tickets_abertos.json (conversas open/pending) e completa contatos.json com os cards que podem virar pendência.
const { open } = require('./common');
const { personify, unpersonify } = require('./pers');
const { installApi } = require('./common_api');
const fs = require('fs');
const OUT = process.argv[2];
const ENCERRA = [32318, 36613, 121919, 44334], ATIVAS = [44341, 69421, 36971, 113074];
(async () => {
  const t0 = Date.now(); let calls = 0;
  const neg = JSON.parse(fs.readFileSync(OUT + '/negocios.json'));
  const contatos = JSON.parse(fs.readFileSync(OUT + '/contatos.json'));
  const { ctx, page } = await open();
  await personify(page); await installApi(page);
  const get = async p => { calls++; const r = await page.evaluate(p => window.__apiGet(p), p); if (r.status !== 200) throw new Error(r.status + ' ' + p); return JSON.parse(r.body); };
  // 1. conversas ainda abertas (open = em atendimento; pending = aguardando)
  const tk = [];
  for (const status of ['open', 'pending']) {
    for (let pg = 1; pg < 300; pg++) {
      const d = await get(`/tickets?pageNumber=${pg}&status=${status}&showAll=true`);
      const ts = d.tickets || [];
      tk.push(...ts.map(t => ({ id: t.id, status: t.status, userId: t.userId, contactId: t.contactId || (t.contact || {}).id, number: (t.contact || {}).number, name: (t.contact || {}).name, updatedAt: t.updatedAt })));
      if (!d.hasMore || !ts.length) break;
    }
  }
  // 2. contatos dos cards ativos e dos encerrados desde 20/10 (quando o botão Ações passou a valer)
  const desde = new Date('2026-10-20T03:00:00Z');
  const alvo = neg.filter(o => ATIVAS.includes(o.step) || (ENCERRA.includes(o.step) && o.moved && new Date(o.moved) >= desde));
  for (const cid of [...new Set(alvo.map(o => o.contactId))]) {
    if (contatos[cid] && contatos[cid].number) continue;
    try { const c = await get('/contacts/' + cid); contatos[cid] = { name: c.name, number: c.number }; } catch (e) { contatos[cid] = { erro: e.message }; }
  }
  fs.writeFileSync(OUT + '/tickets_abertos.json', JSON.stringify(tk));
  fs.writeFileSync(OUT + '/contatos.json', JSON.stringify(contatos));
  const back = await unpersonify(page);
  const meta = { coletadoEm: new Date(), segundos: Math.round((Date.now() - t0) / 1000), chamadas: calls, ticketsAbertos: tk.length, contatos: Object.keys(contatos).length, empresaAoFinal: back };
  fs.writeFileSync(OUT + '/meta_pendencias.json', JSON.stringify(meta, null, 1));
  console.log(JSON.stringify(meta));
  await ctx.close();
})().catch(e => { console.error('ERRO', e.message); process.exit(1); });
