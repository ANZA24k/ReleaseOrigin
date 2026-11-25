import {createClient} from 'genlayer-js'; import {studionet} from 'genlayer-js/chains'; import fs from 'node:fs';
const c=createClient({chain:studionet});
for(const hash of process.argv.slice(2)) {
 const tx=await c.getTransaction({hash});
 const summary={checked_at:new Date().toISOString(),hash:tx.hash,from:tx.from_address,to:tx.to_address,status:tx.statusName,execution_result:tx.txExecutionResultName,execution_mode:tx.execution_mode,leader_only:tx.leader_only,initial_validators:tx.num_of_initial_validators,votes:tx.consensus_data?.votes,leader_receipts:(tx.consensus_data?.leader_receipt||[]).map(r=>({mode:r.mode,vote:r.vote,result:r.result,calldata:r.calldata,eq_outputs:r.eq_outputs,execution_result:r.execution_result,contract_state_hash:r.contract_state_hash})),explorer:'https://explorer-studio.genlayer.com/tx/'+hash};
 fs.writeFileSync('docs/tx-'+hash+'.json',JSON.stringify(summary,null,2)+'\n');
 console.log(JSON.stringify({hash,status:tx.statusName,result:tx.txExecutionResultName,address:tx.to_address,votes:tx.consensus_data?.votes}));
}
