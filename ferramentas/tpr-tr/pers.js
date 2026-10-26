// personifica a Verdes Plantas (7078) se ainda não estiver
async function login(page) {
  await page.goto('https://gestao.portilhoconsultoria.com.br/', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(4000);
  if (!page.url().includes('/login')) return;
  if (!process.env.VP_ROBO_EMAIL || !process.env.VP_ROBO_SENHA) throw new Error('VP_ROBO_EMAIL/VP_ROBO_SENHA ausentes');
  await page.fill('input[name=email]', process.env.VP_ROBO_EMAIL);
  await page.fill('input[name=password]', process.env.VP_ROBO_SENHA);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(8000);
  if (page.url().includes('/login')) throw new Error('login não concluído (código de verificação?)');
}
// fecha anúncios do painel (ex.: "Novidades do DKW System") que cobrem o menu
async function fecharModais(page) {
  for (let i = 0; i < 3; i++) {
    const m = page.locator('[class*=CommunityModal], [class*=releaseModal]');
    if (!(await m.count())) return;
    await page.keyboard.press('Escape'); await page.waitForTimeout(800);
    if (await m.count()) {
      const d = m.first().getByRole('button', { name: 'Dispensar', exact: true });
      if (await d.count()) { await d.click(); await page.waitForTimeout(1000); }
    }
  }
}
async function personify(page) {
  await login(page);
  await page.goto('https://gestao.portilhoconsultoria.com.br/', { waitUntil: 'domcontentloaded' });
  await page.getByText('Bem vindo').waitFor({ timeout: 60000 });
  await page.waitForTimeout(3000);
  const cur = await page.evaluate(() => JSON.parse(localStorage.getItem('user')).company.id);
  if (cur === 7078) return;
  const an = page.getByRole('button', { name: 'Agora não' }); if (await an.count()) { await an.first().click(); await page.waitForTimeout(800); }
  await fecharModais(page);
  // layout novo (26/10): o menu da conta abre no bloco do usuário, no rodapé da barra lateral (nome + e-mail)
  const item = page.getByRole('menuitem', { name: 'Personificar empresa' });
  const email = await page.evaluate(() => (JSON.parse(localStorage.getItem('user')) || {}).email || '');
  if (email) { const u = page.getByText(email.slice(0, 18), { exact: false }).first(); if (await u.count()) { await u.click(); await page.waitForTimeout(1000); } }
  // layout antigo: botão do avatar sem rótulo no topo
  for (let i = 0; i < 12 && !(await item.count()); i++) {
    const b = page.locator('button').nth(i);
    if (await b.getAttribute('aria-label') || (await b.innerText()).trim()) continue;
    await b.click(); await page.waitForTimeout(800);
    if (!(await item.count())) { await page.keyboard.press('Escape'); await page.waitForTimeout(400); }
  }
  await item.click();
  const dlg = page.locator('[role=dialog]'); await dlg.waitFor();
  await dlg.locator('[role=combobox], input').first().click();
  await page.keyboard.type('Verdes', { delay: 80 }); await page.waitForTimeout(2000);
  await page.locator('[role=option]', { hasText: 'Floricultura Verdes Plantas' }).click();
  await dlg.getByRole('button', { name: 'Confirmar' }).click();
  await page.waitForTimeout(6000);
  const n = page.getByRole('button', { name: 'Agora não' }); if (await n.count()) await n.first().click();
  const id = await page.evaluate(() => JSON.parse(localStorage.getItem('user')).company.id);
  if (id !== 7078) throw new Error('personificação falhou: ' + id);
}
async function unpersonify(page) {
  await page.goto('https://gestao.portilhoconsultoria.com.br/', { waitUntil: 'domcontentloaded' });
  await page.getByText('Bem vindo').waitFor({ timeout: 60000 }); await page.waitForTimeout(3000);
  await fecharModais(page);
  // rótulo do botão mudou no layout novo (26/10): "Voltar para empresa original" → "Sair da personificação"
  for (const nome of ['Sair da personificação', 'Voltar para empresa original']) {
    const b = page.getByRole('button', { name: nome });
    if (await b.count()) { await b.first().click(); await page.waitForTimeout(5000); break; }
  }
  return page.evaluate(() => JSON.parse(localStorage.getItem('user')).company.id);
}
module.exports = { personify, unpersonify, login };
