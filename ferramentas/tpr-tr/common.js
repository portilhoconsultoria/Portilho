const { chromium } = require('playwright');
const S = __dirname;
async function open() {
  const ctx = await chromium.launchPersistentContext((process.env.TPR_PROFILE || '/tmp/tpr-profile'), {
    executablePath: '/opt/pw-browsers/chromium', headless: true,
    viewport: { width: 1440, height: 900 }, locale: 'pt-BR' });
  const page = ctx.pages()[0] || await ctx.newPage();
  return { ctx, page };
}
module.exports = { open, S };
