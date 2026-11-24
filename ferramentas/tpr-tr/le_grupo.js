// grupo CRM - Verdes Plantas (ticket 9214242). Uso: node le_grupo.js [n=60] [--json]
const { ler } = require('./le_ticket');
process.argv.splice(2, 0, '9214242'); if (!process.argv[3]) process.argv[3] = '60';
require('./le_ticket_cli');
