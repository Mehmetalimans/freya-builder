import {allCases} from './contract-fixtures.js';
import {writeFileSync} from 'node:fs';
writeFileSync(process.argv[2], JSON.stringify({cases:allCases()},null,2)+'\n');
