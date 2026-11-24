// ack das últimas mensagens ao Fernando (ticket 4719278). Uso: node diag_envio.js [n=10] [--json]
const { ler } = require('./le_ticket');
process.argv.splice(2, 0, '4719278'); if (!process.argv[3]) process.argv[3] = '10';
require('./le_ticket_cli');
