'use strict';

// Read a single GitHub REST comment object on stdin. This prints a token only;
// it never updates an issue or chooses how to reconcile a human's edits.
const {acknowledgement} = require('./monthly_store.cjs');
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try { process.stdout.write(acknowledgement(JSON.parse(input)) + '\n'); }
  catch (error) { process.stderr.write(`reconciliation token failed: ${error.message}\n`); process.exitCode = 1; }
});
