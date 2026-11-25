import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant} from 'genlayer-js/types';
import fs from 'node:fs';
import {canonical,digest} from '../src/canonical.mjs';
import {createHash} from 'node:crypto';
const config=JSON.parse(fs.readFileSync('docs/deployment.json','utf8'));
const client=createClient({chain:studionet});
const code=await client.getContractCode(config.address);
const local=fs.readFileSync('contracts/release_origin.py','utf8');
if(code!==local) throw Error('Deployed source differs from repository');
const read=async (functionName,args)=>JSON.parse(await client.readContract({address:config.address,transactionHashVariant:TransactionHashVariant.LATEST_FINAL,functionName,args}));
const ids=process.argv.slice(2); if(!ids.length) ids.push('RO-LIVE-001');
const records=[];
for (const id of ids) {
  const r=await read('get_release',[id]);
  let previous='0'.repeat(64); const receipts=[];
  for(let i=1;i<=r.sequence;i++) {
    const receipt=await read('get_receipt',[id,i]); const {hash,...body}=receipt;
    if(body.release_id!==id || body.sequence!==i || body.previous!==previous || digest(body)!==hash) throw Error('Receipt chain mismatch '+id+':'+i);
    previous=hash; receipts.push(receipt);
  }
  if(r.head!==previous) throw Error('Head mismatch');
  const last=receipts.at(-1); const before={...r,sequence:r.sequence-1,head:last.previous};
  if(digest(before)!==last.state_hash || digest(r.claim)!==r.claim_hash || digest(r.bundle)!==r.bundle_hash) throw Error('State/evidence commitment mismatch');
  if(r.result && receipts.filter(x=>x.event==='REVIEWED').at(-1).detail.result_hash!==digest(r.result)) throw Error('Result commitment mismatch');
  const hashes=Object.entries(r.bundle).every(([_,e])=>createHash('sha256').update(e.body).digest('hex')===e.sha256 && Buffer.byteLength(e.body)===e.bytes);
  if(!hashes) throw Error('Evidence byte hashes differ');
  fs.writeFileSync('docs/'+id+'-record.json',JSON.stringify(r,null,2)+'\n');
  fs.writeFileSync('docs/'+id+'-receipts.json',JSON.stringify(receipts,null,2)+'\n');
  records.push({release_id:id,phase:r.phase,status:r.result?.status,receipts:r.sequence,head:r.head,attempts:r.attempts});
}
const report={checked_at:new Date().toISOString(),network:'Studionet',chain_id:61999,contract:config.address,source_sha256:createHash('sha256').update(local).digest('hex'),source_matches:true,finalized_reads:true,records};
fs.writeFileSync('docs/verification.json',JSON.stringify(report,null,2)+'\n'); console.log(JSON.stringify(report,null,2));
