// Reuses TCP connections and records progress; all assertions remain exact.
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
const [mock,fixturesPath,manifestPath,output]=process.argv.slice(2);
const base=new URL(mock);
if(base.protocol!=='https:' || base.username || base.password || base.search || base.hash) throw Error('Invalid mock URL');
const raw=readFileSync(fixturesPath);
const fixtures=JSON.parse(raw).cases;
const manifest=JSON.parse(readFileSync(manifestPath,'utf8'));
const results=[];
for(const c of fixtures){
  if(!c.source || !c.path.startsWith('/') || c.path.startsWith('//') || c.path.includes('..')) throw Error('Invalid sourced fixture');
  const start=performance.now();
  try{
    const response=await fetch(mock.replace(/\/$/,'')+c.path,{method:c.method,redirect:'error',
      headers:{'Content-Type':'application/json','User-Agent':'Mozilla/5.0 (build-the-builder)'},
      body:JSON.stringify(c.request_json),signal:AbortSignal.timeout(30000)});
    const actual=await response.json();
    const equal=isDeepStrictEqual(actual,c.response_json);
    results.push({id:c.id,pass:response.status===c.status && equal,status:response.status,
      expected_status:c.status,body_equal:equal,seconds:(performance.now()-start)/1000});
  }catch(e){results.push({id:c.id,pass:false,error_type:e.name,seconds:(performance.now()-start)/1000});}
  if(results.length%50===0)console.log(JSON.stringify({checked:results.length,total:fixtures.length,failed:results.filter(x=>!x.pass).length}));
}
const failed=results.filter(r=>!r.pass).length;
const report={status:failed?'failed':'passed',mock_url:mock.replace(/\/$/,''),case_sha256:manifest.sha256,
 fixtures_sha256:createHash('sha256').update(raw).digest('hex'),checked_at:new Date().toISOString(),
 total:results.length,failed,results,transport:'Node fetch with connection reuse'};
writeFileSync(output,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,total:report.total,failed,output}));
process.exitCode=failed?1:0;
