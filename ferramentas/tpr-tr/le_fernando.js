// privado do Fernando (ticket 4719278). Uso: node le_fernando.js [n=40] [--json]
const { ler } = require('./le_ticket');
process.argv.splice(2, 0, '4719278'); if (!process.argv[3]) process.argv[3] = '40';
require('./le_ticket_cli');
