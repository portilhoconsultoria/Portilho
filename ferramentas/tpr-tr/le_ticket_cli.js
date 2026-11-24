// CLI compartilhado dos atalhos (diag_envio / le_fernando / le_grupo)
const { ler } = require('./le_ticket');
const [ticket, n, flag] = process.argv.slice(2);
ler(ticket, +(n || 30)).then(ms => {
  if (flag === '--json') return console.log(JSON.stringify(ms));
  for (const m of ms.reverse()) {
    const d = new Date(m.createdAt).toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' });
    console.log(`${d} · ${m.fromMe ? 'loja' : 'cliente'}${m.userId ? ' u' + m.userId : ''} · ack ${m.ack} · ${m.mediaType || 'texto'} · ${m.body.replace(/\s+/g, ' ').slice(0, 160)}`);
  }
}).catch(e => { console.error('ERRO', e.message); process.exit(1); });
