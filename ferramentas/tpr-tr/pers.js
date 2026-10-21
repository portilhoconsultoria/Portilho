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
async function personify(page) {
  await login(page);
  await page.goto('https://gestao.portilhoconsultoria.com.br/', { waitUntil: 'domcontentloaded' });
  await page.getByText('Bem vindo').waitFor({ timeout: 60000 });
  await page.waitForTimeout(3000);
  const cur = await page.evaluate(() => JSON.parse(localStorage.getItem('user')).company.id);
  if (cur === 7078) return;
  const an = page.getByRole('button', { name: 'Agora não' }); if (await an.count()) { await an.first().click(); await page.waitForTimeout(800); }
  await page.locator('button').nth(5).click();
  await page.getByRole('menuitem', { name: 'Personificar empresa' }).click();
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
  const b = page.getByRole('button', { name: 'Voltar para empresa original' });
  if (await b.count()) { await b.click(); await page.waitForTimeout(5000); }
  return page.evaluate(() => JSON.parse(localStorage.getItem('user')).company.id);
}
module.exports = { personify, unpersonify };
