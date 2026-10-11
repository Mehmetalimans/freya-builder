// Reuses TCP connections and records progress; all assertions remain exact.
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import https from 'node:https';
import {isIP} from 'node:net';
const [mock,fixturesPath,manifestPath,output,resolvedIP]=process.argv.slice(2);
const base=new URL(mock);
if(base.protocol!=='https:' || base.username || base.password || base.search || base.hash) throw Error('Invalid mock URL');
if(resolvedIP && !isIP(resolvedIP))throw Error('The optional DNS diagnostic address must be an IP');
const agent=new https.Agent({keepAlive:true,maxSockets:4,...(resolvedIP?{lookup:(host,options,callback)=>{
  if(host!==base.hostname)return callback(Error('Unexpected DNS target'));
  const result={address:resolvedIP,family:isIP(resolvedIP)};
  if(options.all)callback(null,[result]);else callback(null,result.address,result.family);
}}:{})});
function request(c){
  return new Promise((resolve,reject)=>{
    const req=https.request(new URL(c.path,base),{method:c.method,agent,
      headers:{'Content-Type':'application/json','User-Agent':'Mozilla/5.0 (build-the-builder)'}},response=>{
      let text='';response.setEncoding('utf8');response.on('data',part=>text+=part);
      response.on('end',()=>{clearTimeout(timer);try{resolve({status:response.statusCode,body:JSON.parse(text)});}catch(e){reject(e);}});
    });
    const timer=setTimeout(()=>req.destroy(Error('Request timeout')),30000);
    req.on('error',e=>{clearTimeout(timer);reject(e);});req.end(JSON.stringify(c.request_json));
  });
}
const raw=readFileSync(fixturesPath);
const fixtures=JSON.parse(raw).cases;
const manifest=JSON.parse(readFileSync(manifestPath,'utf8'));
const results=[];
let index=0;
async function runner(){
while(index<fixtures.length){
  const c=fixtures[index++];
  if(!c.source || !c.path.startsWith('/') || c.path.startsWith('//') || c.path.includes('..')) throw Error('Invalid sourced fixture');
  const start=performance.now();
  try{
    const response=await request(c);
    const equal=isDeepStrictEqual(response.body,c.response_json);
    results.push({id:c.id,pass:response.status===c.status && equal,status:response.status,
      expected_status:c.status,body_equal:equal,seconds:(performance.now()-start)/1000});
  }catch(e){results.push({id:c.id,pass:false,error_type:e.name,seconds:(performance.now()-start)/1000});}
  if(results.length%50===0)console.log(JSON.stringify({checked:results.length,total:fixtures.length,failed:results.filter(x=>!x.pass).length}));
}}
await Promise.all(Array.from({length:4},runner));
agent.destroy();
const failed=results.filter(r=>!r.pass).length;
const report={status:failed?'failed':'passed',mock_url:mock.replace(/\/$/,''),case_sha256:manifest.sha256,
 fixtures_sha256:createHash('sha256').update(raw).digest('hex'),checked_at:new Date().toISOString(),
 total:results.length,failed,results,transport:'Node HTTPS, four connections, normal TLS certificate and hostname verification',
 ...(resolvedIP?{dns_diagnostic_address:resolvedIP}:{} )};
writeFileSync(output,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,total:report.total,failed,output}));
process.exitCode=failed?1:0;
