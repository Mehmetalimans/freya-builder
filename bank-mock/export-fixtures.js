import {allCases} from './contract-fixtures.js';
import {writeFileSync,mkdirSync} from 'node:fs';
import {dirname} from 'node:path';
mkdirSync(dirname(process.argv[2]),{recursive:true});
writeFileSync(process.argv[2], JSON.stringify({cases:allCases()},null,2)+'\n');
