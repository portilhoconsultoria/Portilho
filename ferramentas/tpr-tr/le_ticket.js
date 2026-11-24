// Leitura (só GET) das mensagens de um ticket no DKW da Portilho (empresa 7061). Recriado em 24/11/2026
// (os originais diag_envio.js / le_grupo.js / le_fernando.js viviam só no scratchpad da sessão antiga).
// Uso: node le_ticket.js <ticket> [n=30] [--json]   · recusa rodar se a conta estiver personificando (≠ 7061).
// Saída: data (Brasília) · quem (loja/cliente, nome do usuário) · ack (1 enviada · 2 entregue · 3 lida) · tipo · trecho.
const { open } = require('./common');
const { login } = require('./pers');
async function ler(ticket, n = 30) {
  const { ctx, page } = await open();
  try {
    await login(page);
    await page.goto('https://gestao.portilhoconsultoria.com.br/', { waitUntil: 'domcontentloaded' });
    await page.getByText('Bem vindo').waitFor({ timeout: 60000 }); await page.waitForTimeout(2000);
    const emp = await page.evaluate(() => JSON.parse(localStorage.getItem('user')).company.id);
    if (emp !== 7061) throw new Error('não está no ambiente da Portilho: ' + emp);
    return await page.evaluate(async ({ ticket, n }) => {
      const tok = localStorage.getItem('token').replace(/^"|"$/g, '');
      const h = { authorization: 'Bearer ' + tok, tenant: 'portilho-gestao-comercial-inteligente', accept: 'application/json' };
      let out = [], p = 1;
      while (out.length < n) {
        const r = await (await fetch(`https://api.integrador-crm.com/messages/${ticket}?pageNumber=${p}`, { headers: h })).json();
        const ms = r.messages || [];
        out = out.concat(ms);
        if (!r.hasMore || !ms.length) break; p++;
      }
      return out.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)).slice(0, n).map(m => ({
        id: m.id, createdAt: m.createdAt, fromMe: m.fromMe, userId: m.userId || null, ack: m.ack,
        mediaType: m.mediaType || null, body: (m.body || '').slice(0, 300) }));
    }, { ticket, n });
  } finally { await ctx.close(); }
}
module.exports = { ler };
if (require.main === module) {
  const [ticket, n, flag] = process.argv.slice(2);
  ler(ticket, +(n || 30)).then(ms => {
    if (flag === '--json') return console.log(JSON.stringify(ms));
    for (const m of ms.reverse()) {
      const d = new Date(m.createdAt).toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' });
      console.log(`${d} · ${m.fromMe ? 'loja' : 'cliente'}${m.userId ? ' u' + m.userId : ''} · ack ${m.ack} · ${m.mediaType || 'texto'} · ${m.body.replace(/\s+/g, ' ').slice(0, 160)}`);
    }
  }).catch(e => { console.error('ERRO', e.message); process.exit(1); });
}
