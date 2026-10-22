// Envia o PDF do relatório ao Fernando pelo DKW da Portilho (empresa 7061, nunca o da cliente).
// Autorizado pelo Jhonatan em 22/10/2026. Uso: node enviar.js <pdf> <legenda> [--teste]
// --teste: só localiza a conversa e mostra o que enviaria, sem enviar.
const { open } = require('./common');
const { login } = require('./pers');
const fs = require('fs'), path = require('path');
const NUMERO = '5542999589335';  // Fernando - Verdes Plantas (contato 5517468)
(async () => {
  const [pdf, legenda, flag] = process.argv.slice(2);
  const { ctx, page } = await open();
  await login(page);
  await page.goto('https://gestao.portilhoconsultoria.com.br/', { waitUntil: 'domcontentloaded' });
  await page.getByText('Bem vindo').waitFor({ timeout: 60000 }); await page.waitForTimeout(2000);
  const emp = await page.evaluate(() => JSON.parse(localStorage.getItem('user')).company.id);
  if (emp !== 7061) throw new Error('não está no ambiente da Portilho: ' + emp);
  const r = await page.evaluate(async ({ b64, nome, legenda, numero, teste }) => {
    const tok = localStorage.getItem('token').replace(/^"|"$/g, '');
    const h = { authorization: 'Bearer ' + tok, tenant: 'portilho-gestao-comercial-inteligente' };
    const tk = await (await fetch('https://api.integrador-crm.com/tickets?searchParam=' + numero.slice(-8) + '&pageNumber=1&showAll=true', { headers: h })).json();
    const doFernando = (tk.tickets || []).filter(t => (t.contact || {}).number === numero)
      .sort((a, b) => (a.status === 'open' ? 0 : 1) - (b.status === 'open' ? 0 : 1) || new Date(b.updatedAt) - new Date(a.updatedAt));
    if (!doFernando.length) return { erro: 'conversa do Fernando não encontrada' };
    const ticket = doFernando[0].id;
    if (teste) return { teste: true, ticket, status: doFernando[0].status, contato: doFernando[0].contact.name };
    const bin = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    const fd = new FormData();
    fd.append('medias', new File([bin], nome, { type: 'application/pdf' }), nome);
    fd.append('body', legenda);
    fd.append('fromMe', true);
    const res = await fetch('https://api.integrador-crm.com/messages/' + ticket, { method: 'POST', headers: h, body: fd });
    return { ticket, status: res.status, ok: res.ok };
  }, { b64: fs.readFileSync(pdf).toString('base64'), nome: path.basename(pdf), legenda, numero: NUMERO, teste: flag === '--teste' });
  console.log(JSON.stringify(r));
  await ctx.close();
  if (r.erro || (r.status && !r.ok)) process.exit(1);
})().catch(e => { console.error('ERRO', e.message); process.exit(1); });
