// injeta um helper apiGet na página: o token é lido e usado só dentro dela
async function installApi(page) {
  await page.evaluate(() => {
    window.__apiGet = async (path) => {
      const tok = localStorage.getItem('token').replace(/^"|"$/g, '');
      for (let i = 0; i < 4; i++) {
        const r = await fetch('https://api.integrador-crm.com' + path, { headers: { authorization: 'Bearer ' + tok, tenant: 'portilho-gestao-comercial-inteligente', accept: 'application/json' } });
        if (r.status === 429 || r.status >= 500) { await new Promise(s => setTimeout(s, 1500 * (i + 1))); continue; }
        return { status: r.status, body: await r.text() };
      }
      return { status: 'retry-exhausted', body: '' };
    };
  });
}
module.exports = { installApi };
